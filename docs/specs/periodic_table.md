# ASTROLABIUM CAUDAE RUBRAE
## Periodic Table of Compounds and Resonances
### Version 5.0 — March 2, 2026

---

> **Status:** FINAL — Book II Reference Document
> **Supersedes:** v4.0 (hierarchy reframing), v2.7 (definitions), v3.0 (computed data), Compound Catalogue v1.0 (structural proofs)
> **Companion Documents:** Guidebook v2.2 (computation procedures), Operator's Manual v3.0 (conceptual introduction)
> **Location:** Damanhur (45.4167°N, 7.8833°E), Divine Year 77
> **Computation:** 34,015 samples at 15-minute resolution across 354.31 days

---

## 1. WHAT THIS TABLE IS

This document is the exhaustive indexed reference for every phenomenon the
Astrolabium detects. It contains:

- **18 structural compounds** — deterministic timing alignments between temporal layers
- **9 boolean resonances** — cross-dimensional alignments (elemental, qualitative, rhythmic, calendrical)
- **4 state-value resonances** — categorical temporal positions (alchemical stage, month group, IAO, yang count)
- **6 proven structural impossibilities** — compounds that cannot occur under the 6+2 architecture
- **Computed frequency data** for one complete Divine Year at Damanhur

Every compound and resonance is defined, structurally proven, and measured.

---

## 2. FOUNDATIONAL CONSTRAINTS

### 2.1 The Temporal Substrate

All hourly calculations derive from **solar position** at the practitioner's
location. Civil clock time is never used.

```
SUNRISE ──── MIDDAY ──── SUNSET ──── MIDNIGHT ──── SUNRISE
   |← First Wing (Day) →|          |← Second Wing (Night) →|

   4 Divine Hours              4 Divine Hours
   6 Organ Windows             6 Organ Windows
   6 Earthly Branches          6 Earthly Branches
```

### 2.2 The Five Independent Temporal Layers

| Layer | Symbol | Source | Possible States | Cycle |
|-------|--------|--------|----------------|-------|
| **Primeval Law** (Soul) | P | Lunar elongation | 6 cyclic Laws | ~4.92 days/phase |
| **Derivative Law** (Astral) | D | LGBF vessel | 8 Laws (all) | ~2 hours/vessel |
| **Solar Key** | K | Sunrise/sunset cusp | Gold / Silver / None | Daily events |
| **Organ Clock** | O | Solar position | 12 meridians | ~2 hours/organ |
| **Divine Hour** | H | Solar position | 8 hours (4+4) | ~3 hours/hour |

Plus two calendar layers:

| Layer | Symbol | Source | States | Cycle |
|-------|--------|--------|--------|-------|
| **Divine Month** | M | Lunisolar calendar | 13 months | ~29.53 days |
| **Sephirotic Day** | S | Lunar quarter position | 9 day-types | 1 day |

### 2.3 The 6+2 Architecture

Six cyclic trigrams carry Laws through the lunar month. Kǎn ☵ (Gold Key /
Fall of Events) and Lí ☲ (Silver Key / Divinity) are excluded from the
cyclic rotation — they activate as Water gates at sunrise and sunset cusps.

**Why "Water gates."** In Plum Blossom Alchemy, both excluded trigrams
carry **Water** (Yin Water for Kǎn, Yang Water for Lí). Water is the
medium of transit — the substance through which the cycle passes, not part
of the cycle itself. The Cantong qi tradition excludes Kǎn and Lí from
the monthly cycle as alchemical operators. The Plum Blossom fist form
avoids the Water positions on the Posterior Heaven Bagua. [SOURCE: TCM/Cantong qi,
Plum Blossom Alchemy — Timothy Paul Bielec ~2013, LOCKED March 1, 2026]

### 2.4 Elemental System Separation

Three elemental systems exist and **NEVER** cross-compound:

| System | Elements | Context |
|--------|----------|---------|
| **Wu Xing** | Wood, Fire, Earth, Metal, Water | Organ Clock, TCM |
| **Damanhurian** | Earth, Water, Fire, Air, Ether | Primeval Laws, Calendar |
| **Trigram** | Heaven, Earth, Thunder, Wind, Water, Fire, Mountain, Lake | I Ching |

A New Moon (Kūn/Earth trigram) during SADAM (Earth element) during Spleen
(Earth Wu Xing) creates NO "triple Earth" compound.

### 2.5 Water Gate Qualities Are Non-Cyclic

Gold Key carries **Fall of Events** and Silver Key carries **Divinity**.
These are Water gate qualities — permanently excluded from the 6-phase
cyclic Primeval rotation. They cannot appear as Primeval Laws. Any compound
requiring a Water gate quality to equal a Primeval Law is **structurally
impossible**. The Solar Keys activate at sunrise/sunset cusps as transit
moments, not as expressions of Primeval Law.

### 2.6 Vessel Points Are On Different Meridians

Every Extraordinary Vessel's confluent and coupled points fall on different
meridians. Since the Organ Clock activates one meridian at a time, both
points can never be on the active meridian simultaneously.

### 2.7 LGBF Yin Day Restriction

On Yin days (odd stem index), only 6 of 8 vessels are accessible. **Yang Wei
Mai** (Sole Atom) and **Ren Mai** (Kaos) are unrestricted. The remaining 6
vessels cannot open on Yin days. ~50% of days are Yin.

### 2.8 Type A vs. Type B Phenomena

**Type A (Formal/Calculable):** Derived from astronomy, chronoacupuncture,
stem-branch math. Deterministic. Elements never cross-compound between systems.

