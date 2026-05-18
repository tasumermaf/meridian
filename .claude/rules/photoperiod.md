# Photoperiod & the Ecological Layer

> Daylight duration at a given location on a given date. The single
> most important ecological variable in temperate biology — the cue
> by which plants flower, animals migrate, and circadian clocks
> entrain. The astronomical foundation of the Sprint C Ecological
> Layer (6th body). Offline-first: pure local computation from
> `(lat, lon, tz, dt)` with no network call.

---

## What photoperiod is

**Photoperiod** is the number of hours between sunrise and sunset
at a given point on Earth on a given date. It is a purely
astronomical quantity — derivable from latitude, the date's solar
declination, and the geometry of the horizon — and it requires no
weather data, no atmosphere model beyond standard refraction, and
no live observation.

It is also the **most biologically active environmental signal**
in temperate ecosystems. The variation in temperature, humidity,
rainfall, and cloud cover from one year to the next can be enormous;
the variation in photoperiod is essentially zero. Biology that wants
a reliable seasonal cue tracks the day length, not the weather. The
phenomenon is called **photoperiodism** — first formally described
by Garner and Allard (USDA, 1920) studying tobacco flowering — and
it governs:

- **Plants** — flowering in *short-day* species (chrysanthemums,
  poinsettias, soybeans) is triggered when the dark period crosses
  a species-specific threshold; *long-day* species (spinach, wheat,
  most temperate grains) flower as the dark period shortens.
- **Animals** — antler growth, coat colour change, migration onset,
  reproductive cycling, hibernation entry/exit. Sheep, deer, and
  hamsters are *short-day breeders*; horses and ferrets are
  *long-day breeders*.
- **Humans** — melatonin secretion, sleep architecture, seasonal
  affective disorder (SAD), serotonergic tone. The biological
  machinery is the same; the magnitude is muted by ten thousand
  years of indoor living.

[MATHEMATICAL FACT — photoperiod is a pure function of latitude,
date, and the obliquity of the ecliptic (~23.44°). It does not
depend on weather, elevation (to within seconds), or year-to-year
climate variation.]

[SOURCE: chronobiology — Garner & Allard 1920; modern overviews
in Pittendrigh's work on circadian entrainment.]

---

## The four numbers

The engine reports four quantities. Each carries a distinct
biological and practical meaning.

### 1. Daylight hours — `daylight_hours(dt, lat, lon, tz)`

Sunrise to sunset, in hours. The number a farmer, a gardener, a
walker, or a falconer cares about. This is the **active envelope**
for visually-dependent activity.

| Location          | Equinox  | Summer solstice | Winter solstice |
|-------------------|----------|-----------------|-----------------|
| Equator (0°)      | 12h 07m  | 12h 07m         | 12h 07m         |
| Damanhur (~45°)   | 12h 08m  | 15h 21m         | 8h 51m          |
| London (~51°)     | 12h 09m  | 16h 38m         | 7h 50m          |
| Reykjavík (~64°)  | 12h 12m  | 21h 01m         | 4h 07m          |
| Tromsø (~70°)     | 12h 14m  | 24h 00m         | 0h 00m          |

The seven-minute equinox surplus over a clean 12-hour reading is
real and not a rounding artifact — sunrise is defined as the upper
limb of the sun touching the horizon (not the geometric centre), and
atmospheric refraction lifts the apparent sun ~0.57° above its
geometric position at the horizon. Both effects add to apparent
day length at every latitude.

### 2. Night hours — `night_hours(dt, lat, lon, tz)`

Trivially `24 - daylight_hours`. Provided as its own function
because the orchestrator's downstream logic (Divine Hours night
wing length, organ clock night branches) reads this directly.

### 3. Civil twilight — `twilight_durations(...)["civil_minutes"]`

The interval between **civil dawn** (sun 6° below the horizon) and
**sunrise**. Returned in minutes.

Civil twilight is bright enough for most outdoor activity without
artificial light. Newspapers can still be read; faces remain
identifiable; the horizon at sea is sharp. In civil law, "twilight"
in jurisdictions that define the term (driving headlights, hunting
hours, building permits) almost always means civil twilight. The
Solar Key cusping window in the Astrolabium is anchored to civil
twilight on both sides of the day.

At Damanhur (~45° N) civil twilight is ~30 minutes year-round, with
modest seasonal variation. At Reykjavík (~64° N) it stretches to
hours near the equinoxes and collapses to nothing under the polar
day.

### 4. Nautical & astronomical twilight

