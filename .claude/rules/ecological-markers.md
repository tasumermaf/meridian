# The Ecological Markers Layer

> Climate-norm derived ecological state from latitude and day of year.
> What the LAND is doing right now, at the practitioner's location,
> approximated from first principles — no weather feed, no API call,
> no network. The Astrolabium's quietest layer: it tells you what
> season the dirt is in.

---

## What this layer is

The Ecological Markers layer answers a small but operationally important
question: *what is the general ecological condition at the practitioner's
location right now, given only the calendar date and the latitude?*

It returns four things:

- **Climate zone** — which of five latitude-band classifications the
  practitioner is in (tropical / subtropical / temperate / boreal / polar).
- **Frost-risk state** — whether this date falls in the climate-norm
  frost season for that zone.
- **Vegetation stage** — where in the dormant → awakening → leafing →
  flowering → fruiting → ripening → senescing → dormant cycle the
  region typically is.
- **Growing-degree-day (GDD) state** — a coarse intensity classification
  (none / low / moderate / high) for seasonal heat accumulation.

The layer is implemented in `astrolabium/src/engine/ecological_markers.py`.
It depends only on `photoperiod.py` (which depends only on `solar.py` /
`ephem`). No external services, no datasets to update, no cache. Same
`(dt, lat)` always produces the same answer.

[ANALYTICAL CONTRIBUTION — all four outputs are simple latitude-band
heuristics, not validated meteorological models. They report what a
climate norm *would suggest* for a typical year, not what the weather
is actually doing. Honest about being an approximation.]

---

## Why offline matters

The Astrolabium has always been offline-first. Every other layer in the
instrument — solar position, lunar phase, the Divine Calendar, the
sexagenary cycle, the precessional Great Year, the Vedic yugas — runs
from `ephem` plus local data. Nothing in the existing instrument calls
out to the network at runtime. That is a design commitment, not an
accident:

- **Operability without infrastructure.** The practitioner on a remote
  retreat, in a power outage, on a Raspberry Pi without WiFi, in a
  location whose API provider has gone dark — still has a working
  instrument. The Astrolabium is meant to be carried and used.
- **Determinism.** Same input, same output, forever. No "the API returned
  a different value today" drift. No silent dataset updates changing
  what "now" means.
- **No external dependency surface.** Every network call is a failure
  mode and a cost vector. The instrument's authority comes partly from
  the fact that it cannot fail in those ways.

Live weather data would violate that ethos. Real-time temperature,
humidity, precipitation, frost-point — these are weather, not climate.
The instrument's job is to locate the practitioner inside cycles, not
to forecast tomorrow.

Sprint D may add an **optional** live-weather adapter (Open-Meteo is the
likely candidate — free, no key, reasonable terms). If it ships, it will
be opt-in and clearly marked as an external dependency. The
ecological-markers layer as built here remains the offline default and
the source of truth when the network is unavailable.

---

## The five climate zones

Latitude bands serve as a first-cut Köppen proxy. Real Köppen
classification depends on precipitation patterns, temperature means,
continentality, elevation, and ocean currents. The Astrolabium uses
absolute latitude only — a deliberate simplification.

| Zone          | \|lat\|       | Hemisphere note     | Key biological traits                              |
|---------------|---------------|---------------------|----------------------------------------------------|
| **tropical**     | 0 – 23.5°     | both                | No winter; wet/dry seasons rather than thermal seasons; no frost. |
| **subtropical**  | 23.5 – 35°    | both                | Mild winter; hot summer; occasional inland frost.  |
| **temperate**    | 35 – 55°      | both                | Four seasons; reliable winter frost; growing season ~May–Sep (NH). |
| **boreal**       | 55 – 66.5°    | both                | Long winter; short cool summer; snow most of year. |
| **polar**        | 66.5 – 90°    | both                | Polar day / polar night cycles; no real growing season. |

