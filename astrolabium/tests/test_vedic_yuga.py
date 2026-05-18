"""
Tests for the Vedic yuga / kalpa deep-time engine.

Validates:
  • the canonical year counts (Kali = 432K, Mahā Yuga = 4.32M, Kalpa = 4.32B)
  • years_into_kali_yuga gives ~5127 years for 2026
  • we are in the Kali Yuga
  • kalpa positioning matches Vaishnava reckoning (7th Manvantara, 28th Mahā Yuga)
"""

from datetime import datetime
import pytest
import pytz

from src.engine import vedic_yuga as vy


# ── Constants ────────────────────────────────────────────────────

def test_kali_yuga_is_432000_years():
    assert vy.KALI_YUGA_YEARS == 432_000


def test_maha_yuga_is_4_32_million_years():
    assert vy.MAHA_YUGA_YEARS == 4_320_000


def test_yuga_ratios():
    """Satya:Treta:Dvapara:Kali = 4:3:2:1."""
    assert vy.SATYA_YUGA_YEARS == 4 * vy.KALI_YUGA_YEARS
    assert vy.TRETA_YUGA_YEARS == 3 * vy.KALI_YUGA_YEARS
    assert vy.DVAPARA_YUGA_YEARS == 2 * vy.KALI_YUGA_YEARS


def test_maha_yuga_is_sum_of_four_yugas():
    assert vy.MAHA_YUGA_YEARS == (
        vy.SATYA_YUGA_YEARS + vy.TRETA_YUGA_YEARS
        + vy.DVAPARA_YUGA_YEARS + vy.KALI_YUGA_YEARS
    )


def test_manvantara_definition():
    """71 Mahā Yugas + Satya-sandhya."""
    assert vy.MANVANTARA_YEARS == 71 * vy.MAHA_YUGA_YEARS + vy.SATYA_YUGA_YEARS


def test_kalpa_definition():
    """14 Manvantaras + initial Satya-sandhya."""
    assert vy.KALPA_YEARS == 14 * vy.MANVANTARA_YEARS + vy.SATYA_YUGA_YEARS


def test_kalpa_is_about_4_32_billion_years():
    """Canonical: a Day of Brahmā ≈ 4.32 billion years."""
    assert 4_300_000_000 < vy.KALPA_YEARS < 4_400_000_000


# ── Years into Kali Yuga ─────────────────────────────────────────

def test_years_into_kali_yuga_2026_is_about_5127():
    """2026 is ~5127 years after 3102 BCE Kali Yuga start."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    y = vy.years_into_kali_yuga(dt)
    assert 5125 < y < 5130, f"Expected ~5127 years into Kali Yuga; got {y}"


def test_kali_yuga_fraction_in_2026_is_about_1_2_percent():
    """5127 / 432,000 ≈ 0.012 (1.2%)."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    f = vy.kali_yuga_fraction(dt)
    assert 0.010 < f < 0.013


def test_kali_yuga_years_remaining():
    """~426,870 years remaining."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    r = vy.kali_yuga_years_remaining(dt)
    assert 426_000 < r < 427_500


# ── Current yuga ─────────────────────────────────────────────────

def test_current_yuga_is_kali():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    yuga = vy.current_yuga(dt)
    assert yuga["yuga"] == "Kali Yuga"
    assert yuga["yuga_duration_years"] == 432_000


def test_current_yuga_fraction_consistent():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    yuga = vy.current_yuga(dt)
    assert yuga["fraction_through"] == yuga["years_elapsed"] / yuga["yuga_duration_years"]


# ── Maha Yuga ──────────────────────────────────────────────────

def test_years_into_maha_yuga_2026():
    """Kali Yuga is the 4th quarter of the Mahā Yuga. We should be
    at (Satya + Treta + Dvapara + ~5127) ≈ 3,893,127 years into the
    current Mahā Yuga."""
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    y = vy.years_into_maha_yuga(dt)
    expected_lower = 3_893_000
    expected_upper = 3_894_000
    assert expected_lower < y < expected_upper, (
        f"Expected ~3.893M years into Mahā Yuga; got {y}"
    )


# ── Kalpa ──────────────────────────────────────────────────────

def test_kalpa_state_is_7th_manvantara():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    k = vy.years_into_kalpa(dt)
    assert k["manvantara_number"] == 7
    assert k["manvantara_name"] == "Vaivasvata Manu"


def test_kalpa_state_is_28th_mahayuga_in_manvantara():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    k = vy.years_into_kalpa(dt)
    assert k["mahayuga_number_in_manvantara"] == 28


def test_kalpa_fraction_in_range():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    k = vy.years_into_kalpa(dt)
    assert 0.0 < k["fraction_through_kalpa"] < 1.0


def test_get_vedic_time_has_all_keys():
    dt = pytz.utc.localize(datetime(2026, 5, 18, 12, 0))
    state = vy.get_vedic_time(dt)
    for key in ("current_yuga", "years_into_maha_yuga",
                "maha_yuga_total_years", "kalpa", "constants"):
        assert key in state