**Type B (Interpretive/Resonance):** Derived from semantic correspondence —
color affinity, emotional resonance, anatomical proximity. CAN compound across
systems where resonance is natural and graded (EXACT / NATURAL / NONE).

---

## 3. STRUCTURAL COMPOUNDS (18 Types)

### Category 1 — Law Unity

#### C-01: Two-Body Unity
**Condition:** Primeval Law (P) == Derivative Law (D)
**Layers:** Soul × Astral
**Detection:** `primeval_law == derivative_law` (after yin-day gate)
**Frequency:** 6.71% of the year (2,281 steps)
**Note:** Blocked on Yin days for 6 of 8 vessels. Raw (pre-gate): 9.42%

| Lunar Phase | Primeval Law | Matching Vessel | Confluent |
|-------------|-------------|-----------------|-----------|
| New Moon (Kūn ☷) | Kaos | Ren Mai | LU-7 |
| First Crescent (Zhèn ☳) | Sole Atom | Yang Wei Mai | SJ-5 |
| First Quarter (Duì ☱) | Time Matrix | Dai Mai | GB-41 |
| Full Moon (Qián ☰) | Synchronicity | Du Mai | SI-3 |
| First Wane (Xùn ☴) | Geometric Essence | Yin Wei Mai | PC-6 |
| Last Quarter (Gèn ☶) | Arrow of Complexity | Chong Mai | SP-4 |

#### C-02: Gold Key-Derivative Unity
**Condition:** Derivative Law == Fall of Events during Gold Key cusping window
**Layers:** Key × Astral
**Detection:** `derivative_law == 'Fall of Events' AND gold_key_active`
**Frequency:** Included in Key-Derivative Unity total (1.96%)

#### C-03: Silver Key-Derivative Unity
**Condition:** Derivative Law == Divinity during Silver Key cusping window
**Layers:** Key × Astral
**Detection:** `derivative_law == 'Divinity' AND silver_key_active`
**Frequency:** Included in Key-Derivative Unity total (1.96%)

#### C-04: Key-Derivative Unity (combined)
**Condition:** C-02 OR C-03
**Frequency:** 1.96% (666 steps)

### Category 2 — Anatomical Intersection

#### C-05: Confluent Intersection
**Condition:** LGBF vessel's confluent point meridian == active organ clock meridian
**Layers:** Astral × Organ Clock
**Detection:** `vessel_conf_branch == active_branch`
**Frequency:** 8.81% (2,997 steps)

| Vessel | Confluent Point | Branch | Organ |
|--------|----------------|--------|-------|
| Du Mai | SI-3 | 未 (7) | Small Intestine |
| Ren Mai | LU-7 | 寅 (2) | Lung |
| Chong Mai | SP-4 | 巳 (5) | Spleen |
| Dai Mai | GB-41 | 子 (0) | Gallbladder |
| Yang Qiao Mai | BL-62 | 申 (8) | Bladder |
| Yin Qiao Mai | KI-6 | 酉 (9) | Kidney |
| Yang Wei Mai | SJ-5 | 亥 (11) | San Jiao |
| Yin Wei Mai | PC-6 | 戌 (10) | Pericardium |

#### C-06: Coupled Intersection
**Condition:** LGBF vessel's coupled point meridian == active organ clock meridian
**Layers:** Astral × Organ Clock
**Detection:** `vessel_coup_branch == active_branch`
**Frequency:** 9.17% (3,118 steps)

| Vessel | Coupled Point | Branch | Organ |
|--------|--------------|--------|-------|
| Du Mai | BL-62 | 申 (8) | Bladder |
| Ren Mai | KI-6 | 酉 (9) | Kidney |
| Chong Mai | PC-6 | 戌 (10) | Pericardium |
| Dai Mai | SJ-5 | 亥 (11) | San Jiao |
| Yang Qiao Mai | SI-3 | 未 (7) | Small Intestine |
| Yin Qiao Mai | LU-7 | 寅 (2) | Lung |
| Yang Wei Mai | GB-41 | 子 (0) | Gallbladder |
| Yin Wei Mai | SP-4 | 巳 (5) | Spleen |

**Pair symmetry:** Du Mai's confluent (SI) == Yang Qiao Mai's coupled (SI),
and vice versa. This holds for all four vessel pairs.

### Category 3 — Combined Compounds (Unity + Anatomy)

#### C-07: Full Confluent Alignment
**Condition:** Two-Body Unity AND Confluent Intersection
**Layers:** Soul × Astral × Gross (all three bodies)
**Detection:** `two_body_unity AND confluent_intersection`
**Frequency:** 0.32% (108 steps)

| Lunar Phase | Vessel | Confluent Branch | Law |
|-------------|--------|-----------------|-----|
| New Moon | Ren Mai | LU (寅) | Kaos |
| First Crescent | Yang Wei Mai | SJ (亥) | Sole Atom |
| First Quarter | Dai Mai | GB (子) | Time Matrix |
| Full Moon | Du Mai | SI (未) | Synchronicity |
| First Wane | Yin Wei Mai | PC (戌) | Geometric Essence |
| Last Quarter | Chong Mai | SP (巳) | Arrow of Complexity |

#### C-08: Full Coupled Alignment
**Condition:** Two-Body Unity AND Coupled Intersection
**Layers:** Soul × Astral × Gross (all three bodies)
**Detection:** `two_body_unity AND coupled_intersection`
**Frequency:** 0.84% (287 steps)

