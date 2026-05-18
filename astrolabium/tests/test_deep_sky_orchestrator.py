"""
Orchestrator integration tests for the Sprint B deep-sky layer.

Verifies that calculate_complete_state() now returns the four new
top-level keys (precession, heliacal, lunar_standstills, vedic_time)
and that they contain the expected sub-structures. Backward
compatibility: all old keys (including Sprint A's stellar layer)
still present.
"""

from datetime import datetime
import pytz

from src.astrolabium import calculate_complete_state


DT = pytz.timezone("Europe/Rome").localize(datetime(2026, 5, 18, 12, 0))
DAMANHUR = {"lat": 45.42, "lon": 7.78, "tz": "Europe/Rome"}


def test_complete_state_has_precession_key():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "precession" in state
    assert "current_age" in state["precession"]
    assert state["precession"]["current_age"]["age_english"] == "Pisces"


def test_complete_state_has_heliacal_key():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "heliacal" in state
    assert "upcoming" in state["heliacal"]
    assert isinstance(state["heliacal"]["upcoming"], list)


def test_complete_state_has_lunar_standstills_key():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "lunar_standstills" in state
    assert "cycle_fraction" in state["lunar_standstills"]
    assert "closer" in state["lunar_standstills"]


def test_complete_state_has_vedic_time_key():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "vedic_time" in state
    assert state["vedic_time"]["current_yuga"]["yuga"] == "Kali Yuga"


# ── Backward compatibility: Sprint A keys still present ─────────────

def test_all_sprint_a_keys_still_present():
    state = calculate_complete_state(DT, **DAMANHUR)
    sprint_a_keys = {
        "stellar", "solar_term", "festival_proximity", "tibetan_month",
    }
    for key in sprint_a_keys:
        assert key in state, f"Sprint A key {key} missing — backward compat broken"


def test_all_original_keys_still_present():
    """Every key from the pre-Sprint-A baseline must still be there."""
    state = calculate_complete_state(DT, **DAMANHUR)
    original_keys = {
        "timestamp", "location", "solar", "organ_clock",
        "derivative", "primeval", "solar_key", "divine_hour",
        "calendar", "stem_branch", "compounds", "resonances",
    }
    missing = original_keys - set(state.keys())
    assert not missing, f"Original keys missing: {missing}"


def test_sirius_next_rising_in_heliacal_state():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "sirius_next_heliacal_rising" in state["heliacal"]


def test_precession_summary_contains_pole_star():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "closest_pole_star" in state["precession"]
    assert "Polaris" in state["precession"]["closest_pole_star"]["name"]


def test_vedic_time_contains_kalpa_info():
    state = calculate_complete_state(DT, **DAMANHUR)
    assert "kalpa" in state["vedic_time"]
    assert state["vedic_time"]["kalpa"]["manvantara_number"] == 7
