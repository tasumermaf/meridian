# Lunar Standstills (Major and Minor)

> The 18.6-year cycle of the Moon's monthly extreme declination,
> driven by the westward regression of the lunar nodes. The Deep Sky
> Layer's slowest visible rhythm — slower than the Saros, faster than
> the precession of the equinoxes.

---

## What a standstill IS

The Moon's orbit around the Earth is inclined about **5.14°** to the
ecliptic (the apparent path of the Sun). The two points where the
lunar orbital plane crosses the ecliptic are the **lunar nodes** —
the **ascending node** (where the Moon climbs north of the ecliptic)
and the **descending node** (where it dips south). These two nodes
sit 180° apart on the ecliptic and are the geometric reason eclipses
happen only at certain alignments.

The nodes are not fixed. They **regress westward** — they move
backward through the ecliptic at about 19.34° per year, completing a
full circuit in **18.613 years**. This is the **regression of the
lunar nodes**, and it is the single mechanism that drives the
standstill cycle.

[MATHEMATICAL FACT — nodal precession is a canonical astronomical
constant. The value 18.6128 years is the modern observational figure
used by the Astrolabium engine.]

Because the Moon's orbital tilt is fixed relative to its own orbital
plane, and that plane swings around the ecliptic every 18.6 years,
the Moon's **monthly maximum declination** — the highest point above
the celestial equator it reaches each sidereal month — oscillates
between two extremes over the same 18.6-year period.

- When the ascending node sits at the **vernal equinox point**
  (the 0° boundary of the ecliptic), the orbital tilts **add**:
  obliquity 23.44° + lunar inclination 5.14° ≈ **28.58°**. Each
  month the Moon reaches that far north of the equator and that far
  south. This is a **major standstill**.

- When the ascending node sits at the **autumnal equinox point**
  (180° away), the tilts **subtract**: 23.44° − 5.14° ≈ **18.30°**.
  The Moon's monthly extreme declination is squashed to a much
  narrower band. This is a **minor standstill**.

The engine uses **28.72°** for the major peak (the empirical value
incorporating small perturbations beyond the linear 23.44 + 5.14
calculation) and **18.30°** for the minor.

The cycle goes major → minor → major in 18.613 years — minor falls
**halfway** between two majors, separated by about 9.3 years from
each.

---

## What you actually see

At a major standstill the Moon's **monthly arc of moonrise and
moonset azimuth** is at its widest. The full moon nearest the winter
solstice rises far to the **north** of east and sets far to the
north of west; the full moon nearest the summer solstice swings to
the **south**. The two extremes of the moonrise position on the
horizon are separated by a much larger arc than at any other time
in the 18.6-year cycle.

At a minor standstill the same arc is at its narrowest. The Moon's
rise position drifts through a smaller piece of the horizon each
month, and the visual contrast between summer-solstice and
winter-solstice full moons is muted.

The contrast is most visible by watching where the Moon rises or
sets at the **full moon near a solstice**. Watching the Moon
anywhere mid-month — first quarter, last quarter, near the
equinoxes — washes out the effect, because you are sampling lower
declinations regardless of the standstill phase.

The visual swing between major and minor is **roughly 20° of horizon
azimuth** at temperate latitudes — enough that an observer paying
attention across years cannot miss it, and far more than enough to
make a stone monument worth building.

---

## Why megaliths cared

The major standstill is a **visually striking, rare, and predictable**
astronomical event. Once every 18.6 years the Moon reaches a position
in the sky that it does not reach at any other time in a human
generation. The cycle is long enough that most adults will witness
only three or four major standstills in a lifetime; short enough
that an oral tradition can transmit knowledge of it; regular enough
that a sufficiently observant culture can predict the next one.

Building a stone monument to align with such an event makes sense
**only if you know the cycle**. A one-off observation cannot be
distinguished from a coincidence. Repeated observation across at
least one full 18.6-year period is required to recognize the cycle
at all, and across two or three to confirm it. The presence of
standstill alignments at multiple megalithic sites across multiple
continents is direct archaeological evidence that the cultures
which built them did this.

