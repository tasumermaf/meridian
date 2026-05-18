# The Stellar Layer — Fifth Temporal Body

> The slowest, deepest layer the instrument reads. Where the four
> existing bodies (Soul, Solar Keys, Astral, Gross) measure the
> moment's place within the lunar month, the solar day, and the
> two-hour vessel rotation, the Stellar Layer situates that moment
> within the sidereal year, the agricultural season, the
> cross-tradition festival calendar, and the Tibetan lunar reckoning.
> This is the layer that answers "where in the great wheel are we?"

---

## What the Stellar Layer is

The **Stellar Layer** is the fifth temporal body of the Astrolabium
Caudae Rubrae. It was added in Sprint A (May 2026) to fill the
architectural gap named by Xue Mei's *Living Time Keepers* white paper
Section VI, which identified that the four-body instrument as
originally specified read the moment's *internal* structure (lunar
phase, solar position, vessel rotation, organ window) but lacked any
reading of the moment's *cosmic* situation — where the Sun and Moon
actually stand against the fixed stars, which seasonal threshold is
governing, which festival window is nearby, and which traditional
month the moment falls within in calendars other than the Damanhurian.

The four original bodies are *fast*. The Gross body ticks every two
hours, the Astral every two hours on its own clock, the Solar Keys
twice a day, the Soul every five days. The Stellar Layer is *slow*:
mansions shift over thirteen-day intervals, solar terms over
fifteen-day intervals, festivals on a yearly cycle, Tibetan months on
a roughly monthly cycle whose alignment to Gregorian drifts each year.

The Stellar Layer does not displace the other four. It contextualizes
them. A Two-Body Law Unity inside the Saga Dawa window is a different
moment from the same Two-Body Unity in an ordinary lunation. The
engine surfaces the difference via the same compound/resonance
machinery already in use for the Soul/Astral/Key intersections,
extended to recognize the new layer.

[ANALYTICAL CONTRIBUTION — the integration of these four sub-systems
into a single layer that reads with the existing four bodies. Each
sub-system is [SOURCE]-attested separately.]

## The Five Components

The Stellar Layer is composed of five tightly-coupled sub-systems.
Each has its own dedicated rules file; this file is the
architectural overview that explains how they fit together.

| # | Sub-system                        | Tradition                            | What it gives the layer                                                            | Detail file                                |
|---|-----------------------------------|--------------------------------------|------------------------------------------------------------------------------------|--------------------------------------------|
| 1 | **28 Lunar Mansions** (二十八宿)   | [SOURCE: Chinese classical astronomy] | Sidereal position of Sun and Moon against the actual stellar background           | `.claude/rules/28-lunar-mansions.md`       |
| 2 | **24 Solar Terms** (二十四节气)    | [SOURCE: TCM / Chinese canon]         | Tropical seasonal markers at every 15° of solar ecliptic longitude                | `.claude/rules/24-solar-terms.md`          |
| 3 | **Sacred Festival Registry**      | [SOURCE: Multi-tradition]             | Proximity to canonically-dated festivals across Buddhist, Damanhurian, Hellenistic, and Christian calendars | `.claude/rules/sacred-festivals.md`        |
| 4 | **Tibetan Buddhist Calendar**     | [SOURCE: Tibetan Buddhist canon]      | Tibetan lunar month and day, used to locate Buddhist observances                  | `.claude/rules/tibetan-buddhist-calendar.md` |
| 5 | **The Root Mansion Bridge**       | [ANALYTICAL CONTRIBUTION]             | The cross-tradition link tying the four above into a single readable stellar state | (this file, §"The Saga Dawa Bridge")       |

The fifth is not a separate data source — it is the architectural
integration that makes the other four legible together. It was
discovered while specifying the layer: the Buddhist Saga Dawa month,
the Chinese 28-mansion system, the Tibetan calendar, and the solar
terms turned out to share a single anchoring star — the **Root
Mansion** Dī (氐), the Heart of the Azure Dragon — which is operative
in all four traditions simultaneously during Saga Dawa.

## Sidereal versus Tropical — Not a Bug

The Stellar Layer mixes two reference frames. **The 28 Lunar Mansions
are sidereal. The 24 Solar Terms are tropical.** This is correct per
each tradition's canon and must not be normalized.

