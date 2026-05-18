"""
Tests for the cross-tradition sacred festival registry engine.

Validates:
  • data integrity (festival count, anchor types valid)
  • per-anchor-type resolution correctness
  • Saga Dawa 2026 resolves to May/June window
  • festival proximity returns festivals in the right order
"""

from datetime import datetime, timedelta
import pytest
import pytz

from src.engine import festivals


# ── Data integrity ──────────────────────────────────────────────────

def test_festival_count_positive():
    """At least 30 festivals registered."""
    count = festivals.get_festival_count()
    assert count >= 30, f"Only {count} festivals registered; expected ≥30"


def test_each_festival_has_required_fields():
    for f in festivals.list_festivals():
        assert "id" in f
        assert "name_english" in f
        assert "tradition" in f
        assert "anchor_type" in f
        assert "anchor_data" in f


def test_all_festival_ids_unique():
    ids = [f["id"] for f in festivals.list_festivals()]
    assert len(ids) == len(set(ids)), "Duplicate festival IDs detected"


# ── Solar date resolution ─────────────────────────────────────────

def test_resolve_divine_marriage_2026():
    """Divine Marriage: May 24, fixed solar date."""
    result = festivals.resolve_festival("divine_marriage_damanhur", 2026)
    assert result is not None
    assert result["start_datetime"].month == 5
    assert result["start_datetime"].day == 24


def test_resolve_day_of_dead_2026():
    """Day of the Dead: November 2."""
    result = festivals.resolve_festival("day_of_dead", 2026)
    assert result is not None
    assert result["start_datetime"].month == 11
    assert result["start_datetime"].day == 2


# ── Solar term resolution ─────────────────────────────────────────

def test_resolve_spring_equinox_damanhur_2026():
    """Damanhurian Spring Equinox Great Rite is anchored to Chūnfēn (~Mar 20)."""
    result = festivals.resolve_festival("spring_equinox_damanhur", 2026)
    assert result is not None
    assert result["start_datetime"].month == 3
    assert 19 <= result["start_datetime"].day <= 21


def test_resolve_qingming_2026():
    """Qingming festival: Qīngmíng solar term (~Apr 4-6)."""
    result = festivals.resolve_festival("qingming", 2026)
    assert result is not None
    assert result["start_datetime"].month == 4
    assert 4 <= result["start_datetime"].day <= 6


def test_resolve_winter_solstice_damanhur_2026():
    result = festivals.resolve_festival("winter_solstice_damanhur", 2026)
    assert result is not None
    assert result["start_datetime"].month == 12
    assert 21 <= result["start_datetime"].day <= 22


# ── Tibetan lunar month range — the Saga Dawa test ────────────────

def test_saga_dawa_2026_falls_in_may_june():
    """
    Saga Dawa 2026 should resolve to a Tibetan-month-4 window in May-June.
    The Mama Food Forest text gives May 17 - June 14. Allow ~2 days
    tolerance for Phugpa variant differences.
    """
    result = festivals.resolve_festival("saga_dawa", 2026)
    assert result is not None
    start = result["start_datetime"]
    end = result["end_datetime"]
    # Should start in May
    assert start.month == 5, (
        f"Saga Dawa 2026 should start in May, got {start.month}"
    )
    # Should run roughly 28-31 days
    duration = (end - start).days
    assert 27 <= duration <= 32, (
        f"Saga Dawa duration {duration} days outside expected 27-32"
    )
    # Should overlap with mid-May to mid-June
    expected_start_range = (
        pytz.utc.localize(datetime(2026, 5, 10)),
        pytz.utc.localize(datetime(2026, 5, 25)),
    )
    assert expected_start_range[0] <= start <= expected_start_range[1], (
        f"Saga Dawa 2026 start {start} not in expected window "
        f"{expected_start_range[0]} - {expected_start_range[1]}"
    )


def test_saga_dawa_associated_lunar_mansion_is_root():
    """Saga Dawa should be tagged with associated_lunar_mansion = 2 (Root, 氐)."""
    f = next(x for x in festivals.list_festivals() if x["id"] == "saga_dawa")
    assert f["associated_lunar_mansion"] == 2


