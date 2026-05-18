"""
Photoperiod engine — the ecological layer's astronomical foundation.

Photoperiod is the duration of daylight at a given location on a
given date. It is the single most important ecological variable in
temperate-latitude biology — entraining circadian rhythms, controlling
flowering and migration cues, governing seasonal hormonal cycles, and
defining the practical envelope of agricultural activity.

This module derives photoperiod metrics from the existing solar engine.
No network calls. No climate database. Pure local computation from the
practitioner's location.

Provided metrics:

  • daylight_hours(dt, lat, lon, tz)         — sunrise to sunset
  • civil_twilight_duration                  — sunrise → civil dusk
  • nautical_twilight_duration               — civil → nautical
  • astronomical_twilight_duration           — nautical → astronomical
  • daylight_change_rate_minutes_per_day     — gaining or losing daylight
  • days_from_nearest_solstice
  • days_from_nearest_equinox
  • seasonal_arc_position(dt, lat, lon, tz)  — composite seasonal state
  • photoperiod_state(dt, lat, lon, tz)      — orchestrator-ready summary

All times are computed by astral via the existing engine.solar module.

[MATHEMATICAL FACT] — solar position computation.
[SOURCE: astronomy] — twilight definitions (civil = sun 0-6° below
horizon, nautical 6-12°, astronomical 12-18°).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pytz
from astral import LocationInfo
from astral.sun import sun, dawn, dusk

from . import solar as _solar


# ── Helpers ──────────────────────────────────────────────────────────

def _normalize_to_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


def _location(lat: float, lon: float, tz: str) -> LocationInfo:
    return LocationInfo(latitude=lat, longitude=lon, timezone=tz)


# ── Photoperiod core ─────────────────────────────────────────────────

def daylight_hours(dt: datetime, lat: float, lon: float, tz: str) -> float:
    """
    Return the number of hours between sunrise and sunset for the given
    location and date.
    """
    pos = _solar.get_solar_positions(dt, lat, lon, tz)
    return (pos["sunset"] - pos["sunrise"]).total_seconds() / 3600.0


def night_hours(dt: datetime, lat: float, lon: float, tz: str) -> float:
    """Hours from sunset to next sunrise."""
    return 24.0 - daylight_hours(dt, lat, lon, tz)


# ── Twilight durations ───────────────────────────────────────────────

def twilight_durations(
    dt: datetime, lat: float, lon: float, tz: str
) -> dict:
    """
    Return civil, nautical, and astronomical twilight durations for the
    given location and date.

    Twilight is measured at the SAME end of the day (morning) — the
    interval between the sun being at a given depression angle and
    sunrise itself.

    Civil twilight: sun 6° below horizon → sunrise. Brightest twilight,
    suitable for outdoor activity, lamps usually unnecessary.

    Nautical twilight: sun 12° below horizon → sunrise. Horizon at sea
    still visible; navigation by stars possible.

    Astronomical twilight: sun 18° below horizon → sunrise. Sky fully
    dark for astronomical observation.

    Each duration is returned in minutes.

    Note: at high latitudes near the solstices, some twilight bands
    may not exist (the sun never gets that far below the horizon).
    Returns None for any band that doesn't exist on this date.
    """
    location = _location(lat, lon, tz)
    timezone = pytz.timezone(tz)
    dt_aware = _normalize_to_aware(dt).astimezone(timezone)

    try:
        s = sun(location.observer, date=dt_aware.date(), tzinfo=timezone)
        sunrise = s["sunrise"]
        civil_dawn = s["dawn"]
    except (ValueError, Exception):
        return {"civil_minutes": None, "nautical_minutes": None,
                "astronomical_minutes": None}

    # Civil: dawn → sunrise (astral.sun() gives 6° dawn by default)
    civil_minutes = (sunrise - civil_dawn).total_seconds() / 60.0

    # Nautical and astronomical: use astral.dawn at custom depressions
    try:
        nautical_dawn = dawn(location.observer,
                             date=dt_aware.date(),
                             tzinfo=timezone, depression=12.0)
        nautical_minutes = (sunrise - nautical_dawn).total_seconds() / 60.0
    except (ValueError, Exception):
        nautical_minutes = None

    try:
        astro_dawn = dawn(location.observer,
                         date=dt_aware.date(),
                         tzinfo=timezone, depression=18.0)
        astro_minutes = (sunrise - astro_dawn).total_seconds() / 60.0
    except (ValueError, Exception):
        astro_minutes = None

    return {
        "civil_minutes": civil_minutes,
        "nautical_minutes": nautical_minutes,
        "astronomical_minutes": astro_minutes,
    }


# ── Rate of change ────────────────────────────────────────────────

def daylight_change_rate_minutes_per_day(
    dt: datetime, lat: float, lon: float, tz: str
) -> float:
    """
    Return the rate of change of daylight, in minutes per day.

    Positive = lengthening (between winter solstice and summer solstice
    in the northern hemisphere; between summer solstice and winter
    solstice in the southern hemisphere).

    Negative = shortening.

    Computed as a forward finite difference: tomorrow's daylight minus
    today's daylight.

    At the solstices, this rate is near zero. At the equinoxes it is
    maximal (in absolute value). At extreme latitudes near the solstices
    it can be enormous (the polar day or night transition).
    """
    today = daylight_hours(dt, lat, lon, tz)
    tomorrow = daylight_hours(dt + timedelta(days=1), lat, lon, tz)
    return (tomorrow - today) * 60.0


# ── Solstice / equinox proximity ─────────────────────────────────

def days_from_nearest_solstice(dt: datetime) -> dict:
    """
    Return distance from the nearest June or December solstice.

    Uses approximate fixed dates (June 21, December 21) — accurate to
    ±1 day, sufficient for the ecological framing this module supports.

    Returns:
      - which: "june" or "december"
      - days_offset: float, positive = after solstice, negative = before
      - abs_days: absolute distance in days
    """
    dt = _normalize_to_aware(dt)
    year = dt.year
    june_sols = pytz.utc.localize(datetime(year, 6, 21, 0, 0))
    dec_sols = pytz.utc.localize(datetime(year, 12, 21, 0, 0))
    dec_sols_prev = pytz.utc.localize(datetime(year - 1, 12, 21, 0, 0))

    candidates = [
        ("june",     (dt - june_sols).total_seconds() / 86400),
        ("december", (dt - dec_sols).total_seconds() / 86400),
        ("december", (dt - dec_sols_prev).total_seconds() / 86400),
    ]
    nearest = min(candidates, key=lambda c: abs(c[1]))
    return {
        "which": nearest[0],
        "days_offset": nearest[1],
        "abs_days": abs(nearest[1]),
    }


def days_from_nearest_equinox(dt: datetime) -> dict:
    """
    Return distance from the nearest March or September equinox.

    Uses approximate fixed dates (March 20, September 23). Returns:
      - which: "march" or "september"
      - days_offset: positive = after, negative = before
      - abs_days: absolute distance in days
    """
    dt = _normalize_to_aware(dt)
    year = dt.year
    mar_eq = pytz.utc.localize(datetime(year, 3, 20, 0, 0))
    sep_eq = pytz.utc.localize(datetime(year, 9, 23, 0, 0))
    mar_eq_next = pytz.utc.localize(datetime(year + 1, 3, 20, 0, 0))

    candidates = [
        ("march",     (dt - mar_eq).total_seconds() / 86400),
        ("september", (dt - sep_eq).total_seconds() / 86400),
        ("march",     (dt - mar_eq_next).total_seconds() / 86400),
    ]
    nearest = min(candidates, key=lambda c: abs(c[1]))
    return {
        "which": nearest[0],
        "days_offset": nearest[1],
        "abs_days": abs(nearest[1]),
    }


# ── Seasonal arc framing ─────────────────────────────────────────

def seasonal_arc_position(dt: datetime, lat: float, lon: float, tz: str) -> dict:
    """
    A composite framing of the moment's seasonal state for the
    practitioner.

    Returns dict with:
      - hemisphere: "northern" or "southern" (computed from lat)
      - season: "winter" / "spring" / "summer" / "autumn"
        (computed from days_from_solstice/equinox)
      - days_into_season: float
      - daylight_trend: "lengthening" or "shortening"
      - daylight_minutes_per_day_rate: float (signed)

    This is the practical handle on "what season is it for the
    practitioner at their actual latitude" — which differs from the
    astronomical-calendar abstraction (where everyone is in the same
    "northern season" by convention).
    """
    hemisphere = "northern" if lat >= 0 else "southern"

    # Determine season by combining solstice/equinox proximities
    near_sol = days_from_nearest_solstice(dt)
    near_eq = days_from_nearest_equinox(dt)

    # Northern-hemisphere mapping; flip for southern
    if hemisphere == "northern":
        # Determine current season based on which 90-day window we're in
        # Use month-based rough classification anchored on solstices/equinoxes
        # March equinox → June solstice = Spring
        # June solstice → September equinox = Summer
        # September equinox → December solstice = Autumn
        # December solstice → March equinox = Winter
        # Astronomical seasons:
        month_day_to_season = {
            (3, 20):  "spring",   (6, 21):  "summer",
            (9, 23):  "autumn",   (12, 21): "winter",
        }
        m, d = dt.month, dt.day
        # Spring: Mar 20 - Jun 20
        if (m == 3 and d >= 20) or m in (4, 5) or (m == 6 and d < 21):
            season = "spring"
        elif (m == 6 and d >= 21) or m in (7, 8) or (m == 9 and d < 23):
            season = "summer"
        elif (m == 9 and d >= 23) or m in (10, 11) or (m == 12 and d < 21):
            season = "autumn"
        else:
            season = "winter"
    else:
        # Southern hemisphere — seasons are opposite
        m, d = dt.month, dt.day
        if (m == 3 and d >= 20) or m in (4, 5) or (m == 6 and d < 21):
            season = "autumn"
        elif (m == 6 and d >= 21) or m in (7, 8) or (m == 9 and d < 23):
            season = "winter"
        elif (m == 9 and d >= 23) or m in (10, 11) or (m == 12 and d < 21):
            season = "spring"
        else:
            season = "summer"

    rate = daylight_change_rate_minutes_per_day(dt, lat, lon, tz)
    trend = "lengthening" if rate > 0 else "shortening"

    return {
        "hemisphere": hemisphere,
        "season": season,
        "daylight_trend": trend,
        "daylight_minutes_per_day_rate": rate,
        "days_from_nearest_solstice": near_sol,
        "days_from_nearest_equinox": near_eq,
    }


# ── Composite for orchestrator ──────────────────────────────────

def photoperiod_state(
    dt: datetime, lat: float, lon: float, tz: str
) -> dict:
    """
    One-shot composite of photoperiod state for the orchestrator.

    Returns:
      - daylight_hours
      - night_hours
      - twilight_minutes: civil / nautical / astronomical durations
      - daylight_change_rate_minutes_per_day
      - seasonal_arc: the composite seasonal state
    """
    return {
        "daylight_hours":   daylight_hours(dt, lat, lon, tz),
        "night_hours":      night_hours(dt, lat, lon, tz),
        "twilight_minutes": twilight_durations(dt, lat, lon, tz),
        "daylight_change_rate_minutes_per_day":
            daylight_change_rate_minutes_per_day(dt, lat, lon, tz),
        "seasonal_arc":     seasonal_arc_position(dt, lat, lon, tz),
    }
