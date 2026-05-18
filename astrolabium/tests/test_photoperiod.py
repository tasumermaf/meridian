"""
Tests for the photoperiod engine.

Validates:
  • daylight hours close to 12 at the equator year-round
  • daylight hours = 12 ± a few minutes at all latitudes at equinox
  • daylight maximum at summer solstice, minimum at winter solstice
  • daylight_change_rate is positive in spring, negative in autumn
  • hemisphere flip: southern-hemisphere May is autumn, not spring
  • seasonal_arc_position composes correctly
"""

from datetime import datetime
import pytest
import pytz

from src.engine import photoperiod


DAMANHUR = {"lat": 45.42, "lon": 7.78, "tz": "Europe/Rome"}
EQUATOR  = {"lat": 0.0, "lon": 0.0, "tz": "UTC"}
SYDNEY   = {"lat": -33.87, "lon": 151.21, "tz": "Australia/Sydney"}


# ── Daylight hours ─────────────────────────────────────────────

def test_daylight_at_equator_is_about_12_hours():
    """At the equator, daylight is always ~12 hours regardless of date."""
    dt_jun = pytz.utc.localize(datetime(2026, 6, 21, 12, 0))
    dt_dec = pytz.utc.localize(datetime(2026, 12, 21, 12, 0))
    d_jun = photoperiod.daylight_hours(dt_jun, **EQUATOR)
    d_dec = photoperiod.daylight_hours(dt_dec, **EQUATOR)
    assert abs(d_jun - 12.0) < 0.3
    assert abs(d_dec - 12.0) < 0.3


def test_daylight_max_at_northern_summer_solstice():
    """At Damanhur (45.4°N), the summer solstice has the longest daylight."""
    dt_summer = pytz.utc.localize(datetime(2026, 6, 21, 12, 0))
    dt_winter = pytz.utc.localize(datetime(2026, 12, 21, 12, 0))
    d_summer = photoperiod.daylight_hours(dt_summer, **DAMANHUR)
    d_winter = photoperiod.daylight_hours(dt_winter, **DAMANHUR)
    assert d_summer > 15.0   # ~15:30 at 45°N
    assert d_winter < 9.5    # ~8:50 at 45°N


def test_daylight_max_at_southern_summer_solstice():
    """At Sydney (33.9°S), the SOUTHERN summer is December — longest day there."""
    dt_dec = pytz.utc.localize(datetime(2026, 12, 21, 12, 0))
    dt_jun = pytz.utc.localize(datetime(2026, 6, 21, 12, 0))
    d_dec = photoperiod.daylight_hours(dt_dec, **SYDNEY)
    d_jun = photoperiod.daylight_hours(dt_jun, **SYDNEY)
    assert d_dec > d_jun


def test_daylight_at_equinox_about_12():
    """At any latitude, daylight at the equinox is ~12 hours (slight excess from refraction)."""
    dt = pytz.utc.localize(datetime(2026, 3, 21, 12, 0))
    d_damanhur = photoperiod.daylight_hours(dt, **DAMANHUR)
    assert 11.9 < d_damanhur < 12.3


def test_night_plus_day_is_24():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    d = photoperiod.daylight_hours(dt, **DAMANHUR)
    n = photoperiod.night_hours(dt, **DAMANHUR)
    assert abs((d + n) - 24.0) < 1e-6


# ── Twilight durations ─────────────────────────────────────────

def test_twilight_durations_present():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    tw = photoperiod.twilight_durations(dt, **DAMANHUR)
    # Civil < nautical < astronomical
    assert tw["civil_minutes"] > 0
    assert tw["nautical_minutes"] > tw["civil_minutes"]
    assert tw["astronomical_minutes"] > tw["nautical_minutes"]


def test_twilight_durations_at_equinox():
    """At the equator on the equinox, twilight bands are short and equal."""
    dt = pytz.utc.localize(datetime(2026, 3, 21, 12, 0))
    tw = photoperiod.twilight_durations(dt, **EQUATOR)
    # Civil twilight at equator is ~24 minutes
    assert 20 < tw["civil_minutes"] < 30


# ── Daylight change rate ───────────────────────────────────────

def test_daylight_lengthening_in_spring_northern():
    """In April at Damanhur, daylight is increasing."""
    dt = pytz.utc.localize(datetime(2026, 4, 15, 12, 0))
    rate = photoperiod.daylight_change_rate_minutes_per_day(dt, **DAMANHUR)
    assert rate > 0


def test_daylight_shortening_in_autumn_northern():
    """In October at Damanhur, daylight is decreasing."""
    dt = pytz.utc.localize(datetime(2026, 10, 15, 12, 0))
    rate = photoperiod.daylight_change_rate_minutes_per_day(dt, **DAMANHUR)
    assert rate < 0


def test_daylight_lengthening_in_southern_spring():
    """In October at Sydney (southern spring), daylight is increasing."""
    dt = pytz.utc.localize(datetime(2026, 10, 15, 12, 0))
    rate = photoperiod.daylight_change_rate_minutes_per_day(dt, **SYDNEY)
    assert rate > 0


def test_daylight_rate_near_zero_at_solstice():
    """At the solstices, daylight is changing very little day to day."""
    dt = pytz.utc.localize(datetime(2026, 6, 21, 12, 0))
    rate = photoperiod.daylight_change_rate_minutes_per_day(dt, **DAMANHUR)
    # < 0.5 min/day near solstice
    assert abs(rate) < 0.5


# ── Solstice / equinox proximity ───────────────────────────────

def test_days_from_solstice():
    """May 18 is close to summer solstice (~33 days away)."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    near = photoperiod.days_from_nearest_solstice(dt)
    assert near["abs_days"] < 50


def test_days_from_equinox():
    """May 18 is ~60 days past March 20 equinox."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    near = photoperiod.days_from_nearest_equinox(dt)
    assert near["which"] == "march"
    assert near["days_offset"] > 0


# ── Seasonal arc ───────────────────────────────────────────────

def test_seasonal_arc_may_in_north_is_spring():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    arc = photoperiod.seasonal_arc_position(dt, **DAMANHUR)
    assert arc["hemisphere"] == "northern"
    assert arc["season"] == "spring"
    assert arc["daylight_trend"] == "lengthening"


def test_seasonal_arc_may_in_south_is_autumn():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    arc = photoperiod.seasonal_arc_position(dt, **SYDNEY)
    assert arc["hemisphere"] == "southern"
    assert arc["season"] == "autumn"
    assert arc["daylight_trend"] == "shortening"


def test_seasonal_arc_january_in_north_is_winter():
    dt = pytz.utc.localize(datetime(2026, 1, 15, 12, 0))
    arc = photoperiod.seasonal_arc_position(dt, **DAMANHUR)
    assert arc["season"] == "winter"


# ── photoperiod_state composite ────────────────────────────────

def test_photoperiod_state_has_all_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = photoperiod.photoperiod_state(dt, **DAMANHUR)
    for key in ("daylight_hours", "night_hours", "twilight_minutes",
                "daylight_change_rate_minutes_per_day", "seasonal_arc"):
        assert key in state


def test_photoperiod_state_consistency():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = photoperiod.photoperiod_state(dt, **DAMANHUR)
    direct_daylight = photoperiod.daylight_hours(dt, **DAMANHUR)
    assert abs(state["daylight_hours"] - direct_daylight) < 1e-9
