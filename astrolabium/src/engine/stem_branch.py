"""
Stem-Branch calculations: daily cycle, hourly stem, LGBF substitution, organ clock branch.

Pure TCM calendrical math. No Law names, no interpretive content.
The vessel remainder→name mapping is TCM canonical and stays here.
The vessel→Law mapping does NOT — that comes from the registry.

[SOURCE: TCM] — Traditional stem-branch calendar system.
[SOURCE: O3R Ch.4] — LGBF substitution tables.
"""

from datetime import datetime, date, timedelta
from typing import Dict
import pytz

from .solar import get_solar_positions


# ── Heavenly Stems (天干) ──

HEAVENLY_STEMS = [
    {"chinese": "甲", "pinyin": "Jiǎ",  "index": 0, "element": "Wood",  "yin_yang": "Yang"},
    {"chinese": "乙", "pinyin": "Yǐ",   "index": 1, "element": "Wood",  "yin_yang": "Yin"},
    {"chinese": "丙", "pinyin": "Bǐng", "index": 2, "element": "Fire",  "yin_yang": "Yang"},
    {"chinese": "丁", "pinyin": "Dīng", "index": 3, "element": "Fire",  "yin_yang": "Yin"},
    {"chinese": "戊", "pinyin": "Wù",   "index": 4, "element": "Earth", "yin_yang": "Yang"},
    {"chinese": "己", "pinyin": "Jǐ",   "index": 5, "element": "Earth", "yin_yang": "Yin"},
    {"chinese": "庚", "pinyin": "Gēng", "index": 6, "element": "Metal", "yin_yang": "Yang"},
    {"chinese": "辛", "pinyin": "Xīn",  "index": 7, "element": "Metal", "yin_yang": "Yin"},
    {"chinese": "壬", "pinyin": "Rén",  "index": 8, "element": "Water", "yin_yang": "Yang"},
    {"chinese": "癸", "pinyin": "Guǐ",  "index": 9, "element": "Water", "yin_yang": "Yin"},
]

# ── Earthly Branches (地支) ──

EARTHLY_BRANCHES = [
    {"chinese": "子", "pinyin": "Zǐ",   "index": 0,  "animal": "Rat"},
    {"chinese": "丑", "pinyin": "Chǒu", "index": 1,  "animal": "Ox"},
    {"chinese": "寅", "pinyin": "Yín",  "index": 2,  "animal": "Tiger"},
    {"chinese": "卯", "pinyin": "Mǎo",  "index": 3,  "animal": "Rabbit"},
    {"chinese": "辰", "pinyin": "Chén", "index": 4,  "animal": "Dragon"},
    {"chinese": "巳", "pinyin": "Sì",   "index": 5,  "animal": "Snake"},
    {"chinese": "午", "pinyin": "Wǔ",   "index": 6,  "animal": "Horse"},
    {"chinese": "未", "pinyin": "Wèi",  "index": 7,  "animal": "Goat"},
    {"chinese": "申", "pinyin": "Shēn", "index": 8,  "animal": "Monkey"},
    {"chinese": "酉", "pinyin": "Yǒu",  "index": 9,  "animal": "Rooster"},
    {"chinese": "戌", "pinyin": "Xū",   "index": 10, "animal": "Dog"},
    {"chinese": "亥", "pinyin": "Hài",  "index": 11, "animal": "Pig"},
]


# ── LGBF Substitution Tables [SOURCE: O3R Ch.4] ──

DAILY_STEM_SUB = {0: 10, 1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 9, 7: 8, 8: 7, 9: 6}
DAILY_BRANCH_SUB = {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 9, 7: 8, 8: 7, 9: 6, 10: 5, 11: 4}
HOURLY_STEM_SUB = DAILY_STEM_SUB  # Same table
HOURLY_BRANCH_SUB = {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, 9: 9, 10: 8, 11: 7}

# ── TCM Canonical: LGBF remainder → Vessel Name ──
# This mapping is TCM-canonical (not interpretive). It stays in the engine.
VESSEL_REMAINDER_MAP = {
    1: "Yang Qiao Mai",
    2: "Yin Qiao Mai",
    3: "Yang Wei Mai",
    4: "Dai Mai",
    5: "Yin Qiao Mai",
    6: "Chong Mai",
    7: "Du Mai",
    8: "Yin Wei Mai",
    9: "Ren Mai",
}

# Reference date: January 1, 2000 = 戊午 (Wù Wǔ) — stem 4, branch 6
_REF_DATE = date(2000, 1, 1)
_REF_STEM = 4
_REF_BRANCH = 6
_REF_SEXAGENARY = 54


