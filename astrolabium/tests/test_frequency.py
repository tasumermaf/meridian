"""
Tests for the frequency analysis engine (Phase 3).

Verifies compound scanning, window detection, and next-compound search.
"""

import pytest
from datetime import datetime

import pytz

from src.frequency import (
    scan_compounds,
    find_windows,
    next_compound,
    COMPOUND_TYPES,
    ALL_SEARCHABLE_TYPES,
)
from src.resonance import RESONANCE_BOOLEAN_TYPES

# Standard test location: Los Angeles
LAT = 34.0522
LON = -118.2437
TZ = "America/Los_Angeles"


# ── scan_compounds ────────────────────────────────────────────────────


class TestScanCompounds:
    """Tests for the compound frequency scanner."""

    def test_step_count_one_day(self):
        """24 hours at 60-min intervals = 25 steps (inclusive endpoints)."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 2, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)
        assert result["total_steps"] == 25
        assert result["interval_minutes"] == 60

    def test_distributions_sum_to_total(self):
        """All distributions must sum to total_steps."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 1, 12, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        total = result["total_steps"]
        assert sum(result["law_distribution"]["primeval"].values()) == total
        assert sum(result["law_distribution"]["derivative"].values()) == total
        assert sum(result["organ_distribution"].values()) == total
        assert sum(result["phase_distribution"].values()) == total
        assert sum(result["vessel_distribution"].values()) == total
        assert sum(result["divine_hour_distribution"].values()) == total

    def test_all_compound_types_present(self):
        """Result must contain all compound types."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 1, 6, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        for c in COMPOUND_TYPES:
            assert c in result["compounds"]
            assert "count" in result["compounds"][c]
            assert "pct" in result["compounds"][c]

    def test_compound_counts_non_negative(self):
        """All compound counts and percentages must be >= 0."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 1, 12, 0)
        result = scan_compounds(start, end, LAT, LON, TZ)

        for c in COMPOUND_TYPES:
            assert result["compounds"][c]["count"] >= 0
            assert 0 <= result["compounds"][c]["pct"] <= 100

    def test_raw_unity_gte_effective(self):
        """Raw Two-Body Unity count >= effective count (yin day may block)."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        unity = result["compounds"]["two_body_unity"]
        assert unity["raw_count"] >= unity["count"]

    def test_full_confluent_subset_of_unity(self):
        """Full Confluent = Unity + Intersection, so count <= Unity count."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 15, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        unity_count = result["compounds"]["two_body_unity"]["count"]
        full_conf = result["compounds"]["full_confluent"]["count"]
        full_coup = result["compounds"]["full_coupled"]["count"]

        assert full_conf <= unity_count
        assert full_coup <= unity_count

    def test_week_scan_finds_unity(self):
        """A 7-day scan should find at least one Two-Body Unity."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        assert result["compounds"]["two_body_unity"]["count"] > 0

    def test_primeval_only_six_cyclic_laws(self):
        """Primeval distribution contains only the 6 cyclic Laws."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        cyclic_laws = {
            "Kaos", "Sole Atom", "Time Matrix",
            "Synchronicity", "Geometric Essence", "Arrow of Complexity",
        }
        actual = set(result["law_distribution"]["primeval"].keys())
        assert actual.issubset(cyclic_laws)

    def test_derivative_has_all_eight_laws(self):
        """Over a month, derivative distribution should include all 8 Laws."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 31, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=120)

        all_laws = {
            "Kaos", "Sole Atom", "Time Matrix", "Synchronicity",
            "Geometric Essence", "Arrow of Complexity",
            "Fall of Events", "Divinity",
        }
        actual = set(result["law_distribution"]["derivative"].keys())
        assert actual == all_laws

    def test_duration_days_correct(self):
        """Duration in days matches input range."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=120)

        assert result["duration_days"] == 7.0

    def test_single_step(self):
        """When start == end, exactly one step is produced."""
        dt = datetime(2026, 3, 1, 12, 0)
        result = scan_compounds(dt, dt, LAT, LON, TZ)
        assert result["total_steps"] == 1


