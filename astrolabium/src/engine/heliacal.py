"""
Heliacal risings engine.

A star's HELIACAL RISING is its first dawn appearance after a period
of being too close to the sun to be visible. For most named stars,
the heliacal rising occurs once per year and was historically a
critical calendar marker:

  • Sirius rising heralded the Egyptian agricultural year (~mid-July
    at Egyptian latitudes), predicting the Nile flood.
  • The Pleiades rising marked the start of the sailing/agricultural
    season across the Mediterranean.
  • Spica's rising marked the spring planting season in temperate
    northern Europe.

The heliacal rising of a star depends on:
  1. The star's position (RA, Dec) — fixed against the stars
  2. The Sun's position (changes daily)
  3. The observer's latitude (changes the geometry of the local
     horizon vs the celestial equator)

A star is "heliacally rising" on the first morning when:
  • The star is above the eastern horizon at the start of dawn
  • The Sun is still below the horizon by a sufficient margin
    (conventionally 10-15° below for the bright stars — the
    "arcus visionis", which varies with the star's magnitude)

This engine provides:
  • next_heliacal_rising(star_id, lat, lon, tz, dt) — when next?
  • is_in_heliacal_invisibility(star_id, ...)       — currently invisible at dawn?
  • upcoming_heliacal_risings(lat, lon, tz, dt, window_days)
                                                    — what's coming up

The exact definition of "heliacal rising" varies — different cultures
used different arcus visionis values. We use 13° as a working default
(an average appropriate for naked-eye observation of bright stars).
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import ephem
import pytz


# ── Data loading ─────────────────────────────────────────────────────

_STAR_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "named_stars.json"
_STAR_DATA: Optional[dict] = None


def _load_star_data() -> dict:
    global _STAR_DATA
    if _STAR_DATA is None:
        with open(_STAR_DATA_PATH, "r", encoding="utf-8") as f:
            _STAR_DATA = json.load(f)
    return _STAR_DATA


def _normalize_to_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


def list_stars() -> list:
    return _load_star_data()["stars"]


def get_star_count() -> int:
    return len(_load_star_data()["stars"])


def get_star_by_id(star_id: str) -> Optional[dict]:
    for s in _load_star_data()["stars"]:
        if s["id"] == star_id:
            return s
    return None


# ── Astronomical calculations ────────────────────────────────────────

# Default "arcus visionis" — how far below the horizon the Sun must be
# for a bright star at the horizon to be visible. Classical value is
# 10-15° for first-magnitude stars; we use 13° as a working default.
DEFAULT_ARCUS_VISIONIS_DEG = 13.0


def _make_observer(lat: float, lon: float, dt: datetime) -> ephem.Observer:
    """Construct an ephem.Observer for the given location and time."""
    dt = _normalize_to_aware(dt)
    dt_utc = dt.astimezone(pytz.utc)
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.date = ephem.Date(dt_utc.replace(tzinfo=None))
    obs.pressure = 0  # no atmospheric refraction modeling — keep simple
    return obs


def _build_star(star: dict) -> ephem.FixedBody:
    """Construct an ephem.FixedBody from a star catalog entry."""
    body = ephem.FixedBody()
    body._ra = math.radians(star["ra_deg"])
    body._dec = math.radians(star["dec_deg"])
    body._epoch = ephem.J2000
    return body


def _is_heliacally_visible(
    star: dict,
    lat: float,
    lon: float,
    dt: datetime,
    arcus_visionis_deg: float = DEFAULT_ARCUS_VISIONIS_DEG,
) -> bool:
    """
    Is this star visible at HELIACAL RISING right now (i.e., barely above
    the eastern horizon at the moment the Sun is just enough below the
    horizon to permit naked-eye detection)?

    Simplified check: at the start of nautical/civil twilight on this
    date, is the star above the eastern horizon?
    """
    obs = _make_observer(lat, lon, dt)
    # Find sunrise time (Sun crosses the horizon going up)
    sun = ephem.Sun()
    try:
        sunrise_t = obs.next_rising(sun)
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        return False
    # Set observation time to (sunrise - arcus_visionis / 15) hours
    # (Sun moves about 15° per hour, so an arcus of 13° = ~52 minutes)
    minutes_before_sunrise = arcus_visionis_deg * 4  # 15°/hr → 4 min/°
    obs_time = sunrise_t.datetime() - timedelta(minutes=minutes_before_sunrise)
    obs.date = ephem.Date(obs_time)
    # Compute star position
    body = _build_star(star)
    body.compute(obs)
    # Star is visible at heliacal rising if:
    #   - altitude > 0 (above horizon)
    #   - azimuth is roughly east (between 60° and 120°)
    alt_deg = math.degrees(float(body.alt))
    az_deg = math.degrees(float(body.az))
    if alt_deg < 0:
        return False
    if not (45 < az_deg < 135):  # generously eastern
        return False
    return True


def next_heliacal_rising(
    star_id: str,
    lat: float,
    lon: float,
    tz: str,
    dt: datetime,
    max_search_days: int = 400,
    arcus_visionis_deg: float = DEFAULT_ARCUS_VISIONIS_DEG,
) -> Optional[dict]:
    """
    Find the next heliacal rising of the named star at the given location.

    Strategy: scan forward day by day, checking each morning whether the
    star is heliacally visible. The first morning where it transitions
    from invisible → visible is the heliacal rising.

    Returns dict with star metadata + 'heliacal_rising_datetime' (UTC), or
    None if no rising found in the search window (e.g., circumpolar star).
    """
    star = get_star_by_id(star_id)
    if star is None:
        return None
    dt = _normalize_to_aware(dt)

    # Start: is the star currently visible? If yes, we need to find the
    # NEXT transition invisible → visible, so first find the next time
    # it becomes invisible, then look for next visible.
    cur = dt
    currently_visible = _is_heliacally_visible(
        star, lat, lon, cur, arcus_visionis_deg
    )
    if currently_visible:
        # Walk forward until invisible
        for _ in range(max_search_days):
            cur = cur + timedelta(days=1)
            if not _is_heliacally_visible(star, lat, lon, cur, arcus_visionis_deg):
                break

    # Now find the next day where the star becomes visible
    for day_offset in range(max_search_days):
        check_dt = cur + timedelta(days=day_offset)
        prev_dt = check_dt - timedelta(days=1)
        visible = _is_heliacally_visible(star, lat, lon, check_dt, arcus_visionis_deg)
        prev_visible = _is_heliacally_visible(star, lat, lon, prev_dt, arcus_visionis_deg)
        if visible and not prev_visible:
            return {
                **star,
                "heliacal_rising_datetime": check_dt.astimezone(pytz.utc),
                "observation_location": {"lat": lat, "lon": lon, "tz": tz},
                "arcus_visionis_deg_used": arcus_visionis_deg,
            }
    return None


def upcoming_heliacal_risings(
    lat: float,
    lon: float,
    tz: str,
    dt: datetime,
    window_days: int = 60,
    max_stars: int = 10,
) -> list:
    """
    Return upcoming heliacal risings within `window_days` for all
    catalog stars, sorted by nearest first.

    Useful for the orchestrator's stellar-state output: "what stars
    are about to herald their season?"
    """
    dt = _normalize_to_aware(dt)
    results = []
    end_dt = dt + timedelta(days=window_days)
    for star in list_stars():
        # Skip circumpolar / never-rising stars (Polaris, Alkaid at high lat)
        if star["id"] in ("polaris", "alkaid"):
            continue
        rise = next_heliacal_rising(
            star["id"], lat, lon, tz, dt, max_search_days=window_days
        )
        if rise is None:
            continue
        rising_dt = rise["heliacal_rising_datetime"]
        if dt <= rising_dt <= end_dt:
            days_until = (rising_dt - dt).total_seconds() / 86400
            results.append({**rise, "days_until": days_until})
    results.sort(key=lambda r: r["days_until"])
    return results[:max_stars]


def heliacal_state(
    lat: float,
    lon: float,
    tz: str,
    dt: datetime,
    window_days: int = 60,
) -> dict:
    """
    One-shot summary of heliacal state for the orchestrator.

    Returns dict with:
      - upcoming: list of upcoming heliacal risings within window_days
      - sirius: dedicated entry for Sirius (the canonical case)
    """
    upcoming = upcoming_heliacal_risings(lat, lon, tz, dt, window_days)
    sirius_rise = next_heliacal_rising("sirius", lat, lon, tz, dt, max_search_days=400)
    return {
        "upcoming": upcoming,
        "sirius_next_heliacal_rising": (
            sirius_rise["heliacal_rising_datetime"] if sirius_rise else None
        ),
        "window_days": window_days,
    }