Documented standstill alignments include:

- **Stonehenge** (Salisbury Plain, c. 3000–2000 BCE). The Heel Stone
  marks the northeast horizon position where the major-standstill
  full moon rises around the winter solstice. The Slaughter Stone
  and several of the Station Stones complete the rectangular
  framework whose long axes track major-standstill moonrise and
  moonset extremes. The geometry is documented in Newham (1972) and
  refined by the recent Heritage England / Royal Astronomical
  Society survey of the 2024–2025 major standstill.

- **Callanish** (Calanais, Isle of Lewis, Scotland, c. 2900 BCE).
  The southernmost major-standstill full moon skims the southern
  horizon and appears to "roll along" the Sleeping Beauty hills
  before reappearing through the stone avenue. The phenomenon is
  visible only every 18.6 years and is documented from the 19th
  century onward.

- **Chimney Rock** (Chacoan culture, southwest Colorado, c. 1075
  CE). The major-standstill full moon rises between the two stone
  pillars from which the site takes its name. The Chacoan Great
  House on the ridge was constructed during a major standstill
  event (tree-ring dated to 1076 CE) and rebuilt or expanded
  approximately 18.6 years later, in 1093 CE — a second major
  standstill. The interval is the cycle.

[SOURCE: classical archaeoastronomy — Thom (1971), Burl (2000),
Ruggles (2015). The specific Chimney Rock interval is documented in
Malville and Putnam (1989); the 2024–2025 Stonehenge survey is
ongoing English Heritage research.]

The pattern across all three sites is the same: **the major
standstill is the moonrise that does not happen most years**, and
the architecture is calibrated to it specifically.

---

## The mathematics

Two independent angles combine to produce the standstill extremes:

```
ε  =  obliquity of the ecliptic        =  23.4392811°  (J2000)
i  =  lunar orbital inclination         =   5.14°       (mean)

Major standstill max declination  ≈  ε + i  ≈  28.58°
Minor standstill max declination  ≈  ε − i  ≈  18.30°
```

The Astrolabium uses **28.72°** for the major standstill peak (a
slightly higher value than the linear sum) because the actual
maximum observed declination during a major standstill includes
small perturbations from the **evection** and other lunar
inequalities. The peak monthly maximum across the standstill
"plateau" — the year or two during which the major standstill is
effectively at peak — is empirically closer to 28.72° than to
28.58°. The minor value 18.30° is left at the linear subtraction
because the perturbation correction is smaller and tends to round to
the same first-decimal value.

[MATHEMATICAL FACT — obliquity from IAU 2006 precession model;
lunar inclination from canonical orbital elements. The standstill
extremes are not adjustable parameters; they are direct geometric
consequences of these two angles.]

The **nodal regression rate** is:

```
360° / 18.6128 years  =  19.341° per year
                      =  0.0530° per day (mean)
```

The engine treats the nodal motion as **linear** in time. The
ascending node's sidereal longitude at any date is computed by
back-projecting from a reference epoch:

```
λ_node(t) = (λ_node_ref − 19.341 × Δt_years) mod 360°
```

where `Δt_years` is decimal years since the reference epoch. The
linear approximation is correct to about one degree over a century
— small enough that the **standstill phase** it reports (major,
approaching minor, etc.) is accurate, but not small enough for
high-precision eclipse work. The Astrolabium reports standstill
phase, not eclipse timing.

---

## Reference epochs

The engine anchors its cycle calculation to two recent, well-observed
standstill events:

| Event              | Date                | Notes                                |
|--------------------|---------------------|--------------------------------------|
| LAST_MAJOR_STANDSTILL | **2025-03-22**   | The recent major peak; widely observed |
| LAST_MINOR_STANDSTILL | **2015-10-28**   | Halfway between 2006 and 2025 majors |

[MATHEMATICAL FACT — these dates are accurate to within a few days
of the actual peak. Standstill peaks are not single moments; they
are extended plateaus during which the monthly maximum declination
holds near the extreme for roughly a year on either side of the
nominal peak date.]

