"""
Axial precession engine.

The Earth's rotational axis precesses with a period of ~25,772 years
(the Great Year of Plato). This slow conic motion causes:

  • The vernal equinox to drift westward against the stellar
    background at ~50.29 arcseconds per year.
  • The "Pole Star" to change over millennia (Polaris now,
    Thuban c. 3000 BCE, Vega in c. 14000 CE).
  • The 12 "Ages" of the precessional cycle — each ~2,148 years —
    each named for the constellation against which the spring
    equinox rises (currently the Age of Pisces, transitioning to
    the Age of Aquarius).

This engine exposes:

  • current_ayanamsa(dt)             — Lahiri ayanamsa in degrees
  • current_age(dt)                  — which zodiacal Age we're in
  • equinox_position(dt)             — sidereal RA/longitude of vernal equinox
  • next_age_transition(dt)          — when the equinox moves to the next sign
  • next_pole_star(dt, years_ahead)  — projection of which star is closest to the pole

The 12 Ages are approximate — the exact moment of "transition" between
ages is a matter of convention (which constellation boundaries to use,
which star's heliacal rising to anchor on, etc.). We use the IAU
constellation boundaries projected back to the ecliptic.

[MATHEMATICAL FACT] — axial precession rate and direction.
[SOURCE: classical astronomy] — the 12-Age framing is Mediterranean
(Hellenistic through modern Theosophical). Other traditions (Vedic,
Mesoamerican) use different precessional frames; those are not
implemented here.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pytz

# Reuse the ayanamsa computation from stellar.py for consistency
from . import stellar as _stellar


# ── Constants ────────────────────────────────────────────────────────

# Precession constants
PRECESSION_PERIOD_YEARS = 25772.0          # the Great Year (Plato)
PRECESSION_RATE_ARCSEC_PER_YEAR = 50.29    # standard astronomical value
AGE_DURATION_YEARS = PRECESSION_PERIOD_YEARS / 12.0  # ~2147.7 years

# The 12 Ages, indexed by the sidereal zodiac sign at which the vernal
# equinox is currently rising. Ordered by the direction of precession
# (westward through the zodiac — Aries → Pisces → Aquarius → ...).
#
# Sidereal-longitude ranges follow the Lahiri convention with IAU-
# constellation widths (NOT the equal 30° tropical signs).
AGES = [
    # (English, Sanskrit, Sidereal longitude range of equinox)
    ("Aries",       "Meṣa",      0.0,    25.0),    # ~0° - 25° in modern sky
    ("Pisces",      "Mīna",      330.0,  360.0),   # current age starts here
    ("Aquarius",    "Kumbha",    300.0,  330.0),
    ("Capricorn",   "Makara",    270.0,  300.0),
    ("Sagittarius", "Dhanu",     240.0,  270.0),
    ("Scorpio",     "Vṛścika",   210.0,  240.0),
    ("Libra",       "Tulā",      180.0,  210.0),
    ("Virgo",       "Kanyā",     150.0,  180.0),
    ("Leo",         "Siṃha",     120.0,  150.0),
    ("Cancer",      "Karka",     90.0,   120.0),
    ("Gemini",      "Mithuna",   60.0,   90.0),
    ("Taurus",      "Vṛṣabha",   30.0,   60.0),
]

# Major "pole stars" through the precessional cycle. Each entry is
# (star_name, approximate_year_of_closest_approach_to_pole).
# Used by next_pole_star().
POLE_STARS = [
    ("Thuban (α Dra)",      -2787),    # ~2787 BCE
    ("Kochab (β UMi)",      -1100),    # ~1100 BCE
    ("Polaris (α UMi)",      2100),    # now (closest c. 2100 CE)
    ("Errai (γ Cep)",        4200),    # ~4200 CE
    ("Alfirk (β Cep)",       5200),    # ~5200 CE
    ("Alderamin (α Cep)",    7500),    # ~7500 CE
    ("Deneb (α Cyg)",       10000),    # ~10000 CE
    ("Vega (α Lyr)",        13700),    # ~13700 CE
]


# ── Helpers ──────────────────────────────────────────────────────────

def _decimal_year(dt: datetime) -> float:
    """Convert a datetime to a decimal year (e.g., 2026.37)."""
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    start = datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
    end = datetime(dt.year + 1, 1, 1, tzinfo=dt.tzinfo)
    fraction = (dt - start).total_seconds() / (end - start).total_seconds()
    return dt.year + fraction


# ── Public API ───────────────────────────────────────────────────────

def current_ayanamsa(dt: datetime) -> float:
    """
    Return the Lahiri ayanamsa (degrees) at the given datetime.

    The ayanamsa is the angular offset between the tropical vernal
    equinox (0° Aries tropical) and the sidereal vernal point
    (0° Aries sidereal — fixed against the stars).

    Shares implementation with stellar.py for consistency.

    [MATHEMATICAL FACT] — Lahiri ayanamsa, linear approximation.
    """
    return _stellar._lahiri_ayanamsa(_decimal_year(dt))


def equinox_position(dt: datetime) -> dict:
    """
    Return the sidereal longitude of the vernal equinox point.

    Because the tropical 0° Aries is BY DEFINITION the vernal equinox,
    the equinox's sidereal longitude is (-ayanamsa) mod 360.

    Returns dict with:
      - sidereal_longitude_deg:  the vernal equinox's position in
        sidereal coordinates (where the stars are fixed)
      - constellation_traditional: which classical-zodiac constellation
        the equinox sits within (named per Hellenistic tradition)
      - ayanamsa: the Lahiri ayanamsa value for this datetime
    """
    ayan = current_ayanamsa(dt)
    sidereal_lon = (-ayan) % 360.0

    constellation = None
    for english, sanskrit, lon_start, lon_end in AGES:
        if lon_start <= sidereal_lon < lon_end:
            constellation = english
            break

    return {
        "sidereal_longitude_deg": sidereal_lon,
        "constellation_traditional": constellation,
        "ayanamsa_deg": ayan,
    }


def current_age(dt: datetime) -> dict:
    """
    Return the current zodiacal Age.

    The vernal equinox is currently in the late Pisces region,
    transitioning toward Aquarius. The exact moment of "Age of
    Aquarius" depends on which boundary convention you use — the
    IAU constellation boundary places it around 2597 CE; New Age
    estimates often place it sooner.

    Returns dict with:
      - age_english:     the constellation name (e.g., "Pisces")
      - age_sanskrit:    Vedic equivalent (e.g., "Mīna")
      - sidereal_longitude_deg: vernal equinox sidereal position
      - fraction_through_age: 0.0 (just entered) to 1.0 (about to leave)
      - years_remaining: approximate years before next age
    """
    pos = equinox_position(dt)
    sid_lon = pos["sidereal_longitude_deg"]
    age_info = None
    for english, sanskrit, lon_start, lon_end in AGES:
        if lon_start <= sid_lon < lon_end:
            width = lon_end - lon_start
            fraction = (sid_lon - lon_start) / width
            # Age moves WESTWARD (precession is retrograde through
            # the zodiac), so "remaining" is the fraction back to lon_start.
            fraction_remaining = (sid_lon - lon_start) / width
            years_remaining = fraction_remaining * AGE_DURATION_YEARS
            age_info = {
                "age_english": english,
                "age_sanskrit": sanskrit,
                "sidereal_longitude_deg": sid_lon,
                "lon_start_deg": lon_start,
                "lon_end_deg": lon_end,
                "fraction_through_age": 1.0 - fraction_remaining,
                "years_remaining": years_remaining,
            }
            break

    if age_info is None:
        raise ValueError(
            f"Could not place sidereal longitude {sid_lon}° in any Age. "
            f"This indicates a gap in the AGES table."
        )
    return age_info


def next_age_transition(dt: datetime) -> dict:
    """
    Project when the vernal equinox will next leave the current Age.

    Returns dict with:
      - next_age_english:     the upcoming Age name
      - next_age_sanskrit:    Vedic equivalent
      - approximate_year:     decimal year of the transition
      - years_from_now:       float years until the transition
    """
    age = current_age(dt)
    years_remaining = age["years_remaining"]
    transition_year = _decimal_year(dt) + years_remaining
    # Find the next age in the sequence (precession moves the equinox
    # backwards through the zodiac, so the next age has the lower lon range)
    current_lon_start = age["lon_start_deg"]
    # Wrap-around: if current is Aries (0-25), next is Pisces (330-360)
    if current_lon_start == 0.0:
        next_lon = 330.0
    else:
        next_lon = (current_lon_start - 30.0) % 360.0
    next_english, next_sanskrit = None, None
    for english, sanskrit, lon_start, lon_end in AGES:
        if abs(lon_start - next_lon) < 1.0:
            next_english = english
            next_sanskrit = sanskrit
            break
    return {
        "next_age_english": next_english,
        "next_age_sanskrit": next_sanskrit,
        "approximate_year_ce": transition_year,
        "years_from_now": years_remaining,
    }


def precession_summary(dt: datetime) -> dict:
    """
    One-shot summary: current ayanamsa, equinox position, age,
    next age, current closest pole star.
    """
    return {
        "ayanamsa_deg": current_ayanamsa(dt),
        "equinox_position": equinox_position(dt),
        "current_age": current_age(dt),
        "next_age_transition": next_age_transition(dt),
        "closest_pole_star": closest_pole_star(dt),
        "precession_period_years": PRECESSION_PERIOD_YEARS,
        "precession_rate_arcsec_per_year": PRECESSION_RATE_ARCSEC_PER_YEAR,
    }


def closest_pole_star(dt: datetime) -> dict:
    """
    Return the named pole star currently closest to the celestial pole.

    Uses the POLE_STARS table — each entry has the year of that star's
    closest approach to the pole. We pick the entry whose closest-approach
    year is nearest to the current decimal year.
    """
    year = _decimal_year(dt)
    closest = min(POLE_STARS, key=lambda p: abs(p[1] - year))
    return {
        "name": closest[0],
        "year_of_closest_approach": closest[1],
        "years_offset_from_closest": year - closest[1],
    }


def ayanamsa_at_year(year: float) -> float:
    """Convenience wrapper: ayanamsa at a decimal-year value."""
    return _stellar._lahiri_ayanamsa(year)


def equinox_position_at_year(year: float) -> dict:
    """Convenience: equinox sidereal longitude at decimal year."""
    ayan = ayanamsa_at_year(year)
    sid_lon = (-ayan) % 360.0
    return {
        "sidereal_longitude_deg": sid_lon,
        "ayanamsa_deg": ayan,
        "decimal_year": year,
    }
