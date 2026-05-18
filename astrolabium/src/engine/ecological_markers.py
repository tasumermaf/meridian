"""
Ecological markers — climate-norm derived signals for the
practitioner's location.

This module produces ecological-layer information WITHOUT live weather
data. It derives plausible ecological state from:

  • Latitude (Köppen climate-zone proxy)
  • Day of year (seasonal position)
  • Photoperiod (already computed by photoperiod.py)

What this gets right:
  • The general shape of the seasonal cycle at any latitude
  • The expected presence/absence of frost-risk season
  • The shape of the growing-degree-day curve
  • The shift in vegetation greenness across the year

What this gets WRONG:
  • Year-to-year weather variability (this is a CLIMATE-NORM model,
    not a weather model)
  • Microclimate effects (elevation, coastal proximity, urban heat)
  • Climate-change shifts (norms reflect mid-20th-century baselines)
  • Specific events (this won't tell you a heat wave is coming)

For most practitioner use cases (knowing whether it's "frost season
where you are right now") this is sufficient. For precision work
(planting decisions, frost-risk insurance, etc.), use a live weather
service. Sprint D may add Open-Meteo integration as an option.

[ANALYTICAL CONTRIBUTION] — the climate-norm approximations are simple
latitude-band heuristics, not validated meteorological models. They are
honest about being approximations.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Optional

import pytz

from . import photoperiod as _photoperiod


# ── Climate zones (latitude bands) ────────────────────────────────

# Simplified Köppen-derived bands by absolute latitude.
CLIMATE_ZONES = [
    # (abs_lat_min, abs_lat_max, name, key_traits)
    (0,    23.5, "tropical",
     ["no winter", "wet/dry seasons rather than temperature seasons", "no frost"]),
    (23.5, 35,   "subtropical",
     ["mild winter", "hot summer", "occasional frost in inland north"]),
    (35,   55,   "temperate",
     ["four seasons", "winter frost", "growing season May-Sep (NH)"]),
    (55,   66.5, "boreal",
     ["long winter", "short cool summer", "snow most of year"]),
    (66.5, 90,   "polar",
     ["polar day / polar night cycles", "no real growing season"]),
]


def climate_zone(lat: float) -> dict:
    """
    Return the climate zone for a given latitude.

    [ANALYTICAL CONTRIBUTION] — simplified latitude-band Köppen proxy.
    Real climate classification depends on precipitation, temperature
    means, continentality, etc.; this is the latitude-only first cut.
    """
    abs_lat = abs(lat)
    for lo, hi, name, traits in CLIMATE_ZONES:
        if lo <= abs_lat < hi:
            return {
                "zone": name,
                "abs_latitude": abs_lat,
                "hemisphere": "northern" if lat >= 0 else "southern",
                "key_traits": traits,
            }
    return {
        "zone": "polar",
        "abs_latitude": abs_lat,
        "hemisphere": "northern" if lat >= 0 else "southern",
        "key_traits": ["polar"],
    }


# ── Frost-risk season ──────────────────────────────────────────────

def frost_risk_state(dt: datetime, lat: float) -> dict:
    """
    Return whether the current date is in the climate-norm frost-risk
    season for the given latitude.

    Tropical (|lat| < 23.5°): never any frost season.
    Temperate (35-55°): frost from October to April in NH, April to
        October in SH (flipped).
    Subtropical (23.5-35°): brief frost season at the inland margin.
    Boreal+: extended frost season.

    Returns dict with:
      - in_frost_season: bool
      - season_label:    "frost-likely" / "frost-possible" / "frost-unlikely" / "no frost"
      - notes: brief explanation
    """
    zone = climate_zone(lat)
    abs_lat = zone["abs_latitude"]
    hemisphere = zone["hemisphere"]
    month = dt.month

    # Compute frost-season months for this zone
    if abs_lat < 23.5:
        return {
            "in_frost_season": False,
            "season_label": "no frost",
            "notes": "Tropical latitude — no climate-norm frost season.",
        }

    if abs_lat < 35:
        # Subtropical: brief inland frost season Dec-Feb (NH) / Jun-Aug (SH)
        if hemisphere == "northern":
            frost_months = {12, 1, 2}
        else:
            frost_months = {6, 7, 8}
        if month in frost_months:
            return {
                "in_frost_season": True,
                "season_label": "frost-possible",
                "notes": "Subtropical zone — occasional frost possible inland during winter.",
            }
        return {
            "in_frost_season": False,
            "season_label": "frost-unlikely",
            "notes": "Subtropical zone — frost rare outside deep winter.",
        }

    if abs_lat < 55:
        # Temperate: frost-likely Oct-Apr (NH) / Apr-Oct (SH)
        if hemisphere == "northern":
            frost_months = {10, 11, 12, 1, 2, 3, 4}
        else:
            frost_months = {4, 5, 6, 7, 8, 9, 10}
        if month in frost_months:
            return {
                "in_frost_season": True,
                "season_label": "frost-likely",
                "notes": "Temperate zone — frost a real risk during this period.",
            }
        return {
            "in_frost_season": False,
            "season_label": "frost-unlikely",
            "notes": "Temperate zone — frost-free summer.",
        }

    # Boreal / polar: frost likely most of the year
    if hemisphere == "northern":
        non_frost = {6, 7, 8}
    else:
        non_frost = {12, 1, 2}
    if month in non_frost:
        return {
            "in_frost_season": False,
            "season_label": "frost-possible",
            "notes": "Boreal/polar zone — even high summer can have frost.",
        }
    return {
        "in_frost_season": True,
        "season_label": "frost-likely",
        "notes": "Boreal/polar zone — frost season is the default state.",
    }


# ── Vegetation phenology stage ─────────────────────────────────────

def vegetation_stage(dt: datetime, lat: float) -> dict:
    """
    Return a climate-norm vegetation phenology stage:
      "dormant" / "awakening" / "leafing" / "flowering" /
      "fruiting" / "ripening" / "senescing"

    Mapping uses temperate latitude bands as the reference. Tropical
    latitudes mostly bypass this cycle (perpetual vegetation cycle
    keyed to wet/dry rather than thermal seasons).
    """
    zone = climate_zone(lat)
    abs_lat = zone["abs_latitude"]
    hemisphere = zone["hemisphere"]

    if abs_lat < 23.5:
        return {
            "stage": "continuous",
            "notes": ("Tropical vegetation cycles to wet/dry rather than "
                      "temperature; no temperate phenology stage applies."),
        }

    # For temperate / boreal: rough seasonal mapping
    month = dt.month
    # Use the "agricultural year" lens
    if hemisphere == "southern":
        # Flip the month mapping for southern hemisphere
        flipped = ((month + 6 - 1) % 12) + 1
        month = flipped

    stage_map = {
        12: "dormant",   1: "dormant",   2: "awakening",
        3: "awakening",  4: "leafing",   5: "flowering",
        6: "fruiting",   7: "fruiting",  8: "ripening",
        9: "senescing", 10: "senescing", 11: "dormant",
    }
    stage = stage_map[month]
    return {
        "stage": stage,
        "notes": ("Climate-norm temperate-zone phenology stage. "
                  "Actual local timing varies with elevation, microclimate, "
                  "and species composition."),
    }


# ── Growing-degree-day proxy ───────────────────────────────────────

def growing_degree_day_state(dt: datetime, lat: float) -> dict:
    """
    Return a climate-norm growing-degree-day (GDD) state.

    Growing degree days are a heat-accumulation metric used in
    agriculture to predict crop development. We return a coarse
    indicator (without computing actual GDD totals, which requires
    real temperature data).

    Returns:
      - accumulating: bool — are we in the GDD-accumulation season?
      - intensity:    "none" / "low" / "moderate" / "high"
      - notes:        explanation
    """
    zone = climate_zone(lat)
    abs_lat = zone["abs_latitude"]
    hemisphere = zone["hemisphere"]
    month = dt.month

    # Tropical: always accumulating
    if abs_lat < 23.5:
        return {
            "accumulating": True,
            "intensity": "high",
            "notes": "Tropical latitude — GDD accumulates year-round.",
        }

    # Temperate: peak May-Aug (NH) or Nov-Feb (SH)
    if hemisphere == "northern":
        peak = {5, 6, 7, 8}
        shoulder = {4, 9}
        off = {10, 11, 12, 1, 2, 3}
    else:
        peak = {11, 12, 1, 2}
        shoulder = {10, 3}
        off = {4, 5, 6, 7, 8, 9}

    if month in peak:
        intensity = "high" if abs_lat < 50 else "moderate"
        return {
            "accumulating": True,
            "intensity": intensity,
            "notes": f"Peak GDD accumulation in this {zone['zone']} zone.",
        }
    if month in shoulder:
        return {
            "accumulating": True,
            "intensity": "low",
            "notes": "Shoulder season — modest GDD accumulation.",
        }
    return {
        "accumulating": False,
        "intensity": "none",
        "notes": "Climate-norm cool season — minimal heat accumulation.",
    }


# ── Composite ──────────────────────────────────────────────────────

def ecological_markers_state(dt: datetime, lat: float, lon: float, tz: str) -> dict:
    """
    One-shot composite of ecological markers for the orchestrator.

    Returns dict with:
      - climate_zone:      latitude-band classification
      - frost_risk:        current frost-season status
      - vegetation_stage:  climate-norm phenology stage
      - growing_degree:    GDD accumulation state
      - photoperiod_summary: a brief from the photoperiod engine
    """
    # Pull photoperiod composite (already imported above)
    photo = _photoperiod.photoperiod_state(dt, lat, lon, tz)

    return {
        "climate_zone":      climate_zone(lat),
        "frost_risk":        frost_risk_state(dt, lat),
        "vegetation_stage":  vegetation_stage(dt, lat),
        "growing_degree":    growing_degree_day_state(dt, lat),
        "photoperiod_summary": {
            "daylight_hours": photo["daylight_hours"],
            "trend": photo["seasonal_arc"]["daylight_trend"],
            "rate_min_per_day": photo["daylight_change_rate_minutes_per_day"],
            "season": photo["seasonal_arc"]["season"],
        },
    }
