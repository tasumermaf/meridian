"""
Solar Key cusping window calculations.

Determines WHETHER a cusping window is active and its boundaries.
Does NOT say which Law — that's the registry's job.

[MATHEMATICAL FACT] — astronomical calculation of civil twilight windows.
"""

from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import pytz

def get_cusping_windows(dt: datetime, lat: float, lon: float, tz: str) -> dict:
    """
    Calculate Gold (sunrise) and Silver (sunset) cusping window boundaries.

    Each cusping window extends ±its own civil twilight duration around the
    solar event: Gold uses morning twilight, Silver uses evening twilight.

    Args:
        dt: Datetime to check
        lat, lon, tz: Location

    Returns:
        Dict with:
        - active: bool — whether dt falls within any cusping window
        - key: "gold", "silver", or None
        - gold_window: {start, end, event_time, radius_minutes} or None
        - silver_window: {start, end, event_time, radius_minutes} or None
    """
    timezone = pytz.timezone(tz)
    if dt.tzinfo is None:
        dt = timezone.localize(dt)
    else:
        dt = dt.astimezone(timezone)

    location = LocationInfo(latitude=lat, longitude=lon, timezone=tz)

    try:
        s = sun(location.observer, date=dt.date(), tzinfo=timezone)
        sunrise = s["sunrise"]
        sunset = s["sunset"]
        dawn = s["dawn"]
        dusk = s["dusk"]
    except (ValueError, KeyError):
        return {
            "active": False,
            "key": None,
            "gold_window": None,
            "silver_window": None,
        }

    # Each cusp uses its own twilight duration
    gold_radius_min = (sunrise - dawn).total_seconds() / 60
    silver_radius_min = (dusk - sunset).total_seconds() / 60
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
    }
