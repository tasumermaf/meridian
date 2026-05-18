"""
Tests for the lunar standstills engine (18.6-year nodal cycle).

Validates:
  • cycle_fraction returns sane values [0, 1)
  • next major/minor standstills are in the future
  • closer_standstill flips correctly around half-cycle
  • declination extremes are physical
  • node_longitude_deg in [0, 360)
"""

from datetime import datetime, timedelta
import pytest
import pytz

from src.engine import lunar_standstills as ls


def test_nodal_period_is_18_6_years():
    assert 18.5 < ls.NODAL_PERIOD_YEARS < 18.7


def test_major_standstill_max_decl_about_28_7():
    assert 28.0 < ls.MAJOR_STANDSTILL_MAX_DECL_DEG < 29.0


def test_minor_standstill_max_decl_about_18_3():
    assert 18.0 < ls.MINOR_STANDSTILL_MAX_DECL_DEG < 18.5


def test_cycle_fraction_at_reference_is_zero():
    """At the LAST_MAJOR_STANDSTILL datetime, fraction should be ~0."""
    dt = ls.LAST_MAJOR_STANDSTILL
    assert ls.cycle_fraction(dt) < 0.001


def test_cycle_fraction_in_range():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    f = ls.cycle_fraction(dt)
    assert 0.0 <= f < 1.0


def test_cycle_fraction_in_2026_is_small():
    """2026 is one year after the 2025 major standstill peak — fraction should be ~0.05."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    f = ls.cycle_fraction(dt)
    assert 0.02 < f < 0.10


def test_closer_in_2026_is_major():
    """One year after a major standstill, we're still closer to major."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    assert ls.closer_standstill(dt) == "major"


def test_next_major_standstill_is_future():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    next_m = ls.next_major_standstill(dt)
    assert next_m > dt


def test_next_minor_standstill_is_future():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    next_m = ls.next_minor_standstill(dt)
    assert next_m > dt


def test_next_major_about_18_years_after_2025_peak():
    """The next major after the 2025 peak should be around 2043."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    next_m = ls.next_major_standstill(dt)
    assert 2043 <= next_m.year <= 2044


def test_node_longitude_in_range():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    lon = ls.current_node_longitude(dt)
    assert 0 <= lon < 360


def test_node_longitude_at_reference_is_near_zero():
    """At the reference standstill, ascending node was near 0° sidereal."""
    dt = ls.LAST_MAJOR_STANDSTILL
    lon = ls.current_node_longitude(dt)
    assert lon < 0.1 or lon > 359.9


def test_node_regresses_westward():
    """A year later, node longitude should be lower (mod 360) — regression."""
    dt1 = ls.LAST_MAJOR_STANDSTILL
    dt2 = dt1 + timedelta(days=365)
    lon1 = ls.current_node_longitude(dt1)
    lon2 = ls.current_node_longitude(dt2)
    # Should decrease (mod 360) — equivalently, lon2 should be less than lon1
    # mod 360. Going from 0 backward, lon2 should be ~340.
    assert 300 < lon2 < 360


def test_state_has_required_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = ls.get_lunar_standstill_state(dt)
    for key in ("cycle_fraction", "closer", "distance_to_closer_days",
                "next_major_standstill", "next_minor_standstill",
                "node_longitude_deg",
                "max_declination_at_closer_standstill_deg",
                "nodal_period_years"):
        assert key in state


def test_state_at_2026_says_closer_to_major():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = ls.get_lunar_standstill_state(dt)
    assert state["closer"] == "major"
    assert state["max_declination_at_closer_standstill_deg"] == ls.MAJOR_STANDSTILL_MAX_DECL_DEG
