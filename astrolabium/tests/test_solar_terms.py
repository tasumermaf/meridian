"""
Tests for the 24-Solar-Term engine.

Validates:
  • data integrity (24 terms, alternating sectional/mid, longitudes every 15°)
  • current-term lookup correctness at known anchor dates (equinoxes, solstices)
  • next-term transition finds the right term at the right time
  • term fraction tracking
"""

from datetime import datetime, timedelta
import pytest
import pytz

from src.engine import solar_terms


# ── Data integrity ──────────────────────────────────────────────────

def test_term_count_is_24():
    assert solar_terms.get_term_count() == 24


def test_term_longitudes_are_15deg_multiples():
    for t in solar_terms.list_terms():
        assert t["ecliptic_longitude_deg"] % 15 == 0


def test_terms_alternate_sectional_and_mid():
    """The 24 terms alternate sectional (节) and mid (气). Lìchūn is sectional."""
    terms = solar_terms.list_terms()
    for i, t in enumerate(terms):
        expected = "sectional" if i % 2 == 0 else "mid"
        assert t["category"] == expected, (
            f"Term {i} ({t['english']}) is {t['category']}, expected {expected}"
        )


def test_terms_in_canonical_order():
    """Lìchūn is index 0, Dàhán is index 23. Verify the sequence."""
    terms = solar_terms.list_terms()
    assert terms[0]["pinyin"] == "Lìchūn"
    assert terms[3]["pinyin"] == "Chūnfēn"   # Spring Equinox
    assert terms[9]["pinyin"] == "Xiàzhì"    # Summer Solstice
    assert terms[15]["pinyin"] == "Qiūfēn"   # Autumn Equinox
    assert terms[21]["pinyin"] == "Dōngzhì"  # Winter Solstice
    assert terms[23]["pinyin"] == "Dàhán"


# ── Anchor-date correctness (the four cardinal terms) ─────────────

def test_spring_equinox_2026():
    """Around 2026-03-20 the Sun crosses 0° (Spring Equinox at 14:46 UTC).
    Sample 12 hours after the exact event to be safely inside Chūnfēn."""
    dt = pytz.utc.localize(datetime(2026, 3, 21, 6, 0))  # ~16h after equinox
    term = solar_terms.get_current_solar_term(dt)
    assert term["pinyin"] == "Chūnfēn"
    assert term["english"] == "Spring Equinox"
    assert term["ecliptic_longitude_deg"] == 0


def test_summer_solstice_2026():
    """Around 2026-06-21 08:24 UTC the Sun crosses 90°. Sample later same day."""
    dt = pytz.utc.localize(datetime(2026, 6, 22, 0, 0))  # ~16h after solstice
    term = solar_terms.get_current_solar_term(dt)
    assert term["pinyin"] == "Xiàzhì"
    assert term["english"] == "Summer Solstice"
    assert term["ecliptic_longitude_deg"] == 90


def test_autumn_equinox_2026():
    """Around 2026-09-23 04:05 UTC the Sun crosses 180°. Sample later same day."""
    dt = pytz.utc.localize(datetime(2026, 9, 23, 20, 0))
    term = solar_terms.get_current_solar_term(dt)
    assert term["pinyin"] == "Qiūfēn"
    assert term["ecliptic_longitude_deg"] == 180


def test_winter_solstice_2026():
    """Around 2026-12-21 15:50 UTC the Sun crosses 270°. Sample next morning."""
    dt = pytz.utc.localize(datetime(2026, 12, 22, 8, 0))
    term = solar_terms.get_current_solar_term(dt)
    assert term["pinyin"] == "Dōngzhì"
    assert term["ecliptic_longitude_deg"] == 270


# ── Mid-Saga-Dawa context check ────────────────────────────────────

def test_mid_may_2026_in_xiaoman_or_neighbor():
    """
    May 18 2026 (during Saga Dawa). The Sun should be in the Lìxià →
    Xiǎomǎn region (longitude 45-60° tropical).
    """
    dt = pytz.utc.localize(datetime(2026, 5, 18, 8, 0))
    term = solar_terms.get_current_solar_term(dt)
    # Should be Lìxià (Beginning of Summer, 45°) - we're past it but before Xiǎomǎn
    assert term["pinyin"] in ("Lìxià", "Xiǎomǎn"), (
        f"Expected Lìxià or Xiǎomǎn on 2026-05-18, got {term['pinyin']}"
    )


# ── Fraction-into-term tracking ────────────────────────────────────

def test_fraction_into_term_is_in_range():
    """Fraction should be in [0, 1)."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 8, 0))
    term = solar_terms.get_current_solar_term(dt)
    assert 0.0 <= term["fraction_into_term"] < 1.0


def test_degrees_into_term_under_15():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 8, 0))
    term = solar_terms.get_current_solar_term(dt)
    assert 0.0 <= term["degrees_into_term"] < 15.0


# ── Next-term transition ─────────────────────────────────────────

def test_next_term_after_spring_equinox():
    """After Chūnfēn (Spring Equinox, 0°), the next term should be Qīngmíng (15°)."""
    dt = pytz.utc.localize(datetime(2026, 3, 22, 0, 0))  # day after equinox
    next_t = solar_terms.get_next_solar_term(dt)
    assert next_t["pinyin"] == "Qīngmíng"


def test_next_term_returns_future_datetime():
    """The transition datetime must be after the query datetime."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 8, 0))
    next_t = solar_terms.get_next_solar_term(dt)
    assert next_t["transition_datetime"] > dt


def test_next_term_within_16_days():
    """A solar term is ~15 days, so the next one should be within 16 days."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 8, 0))
    next_t = solar_terms.get_next_solar_term(dt)
    delta = next_t["transition_datetime"] - dt
    assert delta.days <= 16


# ── Year-wrap handling ────────────────────────────────────────────

def test_late_year_wraps_to_january_term():
    """Around mid-January, the next term after Xiǎohán (5-7 Jan) is Dàhán (20-21 Jan)."""
    dt = pytz.utc.localize(datetime(2026, 1, 10, 0, 0))
    next_t = solar_terms.get_next_solar_term(dt)
    assert next_t["pinyin"] == "Dàhán"


# ── State composition ────────────────────────────────────────────

def test_get_solar_term_state_returns_both():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 8, 0))
    state = solar_terms.get_solar_term_state(dt)
    assert "current" in state
    assert "next" in state
    assert state["current"]["index"] != state["next"]["index"]
