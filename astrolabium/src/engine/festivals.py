"""
Cross-tradition sacred festival registry engine.

Resolves festival dates per anchor type:

  solar_date              — fixed Gregorian month + day (e.g., Divine Marriage May 24)
  solar_term              — anchored to one of the 24 Chinese solar terms
  lunar_month_day         — Chinese lunisolar (e.g., Mid-Autumn = 8/15)
  tibetan_lunar_month_full — Tibetan calendar (Phugpa) lunar month + day reference
  tibetan_lunar_month_range — entire Tibetan lunar month (e.g., Saga Dawa)
  computed                — rule-based luni-solar (e.g., Easter, Diwali) — currently
                            uses approximate window; can be refined later
  fixed_window            — known approximate Gregorian window

For "computed" anchors we use the gregorian_window approximation as the
practical date range. Precise canonical computation (Paschal full moon
algorithm, Hindu Vedic calendar arithmetic, etc.) is intentionally
deferred to a follow-up sprint — the current implementation is honest
about its approximation by exposing the window directly.

[SOURCE: per-festival; see sacred_festivals.json]
[ANALYTICAL CONTRIBUTION: the multi-tradition registry design itself]
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import ephem
import pytz

from . import solar_terms


# ── Data loading ─────────────────────────────────────────────────────

_FESTIVAL_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "sacred_festivals.json"
_FESTIVAL_DATA: Optional[dict] = None


def _load_festival_data() -> dict:
    global _FESTIVAL_DATA
    if _FESTIVAL_DATA is None:
        with open(_FESTIVAL_DATA_PATH, "r", encoding="utf-8") as f:
            _FESTIVAL_DATA = json.load(f)
    return _FESTIVAL_DATA


def _normalize_to_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt


# ── Date resolution per anchor type ──────────────────────────────────

def _resolve_solar_date(festival: dict, year: int) -> Optional[datetime]:
    """Solar date anchor: fixed Gregorian month + day."""
    month = festival["anchor_data"]["month"]
    day = festival["anchor_data"]["day"]
    try:
        return pytz.utc.localize(datetime(year, month, day, 12, 0))
    except ValueError:
        # Feb 29 in non-leap year etc.
        return None


def _resolve_solar_term(festival: dict, year: int) -> Optional[datetime]:
    """Solar term anchor: find the Gregorian datetime when the named term begins."""
    target_pinyin = festival["anchor_data"]["term_pinyin"]
    target = None
    for t in solar_terms.list_terms():
        if t["pinyin"] == target_pinyin:
            target = t
            break
    if target is None:
        return None
    target_lon = target["ecliptic_longitude_deg"]
    # Find when the Sun's tropical longitude next crosses target_lon during `year`.
    start = pytz.utc.localize(datetime(year, 1, 1, 0, 0))
    end = pytz.utc.localize(datetime(year + 1, 1, 1, 0, 0))
    return _find_solar_longitude_crossing(start, end, target_lon)


def _resolve_lunar_month_day(festival: dict, year: int) -> Optional[datetime]:
    """
    Chinese lunisolar anchor: Nth day of the Mth lunar month.

    Chinese lunar months begin at New Moon. The first lunar month begins
    at the New Moon nearest Lìchūn (Beginning of Spring, ~Feb 4). The
    Nth day of the Mth month is N-1 days after the start of that month.

    NOTE: This is a simplified approximation that ignores intercalary
    months. Sufficient for typical festival lookup; not for full calendar
    arithmetic.
    """
    target_month = festival["anchor_data"]["lunar_month"]
    target_day = festival["anchor_data"]["lunar_day"]
    # First lunar month: New Moon nearest Lìchūn (Feb 4 ± a few days)
    lichun_date = pytz.utc.localize(datetime(year, 2, 4, 0, 0))
    nm1 = _find_nearest_new_moon(lichun_date)
    # March forward N-1 lunations to reach the target month start
    target_month_start = _add_lunations(nm1, target_month - 1)
    # Day N is (N-1) days after the month start
    return target_month_start + timedelta(days=target_day - 1)


def _resolve_tibetan_lunar_month(festival: dict, year: int) -> Optional[datetime]:
    """
    Tibetan calendar anchor (Phugpa). The Tibetan first month (Losar)
    begins at a specific New Moon — by Phugpa rule, the first new moon
    after Magha (Indian month, ~late January / February).

    Practical approximation: Tibetan month M begins ~(M-1) lunations
    after Losar; Losar typically falls between Feb 5 and Mar 5.

    For Saga Dawa (month 4), this places it in May/June — matching
    documented dates (May 17 - June 14, 2026 per Mama Food Forest text).
    """
    target_month = festival["anchor_data"]["tibetan_month"]
    day_spec = festival["anchor_data"].get("day", None)
    # Losar approximate anchor: first New Moon after Feb 10 (covers Phugpa)
    feb_anchor = pytz.utc.localize(datetime(year, 2, 10, 0, 0))
    losar_nm = _find_next_new_moon(feb_anchor)
    target_month_start = _add_lunations(losar_nm, target_month - 1)

    if day_spec == "full_moon":
        return _find_next_full_moon(target_month_start)
    elif day_spec == "first":
        return target_month_start
    else:
        # Default: return the new moon (start of month)
        return target_month_start


def _resolve_tibetan_lunar_month_range(festival: dict, year: int) -> tuple:
    """Return (start, end) for the full Tibetan lunar month."""
    target_month = festival["anchor_data"]["tibetan_month"]
    feb_anchor = pytz.utc.localize(datetime(year, 2, 10, 0, 0))
    losar_nm = _find_next_new_moon(feb_anchor)
    month_start = _add_lunations(losar_nm, target_month - 1)
    month_end = _add_lunations(losar_nm, target_month)
    return (month_start, month_end)


def _resolve_computed_window(festival: dict, year: int) -> Optional[datetime]:
    """
    Approximate anchor: use the midpoint of the documented Gregorian
    window. Refinement (e.g., true Paschal full moon) deferred to a
    follow-up sprint.
    """
    window = festival["anchor_data"].get("gregorian_window", "")
    if not window or "varies" in window.lower():
        return None
    # Parse "Mar 22 - Apr 25" style windows
    try:
        parts = window.split(" - ")
        if len(parts) != 2:
            return None
        start_str, end_str = parts
        start = _parse_month_day_str(start_str, year)
        end = _parse_month_day_str(end_str, year)
        if start and end:
            mid = start + (end - start) / 2
            return mid
    except Exception:
        pass
    return None


def _parse_month_day_str(s: str, year: int) -> Optional[datetime]:
    """Parse 'Mar 22' style strings into a UTC datetime."""
    s = s.strip()
    months = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }
    parts = s.split()
    if len(parts) < 2:
        return None
    month_name = parts[0]
    if month_name not in months:
        return None
    try:
        day = int(parts[1])
        return pytz.utc.localize(datetime(year, months[month_name], day, 12, 0))
    except (ValueError, IndexError):
        return None


# ── Astronomical helpers ─────────────────────────────────────────────

def _find_next_new_moon(after: datetime) -> datetime:
    """Find the next astronomical New Moon strictly after `after`."""
    obs = ephem.Date(after.astimezone(pytz.utc).replace(tzinfo=None))
    nm = ephem.next_new_moon(obs)
    return pytz.utc.localize(nm.datetime())


def _find_nearest_new_moon(near: datetime) -> datetime:
    """Find the New Moon nearest to `near` (could be before or after)."""
    obs = ephem.Date(near.astimezone(pytz.utc).replace(tzinfo=None))
    prev_nm = ephem.previous_new_moon(obs)
    next_nm = ephem.next_new_moon(obs)
    near_eph = obs
    if abs(float(near_eph) - float(prev_nm)) <= abs(float(next_nm) - float(near_eph)):
        return pytz.utc.localize(prev_nm.datetime())
    return pytz.utc.localize(next_nm.datetime())


def _find_next_full_moon(after: datetime) -> datetime:
    """Find the next astronomical Full Moon strictly after `after`."""
    obs = ephem.Date(after.astimezone(pytz.utc).replace(tzinfo=None))
    fm = ephem.next_full_moon(obs)
    return pytz.utc.localize(fm.datetime())


def _add_lunations(dt: datetime, n: int) -> datetime:
    """Add n synodic lunations (~29.5306 days each) to a datetime."""
    # For precision, find the Nth next new moon
    if n == 0:
        return dt
    cur = dt
    for _ in range(n):
        cur = _find_next_new_moon(cur)
    return cur


def _find_solar_longitude_crossing(start: datetime, end: datetime, target_lon: float) -> Optional[datetime]:
    """Find when the Sun's tropical longitude crosses `target_lon` within window."""
    import math
    cur = start
    prev_lon = _sun_lon(cur)
    step = timedelta(hours=6)
    while cur < end:
        cur += step
        new_lon = _sun_lon(cur)
        if _crossed_target(prev_lon, new_lon, target_lon):
            # Bisect to refine
            lo, hi = cur - step, cur
            for _ in range(30):
                mid = lo + (hi - lo) / 2
                mid_lon = _sun_lon(mid)
                if _crossed_target(prev_lon, mid_lon, target_lon):
                    hi = mid
                else:
                    lo = mid
                    prev_lon = mid_lon
                if (hi - lo).total_seconds() < 60:
                    break
            return hi
        prev_lon = new_lon
    return None