#### C-09: Conditional 3/4 (Silver Key-Derivative + Confluent)
**Condition:** Key-Derivative Silver AND Confluent Intersection
**Detection:** `key_derivative_silver AND confluent_intersection`
**Frequency:** 0.20% (69 steps)
**Note:** Latitude-dependent. Requires BL branch extending into sunset cusp.

#### C-10: Conditional 3/5 (Gold Key-Derivative + Coupled)
**Condition:** Key-Derivative Gold AND Coupled Intersection
**Detection:** `key_derivative_gold AND coupled_intersection`
**Frequency:** 0.64% (218 steps)
**Note:** Latitude-dependent. Requires LU branch extending into sunrise cusp.

### Category 4 — Polarity and Hinge Compounds

#### C-11: Polarity Alignment
**Condition:** Day yin/yang matches vessel polarity
**Detection:** `(yang_day AND yang_vessel) OR (yin_day AND yin_vessel)`
**Frequency:** ~50% (background resonance)

#### C-11b: Water Gate Activation (structural event, not compound)
**What:** A Solar Key cusping window is active, meaning one of the two
Water gates (Kǎn/Lí) is open. During this window, the Water gate carries
its associated quality (Fall of Events for Gold Key, Divinity for Silver Key)
as a transit moment — the cycle passes through, not the gate joining the cycle.
**Detection:** `gold_key_active OR silver_key_active`
**Duration:** ~30 minutes per cusp (civil twilight window), twice daily
**Frequency:** ~4.2% of the year (1,428 steps)
**Significance:** The Water gates are the hinge points of the 6+2 architecture.
All Key-layer compounds (C-02, C-03, C-04, C-12, C-13, C-14) are subsets of
this window.

### Category 5 — Multi-Layer Compounds

#### C-12: Key-Amplified Unity
**Condition:** Two-Body Unity AND any Solar Key active
**Detection:** `two_body_unity AND (gold_key_active OR silver_key_active)`
**Frequency:** Very rare (subset of Two-Body Unity during ~30-min cusping windows)

#### C-13: Anatomical + Key
**Condition:** Any Anatomical Intersection AND any Solar Key active
**Detection:** `(confluent OR coupled) AND (gold_key OR silver_key)`
**Frequency:** Rare

#### C-14: Full Alignment + Key (Maximum Structural Compound)
**Condition:** Full Confluent or Full Coupled AND any Solar Key active
**Detection:** `(full_confluent OR full_coupled) AND (gold_key OR silver_key)`
**Frequency:** Extraordinarily rare — the absolute maximum structural compound

### Category 6 — Calendar Compounds (always active)

#### C-15: Great Rite Month
6 of 12 regular months carry a Great Rite. ~50% frequency.

#### C-16: Alchemical Stage
Nigredo (months 1–4), Albedo (5–8), Rubedo (9–12), Da'ath (13). Always active.

#### C-17: Intercalary Year
VADUSFADAHM year. ~36.6% of years (Metonic cycle).

#### C-18: Sephirotic Station
Days 1–9 within lunar quarter. Days 8–9 are rare events (Chokmah ~65%, Kether ~22%).

---

## 4. CROSS-DIMENSIONAL RESONANCES (13 Types)

### Category A — Elemental (Wu Xing silo, deterministic)

> **Hierarchy note:** R-03 (Plum Blossom Wu Xing) is the **primary**
> elemental bridge — its derivation chain passes through the practitioner's body
> (Extraordinary Vessel → confluent point → host meridian → Wu Xing element),
> threading the 8-trigram system directly to TCM's 5-element system. R-01
> and R-02 use the canonical I Ching trigram-element associations, which are
> architecturally valid but do not pass through the body. Both mappings are
> tracked because they produce different resonance patterns — the Plum
> Blossom mapping carries the practitioner's lived experience, the canonical
> mapping carries the cosmological structure. [ANALYTICAL CONTRIBUTION —
> Timothy Paul Bielec, ~2013, derived from SOURCE: TCM canonical
> correspondences]

#### R-01: Canonical Trigram Wu Xing × Organ Wu Xing (R_WX_01)
**What:** Primeval Law's canonical trigram Wu Xing matches active organ's Wu Xing element.
**Mapping source:** Standard I Ching trigram-element associations (cosmological).
**Example:** Qián (Metal) active during Lung (Metal) hour.
**Detection:** `trigram_wu_xing[primeval_trigram] == organ_element`
**Frequency:** 18.24% (6,205 steps)

| Trigram | Wu Xing | Matching Organs |
|---------|---------|-----------------|
| Qián ☰ | Metal | Lung, Large Intestine |
| Kūn ☷ | Earth | Spleen, Stomach |
| Zhèn ☳ | Wood | Liver, Gallbladder |
| Xùn ☴ | Wood | Liver, Gallbladder |
| Duì ☱ | Metal | Lung, Large Intestine |
| Gèn ☶ | Earth | Spleen, Stomach |

#### R-02: Vessel-Organ Element Match (R_WX_02)
**What:** Derivative vessel's Law-trigram canonical Wu Xing matches active organ's element.
**Mapping source:** Same as R-01 but applied through the LGBF vessel→Law→trigram chain.
**Example:** Du Mai (→ Synchronicity → Qián → Metal) during Lung (Metal) hour.
**Detection:** `trigram_wu_xing[law_trigram[vessel_law]] == organ_element`
**Frequency:** 20.26% (6,890 steps)

