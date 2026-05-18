"""
Orchestrator integration tests for the Sprint C ecological layer.

Verifies state['photoperiod'] and state['ecological_markers'] are
returned by calculate_complete_state(), with the right structure.
Backward compatibility: all prior keys (Sprints A, B, original)
still present.
"""

from datetime import datetime
import pytz

from src.astrolabium import calculate_complete_state


DT = pytz.timezone("Europe/Rome").localize(datetime(2026, 5, 18, 12, 0))
DAMANHUR = {"lat": 45.42, "lon": 7.78, "tz": "Europe/Rome"}


def test_complete_state_has_photoperiod_key():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "photoperiod" in state
    photo = state["photoperiod"]
    for k in ("daylight_hours", "night_hours", "twilight_minutes",
              "daylight_change_rate_minutes_per_day", "seasonal_arc"):
        assert k in photo


def test_complete_state_has_ecological_markers_key():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "ecological_markers" in state
    em = state["ecological_markers"]
    for k in ("climate_zone", "frost_risk", "vegetation_stage",
              "growing_degree", "photoperiod_summary"):
        assert k in em


def test_photoperiod_at_damanhur_in_may_is_long_day():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert state["photoperiod"]["daylight_hours"] > 14.0


def test_ecological_zone_damanhur_is_temperate():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert state["ecological_markers"]["climate_zone"]["zone"] == "temperate"


def test_ecological_season_damanhur_may_is_spring():
    state = calculate_complete_state(DT, **DAMANHUR)
    arc = state["photoperiod"]["seasonal_arc"]
    assert arc["season"] == "spring"
    assert arc["daylight_trend"] == "lengthening"


# ── Backward compatibility ────────────────────────────────────────

def test_sprint_a_b_keys_still_present():
    state = calculate_complete_state(DT, **DAMANHUR)
    required = {
        # Sprint A
        "stellar", "solar_term", "festival_proximity", "tibetan_month",
        # Sprint B
        "precession", "heliacal", "lunar_standstills", "vedic_time",
    }
    missing = required - set(state.keys())
    assert not missing, f"Missing earlier-sprint keys: {missing}"


def test_original_keys_still_present():
    state = calculate_complete_state(DT, **DAMANHUR)
    required = {
        "timestamp", "location", "solar", "organ_clock",
        "derivative", "primeval", "solar_key", "divine_hour",
        "calendar", "stem_branch", "compounds", "resonances",
    }
    missing = required - set(state.keys())
    assert not missing, f"Missing original keys: {missing}"
