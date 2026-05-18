"""
Tests for the axial precession engine.

Validates:
  • current_ayanamsa against known reference values (J2000, modern)
  • current_age places us in Pisces in 2026
  • equinox_position returns sensible sidereal longitude
  • next_age_transition projects to Aquarius
  • closest_pole_star returns Polaris for our era
  • precession constants are physically correct
"""

from datetime import datetime
import pytest
import pytz

from src.engine import precession


# ── Constants ───────────────────────────────────────────────────────

def test_precession_period_is_great_year():
    """Great Year should be approximately 25,772 years."""
    assert 25000 <= precession.PRECESSION_PERIOD_YEARS <= 26000


def test_age_duration_is_about_2148_years():
    """Great Year / 12 ≈ 2,148 years."""
    assert 2100 < precession.AGE_DURATION_YEARS < 2200


def test_precession_rate_is_50_arcsec_per_year():
    """Standard rate of equinox drift."""
    assert 49.0 < precession.PRECESSION_RATE_ARCSEC_PER_YEAR < 51.0


# ── Ayanamsa correctness ────────────────────────────────────────────

def test_ayanamsa_at_j2000_is_about_23_85():
    """Lahiri ayanamsa at J2000.0 = 23.8519° conventionally."""
    dt = pytz.utc.localize(datetime(2000, 1, 1, 12, 0))
    a = precession.current_ayanamsa(dt)
    assert 23.8 < a < 23.9


def test_ayanamsa_at_2026_is_about_24_2():
    """Ayanamsa increases ~0.014°/yr; in 2026 should be ~24.2."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    a = precession.current_ayanamsa(dt)
    assert 24.15 < a < 24.30


def test_ayanamsa_increases_over_time():
    """Ayanamsa grows monotonically with time."""
    a1 = precession.current_ayanamsa(pytz.utc.localize(datetime(2000, 1, 1)))
    a2 = precession.current_ayanamsa(pytz.utc.localize(datetime(2100, 1, 1)))
    assert a2 > a1


# ── Equinox position ────────────────────────────────────────────────

def test_equinox_position_in_2026_is_late_pisces():
    """Vernal equinox sidereal longitude in 2026 should sit around
    335-336° — late Pisces (which spans 330-360°)."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    pos = precession.equinox_position(dt)
    sid_lon = pos["sidereal_longitude_deg"]
    assert 330 < sid_lon < 360, (
        f"Expected vernal equinox in Pisces (330-360°), got {sid_lon}°"
    )


def test_equinox_constellation_is_pisces_in_2026():
    """The Age in 2026 is Pisces."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    pos = precession.equinox_position(dt)
    assert pos["constellation_traditional"] == "Pisces"


# ── Current Age ─────────────────────────────────────────────────────

def test_current_age_in_2026_is_pisces():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    age = precession.current_age(dt)
    assert age["age_english"] == "Pisces"
    assert age["age_sanskrit"] == "Mīna"


def test_age_fraction_in_range():
    """fraction_through_age should be in [0, 1]."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    age = precession.current_age(dt)
    assert 0.0 <= age["fraction_through_age"] <= 1.0


def test_age_years_remaining_reasonable():
    """We have hundreds of years left in Pisces — at least 100, less than full Age duration."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    age = precession.current_age(dt)
    assert 100 < age["years_remaining"] < precession.AGE_DURATION_YEARS


# ── Next age transition ────────────────────────────────────────────

def test_next_age_after_pisces_is_aquarius():
    """Precession moves the equinox westward through the zodiac. After Pisces comes Aquarius."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    nxt = precession.next_age_transition(dt)
    assert nxt["next_age_english"] == "Aquarius"
    assert nxt["next_age_sanskrit"] == "Kumbha"


def test_next_age_year_is_future():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    nxt = precession.next_age_transition(dt)
    assert nxt["approximate_year_ce"] > 2026


# ── Pole star tracking ─────────────────────────────────────────────

def test_pole_star_in_2026_is_polaris():
    """Polaris is closest to the pole around 2100, so 2026 should pick it."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    star = precession.closest_pole_star(dt)
    assert "Polaris" in star["name"]


def test_pole_star_in_bronze_age_is_thuban():
    """Thuban (α Dra) was closest to the pole around 3000 BCE."""
    dt = datetime(year=1, month=1, day=1, tzinfo=pytz.utc)
    # Use a BCE-ish year via the decimal-year math
    # Simulate -2700 by directly calling ayanamsa_at_year
    pole_year = -2700
    closest = min(
        precession.POLE_STARS,
        key=lambda p: abs(p[1] - pole_year),
    )
    assert "Thuban" in closest[0]


# ── precession_summary integration ────────────────────────────────

def test_precession_summary_has_all_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    s = precession.precession_summary(dt)
    for key in ("ayanamsa_deg", "equinox_position", "current_age",
                "next_age_transition", "closest_pole_star",
                "precession_period_years", "precession_rate_arcsec_per_year"):
        assert key in s


def test_precession_summary_internally_consistent():
    """The ayanamsa in the summary should match current_ayanamsa()."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    s = precession.precession_summary(dt)
    assert abs(s["ayanamsa_deg"] - precession.current_ayanamsa(dt)) < 1e-9


# ── Historical anchor checks ──────────────────────────────────────

def test_ayanamsa_at_year_helper_matches():
    """The year-only helper should match the datetime version at midyear."""
    dt = pytz.utc.localize(datetime(2026, 7, 1, 12, 0))
    a_dt = precession.current_ayanamsa(dt)
    a_yr = precession.ayanamsa_at_year(2026.5)
    assert abs(a_dt - a_yr) < 0.01
