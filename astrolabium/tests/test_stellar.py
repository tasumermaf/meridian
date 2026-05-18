"""
Tests for the 28-Lunar-Mansion stellar engine.

Validates:
  • mansion data integrity (28 mansions, 4 palaces, full ecliptic coverage)
  • mansion lookup by ecliptic longitude (including the 0°/360° wrap)
  • sun and moon mansion computation against known reference dates
  • palace assignment correctness
  • planetary mansion lookup
"""

from datetime import datetime
import pytest
import pytz

from src.engine import stellar


# ── Data integrity ──────────────────────────────────────────────────

def test_mansion_count_is_28():
    assert stellar.get_mansion_count() == 28


def test_palace_count_is_4():
    assert stellar.get_palace_count() == 4


def test_each_palace_has_seven_mansions():
    for palace in stellar.list_palaces():
        assert len(palace["mansion_indices"]) == 7, (
            f"Palace {palace['english']} has {len(palace['mansion_indices'])} mansions"
        )


def test_mansion_indices_unique_and_complete():
    """Every index 0..27 appears exactly once across all palaces."""
    all_indices = []
    for palace in stellar.list_palaces():
        all_indices.extend(palace["mansion_indices"])
    assert sorted(all_indices) == list(range(28))


def test_mansions_cover_full_ecliptic():
    """The 28 mansions together must cover the entire 360° of the ecliptic."""
    total_width = sum(m["width_degrees"] for m in stellar.list_mansions())
    assert abs(total_width - 360.0) < 0.01, (
        f"Sum of mansion widths = {total_width}, expected 360°"
    )


def test_each_mansion_width_consistent_with_endpoints():
    """For each mansion, width_degrees should match end−start (mod 360)."""
    for m in stellar.list_mansions():
        start = m["ecliptic_longitude_start"]
        end = m["ecliptic_longitude_end"]
        if start < end:
            implied_width = end - start
        else:
            implied_width = (360.0 - start) + end
        assert abs(implied_width - m["width_degrees"]) < 0.5, (
            f"Mansion {m['index']} ({m['english']}): "
            f"width {m['width_degrees']}° vs implied {implied_width}°"
        )


# ── Lookup correctness ─────────────────────────────────────────────

def test_lookup_at_horn_mansion():
    """Spica (~204°) should land in Horn (Jiǎo, mansion 0)."""
    m = stellar.get_mansion_by_longitude(204.0)
    assert m["index"] == 0
    assert m["pinyin"] == "Jiǎo"
    assert m["english"] == "Horn"
    assert m["palace_english"] == "Azure Dragon of the East"


def test_lookup_at_root_mansion():
    """Root (Dī 氐, mansion 2) sits 216-231°."""
    m = stellar.get_mansion_by_longitude(220.0)
    assert m["index"] == 2
    assert m["pinyin"] == "Dī"
    assert m["english"] == "Root"
    assert m["palace_english"] == "Azure Dragon of the East"


def test_lookup_at_pleiades():
    """Pleiades (Mǎo 昴, mansion 17) sits 56-67°."""
    m = stellar.get_mansion_by_longitude(60.0)
    assert m["index"] == 17
    assert m["pinyin"] == "Mǎo"
    assert m["english"] == "Hairy Head"
    assert m["palace_english"] == "White Tiger of the West"


def test_lookup_handles_boundary_at_360():
    """Encampment (Shì 室, mansion 12) covers 343°-360°; Wall (Bì 壁, mansion 13)
    covers 0°-14°. Test the boundary handling."""
    # 350° should be in Encampment (12)
    m = stellar.get_mansion_by_longitude(350.0)
    assert m["index"] == 12
    assert m["pinyin"] == "Shì"

    # 10° should be in Wall (13)
    m = stellar.get_mansion_by_longitude(10.0)
    assert m["index"] == 13
    assert m["pinyin"] == "Bì"

    # Exactly 0° should also fall in Wall (start of its range)
    m = stellar.get_mansion_by_longitude(0.0)
    assert m["index"] == 13


def test_lookup_wraps_over_360():
    """Longitude > 360 should be normalized."""
    m1 = stellar.get_mansion_by_longitude(60.0)
    m2 = stellar.get_mansion_by_longitude(420.0)  # 60 + 360
    assert m1["index"] == m2["index"]


