# Astrolabium Core — System Identity and Vocabulary

> The single most important file. When in doubt about what the
> instrument is or what its non-negotiable constraints are, this file
> governs.

---

## What the Astrolabium Is

The **Astrolabium Caudae Rubrae** (*L'Astrolabio Coda Rossa*, the Red
Tail Astrolabe) is a temporal navigation instrument. It answers one
question: **what is the alchemical quality of this moment?**

It tells you what the moment is *made of*: which cosmic principles are
active, which energetic channels are open, which organs are peaking,
which lunar phase is governing, which solar threshold may be cusping,
and whether any of these layers happen to be saying the same thing at
the same time.

It is a weather report for the soul. It does not warn, prohibit, or
prescribe. It does not tell you that a moment is "good" or "bad." The
practitioner is assumed competent; the instrument simply displays what
is available.

## The Six Integrated Systems

The Astrolabium synthesizes six ancient systems into a single unified
instrument. All six share a single astronomical substrate: **solar
position and lunar phase at the practitioner's location**.

| # | System                                    | Tradition          | What it gives the instrument                                       |
|---|-------------------------------------------|--------------------|--------------------------------------------------------------------|
| 1 | **Ling Gui Ba Fa** (靈龜八法)             | [SOURCE: TCM]      | Eight Extraordinary Vessels, opened on a 2-hour rotation by formula |
| 2 | **The Six Cyclic Primeval Laws + 2 Keys** | [SOURCE: Damanhurian + Cantong qi] | Six Laws carried by trigrams through the lunar month, two Solar Keys at sunrise/sunset cusps |
| 3 | **The Organ Clock**                       | [SOURCE: TCM]      | Twelve organ windows by solar-position Earthly Branch                |
| 4 | **The Divine Hours**                      | [SOURCE: Damanhurian — Book of Three Responses] | Eight-fold unequal-hour division: 4 day, 4 night                    |
| 5 | **The Sephirotic Week**                   | [SOURCE: Hellenistic / Kabbalistic] | Seven-to-nine day naming inside each lunar quarter                  |
| 6 | **The Divine Calendar**                   | [SOURCE: Damanhurian] | Thirteen lunar months with the Names of Power, six Great Rites, astronomical intercalation |

The **original analytical contribution** is the recognition that these
six systems share a common temporal substrate and the synthesis of them
into a single readable display. The integration itself is
[ANALYTICAL CONTRIBUTION]. Each underlying system is [SOURCE]-attested.

## The Non-Negotiable Constraint

**ALL temporal calculations operate in sacred time. There is no civil
clock anywhere in this system.**

