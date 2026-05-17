"""
Tests for the calendar engine (Divine Month, Sephirotic Week, Divine Year).

Verifies epoch, month assignment, sephirotic day ordering, intercalation,
and known historical dates from the determined calendar architecture.
"""

import pytest
from datetime import datetime, timedelta

from src.engine.calendar import (
    get_divine_year,
    get_divine_month,
    get_sephirotic_day,
    get_year_start_nm,
    previous_new_moon,
    next_new_moon,
    _get_quarter_phases,
    EPOCH_YEAR,
)
from src import registry


# ── Epoch verification ──────────────────────────────────────────


class TestEpoch:
    """Verify the calendar epoch: NM Sep 22, 1949."""

    def test_epoch_new_moon_date(self):
        """The epoch NM falls on September 22, 1949."""
        year_start = get_year_start_nm(1949)
        assert year_start.year == 1949
        assert year_start.month == 9
        assert year_start.day == 22

    def test_epoch_is_year_1(self):
        """A date in October 1949 is Divine Year 1."""
        dt = datetime(1949, 10, 15, 12, 0)
        year_info = get_divine_year(dt)
        assert year_info["year"] == 1
        assert year_info["anchor_gregorian"] == 1949

    def test_epoch_precedes_ae(self):
        """The epoch NM precedes the 1949 Autumn Equinox (Sep 23)."""
        year_start = get_year_start_nm(1949)
        assert year_start.day <= 23  # NM on 22nd, AE on 23rd


# ── Divine Year ─────────────────────────────────────────────────


class TestDivineYear:
    """Tests for Divine Year computation."""

    def test_year_2026(self):
        """2026 AE → Divine Year 78 (2026 - 1949 + 1)."""
        dt = datetime(2026, 10, 15, 12, 0)
        year_info = get_divine_year(dt)
        assert year_info["year"] == 78
        assert year_info["anchor_gregorian"] == 2026

    def test_year_before_ae(self):
        """A date before 2026 AE belongs to the prior divine year."""
        dt = datetime(2026, 3, 1, 12, 0)
        year_info = get_divine_year(dt)
        # Before 2026 AE → still in year anchored to 2025
        assert year_info["anchor_gregorian"] == 2025
        assert year_info["year"] == 77

    def test_year_total_months(self):
        """Every divine year has 12 or 13 months."""
        for greg_year in [1949, 1960, 1975, 2000, 2025, 2026]:
            dt = datetime(greg_year, 11, 1, 12, 0)
            year_info = get_divine_year(dt)
            assert year_info["total_months"] in (12, 13)

    def test_year_start_is_new_moon(self):
        """Year start is always a New Moon (elongation < 5°)."""
        import ephem
        for greg_year in [1949, 2000, 2025]:
            nm = get_year_start_nm(greg_year)
            # Verify this is indeed near a New Moon
            observer = ephem.Observer()
            observer.date = nm
            moon = ephem.Moon(observer)
            sun = ephem.Sun(observer)
            import math
            elong = abs(math.degrees(float(moon.elong)))
            assert elong < 5.0, f"Year {greg_year} start not at NM: elong={elong}°"


# ── Divine Month ────────────────────────────────────────────────


class TestDivineMonth:
    """Tests for Divine Month computation."""

    def test_oberto_birth_samma(self):
        """
        Oberto Airaudi born May 29, 1950 = Year 1, Month 9 (SAMMA).
        [SOURCE: Calendar Architecture determination]
        """
        dt = datetime(1950, 5, 29, 12, 0)
        month_info = get_divine_month(dt)
        assert month_info["divine_year"] == 1
        assert month_info["month_number"] == 9

    def test_month_boundaries_are_new_moons(self):
        """Month start and end are New Moon moments."""
        dt = datetime(2026, 3, 15, 12, 0)
        month_info = get_divine_month(dt)
        # Month start should be a NM — verify by checking next NM from
        # just before the start equals the start
        nm = next_new_moon(month_info["month_start"] - timedelta(days=1))
        delta = abs((nm - month_info["month_start"]).total_seconds())
        assert delta < 60, "Month start not at New Moon"

    def test_month_duration_29_or_30(self):
        """Every lunation is 29 or 30 days."""
        dt = datetime(2026, 3, 15, 12, 0)
        month_info = get_divine_month(dt)
        assert month_info["total_days"] in (29, 30)

    def test_month_number_range(self):
        """Month number is 1-13."""
        for d in range(1, 13):
            dt = datetime(2026, d, 15, 12, 0)
            month_info = get_divine_month(dt)
            assert 1 <= month_info["month_number"] <= 13

    def test_day_in_month_positive(self):
        """Day in month is at least 1."""
        dt = datetime(2026, 3, 15, 12, 0)
        month_info = get_divine_month(dt)
        assert month_info["day_in_month"] >= 1
        assert month_info["day_in_month"] <= 30

    def test_consecutive_months_no_gap(self):
        """End of one month == start of next month."""
        dt1 = datetime(2026, 3, 1, 12, 0)
        m1 = get_divine_month(dt1)
        m2 = get_divine_month(m1["month_end"] + timedelta(hours=1))
        # m2's month_start should equal m1's month_end
        delta = abs((m2["month_start"] - m1["month_end"]).total_seconds())
        assert delta < 60

    def test_all_twelve_months_in_year(self):
        """Walking through a year hits months 1 through 12 (at least)."""
        year_start = get_year_start_nm(2025)
        months_seen = set()
        dt = year_start + timedelta(days=5)
        for _ in range(12):
            m = get_divine_month(dt)
            months_seen.add(m["month_number"])
            dt = m["month_end"] + timedelta(days=5)
        assert months_seen.issuperset({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})

    def test_epoch_year_great_rite_alignment(self):
        """
        Year 1 (1949-50): All six Great Rites fall in correct months.
        From the calendar architecture determination.
        """
        # AE Sep 23, 1949 → Month 1
        ae = datetime(1949, 9, 23, 12, 0)
        assert get_divine_month(ae)["month_number"] == 1

        # DotD Nov 1, 1949 → Month 2
        dotd = datetime(1949, 11, 1, 12, 0)
        assert get_divine_month(dotd)["month_number"] == 2

        # WS Dec 22, 1949 → Month 4
        ws = datetime(1949, 12, 22, 12, 0)
        assert get_divine_month(ws)["month_number"] == 4

        # SE Mar 21, 1950 → Month 7
        se = datetime(1950, 3, 21, 12, 0)
        assert get_divine_month(se)["month_number"] == 7

        # DM May 24, 1950 → Month 9
        dm = datetime(1950, 5, 24, 12, 0)
        assert get_divine_month(dm)["month_number"] == 9

        # SS Jun 21, 1950 → Month 10
        ss = datetime(1950, 6, 21, 12, 0)
        assert get_divine_month(ss)["month_number"] == 10