def test_lookup_handles_negative_longitude():
    """Negative longitude should be normalized."""
    m1 = stellar.get_mansion_by_longitude(300.0)
    m2 = stellar.get_mansion_by_longitude(-60.0)  # equivalent to 300
    assert m1["index"] == m2["index"]


# ── Sun / Moon / planet mansion lookups ───────────────────────────

def test_get_lunar_mansion_returns_valid_mansion():
    """For any reasonable datetime, the Moon must be in one of the 28 mansions."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    m = stellar.get_lunar_mansion(dt)
    assert 0 <= m["index"] < 28
    assert m["body"] == "Moon"
    assert 0.0 <= m["ecliptic_longitude"] < 360.0
    assert m["palace_english"] in [
        "Azure Dragon of the East",
        "Black Tortoise of the North",
        "White Tiger of the West",
        "Vermillion Bird of the South",
    ]


def test_get_solar_mansion_returns_valid_mansion():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    m = stellar.get_solar_mansion(dt)
    assert 0 <= m["index"] < 28
    assert m["body"] == "Sun"


def test_get_planetary_mansions_returns_all_five():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    planets = stellar.get_planetary_mansions(dt)
    assert set(planets.keys()) == {"Mercury", "Venus", "Mars", "Jupiter", "Saturn"}
    for name, m in planets.items():
        assert 0 <= m["index"] < 28
        assert m["body"] == name


def test_naive_datetime_is_assumed_utc():
    """A datetime without tzinfo should be treated as UTC, not local."""
    naive = datetime(2026, 5, 18, 12, 0)
    aware = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    m_naive = stellar.get_lunar_mansion(naive)
    m_aware = stellar.get_lunar_mansion(aware)
    assert m_naive["index"] == m_aware["index"]


# ── Full stellar state composition ────────────────────────────────

def test_get_stellar_state_returns_complete_structure():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = stellar.get_stellar_state(dt)
    assert "sun_mansion" in state
    assert "lunar_mansion" in state
    assert "planet_mansions" in state
    assert "palace_summary" in state
    assert state["sun_mansion"]["body"] == "Sun"
    assert state["lunar_mansion"]["body"] == "Moon"
    assert len(state["planet_mansions"]) == 5
    # palace summary covers all bodies
    assert "Sun" in state["palace_summary"]
    assert "Moon" in state["palace_summary"]
    assert "Jupiter" in state["palace_summary"]


# ── Saga Dawa contextual check ────────────────────────────────────

def test_saga_dawa_2026_moon_visits_root_or_neighbor():
    """
    Saga Dawa 2026 runs May 17 — June 14. The Buddha-month is named for the
    Saga (Sa-ga, ས་ག་) lunar mansion, classically associated with the Root
    region (Dī 氐, mansion 2 in the Chinese system) of the Azure Dragon.

    Over the course of Saga Dawa, the Moon traverses the full ecliptic
    multiple times (each lunation = ~27.3 days against the stars). On the
    full moon of Vesak — which falls during Saga Dawa — the Moon is
    opposite the Sun.

    This test verifies that DURING the Saga Dawa window, the Moon visits
    the Root Mansion or its immediate neighbors at least once. (We don't
    pin to the exact Vesak full-moon date because Tibetan calendar
    variants differ slightly.)
    """
    saga_dawa_start = pytz.utc.localize(datetime(2026, 5, 17, 0, 0))
    saga_dawa_end = pytz.utc.localize(datetime(2026, 6, 14, 23, 59))

    from datetime import timedelta
    cur = saga_dawa_start
    visited = set()
    while cur <= saga_dawa_end:
        m = stellar.get_lunar_mansion(cur)
        visited.add(m["index"])
        cur += timedelta(hours=12)

    # Across a full lunar month, the Moon should visit all 28 mansions.
    # The Root Mansion (index 2) must be among them.
    assert 2 in visited, (
        "During Saga Dawa 2026, the Moon should pass through the Root Mansion (氐) "
        f"at least once. Visited mansion indices: {sorted(visited)}"
    )
    # Sanity: should also visit most or all mansions in 28 days
    assert len(visited) >= 25, (
        f"Expected the Moon to visit ~28 mansions during a full Saga Dawa "
        f"window; only saw {len(visited)}"
    )
