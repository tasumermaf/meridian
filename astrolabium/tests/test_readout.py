"""
Tests for the readout layer and the instantiation sheet.

These tests encode the output discipline itself: data first, no prose,
no invention, no value drift. If a future change reintroduces narration
into the readout, these fail.
"""

import datetime as dt
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import astrolabium as A  # noqa: E402
from src.card_sheet import (  # noqa: E402
    NOT_LOADED,
    SLOT,
    instantiation_sheet,
    marks_for_card,
)
from src.readout import (  # noqa: E402
    COARSE,
    DASH,
    EXACT,
    STORY_LICENSING_COMPOUNDS,
    hour_position,
    active_compounds,
    readout,
    story_gate,
    typed_state,
)

TZ = "America/Chicago"
LAT, LON = 43.0731, -89.4012


def _state(hour=14, minute=0, day=29):
    d = dt.datetime(2026, 7, day, hour, minute, tzinfo=ZoneInfo(TZ))
    return A.calculate_complete_state(d, LAT, LON, TZ)


@pytest.fixture(scope="module")
def aligned_state():
    """29 Jul 2026 14:00 CDT — four compounds active (the Orlee window).

    Re-pinned from 16:00 after the wing-relative branch scheme landed
    (AUDIT_2026-07-24 A-7/A-8, ruled canon): the Small Intestine / Du Mai
    Full-Alignment window at Madison now runs ~13:05–15:30 CDT.
    """
    return _state()


# ── the readout is data, not prose ────────────────────────────────


def test_readout_carries_the_named_correspondences(aligned_state):
    """Vessel, lunar phase + trigram, and organ clock are read directly."""
    text = readout(aligned_state)
    assert "Du Mai — Governing Vessel" in text
    assert "Full Moon" in text
    assert "☰ Qián — Heaven" in text
    assert "Small Intestine" in text or "Sm Intestine" in text
    assert "SI-3 (Small Intestine)" in text  # confluent point, resolved
    assert "Object Consecration" in text  # divine hour protocol


def test_readout_contains_no_prose_descriptions(aligned_state):
    """The presentation layer's sentence fragments must not reach the readout."""
    text = readout(aligned_state)
    banned = [
        "is open, carrying",
        "The Soul and Astral bodies carry",
        "The open Vessel's confluent point falls",
        "Vessel polarity matches",
    ]
    for phrase in banned:
        assert phrase not in text, f"prose leaked into readout: {phrase!r}"


def test_readout_is_deterministic(aligned_state):
    """Same state in, byte-identical output. No vocabulary rotation."""
    assert readout(aligned_state) == readout(aligned_state)


def test_readout_lists_only_active_compounds(aligned_state):
    """Active compounds are named; the ~30 inactive ones are not printed."""
    text = readout(aligned_state)
    assert "COMPOUNDS ACTIVE (4)" in text
    assert "Two-Body Law Unity" in text
    # An inactive compound must not appear at all
    assert "VADUSFADAHM Active" not in text


def test_raw_alias_compound_suppressed(aligned_state):
    """two_body_unity_raw duplicates two_body_unity — reported once."""
    keys = [k for k, _ in active_compounds(aligned_state)]
    assert "two_body_unity" in keys
    assert "two_body_unity_raw" not in keys


def test_absent_data_renders_as_dash_not_invention():
    """A moment with no Solar Key reports none; nothing is filled in."""
    text = readout(_state(hour=16))
    assert "none (no cusping window)" in text
    assert DASH in text  # great_rite is null at this moment


# ── the typed core survives boundaries ────────────────────────────


def test_typed_state_is_one_fact_per_line(aligned_state):
    """Every payload line is a single KEY = value pair (XR-001 form)."""
    lines = typed_state(aligned_state).splitlines()
    assert lines[0].startswith("=== VERIFIED STATE")
    assert lines[-1].startswith("=== END VERIFIED STATE")
    for line in lines[1:-1]:
        assert line.count("=") >= 1
        key, _, value = line.partition("=")
        assert key.strip()
        assert value.strip()


def test_typed_state_values_match_the_engine(aligned_state):
    """Typed values are read from the state, never re-derived."""
    typed = typed_state(aligned_state)
    assert f"vessel.open          = {aligned_state['derivative']['vessel']}" in typed
    assert f"organ.element        = {aligned_state['organ_clock']['element']}" in typed
    assert f"hour.roman           = {aligned_state['divine_hour']['roman']}" in typed


# ── the story gate ────────────────────────────────────────────────