#### R-03: Plum Blossom Wu Xing × Organ Wu Xing (R_WX_03) — PRIMARY BRIDGE
**What:** Trigram's Plum Blossom element assignment matches active organ's Wu Xing element.
**Mapping source:** Plum Blossom Alchemy — the derivation chain EV → confluent point →
host meridian → Wu Xing element (with Six Qi Imperial/Ministerial Fire distinction
from the Huáng Dì Nèi Jīng). This mapping passes through the practitioner's body.
**Detection:** `plum_blossom_wu_xing_map[trigram_plum_blossom] == organ_element`
**Frequency:** 23.67% (8,052 steps) — the most frequent elemental resonance

**Plum Blossom → Wu Xing Mapping:**

| Trigram | EV | Confluent | Host Meridian | Plum Blossom | Wu Xing |
|---------|-----|-----------|--------------|-------------|---------|
| Qián ☰ | Du Mai | SI-3 | Small Intestine | Imperial Fire | Fire |
| Kūn ☷ | Ren Mai | LU-7 | Lung | Metal | Metal |
| Zhèn ☳ | Yang Wei Mai | SJ-5 | San Jiao | Min. Fire (Yang) | Fire |
| Xùn ☴ | Yin Wei Mai | PC-6 | Pericardium | Min. Fire (Yin) | Fire |
| Duì ☱ | Dai Mai | GB-41 | Gallbladder | Wood | Wood |
| Gèn ☶ | Chong Mai | SP-4 | Spleen | Earth | Earth |
| Kǎn ☵ | Yin Qiao Mai | KI-6 | Kidney | Yin Water | Water |
| Lí ☲ | Yang Qiao Mai | BL-62 | Bladder | Yang Water | Water |

**Note:** Kǎn and Lí (the Water gate trigrams) both carry Water in the
Plum Blossom system. They are excluded from the cyclic rotation, so their
Plum Blossom element activates only through the LGBF Derivative layer
(when Yin/Yang Qiao Mai is the active vessel).

### Category B — Qualitative (interpretive, graded)

#### R-04: Color Affinity (R_CLR_01)
**What:** Primeval Law's color matches the Chia color for the active organ's element.
**Grades:** EXACT (identical color term) or NATURAL (recognizable affinity).
**Frequency:** 21.49% (7,311 steps)

**Color Affinity Lookup:**

| Law Color | Chia Color | Grade |
|-----------|-----------|-------|
| Green (Sole Atom) | Green (Wood) | EXACT |
| White (Divinity) | White (Metal) | EXACT |
| Yellow Gold (Kaos) | Yellow (Earth) | NATURAL |
| Orange (Synchronicity) | Red (Fire) | NATURAL |
| Indigo (Fall of Events) | Blue/Black (Water) | NATURAL |
| Azure Blue (Arrow of Complexity) | Blue/Black (Water) | NATURAL |
| Silver (Time Matrix) | White (Metal) | NATURAL |
| Brick Red (Geometric Essence) | Red (Fire) | NATURAL |

#### R-05: Emotion-Perception Resonance (R_EPR_01)
**What:** Chia emotional quality semantically resonates with the Primeval Law's
perception pair.
**Grades:** EXACT (direct semantic match) or NATURAL (recognizable resonance).
**Frequency:** 16.47% (5,603 steps)

**Emotion-Perception Lookup:**

| Law | Element | Polarity | Grade | Basis |
|-----|---------|----------|-------|-------|
| Divinity | Fire | neg | EXACT | Hatred↔Hatred |
| Divinity | Fire | pos | EXACT | Love↔Love/Joy |
| Sole Atom | Wood | pos | NATURAL | Happiness↔Kindness |
| Kaos | Earth | neg | NATURAL | Fear/Terror↔Worry/Mistrust |
| Fall of Events | Water | neg | NATURAL | Loneliness↔Fear/Paranoia |
| Arrow of Complexity | Metal | neg | NATURAL | Reduction↔Grief |
| Time Matrix | Metal | neg | NATURAL | Pain/Suffering↔Grief |
| Synchronicity | Fire | pos | NATURAL | Completeness↔Love/Joy |

#### R-06: Adonaj-Ba Organ Proximity (R_ABD_01)
**What:** The Primeval Law's Adonaj-Ba energy center has anatomical relationship
with the active organ.
**Grades:** EXACT (same region), ADJACENT (neighboring), PROXIMAL (related via pathway).
**Frequency:** 20.68% (7,034 steps)

**Adonaj-Ba Proximity Lookup:**

| Adonaj-Ba | Organ | Grade |
|-----------|-------|-------|
| Heart | Heart | EXACT |
| Heart | Sm Intestine | ADJACENT |
| Heart | Pericardium | ADJACENT |
| Solar Plexus | Stomach | EXACT |
| Solar Plexus | Spleen | ADJACENT |
| Solar Plexus | Liver | PROXIMAL |
| Solar Plexus | Gallbladder | PROXIMAL |
| Sexual Organs | Kidney | ADJACENT |
| Sexual Organs | Bladder | ADJACENT |
| Sacrum | Kidney | ADJACENT |
| Sacrum | Bladder | ADJACENT |
| Sacrum | Lg Intestine | PROXIMAL |
| Crown | San Jiao | PROXIMAL |
| Third Eye | Liver | PROXIMAL |
| Third Eye | Gallbladder | PROXIMAL |
| Throat | Lung | ADJACENT |
| Throat | Lg Intestine | PROXIMAL |
| Mobile 8th | San Jiao | PROXIMAL |

### Category C — Rhythmic (deterministic)