The bounds at **23.5°** (the tropics, equal to Earth's axial tilt) and
**66.5°** (the polar circles, 90° − 23.5°) are astronomical, not
ecological — they're the latitudes inside which the sun never sets / never
rises at the solstices. The 35° and 55° bounds are conventional
ecological-zone divisions and could reasonably be drawn elsewhere; they
are good enough for the instrument's purposes.

[ANALYTICAL CONTRIBUTION — the simplified band map. Köppen-Geiger
classifies the same region differently depending on precipitation;
the Astrolabium's latitude-only first cut intentionally undersells
its precision.]

[MATHEMATICAL FACT — the 23.5° and 66.5° boundaries are deterministic
from Earth's current axial obliquity (≈23.44°). They are the same
boundaries the photoperiod and stellar layers use.]

---

## Frost-risk season by zone

Frost risk in this layer is a **climate-norm classification**, not a
forecast. It says: *during this calendar month at this latitude, is frost
something the climate would normally see?* It does **not** say *frost
will happen this week.*

| Zone          | Frost-season months (NH)   | Frost-season months (SH)   | Label inside frost season   |
|---------------|----------------------------|----------------------------|------------------------------|
| tropical      | none                       | none                       | `no frost`                   |
| subtropical   | Dec, Jan, Feb              | Jun, Jul, Aug              | `frost-possible`             |
| temperate     | Oct – Apr                  | Apr – Oct                  | `frost-likely`               |
| boreal/polar  | all except Jun, Jul, Aug   | all except Dec, Jan, Feb   | `frost-likely`               |
| boreal/polar  | (Jun-Aug NH summer)        | (Dec-Feb SH summer)        | `frost-possible` (high summer can still frost) |

Three labels are used:

- `no frost` — climate-norm zero risk (tropical year-round).
- `frost-unlikely` — outside the climate-norm frost season for the zone.
- `frost-possible` — climate-norm low frost risk (subtropical winter
  inland; boreal/polar high summer).
- `frost-likely` — inside the climate-norm core frost season.

The southern hemisphere months are mirrored by **6 months**. The
boundary months (Apr in temperate NH, Oct in temperate SH) are included
in the frost season because actual frost dates at the edges of the
season are highly variable; better to flag the possibility than to miss it.

[ANALYTICAL CONTRIBUTION — month boundaries are simple thresholds, not
historical climate records. A real "first/last frost date" map would
pull from station data; this is the offline first cut.]

---

## Vegetation phenology stage cycle

Vegetation moves through a recognizable seasonal arc in temperate and
boreal latitudes:

```
dormant → awakening → leafing → flowering → fruiting → ripening → senescing → dormant
```

The Astrolabium maps calendar months to stages using the **northern
hemisphere temperate zone** as the reference. The southern hemisphere
flip is a generic +6 month rotation.

| Month (NH) | Month (SH) | Stage         |
|------------|------------|---------------|
| Jan        | Jul        | dormant       |
| Feb        | Aug        | awakening     |
| Mar        | Sep        | awakening     |
| Apr        | Oct        | leafing       |
| May        | Nov        | flowering     |
| Jun        | Dec        | fruiting      |
| Jul        | Jan        | fruiting      |
| Aug        | Feb        | ripening      |
| Sep        | Mar        | senescing     |
| Oct        | Apr        | senescing     |
| Nov        | May        | dormant       |
| Dec        | Jun        | dormant       |

### Tropical exception

Tropical latitudes (|lat| < 23.5°) bypass this cycle entirely. Tropical
vegetation responds to wet/dry rhythms rather than thermal seasons.
The layer returns a special stage of `"continuous"` with a note that
the temperate phenology mapping does not apply. A practitioner near the
equator should look to the photoperiod layer and to local rainy-season
knowledge for ecological context, not to this stage map.

[ANALYTICAL CONTRIBUTION — the stage map is for "temperate northern
deciduous" biome as the implicit type specimen. A practitioner in a
temperate evergreen forest, a Mediterranean chaparral, or a high
desert will see different actual phenology. The map is a starting
orientation, not a botanical guarantee.]

---

## Growing-degree-day (GDD) state — coarse only

Growing-degree-day (GDD) is the agricultural heat-accumulation metric:
sum of (mean daily temperature − base temperature) over the growing
season, used to predict crop maturity, pest emergence, and
frost-safe planting windows. **Computing real GDD requires real daily
temperature data, which this layer does not have.**

What the layer returns instead is a **classification of seasonal
intensity** based on month and latitude:

| Intensity   | Meaning                                                          |
|-------------|------------------------------------------------------------------|
| `none`      | Off-season — climate-norm cool season, minimal heat accumulation. |
| `low`       | Shoulder season — modest accumulation typical.                   |
| `moderate`  | Active accumulation but not peak.                                |
| `high`      | Peak GDD-accumulation period for the zone.                       |

For temperate northern-hemisphere latitudes:

- **Peak** (`high` if |lat| < 50°, `moderate` otherwise): May, Jun, Jul, Aug.
- **Shoulder** (`low`): Apr, Sep.
- **Off** (`none`): Oct – Mar.

Southern hemisphere flipped by 6 months. Tropical always `high`
(year-round accumulation). Boreal/polar inherits the temperate framework
but realistically rarely reaches `high` (the cap at |lat| > 50° catches
this).

This is a **proxy for season-shape, not a true GDD count**. Useful for
the question "am I in the heat-accumulation season at all" — not for
"how many GDD have accumulated since Jan 1." For actual GDD, use a
weather service.

[ANALYTICAL CONTRIBUTION — the intensity bins are heuristics keyed to
month and latitude band. They do not derive from temperature
climatology data.]

---

## What this DOES get right

- **The general shape of the seasonal cycle at any latitude.** A
  practitioner at 45°N in October knows the layer will report leaf-fall,
  cool-season GDD, frost-risk-likely — and this is correct as a
  climate-norm description of October at 45°N. The shape is right
  even if any specific day's weather is not.
- **The practitioner's orientation to their local seasonal arc.** The
  composite output answers the practical question *"where am I in the
  ecological year at my latitude?"* with a defensible four-axis read
  (zone, frost, phenology, intensity) every time.
- **The hemisphere flip.** A practitioner in Buenos Aires in July gets
  a coherent southern-hemisphere winter answer. The flip is mechanical
  but consistent.
- **The tropical exception.** Equatorial latitudes get a `continuous`
  vegetation stage and `high` GDD year-round, which is the correct
  high-level framing even if the specific tropical biome the
  practitioner is in has its own wet/dry rhythm.
- **The latitude-band climate zones.** The five-zone classification is
  coarse but well-aligned with the latitudes Earth's ecology actually
  organizes around (the tropics, the temperate belt, the polar circles).

---

## What this DOES NOT get right

Be honest with the practitioner about every one of these.

- **Year-to-year variability.** This is a climate-norm model, not a
  weather model. The actual frost date this year may be three weeks
  before or after the climatology suggests. El Niño / La Niña years
  shift everything. The model does not know what year it is.
- **Microclimate effects.** Elevation, coastal proximity, urban heat
  islands, valley cold-air drainage, south-facing slopes versus
  north-facing slopes — all of these can shift local ecology by weeks
  or whole seasons. A practitioner at 1,800m elevation in California
  experiences a colder, shorter growing season than the temperate-zone
  default suggests. The model does not know the elevation.
- **Climate-change shifts.** The climate norms reflect roughly
  mid-20th-century baselines. First-frost dates have moved later by
  weeks in many regions; last-frost dates have moved earlier; growing
  seasons have lengthened; phenology has shifted by days to weeks. The
  model does not currently account for these shifts and would need a
  decadal correction term to do so. Sprint D could address this; the
  current layer does not.
- **Specific weather events.** Heat waves, cold snaps, drought, atypical
  precipitation patterns. None of these are visible to the model. If
  the practitioner needs to know whether to cover the tomatoes tonight,
  this layer cannot help — they need a weather forecast.
- **Local biome specificity.** A temperate-zone Mediterranean climate
  (Los Angeles), a temperate-zone humid continental climate (Boston),
  and a temperate-zone oceanic climate (Dublin) all map to the same
  `temperate` zone label but have very different ecological calendars.
  The model under-discriminates within the temperate band.
- **Polar twilight nuance.** Within the polar band, the model collapses
  to a single "no real growing season" framing. The actual edge of the
  polar zone (~67°N at southern Iceland) has a brief but real growing
  season; the high Arctic does not. The model treats them the same.

---

## Use cases for the practitioner

The Ecological Markers layer is built for these questions:

- **"Am I in frost season where I am?"** The `frost_risk` output answers
  this. A `frost-likely` reading in October at 45°N is the climate
  telling the practitioner: *yes, your region typically has frost risk
  starting around now.* Not a forecast — a context.
- **"What's the general shape of the ecological year I'm in?"** The
  composite (zone + frost + vegetation + GDD) gives a four-axis read
  that locates the moment in the seasonal arc. Useful for ritual
  planning, for connecting the calendar to the land, for noticing
  whether the symbolic season matches the actual season.
- **"What's the seasonal arc — am I closer to dormancy or fruiting?"**
  The vegetation stage is the answer. *Senescing* in October NH means
  the leaves are coming down; *flowering* in May means the meadows are
  starting. The practitioner can match practice to season.
- **"Is the land working right now?"** The GDD intensity says whether
  the heat-accumulation engine is running (the answer is most
  practitioner-relevant in spring/fall transitions, when it goes from
  `low` to `none` or back).

---

## Connection to the four temporal bodies

The Ecological Markers layer is the **Gross layer's local-environment
face**. The four temporal bodies cooperate:

- The **Stellar Layer** says what cosmic moment we are in — which
  Buddha-month, which lunar mansion, which solar term, which yuga.
- The **Soul Layer** says which Primeval Law is active under the
  current trigram / lunar phase.
- The **Astral Layer** (LGBF) says which Extraordinary Vessel is open.
- The **Gross Layer** says what the body is doing right now — which
  organ-clock window, which Divine Hour.
- The **Ecological Layer** extends the Gross layer outward: what is the
  LAND doing right now, at this latitude, in this climate norm?

Together, this composite produces meaningfully different practitioner
moments from the same astronomy:

- A **Spring Equinox new moon at a temperate northern latitude during
  the leafing stage** is a moment of explicit beginning, the
  astronomical and ecological doors opening together.
- The **same Spring Equinox new moon at a tropical latitude during the
  wet season** is a different moment entirely — the astronomy still
  marks the equinox, but the ecology has no leafing stage to crown it,
  and the wet-season context is what the practitioner actually
  inhabits.
- An **Autumn Equinox at a temperate southern latitude during the
  flowering stage** is yet another configuration: the calendar's
  "harvest" is the land's "bloom."

The instrument's job is to surface all of these together so the
practitioner is not stranded inside a northern-hemisphere-by-default
reading of their own moment.

[ANALYTICAL CONTRIBUTION — the integration of ecological markers with
the four-body framework is the Astrolabium's own composition. The
individual layers are independently sourced; the synthesis is the
instrument's.]

---

## Common errors

- **Treating the model as precise.** It is not. A `frost-likely` reading
  is a climate-norm statement, not a weather forecast. A `flowering`
  reading is a seasonal-arc claim, not a botanical census. Report the
  outputs *as climate-norm context*, never as observations.
- **Claiming `frost-likely` means frost will happen this week.** It
  means the current month is inside the climate-norm frost season for
  the zone. The actual first/last frost dates may be weeks off either
  side, and any given week may pass without frost even in deep frost
  season. The label is *seasonal*, not *forecast*.
- **Reading the temperate vegetation stages as universal.** The stage
  map (`leafing`, `fruiting`, `senescing`, etc.) is derived from
  *temperate northern-hemisphere deciduous* phenology. A practitioner
  in a Mediterranean climate, a tropical wet-dry climate, a humid
  subtropical climate, a high-desert climate, or a temperate evergreen
  forest will see actual phenology that does not match the stage label.
  Use the stage as orientation, not as botany.
- **Reading the southern hemisphere flip as biome-aware.** It is not.
  The flip is a generic +6 month shift. It captures the seasonal
  reversal but not any of the actual differences between (say) the
  Patagonian temperate zone and the New England temperate zone. The
  practitioner in Tasmania gets a reasonable orientation; they do not
  get a Tasmania-specific ecology.
- **Reporting GDD numbers as if they were computed.** The layer does
  not compute GDD totals. It returns an intensity classification
  (`none` / `low` / `moderate` / `high`). Any practitioner doing real
  agricultural work should pull GDD from a weather service.
- **Confusing this layer with the photoperiod layer.** The composite
  state includes a `photoperiod_summary` field, but the photoperiod
  layer itself (daylight hours, civil twilight, seasonal arc) is a
  separate engine and has its own rules file. The ecological layer
  consumes the photoperiod summary as context; it does not replace it.
- **Asking it about weather.** It cannot answer. Specific events,
  heat waves, droughts, atypical precipitation — none of this is
  visible. Direct the practitioner to a weather service.
- **Forgetting that climate norms are mid-20th-century.** First-frost
  dates have moved later, growing seasons have lengthened, phenology
  has shifted by days to weeks across much of the temperate world over
  the last several decades. The model's frost-season months are not
  updated for that drift.

---

## Cross-references

- `.claude/rules/photoperiod.md` — daylight-hours and civil-twilight
  layer; the ecological composite consumes this as `photoperiod_summary`.
  Photoperiod is the rigorous astronomical input; ecological markers are
  the climate-norm heuristic overlay.
- `.claude/rules/stellar-layer.md` — what cosmic moment we are in;
  the ecological layer says what the LAND is doing inside that moment.
- `.claude/rules/divine-calendar.md` — the macro-temporal frame
  (13 lunar months, six Great Rites). The ecological layer is what
  grounds the abstract calendar in the practitioner's local biosphere.
- `.claude/rules/temporal-bodies.md` — how the Stellar / Soul / Astral
  / Gross / Ecological layers compose into a single practitioner moment.
- `.claude/rules/how-to-use-this-instrument.md` — when to surface
  ecological markers in a reading and how to present their epistemic
  status.
- `astrolabium/src/engine/ecological_markers.py` — the engine itself.
  All four functions (`climate_zone`, `frost_risk_state`,
  `vegetation_stage`, `growing_degree_day_state`) and the composite
  `ecological_markers_state` live there.
- `astrolabium/src/engine/photoperiod.py` — the upstream daylight
  engine.
