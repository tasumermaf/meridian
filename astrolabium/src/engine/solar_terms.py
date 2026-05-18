"""
24 Solar Terms (二十四节气) engine.

Each of the 24 terms begins at the moment the Sun's *tropical* ecliptic
longitude reaches an exact multiple of 15°. Unlike the sidereal
28-mansion system, the solar terms are tropical — anchored to the
equinoxes and solstices, not to stars. They drift very slightly with
respect to the modern Gregorian calendar but are otherwise stable.

Terms are computed by:
  1. Getting the Sun's current tropical ecliptic longitude via ephem
  2. Dividing by 15° to get the current term index (and fraction into it)
  3. Searching forward for the next 15°-multiple transition to find the
     next term's exact start datetime

[SOURCE: Chinese classical astronomy] for the term definitions.
[MATHEMATICAL FACT] for the ephem-based computations.
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

_TERM_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "solar_terms.json"
_TERM_DATA: Optional[dict] = None


def _load_term_data() -> dict:
    global _TERM_DATA
    if _TERM_DATA is None:
        with open(_TERM_DATA_PATH, "r", encoding="utf-8") as f:
            _TERM_DATA = json.load(f)
    return _TERM_DATA


def _normalize_to_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


# ── Solar position ──────────────────────────────────────────────────

def _sun_tropical_longitude(dt: datetime) -> float:
    """Return the Sun's tropical ecliptic longitude in degrees [0, 360)."""
    dt = _normalize_to_aware(dt)
    dt_utc = dt.astimezone(pytz.utc)
    obs_dt = ephem.Date(dt_utc.replace(tzinfo=None))
    sun = ephem.Sun()
    sun.compute(obs_dt)
    ecl = ephem.Ecliptic(sun)
    return math.degrees(float(ecl.lon)) % 360.0


# ── Term lookup ─────────────────────────────────────────────────────

def _term_index_from_longitude(longitude: float) -> int:
    """
    Map a tropical ecliptic longitude to the corresponding solar term
    index (0–23).

    The terms are indexed by data order:
      0 = Lìchūn (Beginning of Spring) at 315°
      1 = Yǔshuǐ at 330°
      ...
      23 = Dàhán at 300°

    The mapping: (longitude - 315) // 15 mod 24 gives the term index.
    """
    # Term 0 starts at 315°. Compute how many 15° steps past 315° we are.
    steps_past_start = ((longitude - 315.0) % 360.0) / 15.0
    return int(steps_past_start) % 24


def get_current_solar_term(dt: datetime) -> dict:
    """
    Return the solar term that is currently active.

    Includes the term's metadata plus dynamic fields:
      - 'sun_longitude_deg': the Sun's current tropical longitude
      - 'degrees_into_term': how far past the term's start the Sun is
      - 'fraction_into_term': 0.0 (just started) to 1.0 (about to transition)
    """
    data = _load_term_data()
    lon = _sun_tropical_longitude(dt)
    idx = _term_index_from_longitude(lon)
    term = data["terms"][idx]
    start_lon = term["ecliptic_longitude_deg"]
    degrees_in = ((lon - start_lon) % 360.0)
    return {
        **term,
        "sun_longitude_deg": lon,
        "degrees_into_term": degrees_in,
        "fraction_into_term": degrees_in / 15.0,
    }


def get_next_solar_term(dt: datetime, max_search_days: int = 20) -> dict:
    """
    Find the next solar term transition after `dt`.

    Strategy: bracket the transition by checking when the Sun's
    longitude next crosses the next 15° multiple boundary. Bisection
    refines to second-level precision.

    Args:
        dt: starting datetime
        max_search_days: how far to look ahead (default 20 days, safely
            past any single-term duration which is ~15 days)

    Returns: dict with the upcoming term + 'transition_datetime' (UTC).
    """
    dt = _normalize_to_aware(dt)
    data = _load_term_data()
    current = get_current_solar_term(dt)
    # The next term boundary is at (current_start_lon + 15) mod 360
    target_lon = (current["ecliptic_longitude_deg"] + 15.0) % 360.0
    next_idx = (current["index"] + 1) % 24
    next_term = data["terms"][next_idx]

    # Linear search at 1-hour resolution, then bisect to refine
    lo = dt
    hi = dt + timedelta(days=max_search_days)
    # Coarse scan in 1-hour steps to find a sign change in (lon - target)
    step = timedelta(hours=1)
    cur = lo
    prev_lon = _sun_tropical_longitude(cur)
    found_lo = None
    found_hi = None
    while cur < hi:
        cur += step
        new_lon = _sun_tropical_longitude(cur)
        if _crossed_target(prev_lon, new_lon, target_lon):
            found_lo = cur - step
            found_hi = cur
            break
        prev_lon = new_lon
    if found_lo is None:
        raise RuntimeError(
            f"Could not find next solar term transition within "
            f"{max_search_days} days of {dt}. Check engine."
        )
    # Bisection refinement to ~1-second precision
    for _ in range(40):
        mid = found_lo + (found_hi - found_lo) / 2
        mid_lon = _sun_tropical_longitude(mid)
        if _crossed_target(prev_lon, mid_lon, target_lon):
            found_hi = mid
        else:
            found_lo = mid
            prev_lon = mid_lon
        if (found_hi - found_lo).total_seconds() < 1:
            break
    transition = found_hi
    return {
        **next_term,
        "transition_datetime": transition.astimezone(pytz.utc),
    }


def _crossed_target(prev_lon: float, cur_lon: float, target: float) -> bool:
    """
    Did the Sun's longitude just cross the target multiple-of-15° value
    going forward?

    Handles the 0°/360° wrap.
    """
    # Normalize: how far each is past the target, going forward (mod 360)
    prev_offset = (prev_lon - target) % 360.0
    cur_offset = (cur_lon - target) % 360.0
    # If prev was just before target (offset near 360) and cur is just after
    # (offset small), we crossed.
    return prev_offset > 350.0 and cur_offset < 10.0


# ── Convenience: full solar-term state ──────────────────────────────

def get_solar_term_state(dt: datetime) -> dict:
    """
    Return the complete solar-term state: current term + next transition.

    Designed for direct inclusion in the orchestrator's complete state.
    """
    current = get_current_solar_term(dt)
    next_t = get_next_solar_term(dt)
    return {
        "current": current,
        "next": next_t,
    }


# ── Module introspection ────────────────────────────────────────────

def get_term_count() -> int:
    return len(_load_term_data()["terms"])


def list_terms() -> list:
    return _load_term_data()["terms"]