# ── Tibetan full moon (Vesak / Chotrul) ───────────────────────────

def test_vesak_2026_is_in_saga_dawa():
    """Vesak should be the full moon DURING the Saga Dawa window."""
    vesak = festivals.resolve_festival("vesak", 2026)
    saga = festivals.resolve_festival("saga_dawa", 2026)
    assert vesak is not None and saga is not None
    assert saga["start_datetime"] <= vesak["start_datetime"] <= saga["end_datetime"], (
        f"Vesak ({vesak['start_datetime']}) should fall inside "
        f"Saga Dawa ({saga['start_datetime']} - {saga['end_datetime']})"
    )


# ── Lunar month/day resolution ────────────────────────────────────

def test_mid_autumn_2026_in_september_or_october():
    """Mid-Autumn Festival: 15th of 8th lunar month (~mid-September to early October)."""
    result = festivals.resolve_festival("mid_autumn", 2026)
    assert result is not None
    # Should fall around Sep-Oct
    assert result["start_datetime"].month in (9, 10)


# ── Festival proximity ────────────────────────────────────────────

def test_proximity_during_saga_dawa_returns_saga_dawa_active():
    """Querying on May 18 2026 should return Saga Dawa as active."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    nearby = festivals.get_festival_proximity(dt, window_days=14)
    saga = next((f for f in nearby if f["id"] == "saga_dawa"), None)
    assert saga is not None, (
        "Saga Dawa should appear in proximity on 2026-05-18 (during the window)"
    )
    assert saga["status"] == "active"
    assert saga["distance_days"] == 0


def test_proximity_returns_sorted_by_distance():
    """Festivals should be ordered nearest-first."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    nearby = festivals.get_festival_proximity(dt, window_days=30)
    distances = [f["distance_days"] for f in nearby]
    assert distances == sorted(distances), "Festivals not sorted by distance"


def test_proximity_includes_divine_marriage_in_late_may():
    """On May 18 2026, Divine Marriage (May 24) is 6 days away — within 14 days."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    nearby = festivals.get_festival_proximity(dt, window_days=14)
    dm = next((f for f in nearby if f["id"] == "divine_marriage_damanhur"), None)
    assert dm is not None, (
        "Divine Marriage (May 24) should appear in 14-day proximity from May 18"
    )
    assert dm["status"] == "upcoming"
    assert 5 <= dm["distance_days"] <= 7


def test_proximity_window_excludes_far_festivals():
    """Querying on May 18 with 7-day window should NOT return Day of the Dead (Nov 2)."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    nearby = festivals.get_festival_proximity(dt, window_days=7)
    dod = next((f for f in nearby if f["id"] == "day_of_dead"), None)
    assert dod is None


# ── Tibetan calendar API ────────────────────────────────────────────

def test_tibetan_month_on_2026_05_18_is_saga_dawa():
    """May 18, 2026 should fall in the Tibetan 4th month — Saga Dawa."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    m = festivals.get_tibetan_month(dt)
    assert m["month_number"] == 4
    assert m["is_saga_dawa"] is True
    assert "Saga Dawa" in m["month_name_english"]


def test_tibetan_month_returns_required_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    m = festivals.get_tibetan_month(dt)
    for key in ("month_number", "month_name_transliteration", "month_name_tibetan",
                "month_name_english", "month_start", "month_end", "is_saga_dawa",
                "tibetan_year", "losar_datetime"):
        assert key in m, f"Missing key: {key}"


def test_tibetan_month_start_before_end():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    m = festivals.get_tibetan_month(dt)
    assert m["month_start"] < m["month_end"]
    # The given dt should fall inside
    assert m["month_start"] <= dt < m["month_end"]


def test_tibetan_month_handles_pre_losar():
    """A January date should map to the PREVIOUS Tibetan year's 11th or 12th month."""
    dt = pytz.utc.localize(datetime(2026, 1, 20, 12, 0))
    m = festivals.get_tibetan_month(dt)
    assert m["tibetan_year"] == 2025  # previous Gregorian year's Losar applies
    assert m["month_number"] >= 11   # late in Tibetan year