# ── find_windows ──────────────────────────────────────────────────────


class TestFindWindows:
    """Tests for compound window detection."""

    def test_invalid_compound_raises(self):
        """Invalid compound type raises ValueError."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 2, 0, 0)
        with pytest.raises(ValueError):
            find_windows(start, end, LAT, LON, TZ, "fake_compound")

    def test_windows_have_valid_structure(self):
        """Each window must have start, end, duration_minutes, and law."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        windows = find_windows(
            start, end, LAT, LON, TZ,
            "two_body_unity", interval_minutes=30,
        )
        for w in windows:
            assert "start" in w
            assert "end" in w
            assert "duration_minutes" in w
            assert "law" in w
            assert w["duration_minutes"] >= 0

    def test_windows_non_overlapping(self):
        """Windows must not overlap — each end < next start."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        windows = find_windows(
            start, end, LAT, LON, TZ,
            "confluent_intersection", interval_minutes=30,
        )
        for i in range(len(windows) - 1):
            assert windows[i]["end"] <= windows[i + 1]["start"]

    def test_window_law_is_cyclic_for_unity(self):
        """Two-Body Unity windows should report a cyclic Law."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        cyclic = {
            "Kaos", "Sole Atom", "Time Matrix",
            "Synchronicity", "Geometric Essence", "Arrow of Complexity",
        }
        windows = find_windows(
            start, end, LAT, LON, TZ,
            "two_body_unity", interval_minutes=30,
        )
        for w in windows:
            assert w["law"] in cyclic

    def test_empty_range_returns_empty(self):
        """When start == end, zero or one window at most."""
        dt = datetime(2026, 3, 1, 12, 0)
        windows = find_windows(dt, dt, LAT, LON, TZ, "two_body_unity")
        assert isinstance(windows, list)
        assert len(windows) <= 1


# ── next_compound ─────────────────────────────────────────────────────


class TestNextCompound:
    """Tests for the next-compound finder."""

    def test_invalid_compound_raises(self):
        """Invalid compound type raises ValueError."""
        start = datetime(2026, 3, 1, 0, 0)
        with pytest.raises(ValueError):
            next_compound(start, LAT, LON, TZ, "fake_compound")

    def test_finds_next_unity_within_week(self):
        """Should find a Two-Body Unity within a week."""
        start = datetime(2026, 3, 1, 0, 0)
        result = next_compound(start, LAT, LON, TZ, "two_body_unity", max_hours=168)

        assert result["found"] is True
        assert "timestamp" in result
        assert "law" in result
        assert "vessel" in result
        assert result["hours_from_start"] >= 0
        assert result["hours_from_start"] <= 168

    def test_finds_confluent_intersection(self):
        """Confluent intersection should occur within a week."""
        start = datetime(2026, 3, 1, 0, 0)
        result = next_compound(
            start, LAT, LON, TZ, "confluent_intersection", max_hours=168,
        )
        assert result["found"] is True

    def test_not_found_structure(self):
        """When not found, result has correct structure."""
        start = datetime(2026, 3, 1, 12, 0)
        result = next_compound(
            start, LAT, LON, TZ, "conditional_3_5", max_hours=1,
        )
        assert "found" in result
        assert "compound" in result
        if not result["found"]:
            assert "searched_hours" in result

    def test_all_compound_types_accepted(self):
        """Every COMPOUND_TYPE should be accepted without error."""
        start = datetime(2026, 3, 1, 12, 0)
        for c in COMPOUND_TYPES:
            result = next_compound(start, LAT, LON, TZ, c, max_hours=1)
            assert "found" in result
            assert result["compound"] == c


# ── Resonance integration tests ─────────────────────────────────────