Every hourly function derives from solar position (sunrise/sunset at
the practitioner's actual location). The "hours" of the Earthly Branch
system are the 12-fold division of day and night by solar position —
they predate mechanical clocks by millennia and never matched them.

**Never use:** fixed hour values like "03:00–05:00", `getTimeZhi()` from
`lunar_python` (which uses civil time internally), or any hourly
function that doesn't require latitude and longitude as input.

**Always use:** the location-aware engine functions in
`astrolabium/src/engine/solar.py` and the orchestrator at
`astrolabium/src/astrolabium.py`. Every function signature includes
`(dt, lat, lon, tz)`. There are no exceptions.

This constraint was violated once during early development and required
a complete specification rewrite. See `docs/specs/project_midmortem.md`
for the history if a user asks why the system is designed this way.

## Vocabulary Precision

Use the correct term every time. Sloppy vocabulary in this domain
leads directly to wrong computation, because terms encode tradition
distinctions that matter operationally.

| CORRECT                       | INCORRECT                                |
|-------------------------------|------------------------------------------|
| Primeval Laws                 | spiritual laws, cosmic principles        |
| Extraordinary Vessels         | meridians, channels (those are different) |
| Confluent points              | access points, opening points            |
| Adonaj-Ba                     | chakras                                  |
| Divine Hours                  | magical hours, sacred hours              |
| Unequal hours                 | temporal hours, solar hours              |
| Solar Key                     | sunrise event, sunset event              |
| Gold Key                      | Kǎn ☵ / Fall of Events / Sunrise         |
| Silver Key                    | Lí ☲ / Divinity / Sunset                 |
| Cusping window                | sunrise period, twilight                 |
| Two-Body Law Unity            | Law alignment, Law match                 |
| Key-Amplified Law Unity       | Solar amplification                      |
| Anatomical Intersection       | meridian overlap                         |
| VADUSFADAHM                   | the intercalary month / the 13th month   |
| Sephirotic Week               | the lunar quarter period                 |

## Elemental System Separation (NON-NEGOTIABLE)

Three elemental systems coexist inside the Astrolabium. **They never
cross-compound.** A user encountering "Water" in the system needs to
know which Water.

| System         | Elements                                                 | Context                       | Source                       |
|----------------|----------------------------------------------------------|-------------------------------|------------------------------|
| **Wu Xing**    | Wood, Fire, Earth, Metal, Water                          | Organ Clock, TCM correspondences | [SOURCE: TCM]             |
| **Damanhurian** | Earth, Water, Fire, Air                                 | Primeval Laws, Calendar       | [SOURCE: Damanhurian]        |
| **Trigram**    | Heaven, Earth, Thunder, Wind, Water, Fire, Mountain, Lake | I Ching, Cantong qi Laws    | [SOURCE: Cantong qi]         |

When a user asks about "fire," the answer depends on which fire — the
Heart organ's Wu Xing Fire is not the same as the Damanhurian Fire
element of EOROS (Month 4), and neither is the same as the trigram Lí
☲ that activates as the Silver Key at sunset. All three are correct in
their own systems. None of them substitute for another.

## Type A vs Type B Correspondences

**Type A correspondences** (elemental) remain siloed. Wu Xing Fire does
not equal Damanhurian Fire. They are separate vocabularies.

**Type B correspondences** (emotional, perceptual, qualitative) may
compound when timing aligns. If the Heart organ window is open at the
same moment that Synchronicity (the Full Moon Law) is the active
Primeval Law, the resonance between TCM Heart-Joy and the cosmic
fullness of Synchronicity is a real compound that the engine detects.

## The Three Temporal Bodies (plus the Keys)

| Body                      | Layer           | Rhythm                  | Period             | Calculation                                       |
|---------------------------|-----------------|-------------------------|--------------------|---------------------------------------------------|
| **Soul**                  | Primeval Law    | Lunar                   | ~4.9 days/phase    | Moon phase → trigram → Law (6 cyclic)             |
| **Solar Keys** (permanent) | Permanent Laws  | Solar cusps             | Daily events       | Sunrise → Gold Key / Sunset → Silver Key          |
| **Astral**                | Derivative Law  | LGBF                    | ~2 hours/vessel    | Stem-branch + solar position → vessel → Law       |
| **Gross**                 | Organ Clock     | Solar                   | ~2 hours/organ     | Solar position → Earthly Branch → organ           |

These read top-down: Soul slowest, Gross fastest. Solar Keys are not in
the cycle — they are permanent, daily events that activate at the two
cusps.

**Two-Body Law Unity** = Primeval Law (Soul) equals Derivative Law (Astral).
**Key-Amplified Law Unity** = Two-Body Unity active *during* a Solar Key cusping window.
**Key-Derivative Unity** = a Solar Key's Law equals the current Derivative Law during cusping.
**Anatomical Intersection** = an LGBF vessel's confluent or coupled points fall on the currently active meridian.

Full detail in `.claude/rules/temporal-bodies.md`.

## The Unified Temporal Substrate

All hourly calculations share the same solar-position-based foundation:

```
SUNRISE --- MIDDAY --- SUNSET --- MIDNIGHT --- SUNRISE
   |<- First Wing ->|         |<- Second Wing ->|
       4 Divine Hours              4 Divine Hours
       6 Organ Windows             6 Organ Windows
       6 Earthly Branches          6 Earthly Branches
```

Organ Clock and the Earthly Branch sequence are the same calculation.
LGBF uses the Earthly Branch from solar position. These systems tick
over together because they share an identical temporal substrate. This
is maximum resonance, not coincidence — and noticing it was one of the
analytical contributions that made the unified Astrolabium possible.

## What the Astrolabium Is NOT

- It is not astrology in the predictive sense. It does not tell the
  future or assign meaning to natal charts.
- It is not a calendar replacement. It overlays the Gregorian civil
  scaffold; it does not displace it.
- It is not a personality system. It says nothing about who the user is.
- It is not deterministic in the practitioner's response. It displays
  the qualities of the moment. What the practitioner does with that
  display is between them and the moment.

## Source Attribution in Output

```
[SOURCE: TCM]                — Traditional Chinese Medicine canonical
[SOURCE: Damanhurian]         — Damanhurian transmission
[BTR Ch.X]                    — Book of Three Responses, Chapter X
[ANALYTICAL CONTRIBUTION]    — original synthesis (NOT source-canonical)
[MATHEMATICAL FACT]          — verifiable calculation
[UNKNOWN]                    — not in the available material
```

**Never present analytical contributions as source material.** When a
gap exists, the correct answer is "the sources do not specify this."
Honesty about provenance is the instrument's authority.

## Cross-References

- `.claude/rules/temporal-bodies.md` — full bodies + compound detection
- `.claude/rules/divine-hours.md` — the 8-fold unequal hour system
- `.claude/rules/ling-gui-ba-fa.md` — LGBF protocol and formula
- `.claude/rules/trigram-laws.md` — 6+2 architecture in detail
- `.claude/rules/divine-calendar.md` — months, rites, intercalation
- `.claude/rules/location-and-time.md` — the constraint protocol
- `docs/specs/operators_manual.md` — Part 1 of Book II, full instrument
- `docs/specs/trigram_law_architecture.md` — locked architecture spec
- `docs/specs/project_midmortem.md` — the design history
