"""
Astrolabium Caudae Rubrae — Calendar Engine.

Computes Divine Months (New Moon to New Moon), Sephirotic Week days,
and Divine Year from the determined calendar architecture.

Epoch: New Moon September 22, 1949 12:20:56 UTC
Year start: New Moon nearest to Autumn Equinox
Month cycle: 12 lunations per year, 13th = VADUSFADAHM (intercalary)
Sephirotic Week: Days named within lunar quarter-weeks (7-9 days)

[MATHEMATICAL FACT] — ephem-based astronomical calculations.
"""

import ephem
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import pytz

# Calendar epoch: Gregorian year of the first Autumn Equinox
EPOCH_YEAR = 1949


# ── Conversion helpers ──────────────────────────────────────────


def _to_utc(dt: datetime) -> datetime:
    """Convert any datetime to naive UTC."""
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        return dt.astimezone(pytz.UTC).replace(tzinfo=None)
    return dt


def _dt_to_ephem(dt: datetime) -> ephem.Date:
    """Convert Python datetime to ephem.Date (UTC)."""
    return ephem.Date(_to_utc(dt))


def _ephem_to_dt(ed: ephem.Date) -> datetime:
    """Convert ephem.Date to Python datetime (UTC naive)."""
    return ephem.Date(ed).datetime()


# ── New Moon helpers ────────────────────────────────────────────


def previous_new_moon(dt: datetime) -> datetime:
    """Most recent New Moon at or before dt."""
    return _ephem_to_dt(ephem.previous_new_moon(_dt_to_ephem(dt)))


def next_new_moon(dt: datetime) -> datetime:
    """Next New Moon after dt."""
    return _ephem_to_dt(ephem.next_new_moon(_dt_to_ephem(dt)))


# ── Year start computation ──────────────────────────────────────


def get_year_start_nm(greg_year: int) -> datetime:
    """
    Find the New Moon that starts the Divine Year anchored to a
    Gregorian year's Autumn Equinox.

    Rule: the New Moon nearest to the Autumn Equinox.
    """
    ae = _ephem_to_dt(ephem.next_autumnal_equinox(f"{greg_year}/1/1"))

    prev_nm = previous_new_moon(ae)
    nxt_nm = next_new_moon(ae)

    delta_prev = abs((ae - prev_nm).total_seconds())
    delta_next = abs((nxt_nm - ae).total_seconds())

    return prev_nm if delta_prev <= delta_next else nxt_nm


# ── Divine Year ─────────────────────────────────────────────────


def get_divine_year(dt: datetime) -> Dict:
    """
    Determine the Divine Year for a given datetime.

    Year 1 = epoch year (1949 AE). Returns year number, year start NM,
    and total month count (12 or 13).
    """
    dt_utc = _to_utc(dt)
    greg_year = dt_utc.year

    # Determine which AE anchors our year
    year_start = get_year_start_nm(greg_year)

    if dt_utc >= year_start:
        anchor_year = greg_year
    else:
        anchor_year = greg_year - 1
        year_start = get_year_start_nm(anchor_year)

    divine_year = anchor_year - EPOCH_YEAR + 1

    # Find next year's start to count lunations
    next_year_start = get_year_start_nm(anchor_year + 1)

    # Count lunations in this divine year.
    # Use a 12-hour buffer to prevent floating-point double-counting:
    # two independent ephem computations of the same NM event can differ
    # by seconds, causing the boundary NM to be counted twice.
    boundary = next_year_start - timedelta(hours=12)
    total_months = 0
    nm = year_start
    while nm < boundary:
        total_months += 1
        nm = next_new_moon(nm + timedelta(days=1))

    return {
        "year": divine_year,
        "anchor_gregorian": anchor_year,
        "year_start": year_start,
        "next_year_start": next_year_start,
        "total_months": total_months,
        "is_intercalary_year": total_months == 13,
    }


# ── Divine Month ────────────────────────────────────────────────