#### R-07: Waxing-Wing Alignment (R_LUN_01)
**What:** Lunar phase direction matches solar wing. Waxing Moon + Day Wing =
aligned. Waning Moon + Night Wing = aligned.
**Detection:** `(waxing AND wing == "Day") OR (NOT waxing AND wing == "Night")`
**Frequency:** 50.65% (17,227 steps) — the most frequent resonance

#### R-08: Yang Count Progression (R_LUN_02) — State Value
**What:** Lunar phase yang line count tracking position in the energetic wave.
Not boolean — produces values 0 through 3.

| Yang Lines | Frequency | Description |
|------------|-----------|-------------|
| 0 | 16.38% | Pure yin (New Moon, Kūn ☷) |
| 1 | 33.22% | One yang line emerging |
| 2 | 33.67% | Two yang lines |
| 3 | 16.72% | Pure yang (Full Moon, Qián ☰) |

### Category D — Calendrical

#### R-09: Sephirotic Quest Match (R_SPH_01)
**What:** Sephirotic day's planet matches a Primeval Law's Quest Tarot
Continental attribution.
**Detection:** Quest card → Continental attribution → sephirotic planet match
**Frequency:** 10.16% (3,456 steps)

**Quest-to-Planet Mapping:**

| Quest Tarot | Continental Attribution | Sephirotic Planet |
|-------------|----------------------|-------------------|
| Priestess | Moon | Luna (Day 2) |
| Emperor | Jupiter | Jupiter (Day 5) |
| World | Sun | Sol (Day 1) |
| Star | Mercury | Mercury (Day 4) |

Only 4 of 8 Quest cards carry planetary attributions (the others carry
elements or zodiacal signs, which have no sephirotic day correspondence).
Match fires when: Time Matrix/Geometric Essence/Arrow of Complexity active
during their respective sephirotic days.

#### R-10: Season-Great Rite Alignment (R_SEA_01)
**What:** Chia season for active organ's Wu Xing element matches calendar
month's seasonal position via Great Rite.
**Frequency:** 11.85% (4,029 steps) — concentrated in Great Rite months

**Season-Great Rite Lookup:**

| Chia Season | Great Rite | Match |
|-------------|-----------|-------|
| Spring | Spring Equinox | Yes |
| Summer | Summer Solstice | Yes |
| Summer | Divine Marriage | Yes |
| Autumn | Autumn Equinox | Yes |
| Autumn | Day of the Dead | Yes |
| Winter | Winter Solstice | Yes |
| Late Summer | Divine Marriage | Yes |

#### R-11: Alchemical Stage (R_CAL_01) — State Value

| Stage | Months | Frequency |
|-------|--------|-----------|
| Nigredo | 1–4 (ISIS → EOROS) | 33.57% |
| Albedo | 5–8 (TASUMER → AGAFEST) | 33.32% |
| Rubedo | 9–12 (SAMMA → DESURIORIS) | 33.11% |
| Da'ath | 13 (VADUSFADAHM) | 0% this year |

#### R-12: Month Group (R_CAL_02) — State Value

| Group | Months | Frequency |
|-------|--------|-----------|
| Osirian | ISIS, OSIRIS, SET | 24.97% |
| Falcon | LIOTHIL, MENON, AGAFEST, SADAS, DESURIORIS | 41.61% |
| Operative | SADAM, TASUMER | 16.76% |
| Tappetino | EOROS, SAMMA, VADUSFADAHM | 16.66% |

#### R-13: IAO Position (R_CAL_03) — State Value

| Letter | Month | Frequency |
|--------|-------|-----------|
| I | ISIS (1) | 8.38% |
| O | OSIRIS (7) | 8.32% |
| A | SET (10) | 8.26% |
| (none) | All others | 75.03% |

---

## 5. STRUCTURAL IMPOSSIBILITIES (6 Types)

These compounds are proven impossible under the 6+2 architecture.

| # | Compound | Reason |
|---|----------|--------|
| X-01 | Key-Primeval Unity | Water gate qualities excluded from 6-phase Primeval rotation |
| X-02 | Old Three-Body (P==D==K) | Requires Key-Primeval (X-01), which is impossible |
| X-03 | Double Intersection | Vessel confluent/coupled points on different meridians |
| X-04 | Full Alignment + Double | Requires Double Intersection (X-03) |
| X-05 | Key-Derivative + Double | Requires Double Intersection (X-03) |
| X-06 | Old Three-Body + Anatomy | Requires Old Three-Body (X-02) |

---

## 6. THE FOUR DEAD ZONES

Four organ branches have NO vessel access points. Anatomical intersection
is structurally impossible during these windows.

| Branch | Organ | Wing | Duration |
|--------|-------|------|----------|
| 丑 (1) | Liver (LR) | Night | ~2 unequal hours |
| 卯 (3) | Lg Intestine (LI) | Night | ~2 unequal hours |
| 辰 (4) | Stomach (ST) | Day | ~2 unequal hours |
| 午 (6) | Heart (HT) | Day | ~2 unequal hours |

These are 2 dead zones per wing, ~8 hours total per day (~33%). During dead
zones, all other compounds and resonances remain fully active — only
anatomical intersection is excluded.

**Elemental note:** Water is the only Wu Xing element with both organs
(Bladder, Kidney) participating in anatomical intersection.

---

## 7. COMPLETE FREQUENCY TABLE — DIVINE YEAR 77

All 17 boolean phenomena ranked by frequency across 34,015 samples.