- **Sidereal** = position measured against the fixed background stars.
  The mansions are anchored to actual reference stars (Spica anchors
  Jiǎo 角, Antares anchors Xīn 心, the Pleiades anchor Mǎo 昴). When
  the engine reports "the Sun is in 婁 Lóu," it means the Sun's
  position against the stars, not against the seasonal calendar. The
  **Lahiri ayanamsa** is applied to convert tropical ecliptic
  longitude (what astronomy libraries return by default) into the
  sidereal longitude the Chinese system requires.
- **Tropical** = position measured against the equinoxes and
  solstices. The 24 Solar Terms are tropical *by definition* — Chūnfēn
  is the moment the Sun crosses the spring equinox, regardless of
  which sidereal mansion happens to host that point in the current
  precessional era. Two thousand years ago Chūnfēn occurred in the
  mansion Lóu; today it occurs in 室 Shì several mansions earlier.

This is not a contradiction. The mansions tell you which stars are
behind the Sun and Moon right now. The solar terms tell you which
agricultural threshold the Earth has crossed in its orbital
relationship to the Sun. Both are real, both are useful, and conflating
them produces the centuries-old astrological category error that
Western tropical traditions and Indian sidereal traditions have
periodically fought over without resolution. The Astrolabium does not
choose between them; the engine reports both, correctly, in parallel.

[MATHEMATICAL FACT — axial precession is currently ~50.3 arcseconds
per year, displacing the tropical equinox westward against the
sidereal frame at about one degree per 71.6 years. The current Lahiri
ayanamsa is approximately 24.2°.]

## How the Layer Integrates with the Four Existing Bodies

The Stellar Layer is read alongside Soul, Solar Keys, Astral, and
Gross. The orchestrator returns all five layers in a single state
object. The compound detection machinery — already used to flag
Two-Body Law Unity, Key-Amplified Unity, Key-Derivative Unity, and
Anatomical Intersection — is extended to recognize stellar-layer
resonances.

The new compound predicates the engine evaluates:

### Mansion-Law Resonance

**Definition:** The active Primeval Law (Soul layer) and the current
Lunar Mansion (Stellar layer) belong to the same celestial palace or
share a tradition-attested correspondence (Wood palace ↔ Geometric
Essence, etc.).

When the slow lunar cycle and the much slower sidereal lunar position
are pointing at the same quality, the moment carries a long-arc
underline that a Two-Body Unity alone does not provide. These windows
are rarer than Two-Body Unity (which happens several times per lunar
quarter) and more common than Key-Amplified Unity (which requires
threading three layers at a cusp).

### Solar Term Threshold

**Definition:** The current moment falls within ±24 hours of a Solar
Term boundary crossing.

The crossing itself is a singular instant; the threshold window flags
the day-around-the-instant when the seasonal Qi is transitioning.
Practitioners working with seasonal observances treat these windows
specially; the engine simply surfaces them as flags on the state.

### Great Rite ↔ Solar Term Convergence

**Definition:** A Solar Term boundary falls on the same calendar day
as one of the six Damanhurian Great Rites.

This is the architectural payoff of holding both reference frames in
parallel. The four cardinal solar terms — Chūnfēn (Spring Equinox),
Xiàzhì (Summer Solstice), Qiūfēn (Autumn Equinox), Dōngzhì (Winter
Solstice) — align by definition with four of the six Great Rites, and
the engine flags the convergence so the practitioner reading the
state sees both labels at once. The other two Great Rites (Day of the
Dead, Divine Marriage) do not align with cardinal terms and surface
through the Festival Registry instead.

### Festival Proximity Window

**Definition:** The current moment is within ±N days (default 14) of
a registered festival in the cross-tradition registry.

The festival registry is multi-tradition by design: Damanhurian Great
Rites, Buddhist observances (Saga Dawa, Vesak, the four Düchen days,
Losar), Hellenistic festivals where dates are canonically attested,
Christian liturgical anchors that have absorbed older solar markers.
Proximity is reported as a list of nearby festivals with day-offsets,
not as a single "current festival" — adjacent observances stacking
in the same window is itself information.

### Tibetan-Damanhurian Month Resonance

**Definition:** The current Tibetan lunar month and the current
Damanhurian Divine Month carry semantically aligned themes per the
cross-correspondence table maintained in `sacred-festivals.md`.

The Tibetan calendar and the Damanhurian calendar are both lunar but
anchor differently (Tibetan: Losar near the New Moon of February;
Damanhurian: Year start at the New Moon nearest the autumn equinox).
They do not always align by month-number, but specific months carry
similar qualities — Saga Dawa (Tibetan month 4) and TASUMER
(Damanhurian month 5, the Builder) both fall in a late-spring
construction-and-awakening window, and that semantic resonance is
flagged when both are active.

