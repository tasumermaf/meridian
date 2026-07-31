"""
Astrolabium Caudae Rubrae — Instantiation Sheet.

The practical artifact for an instantiation session: which marks go on the
card, in what order, and when the window opens and closes.

WHAT THIS IS NOT
----------------
It is not an analysis. No isopsephic values, no factorizations, no
equations appear on this sheet, because none of them are laid on the
painting. The numbers belong to the corpus analysis and stay there; the
artist's hand needs the marks and the window, nothing else.

CORPUS BOUNDARY
---------------
Card inscriptions are proprietary corpus data (Promptcrafted / TASUMER
MAF) and Damanhurian source material. They live in a private data file
that is NOT distributed with this package:

    data/trumps.private.json        (gitignored)

The mechanism in this module is open. The corpus is not. If the private
file is absent, every corpus-bearing slot renders as [NOT LOADED] and the
sheet still prints its structure — so the code can be published and
tested without shipping the inscriptions.

GLYPH SLOTS
-----------
Two mark types have no digital source in this repository — the Damanhurian
Sacred Language glyph and Falco's magickal alphabet glyph. They are
rendered as explicit slots. They are never invented, approximated, or
substituted. Timothy supplies them from the source material.
"""

import json
from pathlib import Path
from typing import Optional

from .readout import _clock, _v, DASH

PRIVATE_TRUMPS = Path(__file__).resolve().parent.parent / "data" / "trumps.private.json"

NOT_LOADED = "[NOT LOADED — private corpus file absent]"
SLOT = "[SLOT — supplied from source by Timothy]"

# Unicode has a named codepoint for this mark. Offered as a candidate for
# the Fool's fifth-element sign; Timothy confirms the form actually used.
#
# Named in WORDS first, glyph second: U+1F700 is absent from nearly every
# font (on Windows only Segoe UI Symbol carries it) and prints as an empty
# box in PDF pipelines. The text must carry the meaning even where the
# glyph does not — and per the project rule, a mark is never approximated
# with a lookalike character.
QUINTESSENCE_CANDIDATE = (
    "the alchemical QUINTESSENCE sign — Unicode U+1F700 — CONFIRM FORM"
)


def load_trumps(path: Optional[Path] = None) -> dict:
    """Load the private trump table. Returns {} when absent — never raises."""
    p = Path(path) if path else PRIVATE_TRUMPS
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as fh:
        data = json.load(fh)
    return {str(card["number"]): card for card in data.get("trumps", [])}


def marks_for_card(number: int, trumps: Optional[dict] = None) -> list:
    """
    The ordered list of marks to lay on one card.

    Returns a list of (order, mark_name, value) triples. Corpus-bearing
    values render as NOT_LOADED without the private file; glyph values
    with no digital source render as SLOT.
    """
    table = trumps if trumps is not None else load_trumps()
    card = table.get(str(number), {})

    marks = [
        ("Sacred Language — Latin letters", card.get("inscription") or NOT_LOADED),
        ("Sacred Language — Damanhurian glyph", SLOT),
        ("Hebrew letter operator", _hebrew(card)),
        ("Falco's magickal alphabet glyph", SLOT),
        ("Card number", str(number)),
        ("Sound — Latin letters", card.get("sound") or NOT_LOADED),
    ]

    # The Fool alone carries the fifth-element mark.
    if number == 0:
        marks.append(("Quintessence sign (Card 0 only)", QUINTESSENCE_CANDIDATE))

    marks.append(("Artist's seal / signature", "Orlee's own, per Tarot tradition"))
    return [(i + 1, name, value) for i, (name, value) in enumerate(marks)]


def _hebrew(card: dict) -> str:
    """'ש (Shin)' — letter and name, no value. The value is not laid on the card."""
    letter = card.get("hebrew_letter")
    name = card.get("hebrew_name")
    if not letter and not name:
        return NOT_LOADED
    if letter and name:
        return f"{letter}  ({name})"
    return letter or name


def instantiation_sheet(
    number: int,
    state: dict,
    *,
    window: Optional[str] = None,
    place: Optional[str] = None,
    trumps: Optional[dict] = None,
) -> str:
    """
    Render the working sheet for one card at one moment.

    Two blocks only: the marks to lay, and the window they are laid in.
    """
    table = trumps if trumps is not None else load_trumps()
    card = table.get(str(number), {})
    title = card.get("title") or f"Card {number}"

    vessel = state.get("derivative", {}) or {}
    soul = state.get("primeval", {}) or {}
    organ = state.get("organ_clock", {}) or {}
    hour = state.get("divine_hour", {}) or {}
    cal = state.get("calendar", {}) or {}

    L = [f"=== INSTANTIATION SHEET — CARD {number}: {title.upper()} ==="]
    L.append("")
    L.append("MARKS TO LAY")
    for order, name, value in marks_for_card(number, table):
        L.append(f"  {order}. {name:<38} {value}")

    L.append("")
    L.append("THE WINDOW")
    if window:
        L.append(f"  {'when':<20}{window}")
    if place:
        L.append(f"  {'where':<20}{place}")
    L.append(f"  {'divine hour':<20}{_v(hour.get('roman'))} — {_v(hour.get('protocols'))}")
    L.append(f"  {'vessel open':<20}{_v(vessel.get('vessel'))} — {_v(vessel.get('law'))}")
    L.append(f"  {'lunar phase':<20}{_v(soul.get('phase'))} · {_v(soul.get('symbol'))} {_v(soul.get('trigram'))}")
    L.append(f"  {'organ':<20}{_v(organ.get('organ'))} · {_v(organ.get('element'))}")
    L.append(f"  {'healing sound':<20}{_v(organ.get('healing_sound'))}")
    L.append(f"  {'vowel / mudra':<20}{_v(soul.get('vowel'))} · {_v(soul.get('mudra'))}")
    L.append(f"  {'month / day':<20}{_v(cal.get('month_name'))} · day {_v(cal.get('day_in_month'))} · {_v(cal.get('sephirah'))}")

    L.append("")
    L.append("=== END SHEET ===")
    return "\n".join(L)