| Rank | Phenomenon | Cat. | Type | Count | % of Year |
|------|-----------|------|------|------:|----------:|
| 1 | Waxing-Wing Alignment | Rhythmic | A | 17,227 | 50.65% |
| 2 | **Plum Blossom Wu Xing** | Elemental | A | 8,052 | 23.67% |
| 3 | Color Affinity | Qualitative | B | 7,311 | 21.49% |
| 4 | Adonaj-Ba Proximity | Qualitative | B | 7,034 | 20.68% |
| 5 | Vessel-Organ Element (canonical) | Elemental | A | 6,890 | 20.26% |
| 6 | Wu Xing Element Match (canonical) | Elemental | A | 6,205 | 18.24% |
| 7 | Emotion-Perception | Qualitative | B | 5,603 | 16.47% |
| 8 | Season-Great Rite | Calendrical | A | 4,029 | 11.85% |
| 9 | Sephirotic Quest Match | Calendrical | A | 3,456 | 10.16% |
| 10 | Coupled Intersection | Structural | A | 3,118 | 9.17% |
| 11 | Confluent Intersection | Structural | A | 2,997 | 8.81% |
| 12 | Two-Body Unity | Structural | A | 2,281 | 6.71% |
| 13 | Key-Derivative Unity | Structural | A | 666 | 1.96% |
| 14 | Full Coupled | Structural | A | 287 | 0.84% |
| 15 | Conditional 3/5 | Structural | A | 218 | 0.64% |
| 16 | Full Confluent | Structural | A | 108 | 0.32% |
| 17 | Conditional 3/4 | Structural | A | 69 | 0.20% |

**Yin-Day Blocking:** 14,126 steps (41.53%) fell on Yin days. Raw Two-Body
Unity count (before yin-day filter): 3,206 (9.42%).

**Elemental hierarchy:** Plum Blossom Wu Xing (rank 2, 23.67%) is the most
frequent elemental resonance and the **primary bridge** between the 8-trigram
system and TCM. Its derivation passes through the practitioner's body (EV →
confluent point → host meridian → Wu Xing element). The canonical trigram Wu
Xing resonances (ranks 5-6) use the standard I Ching associations. Both are
tracked.

---

## 8. COMPOUND COMBINATORIAL ANALYSIS

When multiple phenomena fire simultaneously, they form **compound recipes** —
unique combinations of 2 or more active types. Computed across the full
Divine Year:

### 8.1 Complexity Distribution

| Components | Steps | % of Year | Unique Recipes |
|:----------:|------:|----------:|---------------:|
| 0 | 6,217 | 18.28% | — |
| 1 | 5,983 | 17.59% | — |
| 2 | 5,942 | 17.47% | 87 |
| 3 | 5,730 | 16.85% | 106 |
| 4 | 4,578 | 13.46% | 85 |
| 5 | 3,026 | 8.90% | 46 |
| 6 | 1,641 | 4.82% | 18 |
| 7 | 749 | 2.20% | 7 |
| 8 | 149 | 0.44% | 2 |

**Total unique recipes:** 351
**Maximum observed complexity:** 8 simultaneous phenomena
**Steps with a compound active (2+):** 21,815 (64.1% of the year)

### 8.2 The 8-Component Peak

The highest complexity observed: **8 simultaneous phenomena**. Two distinct
recipes achieve this level, occurring in 149 steps (37.25 hours total).

Components at the first occurrence (2025-10-04T07:39, Month 1 ISIS):
- Two-Body Unity (C-01)
- Wu Xing Element Match (R-01)
- Vessel-Organ Element Match (R-02)
- Color Affinity (R-04)
- Emotion-Perception (R-05)
- Waxing-Wing Alignment (R-07)
- Sephirotic Quest Match (R-09)
- Season-Great Rite (R-10)

### 8.3 Top 15 Most Frequent Recipes

| Rank | Count | Size | Components |
|-----:|------:|-----:|:-----------|
| 1 | 3,197 | 2 | Plum Blossom Wu Xing + Waxing-Wing Alignment |
| 2 | 2,330 | 2 | Color Affinity + Waxing-Wing Alignment |
| 3 | 2,156 | 2 | Adonaj-Ba Proximity + Waxing-Wing Alignment |
| 4 | 1,959 | 3 | Color Affinity + Emotion-Perception + Waxing-Wing |
| 5 | 1,746 | 2 | Wu Xing Element Match + Waxing-Wing Alignment |
| 6 | 1,686 | 3 | Color Affinity + Plum Blossom WX + Waxing-Wing |
| 7 | 1,647 | 2 | Vessel-Organ Element + Waxing-Wing Alignment |
| 8 | 1,561 | 2 | Color Affinity + Emotion-Perception |
| 9 | 1,417 | 2 | Adonaj-Ba Proximity + Plum Blossom Wu Xing |
| 10 | 1,267 | 2 | Emotion-Perception + Waxing-Wing Alignment |
| 11 | 945 | 3 | Color Affinity + Emotion-Perception + Wu Xing Element |
| 12 | 922 | 3 | Adonaj-Ba + Color Affinity + Emotion-Perception |
| 13 | 921 | 4 | Adonaj-Ba + Color Affinity + Emotion-Perception + WX |
| 14 | 838 | 2 | Adonaj-Ba Proximity + Season-Great Rite |
| 15 | 730 | 2 | Waxing-Wing Alignment + Season-Great Rite |