## Orchestrator State Keys

The orchestrator at `astrolabium/src/astrolabium.py` returns the
Stellar Layer through four new top-level keys on the state dictionary.
They are added without disturbing any of the existing keys; downstream
code that reads `state['soul_law']`, `state['organ']`, etc. continues
to work unchanged.

### `state['stellar']`

Returned by `engine.stellar.get_stellar_state(dt, lat, lon, tz)`.

```python
{
    'sun_mansion':       {'index': int, 'chinese': str, 'pinyin': str, 'english': str, 'palace': str},
    'moon_mansion':      {'index': int, 'chinese': str, 'pinyin': str, 'english': str, 'palace': str},
    'sun_ecliptic_lon':  float,    # sidereal degrees, 0-360
    'moon_ecliptic_lon': float,    # sidereal degrees, 0-360
    'ayanamsa':          float,    # Lahiri ayanamsa applied, current ~24.2°
    'mansion_palace_resonance': bool,  # True if Sun and Moon share a palace
}
```

The two mansion sub-dicts give the full identification — numeric index
(1–28), Chinese glyph, pinyin transliteration, English name (e.g.
"Root", "Stomach", "Heart"), and palace assignment (Azure Dragon,
Black Tortoise, White Tiger, Vermilion Bird). The two longitudes are
sidereal — the Lahiri ayanamsa has already been subtracted from the
underlying ephemeris's tropical output.

### `state['solar_term']`

Returned by `engine.solar_terms.get_solar_term_state(dt)`.

```python
{
    'current':       {'index': int, 'chinese': str, 'pinyin': str, 'english': str, 'longitude': int},
    'next':          {'index': int, 'chinese': str, 'pinyin': str, 'english': str, 'longitude': int},
    'next_crossing': datetime,    # ISO datetime UTC of next term boundary
    'days_to_next':  float,       # decimal days until next_crossing
    'is_cardinal':   bool,        # True if current term is equinox or solstice
    'in_threshold_window': bool,  # True if within ±24h of any boundary
}
```

The `current` term is the most recently entered; the `next` term is
the upcoming boundary. `days_to_next` is a decimal — useful for
displaying countdowns. The cardinal flag identifies the four
equinox/solstice terms that align with Great Rites.

### `state['festival_proximity']`

Returned by `engine.festivals.get_festival_proximity(dt,
window_days=14)`.

```python
[
    {
        'name':         str,         # canonical name
        'tradition':    str,         # 'Damanhurian', 'Buddhist', 'Hellenistic', 'Christian', ...
        'date':         date,        # the festival's date in the current year
        'days_offset':  int,         # negative = past, 0 = today, positive = upcoming
        'is_active':    bool,        # True if the festival itself is today or within its own window
        'notes':        str,         # tradition-specific context
    },
    ...
]
```

A list, ordered by absolute day-offset (closest first). Empty list if
no festivals are in the window. The `window_days` parameter is
adjustable; the default of 14 catches both the approach and the
afterglow of major observances. The Buddhist Düchen days, when active,
appear here with their tradition-attested merit-multiplier notes; the
engine does not editorialize about merit, it just relays what the
tradition records.

### `state['tibetan_month']`

Returned by `engine.festivals.get_tibetan_month(dt)`.

```python
{
    'month_number':  int,       # 1-12, or 13 for an intercalary month
    'month_name':    str,       # Tibetan name, e.g. 'Saga Dawa' for month 4
    'day_number':    int,       # 1-30
    'is_intercalary': bool,
    'phase_label':   str,       # 'waxing', 'waning', or 'full'/'new' on those days
}
```

The Tibetan calendar uses its own lunation-anchored monthly system. The
month number does not align to the Gregorian or Damanhurian month
numbers; Saga Dawa is month 4 in the Tibetan reckoning but typically
falls in May–June Gregorian and inside the Damanhurian TASUMER or
MENON, depending on the year's intercalation pattern.

## The Saga Dawa Bridge — Worked Example

The May 17 2026 *Saga Dawa: Awakening the Root of the Dragon* source
PDF gave the architectural seed for this layer. On **May 18, 2026, at
Damanhur (45.27°N, 7.65°E, Europe/Rome)**, the engine returns the
following Stellar Layer state, which threads all four sub-systems
through a single observance:

| Layer field                        | Value                                                                              |
|------------------------------------|------------------------------------------------------------------------------------|
| `state['stellar']['sun_mansion']`  | `{index: 16, chinese: '婁', pinyin: 'Lóu', english: 'Bond', palace: 'White Tiger'}`  |
| `state['stellar']['moon_mansion']` | `{index: 17, chinese: '胃', pinyin: 'Wèi', english: 'Stomach', palace: 'White Tiger'}` |
| `state['solar_term']['current']`   | `{index: 7, chinese: '立夏', pinyin: 'Lìxià', english: 'Start of Summer'}`           |
| `state['solar_term']['next']`      | `{index: 8, chinese: '小满', pinyin: 'Xiǎomǎn', english: 'Grain Buds'}`              |
| `state['solar_term']['next_crossing']` | `2026-05-21T...` (Xiǎomǎn boundary)                                            |
| `state['tibetan_month']`           | `{month_number: 4, month_name: 'Saga Dawa', day_number: 1, ...}`                   |
| `state['festival_proximity']`      | `[{name: 'Saga Dawa', tradition: 'Buddhist', days_offset: 0, is_active: True, ...}, ...]` |

The reading: the Sun and Moon are both in the White Tiger palace
(Western quadrant of the celestial sphere, autumn-aligned in Chinese
correspondence — note the cross-hemisphere irony of the Western palace
hosting a spring-into-summer transition). The day falls between two
adjacent solar terms, three days before the Xiǎomǎn boundary. The
Tibetan calendar registers the start of Saga Dawa, the Buddhist month
that commemorates Shakyamuni's birth, enlightenment, and
parinirvana.

The cross-tradition resonance the source PDF identifies is not visible
in the mansion list above (Lóu and Wèi are White Tiger mansions, not
the Root Mansion Dī of the Azure Dragon) — but the *thesis* of the
PDF is that Saga Dawa is the month when practitioners ritually return
to the Root Mansion as a regenerative anchor regardless of where the
Sun and Moon happen to be in the sidereal frame during that lunation.
The Root is conceptually present as the month's organizing principle,
not as a transiting position. The engine surfaces Saga Dawa via the
`festival_proximity` and `tibetan_month` fields; the Root Mansion's
operative role inside Saga Dawa is documented in
`.claude/rules/sacred-festivals.md` rather than computed as a
transit.

This worked example demonstrates the layer doing what it was built to
do: read four traditions in parallel, surface the active sidereal and
tropical states without conflating them, and identify the festival
context the practitioner is operating inside.

## Connection to *Living Time Keepers* Section VI

Xue Mei's *Living Time Keepers* white paper (April 2026) closed with
a Section VI titled "The Missing Stellar Layer." The argument was
that the Astrolabium as then-specified was internally complete — the
four bodies, the compounds, the shared substrate — but cosmologically
shallow. The instrument knew which Primeval Law the moon's phase was
carrying; it did not know which stars the moon was actually in front
of. It knew when a Two-Body Unity was forming; it did not know
whether that Unity was forming inside Saga Dawa or in an ordinary
lunation. It knew the Damanhurian Divine Calendar; it did not know
the Buddhist or Tibetan calendars at all.

Section VI named four required additions: a sidereal sky model, a
seasonal threshold model, a cross-tradition festival registry, and at
least one non-Damanhurian lunar calendar of sufficient
operational depth to register the major Buddhist observances. The
Stellar Layer implements exactly those four. The 28-mansion engine is
the sidereal sky model; the 24-term engine is the seasonal threshold
model; the festival registry is the multi-tradition observance
catalog; the Tibetan calendar is the chosen non-Damanhurian lunar
system because the Tibetan canon (a) registers Buddhist observances
with the canonical depth required, (b) interoperates cleanly with the
28-mansion sidereal frame through the shared Indo-Tibetan astronomical
inheritance, and (c) provides the Saga Dawa anchor that the Root
Mansion thesis turns on.

The Section VI gap is closed. The Stellar Layer is the named missing
piece, built to the named specification, integrated through the named
compound machinery.

## Connection to the Saga Dawa Source PDF

The May 17 2026 *Saga Dawa: Awakening the Root of the Dragon*
document is the source-side anchor of the layer. It supplied:

- The identification of **氐 Dī (the Root Mansion, the Heart of the
  Azure Dragon)** as the operative stellar anchor of the Saga Dawa
  month. This is the cross-tradition bridge — a Chinese mansion that
  serves as the metaphysical root of a Tibetan Buddhist observance.
- The thesis that Saga Dawa is a **regenerative dragon-root window**
  in which the practitioner's relationship to the Azure Dragon
  palace is re-anchored to its Heart. Not a transit event, an
  operative observance.