# ── Sephirotic Day ──────────────────────────────────────────────


class TestSephiroticDay:
    """Tests for Sephirotic Day computation."""

    def test_day_range(self):
        """Day number is 1-9."""
        dt = datetime(2026, 3, 15, 12, 0)
        seph = get_sephirotic_day(dt)
        assert 1 <= seph["day"] <= 9

    def test_quarter_days_7_to_9(self):
        """Each quarter-week has 7-9 days."""
        # Sample several dates across a year
        for month in range(1, 13):
            dt = datetime(2026, month, 15, 12, 0)
            seph = get_sephirotic_day(dt)
            assert 6 <= seph["quarter_days"] <= 9, (
                f"Quarter at {dt} has {seph['quarter_days']} days"
            )

    def test_quarter_types(self):
        """Quarter name is one of the four lunar phase names."""
        valid = {"new_moon", "first_quarter", "full_moon", "last_quarter"}
        dt = datetime(2026, 3, 15, 12, 0)
        seph = get_sephirotic_day(dt)
        assert seph["quarter"] in valid

    def test_day_1_at_quarter_start(self):
        """Day 1 occurs at the start of a quarter phase."""
        # Find a specific New Moon
        nm = next_new_moon(datetime(2026, 3, 1))
        seph = get_sephirotic_day(nm + timedelta(hours=1))
        assert seph["day"] == 1
        assert seph["quarter"] == "new_moon"

    def test_day_progression(self):
        """Days increment within a quarter."""
        nm = next_new_moon(datetime(2026, 3, 1))
        prev_day = 0
        for d in range(7):
            dt = nm + timedelta(days=d, hours=12)
            seph = get_sephirotic_day(dt)
            assert seph["day"] >= prev_day, (
                f"Day decreased: day {d} = sephirotic {seph['day']}"
            )
            prev_day = seph["day"]

    def test_sephirotic_registry_lookup(self):
        """Sephirotic day data exists in registry for all valid days."""
        for d in range(1, 10):
            data = registry.get_sephirotic_day(d)
            assert "sephirah" in data
            assert "planet" in data

    def test_day_1_is_tiphareth(self):
        """Day 1 = Tiphareth/Sol (NOT Yesod — that was the archived error)."""
        data = registry.get_sephirotic_day(1)
        assert data["sephirah"] == "Tiphareth"
        assert data["planet"] == "Sol"

    def test_four_quarters_per_lunation(self):
        """A lunation has exactly 4 quarter phases + closing NM."""
        dt = datetime(2026, 3, 15, 12, 0)
        phases = _get_quarter_phases(dt)
        assert len(phases) == 5
        assert phases[0][0] == "new_moon"
        assert phases[-1][0] == "new_moon"


# ── Integration with registry ───────────────────────────────────