def get_daily_stem_branch(dt) -> Dict:
    """
    Daily Heavenly Stem and Earthly Branch from the 60-day sexagenary cycle.

    DATE-ONLY calculation. No location required.
    """
    target = dt.date() if isinstance(dt, datetime) else dt
    days_diff = (target - _REF_DATE).days

    stem_idx = (_REF_STEM + days_diff) % 10
    branch_idx = (_REF_BRANCH + days_diff) % 12
    sexagenary = (_REF_SEXAGENARY + days_diff) % 60

    return {
        "date": target.isoformat(),
        "stem_index": stem_idx,
        "stem_chinese": HEAVENLY_STEMS[stem_idx]["chinese"],
        "stem_pinyin": HEAVENLY_STEMS[stem_idx]["pinyin"],
        "stem_element": HEAVENLY_STEMS[stem_idx]["element"],
        "branch_index": branch_idx,
        "branch_chinese": EARTHLY_BRANCHES[branch_idx]["chinese"],
        "branch_pinyin": EARTHLY_BRANCHES[branch_idx]["pinyin"],
        "branch_animal": EARTHLY_BRANCHES[branch_idx]["animal"],
        "sexagenary_index": sexagenary,
        "is_yang_day": stem_idx % 2 == 0,
    }


def get_hourly_stem(day_stem_index: int, hour_branch_index: int) -> int:
    """
    Five Rat Rule (五鼠遁): hourly stem from daily stem + hourly branch.

    Returns:
        Hourly stem index (0-9).
    """
    first_zi = ((day_stem_index % 5) * 2) % 10
    return (first_zi + hour_branch_index) % 10


def get_lgbf_substitution(
    day_stem_idx: int,
    day_branch_idx: int,
    hour_stem_idx: int,
    hour_branch_idx: int,
) -> Dict:
    """
    LGBF substitution numbers and their sum.

    Returns dict with day_stem_num, day_branch_num, hour_stem_num,
    hour_branch_num, and sum.
    """
    ds = DAILY_STEM_SUB[day_stem_idx]
    db = DAILY_BRANCH_SUB[day_branch_idx]
    hs = HOURLY_STEM_SUB[hour_stem_idx]
    hb = HOURLY_BRANCH_SUB[hour_branch_idx]
    return {
        "day_stem_num": ds,
        "day_branch_num": db,
        "hour_stem_num": hs,
        "hour_branch_num": hb,
        "sum": ds + db + hs + hb,
    }


def get_earthly_branch_from_solar(dt: datetime, lat: float, lon: float, tz: str) -> int:
    """
    Determine the current Earthly Branch index from solar position.

    The 12 branches divide the 24-hour cycle starting from solar midnight.
    Each branch covers 2 solar hours.

    Args:
        dt: Current datetime (naive or aware)
        lat, lon, tz: Location

    Returns:
        Branch index 0–11.
    """
    timezone = pytz.timezone(tz)
    if dt.tzinfo is None:
        dt = timezone.localize(dt)
    else:
        dt = dt.astimezone(timezone)

    solar = get_solar_positions(dt, lat, lon, tz)
    midnight = solar["solar_midnight"]

    # If before today's solar midnight, use yesterday's
    if dt < midnight:
        yesterday = dt - timedelta(days=1)
        solar_y = get_solar_positions(yesterday, lat, lon, tz)
        midnight = solar_y["solar_midnight"]

    elapsed_hours = (dt - midnight).total_seconds() / 3600
    return int(elapsed_hours / 2) % 12


def get_lgbf_remainder(dt: datetime, lat: float, lon: float, tz: str) -> Dict:
    """
    Full LGBF calculation: stem-branch + solar position → vessel remainder.

    Returns dict with remainder, vessel_name, is_yang_day, divisor,
    and full calculation details.
    """
    daily = get_daily_stem_branch(dt)
    hour_branch_idx = get_earthly_branch_from_solar(dt, lat, lon, tz)
    hour_stem_idx = get_hourly_stem(daily["stem_index"], hour_branch_idx)

    subs = get_lgbf_substitution(
        daily["stem_index"], daily["branch_index"],
        hour_stem_idx, hour_branch_idx,
    )

    is_yang = daily["is_yang_day"]
    divisor = 9 if is_yang else 6
    remainder = subs["sum"] % divisor
    if remainder == 0:
        remainder = divisor

    vessel_name = VESSEL_REMAINDER_MAP[remainder]

    return {
        "remainder": remainder,
        "vessel_name": vessel_name,
        "is_yang_day": is_yang,
        "divisor": divisor,
        "daily_stem_index": daily["stem_index"],
        "daily_branch_index": daily["branch_index"],
        "hour_stem_index": hour_stem_idx,
        "hour_branch_index": hour_branch_idx,
        "substitution_sum": subs["sum"],
        "substitution": subs,
    }