class TestResonanceFrequency:
    """Tests for resonance tracking in frequency analysis."""

    def test_scan_includes_resonances(self):
        """scan_compounds returns a 'resonances' key."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 1, 6, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        assert "resonances" in result
        for r in RESONANCE_BOOLEAN_TYPES:
            assert r in result["resonances"]
            assert "count" in result["resonances"][r]
            assert "pct" in result["resonances"][r]

    def test_scan_includes_resonance_distributions(self):
        """scan_compounds returns resonance state-value distributions."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 1, 12, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        rd = result["resonance_distributions"]
        assert "alchemical_stage" in rd
        assert "month_group" in rd
        assert "iao_position" in rd
        assert "yang_count" in rd
        assert "divine_hour_law_unity" in rd

    def test_divine_hour_law_unity_tally_matches_unity_count(self):
        """
        divine_hour_law_unity distribution (AUDIT_2026-07-24 D-09, added
        2026-07-30) sums to the two_body_unity count: R_RHY_02 is non-null
        exactly when Two-Body Unity fires, so the hour-index tally is a
        partition of the unity steps.
        """
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 8, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=60)

        dist = result["resonance_distributions"]["divine_hour_law_unity"]
        unity_count = result["compounds"]["two_body_unity"]["count"]
        assert sum(dist.values()) == unity_count
        # The 7-day scan is known to find unity (test_week_scan_finds_unity),
        # so the distribution must be non-empty with valid hour indices.
        assert unity_count > 0
        for k, v in dist.items():
            assert v > 0
            assert int(k) in range(1, 9)  # Divine Hours 1-8

    def test_scan_includes_solar_key_activity(self):
        """
        Gold/silver key-active counters (AUDIT_2026-07-24 C-18, added
        2026-07-30) are present, well-formed, and consistent: a full-day
        scan at fine interval crosses both cusping windows.
        """
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 2, 0, 0)
        result = scan_compounds(start, end, LAT, LON, TZ, interval_minutes=15)

        ska = result["solar_key_activity"]
        for key_name in ("gold_key_active", "silver_key_active"):
            assert key_name in ska
            assert ska[key_name]["count"] >= 0
            assert 0 <= ska[key_name]["pct"] <= 100
            assert ska[key_name]["count"] <= result["total_steps"]

        # Symmetric ±civil-twilight windows around sunrise and sunset span
        # well over 15 minutes each — a 24h scan at 15-min steps must land
        # inside both.
        assert ska["gold_key_active"]["count"] > 0
        assert ska["silver_key_active"]["count"] > 0

    def test_resonance_counts_non_negative(self):
        """All resonance counts and percentages >= 0."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 1, 12, 0)
        result = scan_compounds(start, end, LAT, LON, TZ)

        for r in RESONANCE_BOOLEAN_TYPES:
            assert result["resonances"][r]["count"] >= 0
            assert 0 <= result["resonances"][r]["pct"] <= 100

    def test_find_windows_accepts_resonance_types(self):
        """find_windows should accept resonance type names."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 2, 0, 0)
        # waxing_wing_alignment should fire at some point in 24 hours
        windows = find_windows(
            start, end, LAT, LON, TZ,
            "waxing_wing_alignment", interval_minutes=30,
        )
        assert isinstance(windows, list)
        # Should find at least one window
        assert len(windows) > 0
        for w in windows:
            assert "start" in w
            assert "end" in w
            assert "duration_minutes" in w

    def test_find_windows_rejects_invalid(self):
        """Invalid resonance type raises ValueError."""
        start = datetime(2026, 3, 1, 0, 0)
        end = datetime(2026, 3, 2, 0, 0)
        with pytest.raises(ValueError):
            find_windows(start, end, LAT, LON, TZ, "fake_resonance")

    def test_next_compound_accepts_resonance_types(self):
        """next_compound should accept resonance type names."""
        start = datetime(2026, 3, 1, 0, 0)
        result = next_compound(
            start, LAT, LON, TZ, "waxing_wing_alignment", max_hours=48,
        )
        assert "found" in result
        assert result["compound"] == "waxing_wing_alignment"

    def test_all_searchable_types_accepted(self):
        """Every ALL_SEARCHABLE_TYPES should be accepted by next_compound."""
        start = datetime(2026, 3, 1, 12, 0)
        for c in ALL_SEARCHABLE_TYPES:
            result = next_compound(start, LAT, LON, TZ, c, max_hours=1)
            assert "found" in result
            assert result["compound"] == c
