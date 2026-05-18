"""
Vedic yuga / kalpa deep-time engine.

The Vedic cosmological system situates ordinary historical time within
nested cycles of immense duration:

  Yuga              individual cosmological age (4 per Mahā Yuga)
                    durations:  Satya/Kṛta Yuga  = 1,728,000 years (4 × 432,000)
                                Treta Yuga       = 1,296,000 years (3 × 432,000)
                                Dvāpara Yuga     =   864,000 years (2 × 432,000)
                                Kali Yuga        =   432,000 years (1 × 432,000)
                                Total Mahā Yuga  = 4,320,000 years (10 × 432,000)

  Manvantara        71 Mahā Yugas + a transition (sandhya) of equal duration
                    to one Kṛta Yuga (1,728,000 yr).
                    Total: 71 × 4,320,000 + 1,728,000 ≈ 308.6 million years

  Kalpa             14 Manvantaras + an initial sandhya of one Kṛta Yuga
                    Total: 14 × 308.6M + 1.728M ≈ 4.32 BILLION years
                    (one "day of Brahmā")

  Year of Brahmā    360 such days + 360 such nights = ~3.1 trillion years
  Life of Brahmā    100 such years = ~311 trillion years

Traditional anchor: the current Kali Yuga began at midnight between
February 17 and February 18, 3102 BCE (Julian) according to the Sūrya
Siddhānta tradition (and the Mahābhārata war attribution).

This engine provides:

  • get_vedic_time(dt)                 — full deep-time framing
  • current_yuga(dt)                   — which yuga, fraction through
  • years_into_kali_yuga(dt)           — years since Kali Yuga began
  • years_into_maha_yuga(dt)           — within the current 4.32M yr cycle
  • years_into_kalpa(dt)               — within the current 4.32B yr "Day of Brahmā"

NOTE: There are competing traditions about WHICH part of the Mahā Yuga
we are in. Most modern adaptations place us in the Kali Yuga that began
3102 BCE. Sri Yukteswar's revised interpretation places us in a Dvāpara
Yuga of a shorter sub-cycle. We use the classical Sūrya Siddhānta
reckoning by default.

[SOURCE: Vedic / Sanskrit cosmology — Sūrya Siddhānta, Bhāgavata Purāṇa]
[MATHEMATICAL FACT] — the year counts and ratios are deterministic from
the traditional definitions.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pytz


# ── Constants — the canonical year counts ────────────────────────────

# Yuga durations (in years)
KALI_YUGA_YEARS         =   432_000
DVAPARA_YUGA_YEARS      =   864_000   # 2 × Kali
TRETA_YUGA_YEARS        = 1_296_000   # 3 × Kali
SATYA_YUGA_YEARS        = 1_728_000   # 4 × Kali  (also called Kṛta Yuga)

# A complete Mahā Yuga = sum of the four (Kṛta → Treta → Dvāpara → Kali)
MAHA_YUGA_YEARS         = 4_320_000   # 10 × Kali = total of 4 yugas

# 71 Mahā Yugas + a transition sandhya equal to one Kṛta Yuga = one Manvantara
MANVANTARA_YEARS        = 71 * MAHA_YUGA_YEARS + SATYA_YUGA_YEARS
# = 308,448,000 years

# 14 Manvantaras + an initial sandhya = one Kalpa = one Day of Brahmā
KALPA_YEARS             = 14 * MANVANTARA_YEARS + SATYA_YUGA_YEARS
# ≈ 4,320,000,000 (with rounding to canonical 4.32 billion)

# Traditional anchor: Kali Yuga began Feb 17/18, 3102 BCE
# In our datetime framework that's year -3101 (no year 0 in Gregorian,
# but we use astronomical year numbering where 1 BCE = year 0, 2 BCE = -1, etc.)
KALI_YUGA_START_DATETIME = datetime(
    year=1, month=1, day=1, tzinfo=pytz.utc
)  # placeholder — we treat it via decimal-year math below

# Astronomical year of the traditional Kali Yuga start
# 3102 BCE = astronomical year -3101
# We use February 18 as the canonical day.
KALI_YUGA_START_YEAR_ASTRO = -3101.13  # approximately Feb 18, -3101


# ── Helpers ──────────────────────────────────────────────────────────

def _decimal_year_astronomical(dt: datetime) -> float:
    """
    Convert a datetime to a decimal astronomical year.

    Standard Gregorian numbering: 1 BCE = -1 here (we ignore the "no year 0"
    convention because we use astronomical year numbering where 1 BCE = 0).
    For positive-year datetimes (which is all our practical inputs), this
    is just the Gregorian decimal year.
    """
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    start = datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
    end = datetime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)
    fraction = (dt - start).total_seconds() / (end - start).total_seconds()
    return dt.year + fraction


def _years_since_kali_yuga_start(dt: datetime) -> float:
    """Years elapsed since the Kali Yuga began."""
    year = _decimal_year_astronomical(dt)
    return year - KALI_YUGA_START_YEAR_ASTRO


# ── Public API ───────────────────────────────────────────────────────

def years_into_kali_yuga(dt: datetime) -> float:
    """Years since the current Kali Yuga began (Feb 18, 3102 BCE)."""
    return _years_since_kali_yuga_start(dt)


def kali_yuga_fraction(dt: datetime) -> float:
    """Position within the 432,000-year Kali Yuga, 0.0 to 1.0."""
    y = _years_since_kali_yuga_start(dt)
    return y / KALI_YUGA_YEARS


def kali_yuga_years_remaining(dt: datetime) -> float:
    """Years until the current Kali Yuga ends and a new Satya begins."""
    return KALI_YUGA_YEARS - _years_since_kali_yuga_start(dt)


def current_yuga(dt: datetime) -> dict:
    """
    Return information about the current yuga.

    In the classical reckoning we are firmly in the Kali Yuga (we are
    only ~5,000 years into a 432,000-year yuga, so ~1.2% complete).
    """
    y = _years_since_kali_yuga_start(dt)
    return {
        "yuga": "Kali Yuga",
        "yuga_sanskrit": "कलि युग",
        "yuga_duration_years": KALI_YUGA_YEARS,
        "years_elapsed": y,
        "years_remaining": KALI_YUGA_YEARS - y,
        "fraction_through": y / KALI_YUGA_YEARS,
    }


def years_into_maha_yuga(dt: datetime) -> float:
    """
    Years elapsed since the current Mahā Yuga began.

    Mahā Yuga sequence: Satya (1.728M) → Treta (1.296M) → Dvāpara (864K) → Kali (432K).
    The current Kali Yuga is the LAST quarter of the current Mahā Yuga.

    So years_into_maha_yuga = SATYA + TRETA + DVAPARA + years_into_kali.
    """
    return (
        SATYA_YUGA_YEARS
        + TRETA_YUGA_YEARS
        + DVAPARA_YUGA_YEARS
        + _years_since_kali_yuga_start(dt)
    )


def years_into_kalpa(dt: datetime) -> dict:
    """
    Return the placement of the current moment within the current Kalpa
    (Day of Brahmā = 4.32 billion years).

    In the Vaishnava tradition (Bhāgavata Purāṇa), we are in the 7th
    Manvantara (Vaivasvata Manu) of the current Kalpa (Shvetavārāha
    Kalpa, the "White Boar Kalpa"), and within that, in the 28th Mahā
    Yuga of 71. Within that Mahā Yuga, we are in the Kali Yuga.

    Returns: dict with manvantara_number, mahayuga_in_manvantara,
    manvantara_name, years_elapsed_in_kalpa.
    """
    # Standard reckoning (Vaishnava):
    # 6 complete Manvantaras + initial sandhya have passed
    # + 27 complete Maha Yugas of the 7th Manvantara
    # + Satya + Treta + Dvapara of the 28th Maha Yuga
    # + years into Kali Yuga
    years_into = (
        SATYA_YUGA_YEARS                                # initial sandhya
        + 6 * MANVANTARA_YEARS                          # 6 completed manvantaras
        + 27 * MAHA_YUGA_YEARS                          # 27 completed maha yugas of current
        + SATYA_YUGA_YEARS + TRETA_YUGA_YEARS + DVAPARA_YUGA_YEARS  # of current maha yuga
        + _years_since_kali_yuga_start(dt)              # into current Kali
    )
    return {
        "manvantara_number": 7,
        "manvantara_name": "Vaivasvata Manu",
        "manvantara_sanskrit": "वैवस्वत मनु",
        "mahayuga_number_in_manvantara": 28,
        "mahayuga_position_kali": True,  # in the Kali quarter
        "years_elapsed_in_kalpa": years_into,
        "kalpa_total_years": KALPA_YEARS,
        "fraction_through_kalpa": years_into / KALPA_YEARS,
        "kalpa_name": "Shvetavārāha Kalpa (the White Boar Kalpa)",
        "kalpa_sanskrit": "श्वेतवाराह कल्प",
    }


def get_vedic_time(dt: datetime) -> dict:
    """
    Composite vedic-time state for the orchestrator.

    Returns dict with:
      • current_yuga         — yuga name + fraction + years remaining
      • years_into_maha_yuga — float, of 4.32M
      • kalpa               — manvantara, kalpa-position info
      • constants           — the canonical year counts for reference
    """
    return {
        "current_yuga": current_yuga(dt),
        "years_into_maha_yuga": years_into_maha_yuga(dt),
        "maha_yuga_total_years": MAHA_YUGA_YEARS,
        "kalpa": years_into_kalpa(dt),
        "constants": {
            "kali_yuga_years": KALI_YUGA_YEARS,
            "dvapara_yuga_years": DVAPARA_YUGA_YEARS,
            "treta_yuga_years": TRETA_YUGA_YEARS,
            "satya_yuga_years": SATYA_YUGA_YEARS,
            "maha_yuga_years": MAHA_YUGA_YEARS,
            "manvantara_years": MANVANTARA_YEARS,
            "kalpa_years": KALPA_YEARS,
            "kali_yuga_start_year_astro": KALI_YUGA_START_YEAR_ASTRO,
        },
    }