**Observation:** Waxing-Wing Alignment (~50%) acts as a carrier wave — it
appears in 11 of the top 15 recipes. The most frequent pure recipe without
Waxing-Wing is Color Affinity + Emotion-Perception (rank 8).

---

## 9. CO-OCCURRENCE MATRIX

The 20 strongest pairwise co-occurrences across all 17 boolean types.

| Pair | Co-occur | % of Year |
|------|:--------:|:---------:|
| Color Affinity + Emotion-Perception | 4,683 | 13.77% |
| Vessel-Organ Element + Waxing-Wing | 3,717 | 10.93% |
| Color Affinity + Waxing-Wing | 3,606 | 10.60% |
| Adonaj-Ba Proximity + Waxing-Wing | 3,408 | 10.02% |
| Color Affinity + Plum Blossom WX | 3,311 | 9.73% |
| Adonaj-Ba + Emotion-Perception | 3,258 | 9.58% |
| Waxing-Wing + Wu Xing Element | 3,224 | 9.48% |
| Plum Blossom WX + Waxing-Wing | 3,104 | 9.13% |
| Color Affinity + Wu Xing Element | 3,058 | 8.99% |
| Emotion-Perception + Wu Xing Element | 3,058 | 8.99% |
| Emotion-Perception + Waxing-Wing | 2,857 | 8.40% |
| Adonaj-Ba + Color Affinity | 2,338 | 6.87% |
| Season-Great Rite + Waxing-Wing | 2,018 | 5.93% |
| Sephirotic Quest + Waxing-Wing | 1,715 | 5.04% |
| Emotion-Perception + Plum Blossom WX | 1,625 | 4.78% |
| Plum Blossom WX + Vessel-Organ | 1,443 | 4.24% |
| Adonaj-Ba + Plum Blossom WX | 1,417 | 4.17% |
| Confluent Intersection + Waxing-Wing | 1,387 | 4.08% |
| Adonaj-Ba + Vessel-Organ | 1,374 | 4.04% |
| Confluent + Vessel-Organ | 1,328 | 3.90% |

**Total co-occurrence pairs observed:** 111

---

## 10. PER-LAW COMPOUND ACTIVITY

Which Primeval Law was governing when each compound/resonance fired.

### Waxing-Wing Alignment (17,227 total)

| Law | Count | % |
|-----|------:|--:|
| Synchronicity | 2,957 | 17.2% |
| Sole Atom | 2,909 | 16.9% |
| Geometric Essence | 2,898 | 16.8% |
| Time Matrix | 2,890 | 16.8% |
| Arrow of Complexity | 2,799 | 16.2% |
| Kaos | 2,774 | 16.1% |

**Near-uniform distribution** — Waxing-Wing is essentially Law-independent.

### Two-Body Unity (2,281 total)

Concentrated in the first half of the year due to the interaction between
lunar phase timing and LGBF vessel availability. Two-Body Unity on Kaos
(Ren Mai) and Sole Atom (Yang Wei Mai) is unrestricted by yin-day gate;
the other four Laws are restricted.

### Season-Great Rite (4,029 total)

**Concentrated in Great Rite months:** 0% in non-rite months (LIOTHIL,
TASUMER, MENON, AGAFEST, SADAS, DESURIORIS). Maximum concentration in
SAMMA (43.6%) and SET (26.8%).

### Sephirotic Quest Match (3,456 total)

**Perfectly trisected:** Time Matrix = Geometric Essence = Arrow of
Complexity, each at 33.3%. Only 3 of 6 cyclic Laws have Quest cards
with planetary attributions.

---

## 11. PER-MONTH FREQUENCY PROFILES

How Two-Body Unity distributes across the year:

| Month | Two-Body Unity | Season-Great Rite | Seph. Quest |
|-------|:--------------:|:-----------------:|:-----------:|
| ISIS | 9.2% | 16.8% | 10.1% |
| SADAM | 8.7% | 16.8% | 10.1% |
| LIOTHIL | 7.9% | 0.0% | 10.1% |
| EOROS | 7.3% | 16.8% | 10.1% |
| TASUMER | 6.8% | 0.0% | 10.1% |
| MENON | 6.3% | 0.0% | 10.2% |
| OSIRIS | 6.1% | 21.6% | 10.2% |
| AGAFEST | 6.5% | 0.0% | 10.2% |
| SAMMA | 6.3% | 43.6% | 10.2% |
| SET | 5.7% | 26.8% | 10.2% |
| SADAS | 4.8% | 0.0% | 10.2% |
| DESURIORIS | 4.9% | 0.0% | 10.2% |

Two-Body Unity declines through the year from 9.2% to 4.8%. This is a
real astronomical effect: the relationship between LGBF vessel timing
and lunar phase drifts across the year.

---

## 12. THE ANATOMICAL INTERSECTION MATRIX

Complete enumeration of which meridians produce intersection for each vessel.

| Branch | Organ | Confluent Vessel | Coupled Vessel | Pair |
|--------|-------|-----------------|----------------|:----:|
| 子 (0) | Gallbladder | Dai Mai | Yang Wei Mai | 4 |
| 丑 (1) | Liver | — (dead zone) | — (dead zone) | — |
| 寅 (2) | Lung | Ren Mai | Yin Qiao Mai | 2 |
| 卯 (3) | Lg Intestine | — (dead zone) | — (dead zone) | — |
| 辰 (4) | Stomach | — (dead zone) | — (dead zone) | — |
| 巳 (5) | Spleen | Chong Mai | Yin Wei Mai | 3 |
| 午 (6) | Heart | — (dead zone) | — (dead zone) | — |
| 未 (7) | Sm Intestine | Du Mai | Yang Qiao Mai | 1 |
| 申 (8) | Bladder | Yang Qiao Mai | Du Mai | 1 |
| 酉 (9) | Kidney | Yin Qiao Mai | Ren Mai | 2 |
| 戌 (10) | Pericardium | Yin Wei Mai | Chong Mai | 3 |
| 亥 (11) | San Jiao | Yang Wei Mai | Dai Mai | 4 |

