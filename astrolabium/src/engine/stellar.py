"""
Stellar layer for the Astrolabium.

Reads the position of the Sun, Moon, and visible planets against the
28 Chinese Lunar Mansions (二十八宿), organized into the four
celestial palaces (Azure Dragon East, Black Tortoise North, White
Tiger West, Vermillion Bird South).

The 28-mansion system divides the ecliptic into 28 non-uniform arcs
anchored to actual reference stars. The Sun and Moon (and the five
classical planets) each occupy exactly one mansion at any moment;
the engine simply locates them.

[SOURCE: Chinese classical astronomy — Han to Ming canon] for the
mansion divisions and palace assignments. [MATHEMATICAL FACT] for
the ephem-based position calculations.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Optional

import ephem
import pytz


# ── Data loading ─────────────────────────────────────────────────────

_MANSION_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "lunar_mansions.json"
_MANSION_DATA: Optional[dict] = None


def _load_mansion_data() -> dict:
    """Lazy-load the 28-mansion table. Cached after first call."""
    global _MANSION_DATA
    if _MANSION_DATA is None:
        with open(_MANSION_DATA_PATH, "r", encoding="utf-8") as f:
            _MANSION_DATA = json.load(f)
    return _MANSION_DATA


def _normalize_to_aware(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware; assume UTC if naive."""
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


# ── Mansion lookup ───────────────────────────────────────────────────

def get_mansion_by_longitude(ecliptic_longitude: float) -> dict:
    """
    Given an ecliptic longitude (degrees, 0–360, sidereal-ish), return
    the lunar mansion that contains it.

    The 28-mansion divisions wrap from mansion 13 (Bì 壁, "Wall") which
    crosses the 0°/360° boundary at the vernal point. Lookup handles
    the wrap correctly.

    Args:
        ecliptic_longitude: degrees, 0 ≤ lon < 360
    Returns:
        dict with all mansion metadata + 'palace' key resolved from the
        palace registry.
    """
    data = _load_mansion_data()
    lon = ecliptic_longitude % 360.0

    for mansion in data["mansions"]:
        start = mansion["ecliptic_longitude_start"]
        end = mansion["ecliptic_longitude_end"]

        if start < end:
            # Normal mansion (does not cross 0°)
            if start <= lon < end:
                return _decorate_mansion(mansion, data)
        else:
            # Wraps across 0° (e.g., Wall 壁: 343 → 14)
            if lon >= start or lon < end:
                return _decorate_mansion(mansion, data)

    # Should never happen if mansion divisions cover the full circle.
    raise ValueError(
        f"Ecliptic longitude {lon}° did not fall in any of the 28 mansions. "
        f"This indicates a gap in the mansion data — check lunar_mansions.json."
    )


def _decorate_mansion(mansion: dict, data: dict) -> dict:
    """Add palace info + a clean output shape to a raw mansion dict."""
    palace_key = mansion["palace"]
    palace = data["palaces"][palace_key]
    return {
        "index": mansion["index"],
        "chinese": mansion["chinese"],
        "pinyin": mansion["pinyin"],
        "english": mansion["english"],
        "palace_key": palace_key,
        "palace_chinese": palace["chinese"],
        "palace_pinyin": palace["pinyin"],
        "palace_english": palace["english"],
        "palace_direction": palace["direction"],
        "palace_season": palace["season"],
        "palace_element_wuxing": palace["element_wuxing"],
        "palace_position": mansion["palace_position"],
        "reference_star_name": mansion["reference_star_name"],
        "reference_star_bayer": mansion["reference_star_bayer"],
        "ecliptic_longitude_start": mansion["ecliptic_longitude_start"],
        "ecliptic_longitude_end": mansion["ecliptic_longitude_end"],
        "width_degrees": mansion["width_degrees"],
        "classical_animal": mansion["classical_animal"],
        "notes": mansion["notes"],
    }


# ── Sun, Moon, and planet positions ──────────────────────────────────

def _lahiri_ayanamsa(year: float) -> float:
    """
    Approximate the Lahiri (Chitrapaksha) ayanamsa in degrees.

    The ayanamsa is the angular offset between the tropical zero point
    (vernal equinox) and the sidereal zero point. The classical Chinese
    28-mansion boundaries are sidereal (anchored to actual stars), so
    tropical longitudes from ephem must be corrected by the ayanamsa
    before mansion lookup.

    The Lahiri ayanamsa at J2000.0 (2000 January 1.5 TT) is conventionally
    taken as 23.8519° (varies slightly by source between 23.85 and 23.86).
    It increases by approximately 50.29 arcseconds per Julian year due
    to general precession of the equinoxes.

    [MATHEMATICAL FACT] — astronomical constant. Linear approximation
    valid to < 1 arcminute over centuries of practical use.
    """
    ayanamsa_at_j2000 = 23.8519
    annual_increase_deg = 50.29 / 3600.0  # arcsec/year → degrees/year
    return ayanamsa_at_j2000 + annual_increase_deg * (year - 2000.0)