def _sun_lon(dt: datetime) -> float:
    """Sun's tropical ecliptic longitude in degrees."""
    import math
    dt_utc = dt.astimezone(pytz.utc)
    obs = ephem.Date(dt_utc.replace(tzinfo=None))
    s = ephem.Sun()
    s.compute(obs)
    return math.degrees(float(ephem.Ecliptic(s).lon)) % 360.0


def _crossed_target(prev_lon: float, cur_lon: float, target: float) -> bool:
    prev_offset = (prev_lon - target) % 360.0
    cur_offset = (cur_lon - target) % 360.0
    return prev_offset > 350.0 and cur_offset < 10.0


# ── Main API ─────────────────────────────────────────────────────────

def resolve_festival(festival_id: str, year: int) -> Optional[dict]:
    """
    Resolve a single festival's date for a given year.

    Returns:
        dict with festival metadata + 'start_datetime' and 'end_datetime'
        keys (both UTC), or None if the festival cannot be resolved
        for this year (e.g., computational window unknown).
    """
    data = _load_festival_data()
    festival = next((f for f in data["festivals"] if f["id"] == festival_id), None)
    if festival is None:
        return None
    return _resolve_one(festival, year)


def _resolve_one(festival: dict, year: int) -> Optional[dict]:
    """Dispatch on anchor_type."""
    anchor_type = festival["anchor_type"]
    duration_days = festival.get("duration_days", 1)

    if anchor_type == "solar_date":
        start = _resolve_solar_date(festival, year)
    elif anchor_type == "solar_term":
        start = _resolve_solar_term(festival, year)
    elif anchor_type == "lunar_month_day":
        start = _resolve_lunar_month_day(festival, year)
    elif anchor_type == "tibetan_lunar_month_full":
        start = _resolve_tibetan_lunar_month(festival, year)
    elif anchor_type == "tibetan_lunar_month_range":
        rng = _resolve_tibetan_lunar_month_range(festival, year)
        start, end = rng
        return {
            **festival,
            "year": year,
            "start_datetime": start,
            "end_datetime": end,
        }
    elif anchor_type == "computed":
        start = _resolve_computed_window(festival, year)
    elif anchor_type == "fixed_window":
        start = _resolve_computed_window(festival, year)
    else:
        return None

    if start is None:
        return None

    end = start + timedelta(days=duration_days)
    return {
        **festival,
        "year": year,
        "start_datetime": start,
        "end_datetime": end,
    }