def test_story_gate_opens_on_structural_alignment(aligned_state):
    gate = story_gate(aligned_state)
    assert gate["licensed"] is True
    assert "Two-Body Law Unity" in gate["subjects"]
    assert gate["max_sentences"] == 3


def test_story_gate_closes_on_a_quiet_moment():
    """17:05 on the same day: compounds drop. No licence to interpret."""
    gate = story_gate(_state(hour=17, minute=30))
    assert gate["licensed"] is False
    assert gate["subjects"] == []


def test_story_licensing_covers_key_amplified_intersections():
    """C-06 (2026-07-30): anatomical intersections amplified by a Solar Key
    are licensed subjects — the gate may lawfully name the Key aspect."""
    for compound in ("anatomical_key", "conditional_3_4", "conditional_3_5"):
        assert compound in STORY_LICENSING_COMPOUNDS


def test_key_derivative_unity_stays_unlicensed():
    """DECISION (2026-07-30): key_derivative_unity is excluded per the
    CLAUDE.md five-class license (Two-Body Unity, anatomical intersection,
    Key amplification, Great Rite, VADUSFADAHM)."""
    assert "key_derivative_unity" not in STORY_LICENSING_COMPOUNDS


# ── the instantiation sheet ───────────────────────────────────────


def test_sheet_never_fabricates_absent_corpus():
    """With no private corpus, corpus slots say so — they do not guess."""
    marks = marks_for_card(0, trumps={})
    values = {name: value for _, name, value in marks}
    assert values["Sacred Language — Latin letters"] == NOT_LOADED
    assert values["Hebrew letter operator"] == NOT_LOADED


def test_glyph_slots_are_always_slots():
    """Glyphs with no digital source are never approximated, corpus or not."""
    for table in ({}, None):
        marks = marks_for_card(0, trumps=table) if table is not None else marks_for_card(0)
        values = {name: value for _, name, value in marks}
        assert values["Sacred Language — Damanhurian glyph"] == SLOT
        assert values["Falco's magickal alphabet glyph"] == SLOT


def test_quintessence_is_card_zero_only():
    fool = [name for _, name, _ in marks_for_card(0, trumps={})]
    other = [name for _, name, _ in marks_for_card(1, trumps={})]
    assert any("Quintessence" in n for n in fool)
    assert not any("Quintessence" in n for n in other)


def test_sheet_carries_no_equations(aligned_state):
    """No isopsephic values or arithmetic reach the artist's sheet.

    B-08 (2026-07-30): the literal corpus value formerly probed here is
    dropped from the banned list — the structural tokens below already
    catch equation leakage, and the value itself must not ship in this
    package (corpus boundary: isopsephic values appear nowhere here).
    """
    text = instantiation_sheet(0, aligned_state, trumps={})
    for token in ("=", "×", "prime", "factor"):
        if token == "=":
            # '=' appears only in the sheet's own banner rules
            assert "= 6" not in text and "= 2" not in text
            continue
        assert token not in text, f"math leaked onto the sheet: {token!r}"


def test_sheet_reports_the_window_from_state(aligned_state):
    text = instantiation_sheet(0, aligned_state, trumps={})
    assert "Object Consecration" in text
    assert "Du Mai" in text
    assert "Full Moon" in text


# ── precision: the Divine Hour is the unit, not the clock ─────────


def test_coarse_is_the_default(aligned_state):
    """Default output carries no minute-exact claim."""
    text = readout(aligned_state)
    assert "~" in text                      # clock times marked approximate
    assert "min remaining" not in text      # no decimal-minute precision
    assert "min total" not in text


def test_exact_available_on_request(aligned_state):
    text = readout(aligned_state, precision=EXACT)
    assert "min remaining" in text
    assert "~" not in text.split("VESSEL")[0]   # frame block unrounded


def test_coarse_rounds_to_five_minutes(aligned_state):
    from src.readout import _clock
    assert _clock("2026-07-29T16:43:00-05:00", COARSE) == "~16:45"
    assert _clock("2026-07-29T16:41:00-05:00", COARSE) == "~16:40"
    assert _clock("2026-07-29T16:43:00-05:00", EXACT) == "16:43"


def test_hour_position_is_a_phrase_when_coarse(aligned_state):
    hour = aligned_state["divine_hour"]
    phrase = hour_position(hour, COARSE)
    assert phrase in {"opening", "well inside", "past the middle", "closing"}
    assert "min" in hour_position(hour, EXACT)


def test_hour_position_handles_absent_progress():
    assert hour_position({}, COARSE) == DASH
