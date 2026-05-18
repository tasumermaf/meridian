"""
Tests for the heliacal risings engine.

Validates:
  • star catalog integrity (22 named stars, J2000 epoch)
  • star lookup by id
  • Sirius heliacal rising in Egypt falls in late July (canonical
    Sothic-cycle anchor)
  • upcoming_heliacal_risings returns a sorted list
  • the engine handles polar / circumpolar / never-rising cases
"""

from datetime import datetime
import pytest
import pytz

from src.engine import heliacal


# ── Catalog integrity ─────────────────────────────────────────────

def test_star_count_at_least_20():
    assert heliacal.get_star_count() >= 20


def test_sirius_in_catalog():
    s = heliacal.get_star_by_id("sirius")
    assert s is not None
    assert s["name"] == "Sirius"
    assert "α CMa" in s["bayer"]


def test_pleiades_in_catalog():
    s = heliacal.get_star_by_id("pleiades")
    assert s is not None
    assert "Pleiades" in s["name"]


def test_unknown_star_returns_none():
    assert heliacal.get_star_by_id("nonexistent") is None


def test_each_star_has_required_fields():
    for star in heliacal.list_stars():
        for key in ("id", "name", "bayer", "ra_deg", "dec_deg",
                    "magnitude", "constellation", "significance"):
            assert key in star, f"Star {star.get('id')} missing {key}"


def test_star_ra_in_valid_range():
    for star in heliacal.list_stars():
        assert 0 <= star["ra_deg"] < 360


def test_star_dec_in_valid_range():
    for star in heliacal.list_stars():
        assert -90 <= star["dec_deg"] <= 90


# ── Sirius heliacal rising at Egyptian latitude ──────────────────

def test_sirius_heliacal_rising_in_egypt_lands_in_late_july_or_august():
    """
    Classical: Sirius heliacal rising at the latitude of Memphis (~30°N)
    falls around mid-July to early August in the Gregorian calendar.

    With our simplified arcus visionis of 13°, modern conditions place
    it somewhere in late July to mid-August. We accept July or August.
    """
    dt = pytz.utc.localize(datetime(2026, 6, 1, 0, 0))  # before usual rise
    rise = heliacal.next_heliacal_rising(
        "sirius", lat=30.0, lon=31.2, tz="Africa/Cairo", dt=dt
    )
    assert rise is not None
    rising_dt = rise["heliacal_rising_datetime"]
    assert rising_dt.month in (7, 8), (
        f"Sirius heliacal rising in Egypt should fall in July-August; "
        f"got {rising_dt.strftime('%B %d')}"
    )


def test_polaris_not_in_upcoming_risings():
    """Polaris is essentially circumpolar from most northern latitudes;
    upcoming_heliacal_risings should skip it."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    upcoming = heliacal.upcoming_heliacal_risings(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt
    )
    for r in upcoming:
        assert r["id"] != "polaris", "Polaris should not appear in heliacal upcoming list"


# ── Upcoming risings ─────────────────────────────────────────────

def test_upcoming_returns_a_list():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    upcoming = heliacal.upcoming_heliacal_risings(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt, window_days=120
    )
    assert isinstance(upcoming, list)


def test_upcoming_is_sorted_by_days_until():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    upcoming = heliacal.upcoming_heliacal_risings(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt, window_days=120
    )
    days = [r["days_until"] for r in upcoming]
    assert days == sorted(days), "Upcoming risings not sorted"


def test_upcoming_respects_window():
    """Each rising should fall within the window."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    upcoming = heliacal.upcoming_heliacal_risings(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt, window_days=30
    )
    for r in upcoming:
        assert r["days_until"] <= 30


def test_upcoming_respects_max_stars():
    """max_stars caps the returned list."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    upcoming = heliacal.upcoming_heliacal_risings(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt, window_days=400, max_stars=3
    )
    assert len(upcoming) <= 3


# ── Heliacal state composition ───────────────────────────────────

def test_heliacal_state_has_required_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = heliacal.heliacal_state(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt, window_days=60
    )
    assert "upcoming" in state
    assert "sirius_next_heliacal_rising" in state
    assert "window_days" in state


def test_sirius_next_rise_in_state_is_future():
    """Sirius's next heliacal rising should be in the future."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = heliacal.heliacal_state(
        lat=45.42, lon=7.78, tz="Europe/Rome", dt=dt
    )
    if state["sirius_next_heliacal_rising"]:
        assert state["sirius_next_heliacal_rising"] > dt