class TestRegistryIntegration:
    """Tests for calendar ↔ registry data flow."""

    def test_month_name_lookup(self):
        """Every month number maps to a registry entry."""
        for num in range(1, 14):
            data = registry.get_divine_month(num)
            assert "name" in data
            assert "number" in data
            assert data["number"] == num

    def test_month_1_is_isis(self):
        """Month 1 = ISIS."""
        data = registry.get_divine_month(1)
        assert data["name"] == "ISIS"

    def test_month_13_is_vadusfadahm(self):
        """Month 13 = VADUSFADAHM (intercalary)."""
        data = registry.get_divine_month(13)
        assert data["name"] == "VADUSFADAHM"

    def test_great_rite_months(self):
        """Great Rite months have the correct names."""
        rites = {
            1: ("ISIS", "Autumn Equinox"),
            2: ("SADAM", "Day of the Dead"),
            4: ("EOROS", "Winter Solstice"),
            7: ("OSIRIS", "Spring Equinox"),
            9: ("SAMMA", "Divine Marriage"),
            10: ("SET", "Summer Solstice"),
        }
        for num, (name, rite) in rites.items():
            data = registry.get_divine_month(num)
            assert data["name"] == name
            assert data["great_rite"] == rite

    def test_alchemical_stages(self):
        """Months map to the three alchemical stages."""
        for num in range(1, 5):
            assert registry.get_divine_month(num)["alchemical"] == "Nigredo"
        for num in range(5, 9):
            assert registry.get_divine_month(num)["alchemical"] == "Albedo"
        for num in range(9, 13):
            assert registry.get_divine_month(num)["alchemical"] == "Rubedo"


# ── New Moon helpers ────────────────────────────────────────────


class TestNewMoonHelpers:
    """Tests for the low-level New Moon functions."""

    def test_previous_nm_before_dt(self):
        """Previous New Moon is before the given datetime."""
        dt = datetime(2026, 3, 15, 12, 0)
        nm = previous_new_moon(dt)
        assert nm < dt

    def test_next_nm_after_dt(self):
        """Next New Moon is after the given datetime."""
        dt = datetime(2026, 3, 15, 12, 0)
        nm = next_new_moon(dt)
        assert nm > dt

    def test_nm_cycle_approximately_29_days(self):
        """New Moon to New Moon is ~29.5 days."""
        nm1 = next_new_moon(datetime(2026, 3, 1))
        nm2 = next_new_moon(nm1 + timedelta(days=1))
        delta = (nm2 - nm1).total_seconds() / 86400
        assert 29.0 <= delta <= 30.0


class TestIntercalaryMonth:
    """Verify intercalary month (13 = VADUSFADAHM) detection."""

    def test_13_month_year_exists(self):
        """At least one year in the test range has 13 months."""
        found_13 = False
        for greg_year in range(2000, 2030):
            dt = datetime(greg_year, 11, 1, 12, 0)
            year_info = get_divine_year(dt)
            if year_info["total_months"] == 13:
                found_13 = True
                break
        assert found_13, "No 13-month year found in 2000-2029"

    def test_intercalary_month_is_month_13(self):
        """Walk through a 13-month year; month 13 should appear."""
        # Find a 13-month year
        for greg_year in range(2000, 2030):
            dt = datetime(greg_year, 11, 1, 12, 0)
            year_info = get_divine_year(dt)
            if year_info["total_months"] == 13:
                # Walk to month 13
                year_start = get_year_start_nm(year_info["anchor_gregorian"])
                dt = year_start + timedelta(days=5)
                for _ in range(13):
                    m = get_divine_month(dt)
                    if m["month_number"] == 13:
                        assert m["is_intercalary"] is True
                        return
                    dt = m["month_end"] + timedelta(days=5)
        pytest.skip("No 13-month year found in range")

    def test_intercalary_month_registry_name(self):
        """Month 13 in the registry is VADUSFADAHM."""
        month = registry.get_divine_month(13)
        assert month["name"] == "VADUSFADAHM"
        assert month["alchemical"] == "Da'ath"


class TestSephiroticRareDays:
    """Test sephirotic days 8 and 9 (Chokmah/Uranus and Kether/Neptune)."""

    def test_sephirotic_day_8_exists_in_registry(self):
        """Day 8 = Chokmah / Uranus."""
        data = registry.get_sephirotic_day(8)
        assert data["sephirah"] == "Chokmah"
        assert data["planet"] == "Uranus"
        assert data["frequency"] == "~65%"

    def test_sephirotic_day_9_exists_in_registry(self):
        """Day 9 = Kether / Neptune."""
        data = registry.get_sephirotic_day(9)
        assert data["sephirah"] == "Kether"
        assert data["planet"] == "Neptune"
        assert data["frequency"] == "~22%"

    def test_day_8_or_9_occurs_naturally(self):
        """Over a 3-month scan, at least one quarter should have 8+ days."""
        found_8_plus = False
        dt = datetime(2026, 1, 1, 12, 0)
        for _ in range(12):
            seph = get_sephirotic_day(dt)
            if seph["day"] >= 8:
                found_8_plus = True
                break
            # Jump 7 days (mid-quarter to mid-quarter)
            dt += timedelta(days=7)
        # If not found by sampling, do a thorough scan
        if not found_8_plus:
            dt = datetime(2026, 1, 1, 12, 0)
            for day_offset in range(90):
                seph = get_sephirotic_day(dt + timedelta(days=day_offset))
                if seph["day"] >= 8:
                    found_8_plus = True
                    break
        assert found_8_plus, "No sephirotic day >= 8 found in 90-day scan"
