"""
Lunar elongation and phase index calculation.

Returns NUMBERS only. The phase index is looked up in the registry to get the Law.

[MATHEMATICAL FACT] — ephem-based astronomical calculations.
"""

import math
import ephem


def get_lunar_elongation(dt) -> float:
    """
    Calculate the moon's elongation (angular distance from sun) in degrees.

    Uses ecliptic longitude difference (Moon - Sun) mod 360 to produce
    an unsigned phase angle where 0 = conjunction (New Moon) and
    180 = opposition (Full Moon). This avoids the sign ambiguity of
    ephem.Moon.elong, which wraps small negative values near New Moon
    to ~358 degrees (incorrectly mapping to the Last Quarter band).

    Args:
        dt: Datetime (UTC preferred; naive assumed UTC, aware converted)

    Returns:
        Elongation in degrees, 0–360 range.
    """
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        import pytz
        dt_utc = dt.astimezone(pytz.UTC).replace(tzinfo=None)
    else:
        dt_utc = dt

    observer = ephem.Observer()
    observer.date = dt_utc

    s = ephem.Sun(observer)
    m = ephem.Moon(observer)

    # Use ecliptic longitudes for unsigned phase angle.
    # ephem.Ecliptic requires epoch; use date-of-observation for precession.
    sun_ecl = ephem.Ecliptic(s, epoch=observer.date)
    moon_ecl = ephem.Ecliptic(m, epoch=observer.date)
    elong_deg = math.degrees(float(moon_ecl.lon) - float(sun_ecl.lon)) % 360

    return elong_deg


def get_phase_index(elongation_deg: float) -> int:
    """
    Map elongation to 6-phase index (60° per phase, Cantong qi).

    The six bands are [0°, 60°), [60°, 120°), ... [300°, 360°).
    At conjunction (New Moon), the ecliptic longitude difference is
    astronomically 0° but computationally may appear as ~359.99° due
    to the modular wrap-around. Values within 6° of 360° are wrapped
    to phase 0, matching the physical reality that the Moon is at
    conjunction, not at the end of the Last Quarter band.

    The 6° threshold covers the maximum elongation change in 1 hour
    (~0.55°/hr) with generous margin. At 354°+ the Moon is within
    hours of conjunction and unambiguously in the New Moon phase.

    Returns:
        0=New Moon, 1=First Crescent, 2=First Quarter,
        3=Full Moon, 4=First Wane, 5=Last Quarter
    """
    # Handle the 0/360 wrap-around at conjunction
    if elongation_deg >= 354.0:
        return 0
    return int(elongation_deg / 60) % 6


def get_illumination(elongation_deg: float) -> float:
    """Illumination percentage from elongation."""
    return (1 - math.cos(math.radians(elongation_deg))) / 2 * 100