Anchoring on 2025-03-22 lets the engine compute the cycle phase for
any date with a single subtraction and a modulus:

```python
years_since_major = (dt - LAST_MAJOR_STANDSTILL).days / 365.25
cycle_fraction    = (years_since_major / NODAL_PERIOD_YEARS) % 1.0
```

The `cycle_fraction` is the canonical way the rest of the system
asks "where are we?".

---

## The cycle_fraction interpretation

| `cycle_fraction` | Phase                | Description                              |
|------------------|----------------------|------------------------------------------|
| 0.00             | **Major standstill** | Monthly max declination at ~28.72°       |
| 0.25             | Quarter-cycle        | Declination dropping toward minor        |
| 0.50             | **Minor standstill** | Monthly max declination at ~18.30°       |
| 0.75             | Three-quarter        | Declination rising back toward major     |
| 1.00 ≡ 0.00      | Next major standstill| ~18.6 years after the previous           |

The cycle is **continuous**, not discrete. There is no single
moment when one becomes the other. The labels are reference points
on a smoothly oscillating curve. Reporting a value like
`cycle_fraction = 0.062` is correct and informative — it means we
are 6.2% past the most recent major standstill peak, in the early
descent of the curve.

The engine also exposes a derived **`current_monthly_max_decl`**
that interpolates between the two extremes as a function of
`cycle_fraction`:

```
decl(f) = MINOR + (MAJOR − MINOR) × cos²(π × f)
```

The cosine-squared interpolation matches the actual standstill
envelope reasonably well — at the major peak the envelope is flat
(slow variation near the extremum), and the same is true at the
minor extremum. The function is symmetric and reaches the minor
exactly at `f = 0.5`.

---

## Live reading for 2026

The Astrolabium engine, queried for `datetime(2026, 5, 18)`, returns:

```
years_since_major   ≈  1.16
cycle_fraction      ≈  0.062
current_monthly_max ≈  28.32°   (still close to major)
phase_label         =  "early descent from major"
next_major          =  2043-10-25   (cycle_fraction returns to 0.0)
next_minor          =  2034-05-26   (cycle_fraction reaches 0.5)
```

Reading this in plain terms: we are **6.2% past the 2025 major
standstill peak**. The Moon's monthly extreme declination is still
within half a degree of the absolute maximum and will remain at
"effectively major" for another year or two before measurably
dropping. The **next minor standstill** is in **2034**; the **next
major** is in **2043**. A child born in 2026 will witness one full
cycle — minor in 2034, major in 2043 — by the time they are
seventeen.

---

## How this connects to Sprint A's lunar mansions

The Stellar Layer (Sprint A) reports which **mansion** the Moon
occupies — a sidereal longitude lookup, independent of declination.
The Deep Sky Layer (Sprint B) reports the Moon's **declination
envelope** — how far north or south of the celestial equator the
Moon can reach in the current month, independent of longitude.

The two are **orthogonal** and **mutually informative**.

At a major standstill, the full moon nearest the summer solstice
rises **far to the north of east** and culminates at an unusually
high altitude in the northern sky. At temperate northern latitudes
this brings the Moon visually closer to the **circumpolar northern
mansions** — particularly **Mǎo 昴 (Hairy Head / Pleiades)** and
the surrounding White Tiger / Black Tortoise boundary stars — and
correspondingly **further from the Vermillion Bird palace** stars
that lie south of the ecliptic.

At a minor standstill the same full moon stays in a tighter band
near the ecliptic. The northern excursion is suppressed; the
visual proximity to the northern circumpolar mansions is reduced.
The Vermillion Bird's southerly culminations dominate the summer
sky in the way they "usually" do.

**This is a real second-order effect on mansion experience.** The
mansion the Moon technically occupies is the same in both cases —
mansion identity is determined by ecliptic longitude, not
declination. But the *visual phenomenology* of the Moon in that
mansion differs significantly across the 18.6-year cycle. A
practitioner observing the Moon in Mǎo at a major standstill
sees it ride exceptionally high in the northern sky; at a minor
standstill, the same Moon in the same mansion sits closer to the
celestial equator.

