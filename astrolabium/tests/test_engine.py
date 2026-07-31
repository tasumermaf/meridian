"""
Engine layer tests — pure algorithms, no registry dependency.

Tests solar positions, stem-branch calculations, LGBF formula,
lunar elongation, and branch synchronization.
"""

import pytest
from datetime import datetime
import pytz

from src.engine.solar import get_solar_positions, get_daylight_duration
from src.engine.twilight import get_cusping_windows
from src.engine.stem_branch import (
    get_daily_stem_branch,
    get_hourly_stem,
    get_lgbf_substitution,
    get_earthly_branch_from_solar,
    get_lgbf_remainder,
    VESSEL_REMAINDER_MAP,
)
from src.engine.lunar import get_lunar_elongation, get_phase_index, get_illumination


# ── Test location: Los Angeles ──
LA_LAT, LA_LON, LA_TZ = 34.0522, -118.2437, "America/Los_Angeles"

# ── Reference date: Jan 1, 2000 = 戊午 (Wù Wǔ) — stem 4, branch 6 ──
REF_DT = datetime(2000, 1, 1, 12, 0, 0)


class TestSolar:
    """Solar position calculations."""

    def test_solar_returns_all_keys(self):
        dt = datetime(2026, 3, 1, 12, 0, 0)
        result = get_solar_positions(dt, LA_LAT, LA_LON, LA_TZ)
        assert "sunrise" in result
        assert "sunset" in result
        assert "solar_noon" in result
        assert "solar_midnight" in result

    def test_sunrise_before_sunset(self):
        dt = datetime(2026, 3, 1, 12, 0, 0)
        result = get_solar_positions(dt, LA_LAT, LA_LON, LA_TZ)
        assert result["sunrise"] < result["sunset"]

    def test_daylight_reasonable(self):
        dt = datetime(2026, 6, 21, 12, 0, 0)  # Summer solstice
        hours = get_daylight_duration(dt, LA_LAT, LA_LON, LA_TZ)
        assert 13.5 < hours < 15.5  # LA summer day ~14.3 hours

    def test_winter_shorter_day(self):
        summer = datetime(2026, 6, 21, 12, 0, 0)
        winter = datetime(2026, 12, 21, 12, 0, 0)
        summer_hrs = get_daylight_duration(summer, LA_LAT, LA_LON, LA_TZ)
        winter_hrs = get_daylight_duration(winter, LA_LAT, LA_LON, LA_TZ)
        assert summer_hrs > winter_hrs

    def test_twilight_in_range(self):
        # Twilight duration is now surfaced only through the live cusping
        # windows (dead helper deleted per AUDIT_2026-07-24 D-01).
        dt = datetime(2026, 3, 1, 12, 0, 0)
        windows = get_cusping_windows(dt, LA_LAT, LA_LON, LA_TZ)
        assert not windows["twilight_undefined"]
        for w in ("gold_window", "silver_window"):
            assert 20 < windows[w]["radius_minutes"] < 45  # Typical civil twilight range

    def test_polar_latitude_raises(self):
        """
        C-2 regression: polar latitudes must raise ValueError, not produce
        fake 12-hour days. Svalbard on summer solstice has midnight sun.
        """
        with pytest.raises(ValueError, match="Polar conditions"):
            get_solar_positions(datetime(2026, 6, 21, 12), 78.2, 15.6, "Europe/Oslo")

    def test_polar_winter_raises(self):
        """Polar night (no sunrise) also raises."""
        with pytest.raises(ValueError, match="Polar conditions"):
            get_solar_positions(datetime(2026, 12, 21, 12), 78.2, 15.6, "Europe/Oslo")

    def test_temperate_high_latitude_works(self):
        """Stockholm (55N) should still work, even in winter."""
        result = get_solar_positions(
            datetime(2026, 12, 21, 12), 55.0, 13.0, "Europe/Stockholm"
        )
        daylight = (result["sunset"] - result["sunrise"]).total_seconds() / 3600
        assert 5 < daylight < 10  # ~7h daylight in Stockholm winter


