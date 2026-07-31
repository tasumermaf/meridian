"""
API tests — endpoint responses and structure.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

LA_PARAMS = {"lat": 34.0522, "lon": -118.2437, "tz": "America/Los_Angeles"}


class TestHealth:
    def test_health_200(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["laws_loaded"] == 8
        assert data["vessels_loaded"] == 8

    def test_version_is_3_3_0(self):
        """B-05 (2026-07-30): version bumped when /display became the
        Output Law surface."""
        response = client.get("/health")
        assert response.json()["version"] == "3.3.0"


class TestState:
    def test_state_returns_all_layers(self):
        response = client.get("/state", params={
            **LA_PARAMS,
            "dt": "2026-03-01T14:00:00",
        })
        assert response.status_code == 200
        data = response.json()
        assert "solar" in data
        assert "organ_clock" in data
        assert "derivative" in data
        assert "primeval" in data
        assert "solar_key" in data
        assert "divine_hour" in data
        assert "calendar" in data
        assert "compounds" in data

    def test_state_requires_location(self):
        response = client.get("/state")
        assert response.status_code == 422  # Missing required params

    def test_state_default_now(self):
        response = client.get("/state", params=LA_PARAMS)
        assert response.status_code == 200


class TestDisplay:
    """B-05 (2026-07-30): /display serves the Output Law shape."""

    DT = "2026-03-01T14:00:00"

    def _get(self, **extra):
        return client.get("/display", params={**LA_PARAMS, "dt": self.DT, **extra})

    def test_display_returns_output_law_shape(self):
        response = self._get()
        assert response.status_code == 200
        data = response.json()
        for key in ("readout", "typed_state", "story_gate", "display"):
            assert key in data, f"missing Output Law key: {key}"

    def test_readout_is_the_verbatim_block(self):
        data = self._get().json()
        text = data["readout"]
        assert text.startswith("=== ASTROLABIUM READOUT ===")
        assert text.rstrip().endswith("=== END READOUT ===")

    def test_typed_state_is_the_machine_core(self):
        data = self._get().json()
        typed = data["typed_state"]
        assert typed.startswith("=== VERIFIED STATE: ASTROLABIUM ===")
        assert "vessel.open" in typed

    def test_story_gate_shape(self):
        gate = self._get().json()["story_gate"]
        assert set(gate.keys()) == {"licensed", "subjects", "max_sentences", "rule"}
        assert isinstance(gate["licensed"], bool)
        assert isinstance(gate["subjects"], list)
        assert gate["max_sentences"] == 3

    def test_precision_defaults_to_coarse(self):
        """Coarse: clock times rounded and marked '~', no minute-exact claim."""
        text = self._get().json()["readout"]
        assert "~" in text
        assert "min remaining" not in text

    def test_precision_exact_opt_in(self):
        text = self._get(precision="exact").json()["readout"]
        assert "min remaining" in text

    def test_precision_invalid_rejected(self):
        response = self._get(precision="verbose")
        assert response.status_code == 422

    def test_display_block_is_prose_free(self):
        """C-05 (2026-07-30): the structured display block carries no
        dynamic prose sentences."""
        display = self._get().json()["display"]
        assert "description" not in display["astral"]
        assert "is open, carrying" not in str(display)


class TestProjection:
    def test_projection_returns_states(self):
        response = client.get("/projection", params={
            **LA_PARAMS,
            "start": "2026-03-01T00:00:00",
            "end": "2026-03-01T06:00:00",
            "interval": 120,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 4  # 0:00, 2:00, 4:00, 6:00
        assert len(data["states"]) == 4


class TestNextUnity:
    def test_next_unity_returns_result(self):
        response = client.get("/next-unity", params={
            **LA_PARAMS,
            "dt": "2026-03-01T00:00:00",
            "max_hours": 336,  # 2 weeks
        })
        assert response.status_code == 200
        data = response.json()
        assert "found" in data


class TestFrequency:
    def test_frequency_returns_compounds(self):
        response = client.get("/frequency", params={
            **LA_PARAMS,
            "start": "2026-03-01T00:00:00",
            "end": "2026-03-01T12:00:00",
            "interval": 60,
        })
        assert response.status_code == 200
        data = response.json()
        assert "compounds" in data
        assert "law_distribution" in data
        assert data["total_steps"] == 13  # 0:00 through 12:00 inclusive

    def test_frequency_requires_params(self):
        response = client.get("/frequency")
        assert response.status_code == 422


class TestWindows:
    def test_windows_returns_list(self):
        response = client.get("/windows", params={
            **LA_PARAMS,
            "start": "2026-03-01T00:00:00",
            "end": "2026-03-08T00:00:00",
            "compound": "two_body_unity",
            "interval": 30,
        })
        assert response.status_code == 200
        data = response.json()
        assert "windows" in data
        assert data["compound"] == "two_body_unity"
        assert isinstance(data["windows"], list)

    def test_windows_invalid_compound(self):
        response = client.get("/windows", params={
            **LA_PARAMS,
            "start": "2026-03-01T00:00:00",
            "end": "2026-03-02T00:00:00",
            "compound": "fake",
        })
        assert response.status_code == 422


class TestNextCompound:
    def test_next_compound_returns_result(self):
        response = client.get("/next-compound", params={
            **LA_PARAMS,
            "compound": "two_body_unity",
            "dt": "2026-03-01T00:00:00",
            "max_hours": 336,
        })
        assert response.status_code == 200
        data = response.json()
        assert "found" in data
        assert data["compound"] == "two_body_unity"

    def test_next_compound_default_now(self):
        response = client.get("/next-compound", params={
            **LA_PARAMS,
            "compound": "confluent_intersection",
        })
        assert response.status_code == 200
