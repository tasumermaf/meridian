"""
Solar position calculations for the Astrolabium.

Foundation for ALL hourly calculations. Sunrise/sunset at practitioner's
location determines the temporal substrate for Organ Clock, Divine Hours,
LGBF hourly branch, and Solar Key cusping windows.

[MATHEMATICAL FACT] — deterministic outputs from astronomical algorithms.
"""

from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sunrise as _astral_sunrise, sunset as _astral_sunset, noon as _astral_noon
import pytz


def get_solar_positions(dt: datetime, lat: float, lon: float, tz: str) -> dict:
    """
    Calculate sunrise, sunset, noon, and midnight for a given location and date.

    Sunrise, sunset, and noon are computed via INDIVIDUAL astral calls
    (AUDIT_2026-07-24 B-02): the bundled sun() call also computes civil
    dawn/dusk, which fail at white-nights latitudes (~61–66.5°N summer)
    where the sun genuinely rises and sets — bundling made the whole
    engine refuse service there. True polar day/night still raises
    ValueError with a structured message.

    Args:
        dt: Datetime for calculation (date portion used)
        lat: Latitude
        lon: Longitude
        tz: Timezone name (e.g., 'US/Eastern')

    Returns:
        Dict with 'sunrise', 'sunset', 'solar_noon', 'solar_midnight'
        (all timezone-aware datetimes) plus 'solar_midnight_approximate'
        (bool — True when tomorrow's sunrise was unavailable and midnight
        fell back to noon + 12h; flagged per C-04, never silent).
    """
    location = LocationInfo(latitude=lat, longitude=lon, timezone=tz)
    timezone = pytz.timezone(tz)
    observer = location.observer
    day = dt.date()

    try:
        sunrise = _astral_sunrise(observer, date=day, tzinfo=timezone)
        sunset = _astral_sunset(observer, date=day, tzinfo=timezone)
        solar_noon = _astral_noon(observer, date=day, tzinfo=timezone)
    except ValueError as e:
        # Polar day/night — the sun never rises or never sets.
        # Raising explicitly rather than producing a fake 12-hour day.
        # The caller (API layer) catches this and returns a structured
        # polar-condition response.
        raise ValueError(
            f"Polar conditions at lat={lat}, lon={lon} on {day}: {e}. "
            f"Solar-position-based calculations require distinct sunrise and sunset events."
        )

    # Solar midnight: halfway between today's sunset and tomorrow's sunrise.
    midnight_approximate = False
    try:
        next_sunrise = _astral_sunrise(
            observer, date=day + timedelta(days=1), tzinfo=timezone
        )
        solar_midnight = sunset + (next_sunrise - sunset) / 2
    except ValueError:
        # Polar-transition edge: tomorrow's sunrise does not exist.
        # Approximation is FLAGGED, never silent (C-04).
        solar_midnight = solar_noon + timedelta(hours=12)
        midnight_approximate = True

    return {
        "sunrise": sunrise,
        "sunset": sunset,
        "solar_noon": solar_noon,
        "solar_midnight": solar_midnight,
        "solar_midnight_approximate": midnight_approximate,
    }


def get_daylight_duration(dt: datetime, lat: float, lon: float, tz: str) -> float:
    """Duration of daylight in decimal hours."""
    pos = get_solar_positions(dt, lat, lon, tz)
    return (pos["sunset"] - pos["sunrise"]).total_seconds() / 3600
