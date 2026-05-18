"""
Tests for the ecological_markers engine.

Validates:
  • climate zone classification by latitude
  • frost risk by zone × season
  • vegetation stage flipping correctly for southern hemisphere
  • GDD accumulation state by latitude and month
  • composite state structure
"""

from datetime import datetime
import pytest
import pytz

from src.engine import ecological_markers as em


DAMANHUR_LAT = 45.42
SYDNEY_LAT   = -33.87
EQUATOR_LAT  = 0.0
REYKJAVIK_LAT = 64.15


# ── Climate zone ────────────────────────────────────────────────

def test_equator_is_tropical():
    z = em.climate_zone(EQUATOR_LAT)
    assert z["zone"] == "tropical"


def test_damanhur_is_temperate():
    z = em.climate_zone(DAMANHUR_LAT)
    assert z["zone"] == "temperate"


def test_sydney_is_subtropical_southern():
    """Sydney at -33.87° falls in the 23.5-35° subtropical band."""
    z = em.climate_zone(SYDNEY_LAT)
    assert z["zone"] == "subtropical"
    assert z["hemisphere"] == "southern"


def test_reykjavik_is_boreal():
    z = em.climate_zone(REYKJAVIK_LAT)
    assert z["zone"] == "boreal"


def test_polar_zone():
    z = em.climate_zone(75.0)
    assert z["zone"] == "polar"


# ── Frost risk ──────────────────────────────────────────────────

def test_tropics_never_have_frost_season():
    for month in range(1, 13):
        dt = pytz.utc.localize(datetime(2026, month, 15))
        risk = em.frost_risk_state(dt, EQUATOR_LAT)
        assert risk["in_frost_season"] is False
        assert risk["season_label"] == "no frost"


def test_damanhur_january_is_frost_likely():
    dt = pytz.utc.localize(datetime(2026, 1, 15))
    risk = em.frost_risk_state(dt, DAMANHUR_LAT)
    assert risk["in_frost_season"] is True
    assert risk["season_label"] == "frost-likely"


def test_damanhur_july_is_frost_unlikely():
    dt = pytz.utc.localize(datetime(2026, 7, 15))
    risk = em.frost_risk_state(dt, DAMANHUR_LAT)
    assert risk["in_frost_season"] is False


def test_sydney_july_is_frost_likely():
    """Southern hemisphere: July = winter."""
    dt = pytz.utc.localize(datetime(2026, 7, 15))
    risk = em.frost_risk_state(dt, SYDNEY_LAT)
    assert risk["in_frost_season"] is True


def test_sydney_january_is_frost_unlikely():
    """Southern hemisphere: January = summer."""
    dt = pytz.utc.localize(datetime(2026, 1, 15))
    risk = em.frost_risk_state(dt, SYDNEY_LAT)
    assert risk["in_frost_season"] is False


# ── Vegetation stage ────────────────────────────────────────────

def test_tropical_vegetation_is_continuous():
    dt = pytz.utc.localize(datetime(2026, 5, 18))
    stage = em.vegetation_stage(dt, EQUATOR_LAT)
    assert stage["stage"] == "continuous"


def test_damanhur_may_is_flowering():
    """May at 45°N: flowering season in the temperate cycle."""
    dt = pytz.utc.localize(datetime(2026, 5, 18))
    stage = em.vegetation_stage(dt, DAMANHUR_LAT)
    assert stage["stage"] == "flowering"


def test_damanhur_january_is_dormant():
    dt = pytz.utc.localize(datetime(2026, 1, 15))
    stage = em.vegetation_stage(dt, DAMANHUR_LAT)
    assert stage["stage"] == "dormant"


def test_sydney_may_is_dormant():
    """Southern May = late autumn = our November = entering dormancy."""
    dt = pytz.utc.localize(datetime(2026, 5, 18))
    stage = em.vegetation_stage(dt, SYDNEY_LAT)
    assert stage["stage"] == "dormant"


# ── Growing degree days ─────────────────────────────────────────

def test_tropical_gdd_always_accumulating():
    dt = pytz.utc.localize(datetime(2026, 1, 15))
    gdd = em.growing_degree_day_state(dt, EQUATOR_LAT)
    assert gdd["accumulating"] is True
    assert gdd["intensity"] == "high"


def test_damanhur_july_peak_gdd():
    dt = pytz.utc.localize(datetime(2026, 7, 15))
    gdd = em.growing_degree_day_state(dt, DAMANHUR_LAT)
    assert gdd["accumulating"] is True
    assert gdd["intensity"] == "high"


def test_damanhur_january_no_gdd():
    dt = pytz.utc.localize(datetime(2026, 1, 15))
    gdd = em.growing_degree_day_state(dt, DAMANHUR_LAT)
    assert gdd["accumulating"] is False
    assert gdd["intensity"] == "none"


def test_sydney_january_peak_gdd():
    """Southern hemisphere January = summer = peak GDD."""
    dt = pytz.utc.localize(datetime(2026, 1, 15))
    gdd = em.growing_degree_day_state(dt, SYDNEY_LAT)
    assert gdd["accumulating"] is True
    assert gdd["intensity"] == "high"


# ── Composite state ────────────────────────────────────────────

def test_ecological_state_has_all_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = em.ecological_markers_state(
        dt, lat=DAMANHUR_LAT, lon=7.78, tz="Europe/Rome"
    )
    for key in ("climate_zone", "frost_risk", "vegetation_stage",
                "growing_degree", "photoperiod_summary"):
        assert key in state


def test_ecological_state_internally_consistent():
    """Damanhur May 18 should report temperate / flowering / GDD high."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = em.ecological_markers_state(
        dt, lat=DAMANHUR_LAT, lon=7.78, tz="Europe/Rome"
    )
    assert state["climate_zone"]["zone"] == "temperate"
    assert state["vegetation_stage"]["stage"] == "flowering"
    assert state["growing_degree"]["accumulating"] is True
    assert state["frost_risk"]["in_frost_season"] is False
