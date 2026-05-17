# The Divine Hours

> The eight-fold unequal-hour division of day and night. Two wings of
> four hours each. Where it comes from, what each one favors, and how
> the engine computes it.

---

## What they are

The day is divided at sunrise and sunset into two **wings**:

- **First Wing** — sunrise to sunset (the day half)
- **Second Wing** — sunset to next sunrise (the night half)

Each wing is then divided into **four equal Divine Hours**. The day
hour length and the night hour length are usually different (they are
equal only at the equinoxes), and both vary by latitude and season.

The eight hours are numbered I–IV (day wing) and V–VIII (night wing).
Hour I begins at sunrise. Hour V begins at sunset. Hour VIII ends at
the next sunrise.

[SOURCE: Damanhurian — Book of Three Responses, Chapter 4]

## The mathematics

```
day_hour_length   = (sunset - sunrise)        / 4
night_hour_length = (next_sunrise - sunset)   / 4
```

At Damanhur on the spring equinox (2026-03-20):
- Day wing: ~12h 8m → each day hour ≈ **182 minutes**
- Night wing: ~11h 48m → each night hour ≈ **177 minutes**

(They are nearly but not exactly equal even at the equinox because of
atmospheric refraction and the sun's apparent diameter — sunrise is
defined as the upper limb touching the horizon, not the geometric
center.)

At Reykjavík on the winter solstice (≈21 Dec):
- Day wing: ~4h 7m → each day hour ≈ **62 minutes**
- Night wing: ~19h 53m → each night hour ≈ **298 minutes**

At Reykjavík on the summer solstice (≈21 Jun):
- Day wing: ~21h 1m → each day hour ≈ **315 minutes**
- Night wing: ~2h 59m → each night hour ≈ **45 minutes**

**The hours grow and shrink with the year because the day itself does.**
The unequal-hour system is the original temporal mode of every
pre-mechanical-clock civilization in the temperate zones.

## The "3 solar hours = 1 divine hour" misconception

A common simplification is "3 modern hours = 1 Divine Hour." **This is
only true on the equinox.** The simplified ratio is a teaching shortcut,
not the formula. The actual ratio is `(day_length / 4) / 60` in minutes,
and that ratio changes day by day, latitude by latitude. The engine
computes the actual ratio every time. Do not use the shortcut for any
real reading.

## Where the system comes from

The eight-fold division is documented in the *Book of Three Responses*
(*Il Libro Dalle Tre Risposte*, 1988, Falco Tarassaco), Chapter 4 in
particular. The text describes a tripartite structure — wings, hours,
and a relationship between certain hours and certain ritual operations
— and gives operational instructions for using the hour count in
formula-based work.

The unequal-hour system itself is far older than the Damanhurian
codification. It is the canonical hour system of Vedic temple time,
ancient Egyptian decanal time, Greek and Roman civic time (the *hora*),
Jewish ritual time (the *sha'ah zmanit* of rabbinic literature), Islamic
prayer time (the *salat al-asr* calculations), and the Christian
liturgical office (Prime at sunrise, Compline at sunset, with the
intermediate canonical hours sliding through the year). The
Damanhurian system explicitly recovers this older mode of measuring
time.

## What each Hour favors

[SOURCE: Damanhurian, with practical attributions from Of the Three
Responses Chapter 4, plus ANALYTICAL CONTRIBUTION for some specifics]

### First Wing (Day)

| Hour | Range                      | Quality                                     |
|------|----------------------------|---------------------------------------------|
| I    | sunrise → 1/4 day wing     | Initiation. New work, beginnings, the first breath. |
| II   | 1/4 → midday               | Construction. Building, accumulation, ascent. |
| III  | midday → 3/4 day wing      | Culmination. Strongest light, peak action.   |
| IV   | 3/4 → sunset               | Completion. Closing the day's work, integration. |

### Second Wing (Night)

| Hour | Range                        | Quality                                     |
|------|------------------------------|---------------------------------------------|
| V    | sunset → 1/4 night wing      | Reception. Releasing the day, settling.      |
| VI   | 1/4 → midnight               | Dissolution. The first depth.                |
| VII  | midnight → 3/4 night wing    | The depth proper. Dream, oracle, deep stillness. |
| VIII | 3/4 → next sunrise           | Return. The last threshold before light.     |

**The qualities above are interpretive scaffolding.** Sources are
explicit about a tripartite structure and about specific operations
keyed to specific hours; they are less explicit about a full
hour-by-hour quality table. The summary above is consistent with the
documented attributions for Hours I–IV but extends the quality logic
to V–VIII as analytical synthesis. When asked specifically what a
source says about (e.g.) Hour VII, the honest answer is: *the Book
of Three Responses does not assign a formal quality to Hour VII; the
description above is consistent with the dream-hour tradition across
many cultures, but mark it as [ANALYTICAL CONTRIBUTION].*

## The Solar Key relationship

Hour I begins at sunrise. **Sunrise is when the Gold Key (Kǎn ☵, Fall
of Events) is active.** Hour V begins at sunset. **Sunset is when the
Silver Key (Lí ☲, Divinity) is active.** The Solar Key cusping window
brackets the transition.

So Hour I is *the hour that begins at the Gold Key cusp* and Hour V is
*the hour that begins at the Silver Key cusp*. The two thresholds
(sunrise and sunset) are also the two daily moments when the Cantong
qi treats the alchemical fire as most precisely controllable. The
Divine Hours and the Solar Keys are the same astronomical event read
through two different traditions.

## How the engine computes them

```python
from astrolabium.engine import solar

solar_pos = solar.get_solar_positions(dt, lat, lon, tz)
sunrise = solar_pos["sunrise"]
sunset = solar_pos["sunset"]

# ... and then divine_hour returns the (hour_number, wing, fraction_into_hour)
```

The full computation goes through the orchestrator's
`_calculate_divine_hour` helper (private function inside
`astrolabium.py`). It handles the wing logic (day if `sunrise <= dt <
sunset`, night otherwise), the four-fold division, and the edge case
of crossing midnight.

## What never to do

- Never report a Divine Hour without location. The hour number depends
  on solar position, which depends on `(lat, lon, tz)`.
- Never report a Divine Hour from civil time. The 3-hour shortcut is
  wrong everywhere except the equinox, and even there it is wrong by
  several minutes.
- Never claim a Divine Hour is "good" or "bad." The hour has a quality;
  the practitioner's relationship to that quality is theirs to determine.

## Cross-references

- `.claude/rules/temporal-bodies.md` — how Divine Hours layer with the
  other temporal bodies
- `.claude/rules/trigram-laws.md` — Solar Keys and the cusping
  relationship to Hours I and V
- `docs/sources/Of_the_Three_Responses_Chapter_4.md` — primary source
  on the eight-fold division
- `docs/specs/operators_manual.md` — Part 1 of the Operator's Manual,
  which describes the user-facing presentation of the hours
- `docs/specs/guidebook.md` — Part 2, which contains the full computational
  tables and worked examples for Divine Hour computation