class TestStemBranch:
    """Stem-branch calendar calculations."""

    def test_reference_date(self):
        """Jan 1, 2000 = stem 4 (戊 Wù), branch 6 (午 Wǔ)."""
        result = get_daily_stem_branch(REF_DT)
        assert result["stem_index"] == 4
        assert result["branch_index"] == 6
        assert result["stem_chinese"] == "戊"
        assert result["branch_chinese"] == "午"
        assert result["is_yang_day"] is True

    def test_next_day_increments(self):
        """Jan 2, 2000 should be stem 5, branch 7."""
        dt = datetime(2000, 1, 2, 12, 0, 0)
        result = get_daily_stem_branch(dt)
        assert result["stem_index"] == 5
        assert result["branch_index"] == 7

    def test_stem_wraps_at_10(self):
        """After 10 days, stem wraps back."""
        dt = datetime(2000, 1, 11, 12, 0, 0)  # +10 days
        result = get_daily_stem_branch(dt)
        assert result["stem_index"] == (4 + 10) % 10  # = 4

    def test_branch_wraps_at_12(self):
        """After 12 days, branch wraps back."""
        dt = datetime(2000, 1, 13, 12, 0, 0)  # +12 days
        result = get_daily_stem_branch(dt)
        assert result["branch_index"] == (6 + 12) % 12  # = 6

    def test_yin_day(self):
        """Jan 2, 2000 (stem 5 = 己 Jǐ) should be Yin day."""
        dt = datetime(2000, 1, 2, 12, 0, 0)
        result = get_daily_stem_branch(dt)
        assert result["is_yang_day"] is False

    def test_five_rat_rule(self):
        """Hourly stem from Five Rat Rule."""
        # Day stem 0 (甲 Jiǎ): first Zi stem = 0 (甲)
        assert get_hourly_stem(0, 0) == 0
        assert get_hourly_stem(0, 1) == 1
        # Day stem 4 (戊 Wù): first Zi stem = (4%5*2)%10 = 8
        assert get_hourly_stem(4, 0) == 8

    def test_lgbf_substitution_sum(self):
        """LGBF substitution numbers sum correctly."""
        result = get_lgbf_substitution(4, 6, 8, 0)
        # stem 4 → 6, branch 6 → 9, h_stem 8 → 7, h_branch 0 → 9
        assert result["day_stem_num"] == 6
        assert result["day_branch_num"] == 9
        assert result["hour_stem_num"] == 7
        assert result["hour_branch_num"] == 9
        assert result["sum"] == 31

    def test_vessel_remainder_map_complete(self):
        """All 9 remainders map to vessels."""
        for r in range(1, 10):
            assert r in VESSEL_REMAINDER_MAP
            assert isinstance(VESSEL_REMAINDER_MAP[r], str)

    def test_remainder_5_maps_to_yin_qiao(self):
        """Remainder 5 = Yin Qiao Mai (same as remainder 2)."""
        assert VESSEL_REMAINDER_MAP[5] == "Yin Qiao Mai"
        assert VESSEL_REMAINDER_MAP[2] == "Yin Qiao Mai"

    def test_earthly_branch_returns_valid_index(self):
        """Branch index should be 0-11."""
        dt = datetime(2026, 3, 1, 14, 0, 0)
        idx = get_earthly_branch_from_solar(dt, LA_LAT, LA_LON, LA_TZ)
        assert 0 <= idx <= 11

    def test_lgbf_remainder_full(self):
        """Full LGBF calculation returns valid vessel."""
        dt = datetime(2026, 3, 1, 14, 0, 0)
        result = get_lgbf_remainder(dt, LA_LAT, LA_LON, LA_TZ)
        assert 1 <= result["remainder"] <= 9
        assert result["vessel_name"] in VESSEL_REMAINDER_MAP.values()