def get_festival_proximity(dt: datetime, window_days: int = 14) -> list:
    """
    Return all festivals whose start_datetime falls within ±window_days
    of `dt`, sorted by proximity (closest first).

    For festivals that span a range (e.g., Saga Dawa), include them if
    `dt` falls inside the range OR within `window_days` of either end.

    Performance: only resolves festivals for years whose calendar could
    plausibly produce a date within the window. For small windows
    (≤30 days), the current year is enough; only enlarges the year
    search when dt is near a year boundary.
    """
    dt = _normalize_to_aware(dt)
    data = _load_festival_data()
    nearby = []
    window = timedelta(days=window_days)

    # Determine which years to resolve. The current year always.
    # Add the previous year only if dt is within (window + 14 days) of Jan 1.
    # Add the next year only if dt is within (window + 14 days) of Dec 31.
    # The +14 buffer handles festivals that can land up to 2 weeks into
    # the neighboring calendar year (e.g., Chinese New Year in mid-Feb).
    years_to_check = [dt.year]
    boundary_buffer = timedelta(days=window_days + 14)
    year_start = pytz.utc.localize(datetime(dt.year, 1, 1))
    year_end = pytz.utc.localize(datetime(dt.year, 12, 31, 23, 59))
    if dt - year_start < boundary_buffer:
        years_to_check.append(dt.year - 1)
    if year_end - dt < boundary_buffer:
        years_to_check.append(dt.year + 1)

    for year in years_to_check:
        for festival in data["festivals"]:
            resolved = _resolve_one(festival, year)
            if resolved is None:
                continue
            start = resolved["start_datetime"]
            end = resolved["end_datetime"]
            if start - window <= dt <= end + window:
                if start <= dt <= end:
                    distance = timedelta(0)
                    status = "active"
                elif dt < start:
                    distance = start - dt
                    status = "upcoming"
                else:
                    distance = dt - end
                    status = "past"
                nearby.append({
                    **resolved,
                    "distance_days": distance.days + distance.seconds / 86400,
                    "status": status,
                })

    nearby.sort(key=lambda f: (f["distance_days"]))
    seen = set()
    deduped = []
    for f in nearby:
        if f["id"] in seen:
            continue
        seen.add(f["id"])
        deduped.append(f)
    return deduped