The Astrolabium reports both data points and trusts the
practitioner to integrate them.

---

## What never to do

- **Never confuse the 18.6-year nodal cycle with the 19-year
  Metonic cycle.** The Metonic cycle (19 tropical years ≈ 235
  synodic months) is the relationship between the solar and lunar
  calendars and is the basis for things like the Easter computus
  and the Jewish leap-month rule. It is a near-coincidence of
  *periods*, not a single physical phenomenon. The 18.6-year nodal
  cycle is the *regression of the lunar nodes* — a single physical
  motion of the lunar orbital plane. The two periods are similar
  numerically and have no causal relationship. Treating them as the
  same is the most common confusion in popular astronomy writing
  about the Moon.

- **Never expect a single dramatic event at the standstill peak.**
  The peak is a **plateau** lasting one to two years on either side
  of the nominal date. The monthly maximum declination changes very
  slowly near the extremum (the cosine-squared envelope is flat
  there by construction). Calling the 2025 major standstill "the
  March 22 standstill" is shorthand; the standstill character is in
  effect for roughly 2024-mid through 2026-end.

- **Never report standstill character from a single moonrise
  observation.** Determining a standstill requires comparing the
  Moon's extreme declination over at least a few sidereal months,
  ideally near the solstices. A single observation cannot
  distinguish a major standstill from any other moonrise the same
  month.

- **Never invoke standstill effects at non-solstice full moons
  without noting the framing.** The 28.72° / 18.30° contrast is
  most visible at the **full moon near the solstices** — that is
  the moment when the Moon's declination is opposite the Sun's,
  and both bodies are at the geometric extremes of their respective
  envelopes. The same standstill is present mid-month and away
  from solstice, but the visual signature is suppressed because
  the Moon's declination is closer to zero regardless.

- **Never claim the standstill changes the Moon's calendrical
  month.** Mansion occupancy, lunar phase, synodic month, sidereal
  month, lunar mansion through which the Moon passes — none of
  these are affected by the standstill phase. The standstill
  governs **declination envelope only**. The calendar architecture
  is independent.

- **Never read a body other than the Moon through the standstill
  framework.** The Sun's monthly declination range is fixed at
  ±23.44° (the obliquity). The planets each have their own orbital
  inclinations, generally small, and their declination envelopes
  are dominated by the Sun's orbital plane, not by an 18.6-year
  cycle. The standstill is a *Moon-only* phenomenon, because only
  the Moon orbits the Earth with an inclined plane whose nodes
  regress on this timescale.

- **Never report a node longitude without specifying ascending or
  descending.** The two nodes are 180° apart. `current_node_longitude`
  in the engine returns the **ascending node**'s sidereal longitude
  by convention. The descending node is exactly 180° further along
  the ecliptic.

---

## Cross-references

- `.claude/rules/28-lunar-mansions.md` — sidereal mansion lookup;
  the standstill cycle modulates the visual phenomenology of mansion
  occupancy without changing the mansion identity itself
- `.claude/rules/stellar-layer.md` — the Sprint A layer that the
  Deep Sky Layer extends; standstills sit in the Deep Sky bucket
  along with precession and other slow rhythms
- `.claude/rules/precession.md` — the 26,000-year precession of the
  equinoxes; a different and much slower nodal-like phenomenon
  affecting the Earth's rotational axis rather than the lunar orbital
  plane
- `.claude/rules/divine-hours.md` — local solar hours; standstill
  reading is global / geocentric and does not require `(lat, lon, tz)`
- `astrolabium/src/engine/lunar_standstills.py` — the implementation
  exposing `get_lunar_standstill_state`, `next_major_standstill`,
  `next_minor_standstill`, and `current_node_longitude`
- `docs/specs/operators_manual.md` — Part 1, user-facing presentation
  of the Deep Sky Layer
- `docs/specs/guidebook.md` — Part 2, technical reference and worked
  examples for standstill computation