class TestLunar:
    """Lunar elongation and phase calculations."""

    def test_elongation_in_range(self):
        dt = datetime(2026, 3, 1, 12, 0, 0)
        elong = get_lunar_elongation(dt)
        assert 0 <= elong < 360

    def test_phase_index_in_range(self):
        for deg in [0, 59, 60, 119, 120, 179, 180, 239, 240, 299, 300, 359]:
            idx = get_phase_index(float(deg))
            assert 0 <= idx <= 5

    def test_phase_boundaries(self):
        """Each 60° band maps to correct phase."""
        assert get_phase_index(0) == 0    # New Moon
        assert get_phase_index(30) == 0   # Still New Moon
        assert get_phase_index(60) == 1   # First Crescent
        assert get_phase_index(180) == 3  # Full Moon
        assert get_phase_index(300) == 5  # Last Quarter

    def test_phase_at_exact_new_moon(self):
        """
        C-1 regression: phase index must be 0 at exact New Moon.

        Before fix, ephem.Moon.elong returned ~358° at conjunction,
        mapping to phase 5 (Last Quarter) instead of phase 0 (New Moon).
        """
        from src.engine.calendar import next_new_moon
        nm = next_new_moon(datetime(2026, 3, 1))
        elong = get_lunar_elongation(nm)
        assert get_phase_index(elong) == 0, (
            f"Phase at exact NM should be 0, got {get_phase_index(elong)} "
            f"(elong={elong:.2f}°)"
        )

    def test_phase_near_conjunction_wrap(self):
        """
        C-1 regression: values near 360° wrap to phase 0, not phase 5.
        """
        assert get_phase_index(359.99) == 0
        assert get_phase_index(358.0) == 0
        assert get_phase_index(354.0) == 0
        # Below threshold stays phase 5
        assert get_phase_index(353.9) == 5

    def test_phase_at_multiple_new_moons(self):
        """Verify phase 0 at New Moons across different months."""
        from src.engine.calendar import next_new_moon
        for start_month in [1, 4, 7, 10]:
            nm = next_new_moon(datetime(2026, start_month, 1))
            elong = get_lunar_elongation(nm)
            assert get_phase_index(elong) == 0, (
                f"Phase at NM {nm} should be 0 (elong={elong:.2f}°)"
            )

    def test_illumination_new_moon(self):
        """Near 0° elongation → near 0% illumination."""
        assert get_illumination(0) < 1

    def test_illumination_full_moon(self):
        """Near 180° elongation → near 100% illumination."""
        assert get_illumination(180) > 99


class TestTwilight:
    """Cusping window calculations."""

    def test_midday_no_cusping(self):
        """Midday should not be in a cusping window."""
        dt = datetime(2026, 3, 1, 12, 0, 0)
        result = get_cusping_windows(dt, LA_LAT, LA_LON, LA_TZ)
        assert result["active"] is False
        assert result["key"] is None

    def test_both_windows_returned(self):
        """Both gold and silver window data should be present."""
        dt = datetime(2026, 3, 1, 12, 0, 0)
        result = get_cusping_windows(dt, LA_LAT, LA_LON, LA_TZ)
        assert result["gold_window"] is not None
        assert result["silver_window"] is not None
        assert result["gold_window"]["event_time"] < result["silver_window"]["event_time"]

    def test_at_sunrise_gold_active(self):
        """At sunrise, gold key should be active."""
        # Get actual sunrise for this date
        solar_pos = get_solar_positions(
            datetime(2026, 3, 1, 6, 0, 0), LA_LAT, LA_LON, LA_TZ
        )
        sunrise = solar_pos["sunrise"]
        result = get_cusping_windows(sunrise, LA_LAT, LA_LON, LA_TZ)
        assert result["active"] is True
        assert result["key"] == "gold"

    def test_at_sunset_silver_active(self):
        """At sunset, silver key should be active."""
        solar_pos = get_solar_positions(
            datetime(2026, 3, 1, 18, 0, 0), LA_LAT, LA_LON, LA_TZ
        )
        sunset = solar_pos["sunset"]
        result = get_cusping_windows(sunset, LA_LAT, LA_LON, LA_TZ)
        assert result["active"] is True
        assert result["key"] == "silver"


