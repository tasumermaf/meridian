"""
Solar position calculations for the Astrolabium.

Foundation for ALL hourly calculations. Sunrise/sunset at practitioner's
location determines the temporal substrate for Organ Clock, Divine Hours,
LGBF hourly branch, and Solar Key cusping windows.

[MATHEMATICAL FACT] — deterministic outputs from astronomical algorithms.
"""

from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import pytz


def get_solar_positions(dt: datetime, lat: float, lon: float, tz: str) -> dict:
    """
    Calculate sunrise, sunset, noon, and midnight for a given location and date.

    Args:
        dt: Datetime for calculation (date portion used)
        lat: Latitude
        lon: Longitude
        tz: Timezone name (e.g., 'US/Eastern')

    Returns:
        Dict with 'sunrise', 'sunset', 'solar_noon', 'solar_midnight'
        (all timezone-aware datetimes)
    """
    location = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
    timezone = pytz.timezone(tz)

    try:
        s = sun(location.observer, date=dt.date(), tzinfo=timezone)
        sunrise = s["sunrise"]
        sunset = s["sunset"]
        solar_noon = s["noon"]
    except ValueError as e:
        # Polar day/night — the sun never rises or never sets.
        # Raising explicitly rather than producing a fake 12-hour day.
        # The caller (API layer) catches this and returns a structured
        # polar-condition response.
        raise ValueError(
            f"Polar conditions at lat={lat}, lon={lon} on {dt.date()}: {e}. "
            f"Solar-position-based calculations require distinct sunrise and sunset events."
        )

    # Solar midnight: halfway between today's sunset and tomorrow's sunrise
    try:
        next_day = dt.date() + timedelta(days=1)
        s_next = sun(location.observer, date=next_day, tzinfo=timezone)
        solar_midnight = sunset + (s_next["sunrise"] - sunset) / 2
    except Exception:
        solar_midnight = solar_noon + timedelta(hours=12)

    return {
        "sunrise": sunrise,
        "sunset": sunset,
        "solar_noon": solar_noon,
        "solar_midnight": solar_midnight,
    }


def get_daylight_duration(dt: datetime, lat: float, lon: float, tz: str) -> float:
    """Duration of daylight in decimal hours."""
    pos = get_solar_positions(dt, lat, lon, tz)
    return (pos["sunset"] - pos["sunrise"]).total_seconds() / 3600


def get_solar_hour_duration(
    dt: datetime, lat: float, lon: float, tz: str, is_day: bool = True
) -> float:
    """Duration of one unequal hour (1/12 of day or night) in decimal hours."""
    daylight = get_daylight_duration(dt, lat, lon, tz)
    return daylight / 12 if is_day else (24 - daylight) / 12


def get_civil_twilight_duration(dt: datetime, lat: float, lon: float, tz: str) -> float:
    """
    Civil twilight duration in minutes.

    Civil twilight = sun between 0° and 6° below horizon.
    Returns the average of morning and evening durations.
    """
    location = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
    timezone = pytz.timezone(tz)

    try:
        s = sun(location.observer, date=dt.date(), tzinfo=timezone)
        morning = (s["sunrise"] - s["dawn"]).total_seconds() / 60
        evening = (s["dusk"] - s["sunset"]).total_seconds() / 60
        return (morning + evening) / 2
    except (ValueError, KeyError):
        return 30.0  # Polar regions fallback