# ── Tibetan calendar API ─────────────────────────────────────────────

# Tibetan month names (Phugpa). Standard 12-month sequence; intercalary
# months exist but are handled implicitly by the lunation-counting logic.
TIBETAN_MONTH_NAMES = [
    ("Dawa Dangpo",       "ཟླ་བ་དང་པོ་",     "First Month (Mchu)"),
    ("Dawa Nyipa",        "ཟླ་བ་གཉིས་པ་",     "Second Month (Dbo)"),
    ("Dawa Sumpa",        "ཟླ་བ་གསུམ་པ་",     "Third Month (Nag-pa)"),
    ("Dawa Zhipa",        "ཟླ་བ་བཞི་པ་",      "Fourth Month — Saga Dawa"),
    ("Dawa Ngapa",        "ཟླ་བ་ལྔ་པ་",       "Fifth Month (Snron)"),
    ("Dawa Drukpa",       "ཟླ་བ་དྲུག་པ་",      "Sixth Month (Chu-stod)"),
    ("Dawa Dunpa",        "ཟླ་བ་བདུན་པ་",     "Seventh Month (Gro-bzhin)"),
    ("Dawa Gyepa",        "ཟླ་བ་བརྒྱད་པ་",    "Eighth Month (Khrums)"),
    ("Dawa Gupa",         "ཟླ་བ་དགུ་པ་",      "Ninth Month (Tha-skar)"),
    ("Dawa Chupa",        "ཟླ་བ་བཅུ་པ་",      "Tenth Month (Smin-drug)"),
    ("Dawa Chu Chigpa",   "ཟླ་བ་བཅུ་གཅིག་པ་", "Eleventh Month (Mgo)"),
    ("Dawa Chu Nyipa",    "ཟླ་བ་བཅུ་གཉིས་པ་", "Twelfth Month (Rgyal)"),
]


def get_tibetan_month(dt: datetime) -> dict:
    """
    Return the Tibetan lunar month containing the given datetime.

    Uses Phugpa reckoning (the most widely-used Tibetan calendar variant).
    The first Tibetan month begins at the first New Moon after Feb 10 of
    the same Gregorian year (Losar/Tibetan New Year typically falls
    between mid-February and early March).

    Note: this is a practical approximation that treats months as
    consecutive lunations. The full Phugpa system handles skipped and
    doubled days that affect calendar-display ordering but do not affect
    which lunar month a given moment falls in.

    Returns dict with:
      - month_number (1-12; 13 for intercalary if applicable)
      - month_name_transliteration / month_name_tibetan / month_name_english
      - month_start (UTC datetime, New Moon)
      - month_end (UTC datetime, next New Moon)
      - is_saga_dawa (bool — convenience flag for Tibetan month 4)
    """
    dt = _normalize_to_aware(dt)

    # Find the Losar for the calendar year. If dt is before this year's Losar,
    # we're actually in the previous year's Tibetan calendar.
    year = dt.year
    feb_anchor = pytz.utc.localize(datetime(year, 2, 10, 0, 0))
    losar = _find_next_new_moon(feb_anchor)

    if dt < losar:
        # Use previous year's Losar
        year -= 1
        feb_anchor = pytz.utc.localize(datetime(year, 2, 10, 0, 0))
        losar = _find_next_new_moon(feb_anchor)

    # Walk lunations from Losar to find which month dt is in
    cur_start = losar
    for month_idx in range(13):  # support up to 13 lunations (intercalary years)
        cur_end = _find_next_new_moon(cur_start + timedelta(hours=1))
        if cur_start <= dt < cur_end:
            month_number = month_idx + 1
            if month_number <= 12:
                name = TIBETAN_MONTH_NAMES[month_idx]
            else:
                name = ("Intercalary", "ཟླ་བཤོལ་", "Intercalary Month")
            return {
                "month_number": month_number,
                "month_name_transliteration": name[0],
                "month_name_tibetan": name[1],
                "month_name_english": name[2],
                "month_start": cur_start,
                "month_end": cur_end,
                "is_saga_dawa": (month_number == 4),
                "tibetan_year": year,
                "losar_datetime": losar,
            }
        cur_start = cur_end

    # Should be unreachable
    raise RuntimeError(
        f"Could not locate Tibetan month for {dt}. This indicates a bug."
    )


# ── Introspection ────────────────────────────────────────────────────

def get_festival_count() -> int:
    return len(_load_festival_data()["festivals"])


def list_festivals() -> list:
    return _load_festival_data()["festivals"]
