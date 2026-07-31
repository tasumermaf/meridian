"""
Solar Key cusping window calculations.

Determines WHETHER a cusping window is active and its boundaries.
Does NOT say which Law — that's the registry's job.

Window shape: SYMMETRIC — each window brackets its solar event by ± the
event's own civil twilight duration. Ruled canon 2026-07-24 (R3): the
Gold/Silver Key practice is attested from source teaching (Sifu Ken Lo,
Wu Mei Chi Gung tradition) as training done AT sunrise and sunset,
20 minutes to 1 hour long — a window that contains the event, which the
symmetric bracket (~40–70 min total at mid-latitudes) matches.

[MATHEMATICAL FACT] — astronomical calculation of civil twilight windows.
[SOURCE: Wu Mei Chi Gung (Sifu Ken Lo)] — the sunrise/sunset training
window attestation. Key names and Laws are Damanhurian, from the registry.
"""

from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import (
    sunrise as _astral_sunrise,
    sunset as _astral_sunset,
    dawn as _astral_dawn,
    dusk as _astral_dusk,
)
import pytz

# Fallback radius when civil twilight is undefined (white nights: the sun
# rises and sets but never reaches 6° below the horizon). Sits inside the
# attested 20 min – 1 h practice range. ALWAYS flagged via
# twilight_undefined — absence is reportable data, never silent (B-03).
_DEFAULT_RADIUS_MIN = 30.0


def get_cusping_windows(dt: datetime, lat: float, lon: float, tz: str) -> dict:
    """
    Calculate Gold (sunrise) and Silver (sunset) cusping window boundaries.

    Each cusping window extends ±its own civil twilight duration around the
    solar event: Gold uses morning twilight, Silver uses evening twilight.
    Where twilight is undefined but the sun rises and sets (white nights),
    a flagged fallback radius applies (see _DEFAULT_RADIUS_MIN).

    Args:
        dt: Datetime to check
        lat, lon, tz: Location

    Returns:
        Dict with:
        - active: bool — whether dt falls within any cusping window
        - key: "gold", "silver", or None
        - gold_window: {start, end, event_time, radius_minutes} or None
        - silver_window: {start, end, event_time, radius_minutes} or None
        - polar_conditions: bool — True when the sun does not rise/set
        - twilight_undefined: bool — True when a fallback radius was used
    """
    timezone = pytz.timezone(tz)
    if dt.tzinfo is None:
        dt = timezone.localize(dt)
    else:
        dt = dt.astimezone(timezone)

    location = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
    observer = location.observer
    day = dt.date()

    try:
        sunrise = _astral_sunrise(observer, date=day, tzinfo=timezone)
        sunset = _astral_sunset(observer, date=day, tzinfo=timezone)
    except ValueError:
        # True polar day/night: no sunrise/sunset events exist, so no
        # cusps exist. Reported explicitly, never swallowed (B-03).
        return {
            "active": False,
            "key": None,
            "gold_window": None,
            "silver_window": None,
            "polar_conditions": True,
            "twilight_undefined": False,
        }

    twilight_undefined = False

    try:
        dawn = _astral_dawn(observer, date=day, tzinfo=timezone)
        gold_radius_min = (sunrise - dawn).total_seconds() / 60
    except ValueError:
        gold_radius_min = _DEFAULT_RADIUS_MIN
        twilight_undefined = True

    try:
        dusk = _astral_dusk(observer, date=day, tzinfo=timezone)
        silver_radius_min = (dusk - sunset).total_seconds() / 60
    except ValueError:
        silver_radius_min = _DEFAULT_RADIUS_MIN
        twilight_undefined = True

    gold_radius = timedelta(minutes=gold_radius_min)
    silver_radius = timedelta(minutes=silver_radius_min)

    gold_start = sunrise - gold_radius
    gold_end = sunrise + gold_radius
    silver_start = sunset - silver_radius
    silver_end = sunset + silver_radius

    in_gold = gold_start <= dt <= gold_end
    in_silver = silver_start <= dt <= silver_end

    def _window(start, end, event, r):
        return {
            "start": start,
            "end": end,
            "event_time": event,
            "radius_minutes": r,
        }

    active_key = None
    if in_gold:
        active_key = "gold"
    elif in_silver:
        active_key = "silver"

    return {
        "active": active_key is not None,
        "key": active_key,
        "gold_window": _window(gold_start, gold_end, sunrise, round(gold_radius_min, 1)),
        "silver_window": _window(silver_start, silver_end, sunset, round(silver_radius_min, 1)),
        "polar_conditions": False,
        "twilight_undefined": twilight_undefined,
    }