def _decimal_year(dt: datetime) -> float:
    """Convert a datetime to a decimal year (e.g., 2026.37)."""
    start_of_year = datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
    end_of_year = datetime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)
    year_fraction = (dt - start_of_year).total_seconds() / (end_of_year - start_of_year).total_seconds()
    return dt.year + year_fraction


def _ecliptic_longitude_of_body(body_class, dt: datetime, sidereal: bool = True) -> float:
    """
    Compute the ecliptic longitude (degrees) of an ephem body at a
    given datetime.

    Args:
        body_class: ephem body class (e.g., ephem.Sun)
        dt: datetime (timezone-aware; UTC assumed if naive)
        sidereal: if True (default), apply Lahiri ayanamsa correction
                  to produce SIDEREAL longitudes aligned with the
                  classical 28-mansion boundaries. If False, return
                  tropical longitudes (modern Western convention).

    Returns: longitude in degrees, [0, 360).
    """
    dt = _normalize_to_aware(dt)
    dt_utc = dt.astimezone(pytz.utc)
    obs_dt = ephem.Date(dt_utc.replace(tzinfo=None))
    body = body_class()
    body.compute(obs_dt)
    ecl = ephem.Ecliptic(body)
    lon_rad = float(ecl.lon)
    lon_deg = math.degrees(lon_rad) % 360.0
    if sidereal:
        ayanamsa = _lahiri_ayanamsa(_decimal_year(dt))
        lon_deg = (lon_deg - ayanamsa) % 360.0
    return lon_deg


def get_lunar_mansion(dt: datetime) -> dict:
    """
    Return the lunar mansion currently occupied by the Moon.

    Includes ecliptic longitude, mansion identity, palace, reference
    star, and the classical notes.
    """
    lon = _ecliptic_longitude_of_body(ephem.Moon, dt)
    mansion = get_mansion_by_longitude(lon)
    mansion["body"] = "Moon"
    mansion["ecliptic_longitude"] = lon
    return mansion


def get_solar_mansion(dt: datetime) -> dict:
    """
    Return the lunar mansion currently occupied by the Sun.

    The Sun spends approximately 13 days in each mansion (360° / 28 / 1°-per-day).
    """
    lon = _ecliptic_longitude_of_body(ephem.Sun, dt)
    mansion = get_mansion_by_longitude(lon)
    mansion["body"] = "Sun"
    mansion["ecliptic_longitude"] = lon
    return mansion


def get_planetary_mansions(dt: datetime) -> dict:
    """
    Return mansions for all five classical (visible) planets.

    Mercury, Venus, Mars, Jupiter, Saturn — the five wandering stars
    of the classical world. Each gets the same mansion-lookup treatment.
    """
    planets = {
        "Mercury": ephem.Mercury,
        "Venus":   ephem.Venus,
        "Mars":    ephem.Mars,
        "Jupiter": ephem.Jupiter,
        "Saturn":  ephem.Saturn,
    }
    result = {}
    for name, body_class in planets.items():
        lon = _ecliptic_longitude_of_body(body_class, dt)
        mansion = get_mansion_by_longitude(lon)
        mansion["body"] = name
        mansion["ecliptic_longitude"] = lon
        result[name] = mansion
    return result


# ── Convenience: full stellar state ──────────────────────────────────

def get_stellar_state(dt: datetime) -> dict:
    """
    Return the complete stellar layer state at a given moment.

    Composes Sun mansion + Moon mansion + planetary mansions + palace
    summary so the orchestrator can attach it whole.
    """
    sun = get_solar_mansion(dt)
    moon = get_lunar_mansion(dt)
    planets = get_planetary_mansions(dt)

    # Quick palace summary — which palace each body is in
    palace_summary = {
        "Sun":  sun["palace_english"],
        "Moon": moon["palace_english"],
    }
    for name, p in planets.items():
        palace_summary[name] = p["palace_english"]

    return {
        "sun_mansion":      sun,
        "lunar_mansion":    moon,
        "planet_mansions":  planets,
        "palace_summary":   palace_summary,
    }


# ── Module-level metadata for introspection ─────────────────────────

def get_mansion_count() -> int:
    return len(_load_mansion_data()["mansions"])


def get_palace_count() -> int:
    return len(_load_mansion_data()["palaces"])


def list_palaces() -> list:
    """Return list of palace dicts (with mansion_indices)."""
    return list(_load_mansion_data()["palaces"].values())


def list_mansions() -> list:
    """Return list of all 28 mansion dicts."""
    return _load_mansion_data()["mansions"]
