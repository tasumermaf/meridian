"""
Orchestrator integration tests for the new stellar layer.

Verifies that calculate_complete_state() returns the new top-level
keys (stellar, solar_term, festival_proximity, tibetan_month) and
that they contain the expected sub-structures.

Backward compatibility: also verifies that all the OLD top-level keys
still exist and are unchanged.
"""

from datetime import datetime
import pytz

from src.astrolabium import calculate_complete_state


SAGA_DAWA_DT = pytz.timezone("Europe/Rome").localize(datetime(2026, 5, 18, 12, 0))
DAMANHUR = {"lat": 45.42, "lon": 7.78, "tz": "Europe/Rome"}


def test_complete_state_has_stellar_key():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    assert "stellar" in state
    assert "sun_mansion" in state["stellar"]
    assert "lunar_mansion" in state["stellar"]
    assert "planet_mansions" in state["stellar"]
    assert "palace_summary" in state["stellar"]


def test_complete_state_has_solar_term_key():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    assert "solar_term" in state
    assert "current" in state["solar_term"]
    assert "next" in state["solar_term"]
    assert state["solar_term"]["current"]["pinyin"]  # has a pinyin name


def test_complete_state_has_festival_proximity():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    assert "festival_proximity" in state
    assert isinstance(state["festival_proximity"], list)
    # During Saga Dawa, the list should be non-empty
    assert len(state["festival_proximity"]) > 0


def test_complete_state_has_tibetan_month():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    assert "tibetan_month" in state
    assert state["tibetan_month"]["month_number"] == 4
    assert state["tibetan_month"]["is_saga_dawa"] is True


def test_saga_dawa_appears_active_in_proximity():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    saga = next(
        (f for f in state["festival_proximity"] if f["id"] == "saga_dawa"),
        None,
    )
    assert saga is not None
    assert saga["status"] == "active"


# ── Backward compatibility: the existing keys are still present ────

def test_existing_keys_still_present():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    expected = {
        "timestamp", "location", "solar", "organ_clock",
        "derivative", "primeval", "solar_key", "divine_hour",
        "calendar", "stem_branch", "compounds", "resonances",
    }
    missing = expected - set(state.keys())
    assert not missing, f"Backward compatibility broken: missing keys {missing}"


def test_existing_organ_clock_unchanged():
    """Organ clock should still report the same shape it did before the stellar layer."""
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    oc = state["organ_clock"]
    assert "organ" in oc
    assert "branch_chinese" in oc
    assert "branch_name" in oc
    assert "element" in oc


def test_divine_hour_unchanged():
    state = calculate_complete_state(SAGA_DAWA_DT, **DAMANHUR)
    dh = state["divine_hour"]
    assert "roman" in dh
    assert "wing" in dh
    assert "duration_minutes" in dh
