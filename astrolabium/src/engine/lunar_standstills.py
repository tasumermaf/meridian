"""
Major / minor lunar standstills.

The Moon's orbital plane is inclined ~5.14° to the ecliptic. The
intersection of the lunar orbital plane with the ecliptic — the
lunar nodes — precesses westward with a period of 18.613 years
(the Saros-related "regression of nodes").

This nodal precession causes the Moon's monthly extreme declination
(its highest and lowest points each month against the celestial
equator) to oscillate over the 18.6-year cycle:

  • MAJOR STANDSTILL: when the Moon's monthly maximum declination
    reaches its greatest value (~±28.7° from the celestial equator).
    The Moon rises and sets at its extreme northern and southern
    horizon points; the moonrise azimuth swings through its widest
    arc each lunar month.

  • MINOR STANDSTILL: when the Moon's monthly maximum declination
    is at its smallest value (~±18.3° from the equator). The
    moonrise arc is at its narrowest.

  • The cycle goes major → minor → major in 18.613 years.

Recent reference epochs:
  • Major standstill: 2024-2025 (the last major standstill peak;
    visible at Callanish, Chimney Rock, Stonehenge alignments)
  • Minor standstill: 2015 (and previous major was 2006)

This module exposes:

  • get_lunar_standstill_state(dt)  — current position in the cycle
  • next_major_standstill(dt)       — when next?
  • next_minor_standstill(dt)       — when next?
  • current_node_longitude(dt)      — sidereal longitude of ascending node

[MATHEMATICAL FACT] — nodal precession period; canonical astronomical value.
[SOURCE: classical archaeoastronomy] — the practical use of standstills
in megalithic alignments.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pytz


# ── Constants ────────────────────────────────────────────────────────

# Nodal precession period (regression of the lunar nodes)
NODAL_PERIOD_YEARS = 18.6128                # 18 years 220 days

# Extreme monthly declination at standstills (from canonical value
# of obliquity of ecliptic 23.4° ± lunar orbital inclination 5.14°)
MAJOR_STANDSTILL_MAX_DECL_DEG = 28.72        # 23.44 + 5.14 + ε
MINOR_STANDSTILL_MAX_DECL_DEG = 18.30        # 23.44 - 5.14

# Reference epoch: last well-documented MAJOR standstill peak
# 2025 March 22 ± a few days (the recent major standstill)
LAST_MAJOR_STANDSTILL = datetime(2025, 3, 22, 0, 0, tzinfo=pytz.utc)
# Subsequent minor standstill is half the period later
LAST_MINOR_STANDSTILL = datetime(2015, 10, 28, 0, 0, tzinfo=pytz.utc)


# ── Helpers ──────────────────────────────────────────────────────────

def _normalize_to_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


def _years_between(d1: datetime, d2: datetime) -> float:
    """Decimal years between two datetimes."""
    return (d2 - d1).total_seconds() / (365.25 * 86400)


# ── Public API ───────────────────────────────────────────────────────

def cycle_fraction(dt: datetime) -> float:
    """
    Return the position within the 18.6-year nodal cycle, 0.0 to 1.0.

    Phase 0.0 = exactly at a major standstill peak.
    Phase 0.5 = exactly at a minor standstill (midway between majors).
    Phase 1.0 = the next major standstill peak (= 0.0 of next cycle).
    """
    dt = _normalize_to_aware(dt)
    years_since_major = _years_between(LAST_MAJOR_STANDSTILL, dt)
    fraction = (years_since_major % NODAL_PERIOD_YEARS) / NODAL_PERIOD_YEARS
    return fraction


def closer_standstill(dt: datetime) -> str:
    """
    Return "major" or "minor" depending on which standstill we are
    closer to in the cycle.

    Major is at fraction 0.0 and 1.0 (start/end of cycle).
    Minor is at fraction 0.5 (middle).
    """
    f = cycle_fraction(dt)
    # Distance to nearest major (either end of [0,1])
    dist_to_major = min(f, 1.0 - f)
    # Distance to minor (always at 0.5)
    dist_to_minor = abs(f - 0.5)
    return "major" if dist_to_major < dist_to_minor else "minor"


def next_major_standstill(dt: datetime) -> datetime:
    """Project the next major-standstill peak after `dt`."""
    dt = _normalize_to_aware(dt)
    # Walk forward from last known major by full periods until we pass dt
    candidate = LAST_MAJOR_STANDSTILL
    while candidate <= dt:
        candidate = candidate + timedelta(days=NODAL_PERIOD_YEARS * 365.25)
    return candidate


def next_minor_standstill(dt: datetime) -> datetime:
    """Project the next minor-standstill peak after `dt`."""
    dt = _normalize_to_aware(dt)
    candidate = LAST_MINOR_STANDSTILL
    while candidate <= dt:
        candidate = candidate + timedelta(days=NODAL_PERIOD_YEARS * 365.25)
    return candidate


def current_node_longitude(dt: datetime) -> float:
    """
    Approximate the sidereal longitude (degrees) of the lunar ascending
    node, given that the node regresses westward through 360° every
    18.613 years.

    Reference: at the last major standstill (2025-03-22), the ascending
    node was at approximately 0° sidereal longitude (Aries), which
    aligned the lunar orbit's northernmost extreme with the spring
    equinox direction in the sidereal frame.

    This is a kinematic approximation suitable for the standstill
    cycle's interpretive use; for sub-degree node tracking use an
    ephemeris.
    """
    dt = _normalize_to_aware(dt)
    years_since_major = _years_between(LAST_MAJOR_STANDSTILL, dt)
    # Regression: node moves WESTWARD (subtract) by 360° / period per year
    degrees_regressed = (years_since_major / NODAL_PERIOD_YEARS) * 360.0
    return (0.0 - degrees_regressed) % 360.0


def get_lunar_standstill_state(dt: datetime) -> dict:
    """
    One-shot composite state for the orchestrator.

    Returns dict with:
      - cycle_fraction:      0.0 at major, 0.5 at minor, 1.0 at next major
      - closer:              "major" or "minor"
      - distance_to_closer_days: float
      - next_major_standstill: datetime (UTC)
      - next_minor_standstill: datetime (UTC)
      - node_longitude_deg:  sidereal longitude of ascending node
      - max_declination_at_closer_standstill_deg: ±28.72 (major) or ±18.30 (minor)
      - nodal_period_years:  18.6128 (the constant)
    """
    dt = _normalize_to_aware(dt)
    fraction = cycle_fraction(dt)
    closer = closer_standstill(dt)
    next_major = next_major_standstill(dt)
    next_minor = next_minor_standstill(dt)
    if closer == "major":
        closer_dt = min(next_major, dt + timedelta(days=NODAL_PERIOD_YEARS * 365.25 * 0.5))
        if (next_major - dt).total_seconds() > NODAL_PERIOD_YEARS * 365.25 * 86400 * 0.5:
            # We're closer to the PREVIOUS major; estimate as previous-major reference
            prev_major = LAST_MAJOR_STANDSTILL
            while prev_major + timedelta(days=NODAL_PERIOD_YEARS * 365.25) < dt:
                prev_major = prev_major + timedelta(days=NODAL_PERIOD_YEARS * 365.25)
            closer_dt = prev_major
        days_to_closer = abs((closer_dt - dt).total_seconds()) / 86400
        max_decl = MAJOR_STANDSTILL_MAX_DECL_DEG
    else:
        days_to_closer = abs((next_minor - dt).total_seconds()) / 86400
        # If next minor is more than half a cycle away, the previous minor is closer
        half_cycle_days = NODAL_PERIOD_YEARS * 365.25 * 0.5
        if days_to_closer > half_cycle_days:
            prev_minor = LAST_MINOR_STANDSTILL
            while prev_minor + timedelta(days=NODAL_PERIOD_YEARS * 365.25) < dt:
                prev_minor = prev_minor + timedelta(days=NODAL_PERIOD_YEARS * 365.25)
            days_to_closer = abs((prev_minor - dt).total_seconds()) / 86400
        max_decl = MINOR_STANDSTILL_MAX_DECL_DEG

    return {
        "cycle_fraction": fraction,
        "closer": closer,
        "distance_to_closer_days": days_to_closer,
        "next_major_standstill": next_major,
        "next_minor_standstill": next_minor,
        "node_longitude_deg": current_node_longitude(dt),
        "max_declination_at_closer_standstill_deg": max_decl,
        "nodal_period_years": NODAL_PERIOD_YEARS,
    }