**8 active branches, 4 dead zones, 4 vessel pairs, 16 unique intersection
configurations collapsing to 8 unique meridian-vessel encounters via pair
symmetry.**

---

## 13. TEMPORAL DISTRIBUTIONS

### Primeval Law (Soul Body)

| Law | Count | % |
|-----|------:|--:|
| Geometric Essence | 5,837 | 17.16% |
| Synchronicity | 5,689 | 16.72% |
| Sole Atom | 5,686 | 16.72% |
| Time Matrix | 5,617 | 16.51% |
| Arrow of Complexity | 5,613 | 16.50% |
| Kaos | 5,573 | 16.38% |

Near-uniform. Geometric Essence slightly overrepresented due to phase
boundary positioning.

### Derivative Law (Astral Body)

| Law | Count | % |
|-----|------:|--:|
| Fall of Events | 9,495 | 27.91% |
| Divinity | 5,008 | 14.72% |
| Sole Atom | 5,000 | 14.70% |
| Time Matrix | 4,507 | 13.25% |
| Arrow of Complexity | 4,335 | 12.74% |
| Kaos | 1,985 | 5.84% |
| Synchronicity | 1,851 | 5.44% |
| Geometric Essence | 1,834 | 5.39% |

**Non-uniform.** Fall of Events (Yin Qiao Mai) dominates at 27.91% — a
consequence of the LGBF formula's remainder distribution. The Water gate
qualities (Fall of Events, Divinity) together account for 42.63% of Derivative time.

### Vessel (LGBF)

| Vessel | Law | Count | % |
|--------|-----|------:|--:|
| Yin Qiao Mai | Fall of Events | 9,495 | 27.91% |
| Yang Qiao Mai | Divinity | 5,008 | 14.72% |
| Yang Wei Mai | Sole Atom | 5,000 | 14.70% |
| Dai Mai | Time Matrix | 4,507 | 13.25% |
| Chong Mai | Arrow of Complexity | 4,335 | 12.74% |
| Ren Mai | Kaos | 1,985 | 5.84% |
| Du Mai | Synchronicity | 1,851 | 5.44% |
| Yin Wei Mai | Geometric Essence | 1,834 | 5.39% |

---

## 14. THE FAIL-SAFE

The meta-registry (`src/meta_registry.py`) maintains a census of every
comparable field across all 10 register dimensions:

- **29 total comparable fields** catalogued
- **23 fields** participate in resonance detection
- **6 fields** explicitly exempted (identity/structural markers)
- **0 uncatalogued fields**

A test assertion enforces zero gaps. If `registers.json` gains new
comparable fields without corresponding resonance entries or explicit
exemptions, the test suite breaks. The Astrolabium cannot silently
become incomplete.

---

## 15. SUMMARY

| Metric | Value |
|--------|-------|
| Structural compounds | 18 types |
| Cross-dimensional resonances | 13 types (9 boolean + 4 state-value) |
| Proven impossibilities | 6 |
| Total trackable phenomena | 31 |
| Unique compound recipes (DY 77) | 351 |
| Maximum observed complexity | 8 simultaneous phenomena |
| % of year with compound active | 64.1% |
| Co-occurrence pairs observed | 111 |
| Compound windows (Mar 2 → year end) | 1,699 |
| Tests | 218 passing |
| Field coverage fail-safe | 29 fields, 0 uncatalogued |

---

## 16. CODE REFERENCES

| Module | Purpose |
|--------|---------|
| `src/astrolabium.py` | Orchestrator — `detect_compounds()` + `detect_resonances()` |
| `src/resonance.py` | Resonance scanner — 13 types, 4 evaluator functions |
| `src/meta_registry.py` | Fail-safe — field census + coverage check |
| `data/registers.json` | All interpretive data (11 dimensions, 89 entries) |
| `data/resonances.json` | Resonance definitions + 8 lookup tables |
| `scripts/compute_periodic_table.py` | Generates frequency data |
| `scripts/analyze_compounds.py` | Combinatorial recipe analysis |
| `scripts/compound_timeline.py` | Chronological compound window timeline |

---

## 17. COMPOUND TIMELINE

A separate document (`data/compound_timeline.md`) contains the chronological
list of all 1,699 compound windows from March 2, 2026 through the end of
Divine Year 77 (September 11, 2026), organized by Divine Month. Each window
includes: start time, end time, duration, active components, and full state
context (Laws, organ, vessel, phase, hour, sephirotic day).

---

*Periodic Table v5.0 compiled March 2, 2026. Merges definitional framework
(v2.7), structural proofs (Compound Catalogue v1.0), computed frequency data
(v3.0), and the Plum Blossom Alchemy/Water hinge reframing (v5.0) into a
single indexed reference. Every compound defined, proven, and measured. Every
resonance catalogued, detected, and quantified. The Plum Blossom bridge
threads the 8-element cosmic system to the 5-element body system through the
practitioner's own Extraordinary Vessels. The Water gates stand where the
cycle passes through. 218 tests passing. Zero fail-safe gaps.*