def get_divine_month(dt: datetime) -> Dict:
    """
    Determine the current Divine Month.

    Counts lunations from the Divine Year start NM.
    Months 1-12 are the standard sequence; Month 13 = VADUSFADAHM.

    Returns month number (1-13), month start/end, day within month.
    """
    dt_utc = _to_utc(dt)
    year_info = get_divine_year(dt_utc)
    year_start = year_info["year_start"]

    # Walk forward from year start
    month_start = year_start
    month_num = 1

    while month_num <= 13:
        month_end = next_new_moon(month_start + timedelta(days=1))

        if month_start <= dt_utc < month_end:
            break

        month_num += 1
        month_start = month_end

    if month_num > 13:
        raise RuntimeError(
            f"Calendar error: {dt_utc} fell outside all 13 months "
            f"of Divine Year starting {year_start}"
        )

    # Day within month (1-indexed, fractional days truncated)
    day_in_month = int((dt_utc - month_start).total_seconds() / 86400) + 1

    # Total days in this lunation
    total_days = round((month_end - month_start).total_seconds() / 86400)

    return {
        "month_number": month_num,
        "month_start": month_start,
        "month_end": month_end,
        "day_in_month": day_in_month,
        "total_days": total_days,
        "divine_year": year_info["year"],
        "is_intercalary": month_num == 13,
        "year_is_intercalary": year_info["is_intercalary_year"],
    }


# ── Quarter-phase computation (for Sephirotic Week) ────────────


def _get_quarter_phases(dt: datetime) -> List[Tuple[str, datetime]]:
    """
    Find the quarter-phase boundaries for the lunation containing dt.

    Returns a sorted list of (phase_name, datetime) tuples:
    [new_moon, first_quarter, full_moon, last_quarter, next_new_moon].
    """
    ed = _dt_to_ephem(dt)

    prev_nm = _ephem_to_dt(ephem.previous_new_moon(ed))
    next_nm = _ephem_to_dt(ephem.next_new_moon(ed))

    # Compute intermediate quarter phases from just after the prev NM
    after_nm = _dt_to_ephem(prev_nm + timedelta(hours=1))

    fq = _ephem_to_dt(ephem.next_first_quarter_moon(after_nm))
    fm = _ephem_to_dt(ephem.next_full_moon(after_nm))
    lq = _ephem_to_dt(ephem.next_last_quarter_moon(after_nm))

    phases = [
        ("new_moon", prev_nm),
        ("first_quarter", fq),
        ("full_moon", fm),
        ("last_quarter", lq),
        ("new_moon", next_nm),
    ]

    phases.sort(key=lambda x: x[1])
    return phases


def get_sephirotic_day(dt: datetime) -> Dict:
    """
    Determine the Sephirotic Day within the current lunar quarter-week.

    Each quarter-lunation (NM→FQ, FQ→FM, FM→LQ, LQ→NM) contains 7-9 days.
    Day 1 = Tiphareth/Sol ... Day 9 = Kether/Neptune.

    Returns day number (1-9), quarter name, quarter boundaries, and
    total days in the quarter.
    """
    dt_utc = _to_utc(dt)
    phases = _get_quarter_phases(dt_utc)

    quarter_start = None
    quarter_end = None
    quarter_name = None
    quarter_index = 0

    for i in range(len(phases) - 1):
        if phases[i][1] <= dt_utc < phases[i + 1][1]:
            quarter_start = phases[i][1]
            quarter_end = phases[i + 1][1]
            quarter_name = phases[i][0]
            quarter_index = i
            break

    if quarter_start is None:
        # Fallback to first quarter
        quarter_start = phases[0][1]
        quarter_end = phases[1][1]
        quarter_name = phases[0][0]

    # Day number within the quarter (1-indexed)
    days_elapsed = (dt_utc - quarter_start).total_seconds() / 86400
    day_number = int(days_elapsed) + 1

    # Clamp to 1-9
    day_number = max(1, min(9, day_number))

    # Total days in this quarter
    quarter_days = round((quarter_end - quarter_start).total_seconds() / 86400)

    return {
        "day": day_number,
        "quarter": quarter_name,
        "quarter_index": quarter_index,
        "quarter_start": quarter_start,
        "quarter_end": quarter_end,
        "quarter_days": quarter_days,
    }