**Nautical twilight** ends at sun 12° below the horizon — when the
sea horizon is no longer reliably visible against the sky, and the
brighter navigational stars are visible against a still-distinguishable
horizon. The traditional window for celestial navigation at sea.

**Astronomical twilight** ends at sun 18° below the horizon — when
the sky is photometrically dark. Below this threshold, faint deep-sky
objects can be observed without skyglow contamination from the sun.
The opening of the working night for an astronomer.

Both are returned in minutes from the respective dawn marker to
sunrise. Both can be `None` at high latitudes near the solstices —
see the polar edge cases section.

[SOURCE: astronomy — twilight depression conventions are codified in
the *Astronomical Almanac* (US Naval Observatory / HM Nautical
Almanac Office), values 6° / 12° / 18° unchanged since the 1830s.]

---

## How photoperiod varies by latitude

The seasonal swing in daylight is a function of latitude — specifically,
of the latitude's relationship to the **obliquity of the ecliptic**
(~23.44°, the tilt of Earth's rotational axis).

| Latitude band              | Annual photoperiod swing      | Behaviour                          |
|----------------------------|-------------------------------|-------------------------------------|
| Equator (0°)               | ~0h (12.0 ± 0.05h constant)   | No photoperiodic cue                |
| Tropics (0–23.44°)         | < 2h                           | Mild seasonality; bimodal rainy cue dominates |
| Temperate (23.44° – 66.5°) | 3h – 12h                       | Strong photoperiod; entrainment central |
| Polar (> 66.5°)            | All or nothing (24h / 0h)     | Photoperiod degenerate at solstices |

The 66.5° latitude is the **Arctic / Antarctic Circle** — defined
precisely as `90° − obliquity = 90° − 23.44° = 66.56°`. Above this
line, the sun fails to rise for at least one full day around the
winter solstice and fails to set around the summer solstice. The
polar day and polar night are not gradual; they are switches.

The biological consequence is enormous. **Tropical organisms cannot
use photoperiod as a seasonal cue** — the signal is too weak. They
rely on rainfall patterns, temperature, or food availability instead.
**Polar organisms cannot use photoperiod meaningfully near the
solstices** — the signal is saturated. They typically use the equinox
crossings (when day length passes through 12 hours) as their cue.
**Temperate organisms live in the regime where photoperiod is the
clean seasonal signal** — and the bulk of the photoperiodism literature
was written by researchers working in this band, which is
not coincidental.

A practitioner at any temperate latitude can use this layer with
confidence. At equatorial or polar latitudes the layer still
*reports* — but the meaning the practitioner draws from it must
shift. Cross-reference `location-and-time.md` for the latitude
ranges in which each Astrolabium layer is fully meaningful.

---

## The change rate — `daylight_change_rate_minutes_per_day`

The function returns a **signed rate** in minutes per day, computed
as `daylight(tomorrow) - daylight(today)` in minutes. Positive =
**lengthening**; negative = **shortening**.

This is the cue biology actually uses. A flat 12-hour day at the
equator is ecologically silent; a 12-hour day in March at 45° N
carries information *because the rate is large and positive*. The
organism reads the derivative, not the value.

The rate has a characteristic shape across the year — a slowed
trigonometric wave whose extremes sit at the **equinoxes**, not
the solstices:

| Latitude        | Maximum rate (at equinox) | Rate at solstices |
|-----------------|----------------------------|--------------------|
| Equator (0°)    | ~0 min/day                | ~0 min/day         |
| 30° N           | ~2.0 min/day              | ~0 min/day         |
| 45° N (Damanhur)| ~2.7 min/day              | ~0 min/day         |
| 51° N (London)  | ~3.0 min/day              | ~0 min/day         |
| 60° N           | ~3.7 min/day              | ~0 min/day         |
| 66° N (just below polar circle) | ~7+ min/day | ~0 min/day |
| Above polar circle | discontinuous (jumps at polar day/night transition) | undefined |

At Damanhur on the spring equinox, the day is lengthening by about
**2 minutes 40 seconds per day** — the maximum rate of the year.
That rate falls to zero at the summer solstice, then reverses sign
through the autumn equinox (~−2.7 min/day) before returning to zero
at the winter solstice. The full cycle is sinusoidal in the rate,
which means *cosinusoidal* in the daylight length — a fact every
gardener knows operationally without naming.

The Astrolabium reports the rate signed because the **sign carries
meaning**. A May reading at 45° N reports `+1.5 min/day`; a July
reading reports `−1.3 min/day` even though both are "summer."
The organism (and the practitioner) cares about which side of the
solstice it is on, not just how long the day is.

---

## Seasonal arc — `seasonal_arc_position`

A composite reading designed for orchestrator consumption. Returns:

- `hemisphere` — `"northern"` or `"southern"`, computed from sign of `lat`
- `season` — `"spring" | "summer" | "autumn" | "winter"`,
  **hemisphere-aware** (May at 45° N is `spring`; May at 33° S is `autumn`)
- `daylight_trend` — `"lengthening"` or `"shortening"`
- `daylight_minutes_per_day_rate` — the signed rate
- `days_from_nearest_solstice` and `days_from_nearest_equinox` — both as dicts

The hemisphere-awareness is the load-bearing detail. A naive engine
that reports "May is spring" for every user produces nonsense for
the Australian, Argentine, South African, or New Zealand practitioner.
The Astrolabium's seasonal labels are **observer-local**, not
calendar-fixed.

Northern-hemisphere mapping:

| Window (Northern)             | Season |
|-------------------------------|--------|
| Mar 20 → Jun 20               | spring |
| Jun 21 → Sep 22               | summer |
| Sep 23 → Dec 20               | autumn |
| Dec 21 → Mar 19               | winter |

The southern mapping is the same windows with reversed labels
(`autumn`, `winter`, `spring`, `summer`). The boundary dates are
fixed approximations (the true astronomical seasons drift by a day
or two across the leap-year cycle); this matters for ecological
framing but not for ritual timing where the engine uses true
astronomical events from `solar.py`.

---

## Twilight bands — practical use

Each twilight band defines a regime of activity. The bands' utility
is direct, operational, and traditional.

- **Daylight** (sun above horizon) — full visual work, navigation
  by sight, agriculture, ordinary outdoor activity. The original
  human working day.

- **Civil twilight** (sun 0° → 6° below) — outdoor activity without
  lamps. Reading possible if not strained. The Solar Keys' cusping
  window opens and closes within this band on both ends of the day.
  Civic and legal "twilight" almost always refers to this band.

- **Nautical twilight** (6° → 12° below) — sea horizon visible against
  sky; navigational stars (1st and 2nd magnitude) appearing or
  fading. Traditional window for sextant work at sea.

- **Astronomical twilight** (12° → 18° below) — sky still has measurable
  solar contribution; faint deep-sky objects (galaxies, nebulae below
  magnitude ~6) compromised. Observatory work begins when this ends.

- **Full astronomical night** (sun > 18° below) — true dark sky.
  The window for any work — astronomical, ritual, deep meditative —
  that depends on the absence of solar illumination.

For ritual timing, the relevant twilight is almost always **civil**:
the Solar Keys cusp within civil twilight, the Divine Hour boundaries
at sunrise and sunset sit at the same point, and the practitioner's
threshold experience of dawn or dusk is a civil-twilight phenomenon.
Nautical and astronomical twilight matter for sky observation and
for the deeper ritual modes that explicitly want a dark sky.

---

## Connection to existing layers

The Ecological Layer does not replace earlier layers; it gives them
their physical envelope. Three integration points matter.

### Divine Hours

`daylight_hours` is the **day wing length** before the four-fold
division. `night_hours` is the **night wing length**. The Divine
Hour computation in `astrolabium.py` reads sunrise and sunset from
the solar engine; the photoperiod engine reads the same two points
and reports the totals. Both call `solar.get_solar_positions` and
will always agree.

A Divine Hour at the equinox is ~3 modern hours long. At Reykjavík
in winter, day Hour I is ~62 minutes long and night Hour VII is ~5
hours long. The photoperiod values explain *why* — they are the raw
inputs the Divine Hour computation divides into four.

See `divine-hours.md` for the wing division and the qualitative
attributions of the eight hours.

### Organ Clock

The TCM Organ Clock's twelve Earthly Branch windows tick over with
**solar position**, not civil time. Photoperiod determines the
day/night branch boundaries: the day branches (Mǎo through Wèi)
span the daylight period, the night branches (Shēn through Yín)
span the night. When daylight is short, day branches compress and
night branches stretch. Cross-reference `astrolabium.md` (the
Organ Clock domain rules) and `temporal-bodies.md` (the layering).

### Solar Keys (Gold and Silver)

The Gold Key (Kǎn ☵, sunrise, Fall of Events) and Silver Key
(Lí ☲, sunset, Divinity) cusp during civil twilight. The cusping
window's duration is the civil twilight duration. The photoperiod
engine reports civil twilight in minutes; the Solar Key cusping
window engine in `twilight.py` operates on the same astronomical
boundary. Both should always agree; if they diverge, the cause is
almost always a date or timezone mismatch in one call.

See `trigram-laws.md` for the Solar Key architecture (6+2 trigram
cycle, the two Keys as the operators excluded from the lunar
month cycle).

---

## Polar edge cases

Above the Arctic Circle (~66.56° N) or below the Antarctic Circle,
photoperiod degenerates near the solstices. The engine handles this
gracefully but the practitioner must read the output with
understanding.

| Condition | `daylight_hours` | `night_hours` | Twilight bands |
|-----------|------------------|---------------|-----------------|
| Polar day (sun never sets) | 24.0 | 0.0 | None for all three |
| Polar night (sun never rises) | 0.0 | 24.0 | Civil possible if sun ≤ 6° below; nautical/astronomical may exist if sun stays > 18° below |
| Partial polar night, sun stays below civil but above nautical depression | 0.0 | 24.0 | Civil = None, Nautical = some, Astronomical = some |

The engine returns `None` for any twilight band that does not exist
on the queried date. The `daylight_change_rate` is well-defined
even across the polar day/night switch but can return discontinuous
values of dozens of minutes per day in the few days when the polar
transition is happening.

The seasonal labels (`spring`, `summer`, etc.) still apply at polar
latitudes by the standard month-window convention — but they
correspond to *photoperiod regimes* (polar day in high-latitude
summer, polar night in high-latitude winter) that have no temperate
analogue. A practitioner at Longyearbyen reading "summer, lengthening"
is being told something true and useless; the temperate framing
breaks down here.

Cross-reference `location-and-time.md` for the polar advisory the
orchestrator should surface to users above 60° latitude.

---

## Common errors

- **Treating May as spring everywhere.** Hemisphere matters. The
  `seasonal_arc_position` function returns the hemisphere-correct
  label; do not paraphrase the result by mapping month to season
  from a northern-hemisphere mental model. A southern-hemisphere
  user reading "spring" in May is being told the wrong thing.

- **Confusing civil twilight (the 0–6° band) with the civic concept
  of a "civil twilight zone."** They are unrelated. The 6° depression
  angle has no relationship to any geographic or political boundary.

- **Reading the rate as unsigned.** `daylight_change_rate_minutes_per_day`
  is signed; a +1.5 and a −1.5 are biologically opposite. Always
  report the sign when quoting the rate, and prefer the trend label
  (`lengthening` / `shortening`) for natural-language summaries.

- **Equating photoperiod with daylight saving time.** DST is a civil-
  clock construct; photoperiod is solar geometry. The wall-clock
  hour of sunrise changes by an hour twice a year; the duration of
  sunrise-to-sunset does not.

- **Quoting daylight to the nearest minute and treating that as
  meaningful.** Atmospheric refraction at the horizon varies by
  several minutes of apparent rise/set time depending on local
  temperature lapse rate. The engine's `daylight_hours` is accurate
  to ~1 minute under standard refraction; precision beyond that
  is false precision.

- **Querying twilight at high latitude without checking for `None`.**
  Above ~60° during much of summer, astronomical twilight does not
  exist (the sun never gets 18° below the horizon). The engine
  returns `None`; downstream code must check.

- **Treating photoperiod as a *circadian* signal directly.** Photoperiod
  is the *seasonal* envelope; the *circadian* signal is the
  sunrise/sunset transition itself. The two are related but distinct
  in the chronobiological literature.

---

## Cross-references

- `ecological-markers.md` — the species-level markers built on top
  of photoperiod (flowering windows, migration cues, the practical
  ecological calendar for a latitude band).
- `divine-hours.md` — the wing-length consumer of `daylight_hours`
  and `night_hours`. The two layers should always agree; if they
  diverge, the cause is upstream of both in `solar.py`.
- `location-and-time.md` — the latitude advisory band system. The
  Ecological Layer is fully meaningful in the temperate band
  (23.44° – 66.5°); degraded but reported outside it.
- `stellar-layer.md` — the sidereal foundation. Photoperiod is a
  tropical (equinox-anchored) quantity, distinct from the sidereal
  (star-anchored) framing of the Stellar Layer.
- `astrolabium-core.md` — the orchestrator that composes the
  Ecological Layer with the other five bodies (Soul / Astral / Gross /
  Solar Keys / Stellar) into the unified six-body state.
- `astrolabium/src/engine/photoperiod.py` — the implementation.
- `astrolabium/src/engine/solar.py` — the shared sunrise/sunset
  computation consumed by both this layer and the Divine Hours.
- `astrolabium/src/engine/twilight.py` — the Solar Key cusping
  window engine, which operates on the same civil-twilight boundary
  reported here.