- The mapping from the Azure Dragon's seven mansions to seven stages
  of dragon-root awakening, documented per-mansion in
  `.claude/rules/28-lunar-mansions.md`.
- The structural pattern that **each celestial palace has a Heart
  mansion** that operates as that palace's regenerative anchor in
  observances tied to that palace's season. The Azure Dragon's Heart
  is Dī; the White Tiger's Heart is Mǎo 昴 (the Pleiades); the Black
  Tortoise's Heart is Xū 虛; the Vermilion Bird's Heart is Xīng 星.
  Future festival registry entries can hook into the corresponding
  Heart mansion of whichever palace governs the observance.

The PDF is now operationally legible inside the instrument. A
practitioner asking "is Saga Dawa active and what does it mean?" gets
a structured answer: `festival_proximity` lists it, `tibetan_month`
confirms it, the source notes attached in the registry name the Root
Mansion thesis, and `28-lunar-mansions.md` carries the full mansion
catalog with the Azure Dragon's Heart documented.

## Connection to the Rhombic Dodecahedron Thesis

The 28-mansion system is organized as **four palaces of seven mansions
each**. Each palace carries one of the four cardinal directions, one
of four animal-totems (Azure Dragon East, Vermilion Bird South, White
Tiger West, Black Tortoise North), and one of four Wu Xing element
sub-clusters. The total of 28 mansions does not divide evenly into
the Astrolabium's 12-fold rhombic-dodecahedral matrix — and that is
the architectural point.

The rhombic dodecahedron has twelve faces; the Damanhurian Divine
Calendar has twelve months (plus VADUSFADAHM as the intercalary
thirteenth); the TCM Organ Clock has twelve windows; the trigram-law
architecture has six cyclic Laws plus two Keys for a total of eight
trigrams. The 28-mansion system operates at a different granularity
— roughly 12.86 days per mansion, compared to the 30-day months and
two-hour organ windows. It does not need to align with the twelve-fold
matrix because it occupies a different scale of the integration: the
twelve-fold matrix governs the moment's *operative* timing, the
twenty-eight-fold system governs the moment's *sidereal* situation.

What does align cleanly: the four palaces of the 28-mansion system
map to the four cardinal-direction Great Rites (Spring Equinox /
Vermilion Bird, Summer Solstice / Azure Dragon — or, in the Damanhur
attribution, the assignment depends on whose canonical mapping you
adopt and the engine carries the documented options as data rather
than picking one). The four palaces × seven mansions geometry
extends the twelve-fold matrix rather than disrupting it: twelve for
the operative timing of the practitioner's day, twenty-eight for the
contextual placement of that day inside the sidereal year, both
readable in parallel through the same state object.

The Tappetino Proof gives the twelve-fold rhombic geometry its
foundation. The Stellar Layer adds a parallel sidereal foundation
that does not compete with that geometry — it situates it. The
practitioner stands inside the twelve-fold cocoon; the cocoon stands
inside the twenty-eight-fold stellar context. The instrument now
reads both.

[ANALYTICAL CONTRIBUTION — the recognition that the 28-mansion
sidereal scale and the 12-fold rhombic-dodecahedral operative scale
are complementary rather than competing, and that they can be read in
parallel through a single state object.]

## What the Stellar Layer is NOT

- **It is not astrological prediction.** The instrument reports which
  mansion the Sun is in. It does not say "you will have a difficult
  Tuesday." Predictive astrology is outside the Astrolabium's
  epistemic charter.
- **It is not a personality system.** The mansion the moon was in at
  the practitioner's birth is not computed, not stored, and not
  reported. Natal-chart functionality is intentionally absent.
- **It is not prescriptive.** "Saga Dawa is active" is a fact the
  engine reports. What the practitioner does with that fact is
  between them and the moment. The instrument displays; it does not
  advise.
- **It is not a substitute for the four existing bodies.** A
  practitioner reading the state still needs the Soul, Solar Keys,
  Astral, and Gross layers. The Stellar Layer adds context; it does
  not replace the operative timing.
- **It is not a single-tradition reading.** The festival registry is
  multi-tradition by design. The instrument does not privilege the
  Damanhurian or the Buddhist or the Hellenistic calendar. It reports
  what each tradition records for the current moment.

## Sprint B — The Deep Sky Layer (added May 2026)

After Sprint A locked the Stellar Layer's four sub-systems, Sprint B
added four further sub-systems extending the temporal architecture to
its full sky-deep reach. All four are now operational:

- **Axial precession** — the Lahiri ayanamsa, the current sidereal
  position of the vernal equinox, the current zodiacal Age (Pisces,
  ~80% complete), the next transition (Aquarius, ~2440 CE), and the
  precessional pole-star sequence (Thuban → Polaris → Vega across
  the 25,772-year Great Year). See `.claude/rules/axial-precession.md`.
- **Heliacal risings** — first-dawn appearances of 22 named stars at
  the practitioner's location, including the canonical Sothic-cycle
  anchor (Sirius/Sopdet at Egyptian latitudes), the Pleiades
  agricultural marker, the Royal Stars of ancient Persia, and the
  Chinese 28-mansion reference stars. See
  `.claude/rules/heliacal-risings.md`.
- **Major lunar standstills** — the 18.6-year nodal cycle, current
  cycle phase, next major and minor peaks, the ascending node's
  sidereal regression rate. The last major standstill was 2025-03-22;
  the next is ~2043. See `.claude/rules/lunar-standstills.md`.
- **Vedic yuga / kalpa deep-time** — the nested cosmological cycles
  of Sanskrit astronomy. Current yuga (Kali, ~1.2% complete), Mahā
  Yuga position, Kalpa context (the Shvetavārāha Kalpa, 7th
  Manvantara of 14, 45.67% through the Day of Brahmā). See
  `.claude/rules/vedic-yuga.md`.

These four engines added 71 tests (647 → 718 baseline) and four new
orchestrator state keys: `precession`, `heliacal`, `lunar_standstills`,
`vedic_time`. Backward compatibility preserved for all Sprint A and
original-baseline keys.

The Deep Sky Layer is what makes the Astrolabium answer not only
"what is the alchemical quality of this moment" but also "what is
its placement in the longest cosmological cycles human cultures have
measured." A practitioner can now ask: where are we in the Age,
when does Sirius rise here, are we in a standstill window, how
many years remain in the Kali Yuga.

## What is Still Out of Scope

The remaining gap from Xue Mei's *Living Time Keepers* Section VI is
the Ecological Layer (Tier 3 in the original sprint plan): live
environmental data ingestion (vegetation phenology, precipitation,
migration tracking). Reserved for Sprint C, which is its own planning
round once the data-source decisions are made.

If a user asks about ecological-layer features, the correct answer is
"queued for Sprint C; not currently implemented." Honesty about scope is part of
the instrument's authority.

## What is Out of Scope (Tier 3, Sprint C)

The Stellar Layer reads the *celestial* situation of the moment. It
does not read the *ecological* situation. The following are
intentionally out of scope for the entire Astrolabium project as
currently planned, and would require a separate planning round:

- Live weather data, local microclimate sensors, real-time
  atmospheric readings
- Bird migration corridors, regional flowering and fruiting cycles,
  ecological observances tied to local species
- Geomagnetic conditions, solar storm activity, real-time space
  weather feeds
- Tide tables, river flow rates, hydrological observances

These are valid temporal markers in their own traditions, and an
instrument that integrated them would be more cosmologically
complete than the Astrolabium. They are not on the roadmap. If a
user asks, the answer is "Tier 3, separate planning round, not
currently scoped."

## Cross-References

- `.claude/rules/28-lunar-mansions.md` — the sidereal sky model
- `.claude/rules/24-solar-terms.md` — the seasonal threshold model
- `.claude/rules/sacred-festivals.md` — the cross-tradition festival registry
- `.claude/rules/tibetan-buddhist-calendar.md` — the Tibetan lunar system
- `.claude/rules/astrolabium-core.md` — the system identity and the four-body architecture this layer extends
- `.claude/rules/temporal-bodies.md` — the four existing bodies the Stellar Layer reads alongside
- `.claude/rules/divine-calendar.md` — the Damanhurian calendar the festival registry interoperates with
- `.claude/rules/tappetino-proof.md` — the rhombic-dodecahedral foundation the layer extends
- `docs/specs/living_time_keepers.md` — Xue Mei's white paper, Section VI of which named this layer as required
- `docs/sources/saga_dawa_root_of_the_dragon.pdf` — the source for the Root Mansion bridge
- `astrolabium/src/engine/stellar.py` — the engine module producing `state['stellar']`
- `astrolabium/src/engine/solar_terms.py` — the engine module producing `state['solar_term']`
- `astrolabium/src/engine/festivals.py` — the engine module producing `state['festival_proximity']` and `state['tibetan_month']`