class TestWingRelativeBranches:
    """
    Regression tests for the wing-relative branch scheme
    (AUDIT_2026-07-24 A-7/A-8, ruled canon 2026-07-24).
    """

    def test_branch_continuous_across_civil_midnight(self):
        """A-7: the branch never flips AT civil midnight (no midnight anchor)."""
        tz = pytz.timezone(LA_TZ)
        before = tz.localize(datetime(2026, 7, 29, 23, 59))
        after = tz.localize(datetime(2026, 7, 30, 0, 1))
        b_before = get_earthly_branch_from_solar(before, LA_LAT, LA_LON, LA_TZ)
        b_after = get_earthly_branch_from_solar(after, LA_LAT, LA_LON, LA_TZ)
        # Two minutes apart: identical, or an adjacent night-sequence step —
        # never the old discontinuous 11->0 civil-midnight jump AND
        # 0 is allowed only if 23:59 was already 0's neighbor 11 at a real
        # sixth boundary; both instants sit mid-night so they must be equal
        # or consecutive in the night order [10, 11, 0, 1, 2, 3].
        night_order = [10, 11, 0, 1, 2, 3]
        i, j = night_order.index(b_before), night_order.index(b_after)
        assert j - i in (0, 1)

    def test_day_wing_boundaries_fall_at_sunrise_and_sunset(self):
        """A-8: branch 4 begins AT sunrise; branch 10 begins AT sunset."""
        tz = pytz.timezone(LA_TZ)
        dt = tz.localize(datetime(2026, 3, 20, 12, 0))
        pos = get_solar_positions(dt, LA_LAT, LA_LON, LA_TZ)
        assert get_earthly_branch_from_solar(pos["sunrise"], LA_LAT, LA_LON, LA_TZ) == 4
        assert get_earthly_branch_from_solar(pos["sunset"], LA_LAT, LA_LON, LA_TZ) == 10

    def test_equinox_matches_guidebook_worked_positions(self):
        """A-8: engine agrees with Guidebook §4.6 at the equinox probes."""
        from datetime import timedelta
        tz = pytz.timezone(LA_TZ)
        dt = tz.localize(datetime(2026, 3, 20, 12, 0))
        pos = get_solar_positions(dt, LA_LAT, LA_LON, LA_TZ)
        cases = [
            (pos["sunrise"] + timedelta(minutes=10), 4),
            (pos["solar_noon"] + timedelta(minutes=30), 7),
            (pos["sunset"] - timedelta(minutes=10), 9),
        ]
        for probe, expected in cases:
            assert get_earthly_branch_from_solar(probe, LA_LAT, LA_LON, LA_TZ) == expected

    def test_day_wing_spans_branches_4_through_9(self):
        """A-8: every day wing carries exactly branches 4-9, in order."""
        from datetime import timedelta
        tz = pytz.timezone(LA_TZ)
        dt = tz.localize(datetime(2026, 12, 21, 12, 0))  # winter solstice
        pos = get_solar_positions(dt, LA_LAT, LA_LON, LA_TZ)
        seen = []
        t = pos["sunrise"]
        while t < pos["sunset"]:
            b = get_earthly_branch_from_solar(t, LA_LAT, LA_LON, LA_TZ)
            if not seen or seen[-1] != b:
                seen.append(b)
            t += timedelta(minutes=10)
        assert seen == [4, 5, 6, 7, 8, 9]

    def test_white_nights_latitude_serves(self):
        """B-02: sun rises and sets at 63.4N midsummer -> engine serves."""
        tz = pytz.timezone("Europe/Oslo")
        dt = tz.localize(datetime(2026, 6, 21, 12, 0))
        pos = get_solar_positions(dt, 63.4305, 10.3951, "Europe/Oslo")
        assert pos["sunrise"] < pos["sunset"]
        windows = get_cusping_windows(pos["sunrise"], 63.4305, 10.3951, "Europe/Oslo")
        assert windows["active"] is True
        assert windows["key"] == "gold"
        assert windows["twilight_undefined"] is True  # flagged, never silent
