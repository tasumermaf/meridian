# Astrolabium Caudae Rubrae — Pen-and-Paper Guidebook

> **Version:** 2.2
> **Date:** March 2, 2026
> **Author:** Timothy Paul Bielec with Meridian
> **Status:** LOCKED — The sole specification for the Astrolabium Caudae Rubrae
>
> **Purpose:** A complete, self-contained reference for computing the
> alchemical quality of any moment using pen, paper, an ephemeris, and
> a sunrise/sunset table. Every lookup table. Every procedure. Worked
> examples. One madman in a cave with a pen, a set of tables, and the
> ephemeris could compute anything the software computes. This document
> IS the specification. Code is rebuilt from it. Nothing else is needed.
>
> **Epistemic tags:** Every table and mapping carries its source:
> - **[SOURCE: DAM]** — Damanhurian teaching (Falco Tarassaco)
> - **[SOURCE: TCM]** — Traditional Chinese Medicine canonical
> - **[SOURCE: Neidan]** — Internal alchemy tradition (Cantong qi)
> - **[SOURCE: Plum Blossom Alchemy]** — Timothy's analytical derivation (~2013) from TCM canonical correspondences, developed during Wu Mei Kung Fu training
> - **[ANALYTICAL CONTRIBUTION]** — Timothy's synthesis
> - **[MATHEMATICAL FACT]** — Deterministic calculation

---

## Section 1: The Eight Laws — Master Correspondence Table

The eight Primeval Laws are the cosmological principles governing the
universe of Form. Each Law has been mapped — through constraint
propagation across three independent data streams (Quest-Tarot pairings,
ADONAJ BA correspondences, and prime factorization of Sacred Language
inscriptions) — to a unique prime number, trigram, body center, color,
Quest, and perception pair. The derivation is documented in
`docs/eight-threads-on-the-loom-of-maat.md`. The mapping is **forced
by the mathematics** — no arbitrary choices are required.

### 1.1 Master Table

| # | Law | Trigram | Symbol | Binary | Prime | Adonaj-Ba | Color | Quest (Full) | Quest (Short) |
|---|-----|---------|--------|--------|-------|-----------|-------|--------------|---------------|
| 1 | **Synchronicity** | Qián | ☰ | 111 | **89** | Heart (cuore) | Orange (arancio) | Act in Order to Be | ACTION |
| 2 | **Sole Atom** | Zhèn | ☳ | 100 | **19** | Sexual Organs (organi sessuali) | Green (verde) | Keep on Acting | CONTINUITY |
| 3 | **Divinity** | Lí | ☲ | 101 | **31** | Head / Crown (capo) | White (bianco) | Change Your Logic | TRANSMUTATION |
| 4 | **Geometric Essence** | Xùn | ☴ | 011 | **67** | Sacrum (sacro) | Brick Red (mattone) | Feminine | FEMININE |
| 5 | **Time Matrix** | Duì | ☱ | 110 | **29** | Mobile 8th (mobile) | Silver (argento) | Masculine | MASCULINE |
| 6 | **Fall of (Neutral) Events** | Kǎn | ☵ | 010 | **11** | Third Eye (3° occhio) | Indigo (indaco) | Artist of Your Life | INVERSION |
| 7 | **Kaos** | Kūn | ☷ | 000 | **23** | Solar Plexus (plesso solare) | Yellow Gold (giallo oro) | Explore Change | UNCERTAINTY |
| 8 | **Arrow of Complexity** | Gèn | ☶ | 001 | **17** | Throat (gola) | Azure Blue (azzurro) | Transmit Life | REPRODUCTION |

**Sources:** Law names and descriptions [SOURCE: DAM]. Trigram assignments
[ANALYTICAL CONTRIBUTION — Timothy's Wu Mei synthesis, 2013]. Prime
assignments [ANALYTICAL CONTRIBUTION — constraint propagation derivation].
Adonaj-Ba body centers and colors [SOURCE: DAM — Quest document]. Quest
names [SOURCE: DAM — The 8 Quests]. Quest short forms [ANALYTICAL
CONTRIBUTION].

### 1.2 Perception Pairs

Each Law carries positive and negative perceptual poles. These are
the emotional/experiential qualities that manifest when the Law is
active. [SOURCE: DAM]

| Law | Perception (+) | Perception (−) |
|-----|----------------|----------------|
| Synchronicity | Completeness | Incompleteness |
| Sole Atom | Happiness | Unhappiness |
| Divinity | Love | Hatred |
| Geometric Essence | Sweetness, Order | Hardness, Loss |
| Time Matrix | Sharing, Joy | Pain, Suffering |
| Fall of Events | Beauty, Art | Ugliness, Loneliness |
| Kaos | Certainty, Understanding | Fear, Terror |
| Arrow of Complexity | Curiosity, Expansion | Eternal Reduction |

### 1.3 Three Reservoirs Confirmation

Falco's Three Reservoirs of Man independently confirm three assignments
(from a 1993 teaching, *Magic Levels and Man Tanks*). [SOURCE: DAM]

| Reservoir | Law | Prime | Confirmation |
|-----------|-----|-------|-------------|
| **Will** | Arrow of Complexity | 17 | "It guides and organizes" → Star card = sorting insights |
| **Memory** | Geometric Essence | 67 | "The mapping into which Form is placed" → Priestess = mystery, memory |
| **Energy** | Fall of Events | 11 | "Organization of the cascade of events" → most energetic prime (44% of cards) |

### 1.4 Anchor Evidence

The mapping is anchored by two single-prime Quest cards that determine
all other assignments through constraint propagation:

- **Hierophant** (Card V) activates only prime **31** → Quest 3 = Divinity → **31 → Divinity**
- **Emperor** (Card IV) activates only prime **29** → Quest 5 = Time Matrix → **29 → Time Matrix**

Final disambiguation: the Justice card's own gematria selects prime **19** at
Card VIII (Justice) = Quest 2 = Sole Atom. Therefore **19 → Sole Atom**
and **89 → Synchronicity** (by elimination).

---

## Section 2: The 6+2 Architecture

The Cantong qi (周易參同契, c. 142 CE) maps the lunar month through
**six trigrams** representing the waxing and waning of yang. **Kǎn (☵)
and Lí (☲) are excluded** from the monthly cycle — they are the
alchemical operators, not cyclic phases. Wei Boyang's system places
them outside the rotation as the agents of transformation.

The Astrolabium adopts this structure:
- **6 cyclic Laws** carried by 6 trigrams through the lunar month
- **2 permanent Keys** (Gold and Silver) standing outside the lunar
  cycle, activating at the daily solar cusps (sunrise and sunset)

### 2.1 The Six Cyclic Laws

The six trigrams trace the waxing and waning of yang through the
synodic month. Each phase spans 60° of lunar elongation (~4.92 days).
[SOURCE: Neidan — Cantong qi waxing/waning progression]

#### Waxing (Yang Growing)

| Elongation | Phase | Lunar Day | Trigram | Yang Lines | Law | Prime |
|------------|-------|-----------|---------|------------|-----|-------|
| 0°–59° | New Moon | ~30 | Kūn ☷ | 0 (pure yin) | **Kaos** | 23 |
| 60°–119° | First Crescent | ~3 | Zhèn ☳ | 1 (bottom) | **Sole Atom** | 19 |
| 120°–179° | First Quarter | ~8 | Duì ☱ | 2 | **Time Matrix** | 29 |
| 180°–239° | Full Moon | ~15 | Qián ☰ | 3 (pure yang) | **Synchronicity** | 89 |

#### Waning (Yin Growing)

| Elongation | Phase | Lunar Day | Trigram | Yin Lines | Law | Prime |
|------------|-------|-----------|---------|-----------|-----|-------|
| 240°–299° | First Wane | ~16 | Xùn ☴ | 1 (bottom) | **Geometric Essence** | 67 |
| 300°–359° | Last Quarter | ~23 | Gèn ☶ | 2 | **Arrow of Complexity** | 17 |

Then back to Kūn ☷ (New Moon / Kaos) — the cycle restarts.

### 2.2 The Two Permanent Keys (Solar Cusps)

Following Neidan reversal logic (逆, nì) — the practitioner works with
the container at the moment its contents would naturally escape. The
Keys activate at the hinges between the First Wing (day) and Second
Wing (night) of the temporal substrate. [SOURCE: Neidan — Cantong qi reversal principle. SOURCE: Plum Blossom
Alchemy — Water gate identification from Timothy's EV→element derivation
(~2013). ANALYTICAL CONTRIBUTION — application of nì to cusp assignments.]

| Key | Trigram | Law | Prime | Event | Reversal Logic |
|-----|---------|-----|-------|-------|----------------|
| **Gold Key** | Kǎn ☵ | **Fall of Events** | **11** | Sunrise | Yang ascending — work with Kǎn (container of true yang / True Lead 真鉛) to capture it. The cascade of neutral events begins at dawn. |
| **Silver Key** | Lí ☲ | **Divinity** | **31** | Sunset | Yin descending — work with Lí (container of true yin / True Mercury 真汞) to hold it. The divine spark turns inward at dusk. |

**Cusping window:** The Key is active during the civil twilight period
surrounding its solar cusp. Civil twilight begins/ends when the Sun is
6° below the horizon. The Key event is the astronomical instant of
sunrise or sunset; the cusping window extends from the start of morning
civil twilight to sunrise (Gold Key) and from sunset to the end of
evening civil twilight (Silver Key).

### 2.3 Structural Bridges (Prime Number Relationships)

The prime-number assignments create three structural bridges between
the cyclic and permanent registers:

**Sophie Germain pair: 2(11) + 1 = 23 — Permanent → Cyclic.**
The Gold Key's Fall of Events (11) generates the New Moon's Kaos (23).
The permanent cascade at dawn feeds the cyclic origin. The Sophie
Germain relation is circular: chaos sets the conditions for the
cascade, the cascade generates the next chaos.

**Twin primes (29, 31) — Cyclic ↔ Permanent.**
Time Matrix (29, Duì, cyclic) twins with Divinity (31, Lí/Silver Key,
permanent). The circulating mobile Adonaj-Ba and the crown are twinned
in the number theory.

**Twin primes (17, 19) — Both cyclic (threshold pair).**
Arrow of Complexity (17, Gèn) and Sole Atom (19, Zhèn) mark the two
threshold moments in the lunar month — the last waning and the first
waxing. They bracket the New Moon darkness.

### 2.4 The Earlier Heaven / Later Heaven Parallel

The Primeval Laws / Derivative Laws distinction maps directly onto the
Earlier Heaven / Later Heaven (先天/後天, Xiantian/Houtian) distinction
in the Bagua:

- **Primeval Laws** = cosmological principles prior to Form (Earlier Heaven)
- **Derivative Laws** = Laws in armistice, operating within Form (Later Heaven)

Same mechanic, different tradition's vocabulary.
[ANALYTICAL CONTRIBUTION]

---

## Section 3: Vessel-Trigram Mapping

The eight Extraordinary Vessels of Chinese medicine each carry a
trigram and therefore a Law. This mapping follows the Li Shizhen
tradition (奇經八脈考, Qijing Bamai Kao, 1572). [SOURCE: TCM]

The Law assignment follows from the derivation chain:
**Vessel → Trigram** (Li Shizhen, §3) → **Trigram → Law** (§1 Master Table)

### 3.1 Complete Vessel Table

| Vessel | English | Chinese | Confluent | Coupled | Trigram | Law | Prime |
|--------|---------|---------|-----------|---------|---------|-----|-------|
| **Du Mai** | Governing | 督脈 | SI-3 (Hòuxī) | BL-62 (Shēnmài) | Qián ☰ | Synchronicity | 89 |
| **Ren Mai** | Conception | 任脈 | LU-7 (Lièquē) | KI-6 (Zhàohǎi) | Kūn ☷ | Kaos | 23 |
| **Chong Mai** | Penetrating | 衝脈 | SP-4 (Gōngsūn) | PC-6 (Nèiguān) | Gèn ☶ | Arrow of Complexity | 17 |
| **Dai Mai** | Belt | 帶脈 | GB-41 (Zúlínqì) | SJ-5 (Wàiguān) | Duì ☱ | Time Matrix | 29 |
| **Yang Qiao Mai** | Yang Heel | 陽蹻脈 | BL-62 (Shēnmài) | SI-3 (Hòuxī) | Lí ☲ | Divinity | 31 |
| **Yin Qiao Mai** | Yin Heel | 陰蹻脈 | KI-6 (Zhàohǎi) | LU-7 (Lièquē) | Kǎn ☵ | Fall of Events | 11 |
| **Yang Wei Mai** | Yang Linking | 陽維脈 | SJ-5 (Wàiguān) | GB-41 (Zúlínqì) | Zhèn ☳ | Sole Atom | 19 |
| **Yin Wei Mai** | Yin Linking | 陰維脈 | PC-6 (Nèiguān) | SP-4 (Gōngsūn) | Xùn ☴ | Geometric Essence | 67 |

### 3.2 Vessel Pairs

Each pair shares confluent and coupled points (the coupled point of
one vessel is the confluent of the other):

| Pair | Points | Vessels | Trigram Pair |
|------|--------|---------|-------------|
| 1 | SI-3 / BL-62 | Du Mai + Yang Qiao Mai | Qián ☰ / Lí ☲ |
| 2 | LU-7 / KI-6 | Ren Mai + Yin Qiao Mai | Kūn ☷ / Kǎn ☵ |
| 3 | SP-4 / PC-6 | Chong Mai + Yin Wei Mai | Gèn ☶ / Xùn ☴ |
| 4 | GB-41 / SJ-5 | Dai Mai + Yang Wei Mai | Duì ☱ / Zhèn ☳ |

---

## Section 4: LGBF Calculation — Step by Step

Ling Gui Ba Fa (靈龜八法, "Sacred Turtle Eight Methods") determines
which Extraordinary Vessel is currently open. The calculation combines
a calendar component (daily stem-branch, date only) with a solar
position component (hourly branch, requires location). [SOURCE: TCM]

### 4.1 Reference Date

**January 1, 2000 = 戊午 (Wù Wǔ)**
- Heavenly Stem index: **4** (戊 Wù)
- Earthly Branch index: **6** (午 Wǔ)

This is the epoch from which all daily stem-branch calculations derive.

### 4.2 Daily Stem-Branch from Date

Given a target date:

1. Count the number of days from January 1, 2000 to the target date.
   Call this **Δ** (positive for future dates, negative for past).
2. **Daily Stem index** = (4 + Δ) mod 10
3. **Daily Branch index** = (6 + Δ) mod 12

The mod operation always returns 0–9 (stem) or 0–11 (branch).
For negative Δ, add the modulus first: e.g., (4 + (−3)) mod 10 = 1 mod 10 = 1.

### 4.3 Heavenly Stems Reference

| Index | Chinese | Pinyin | Yin/Yang | Element |
|-------|---------|--------|----------|---------|
| 0 | 甲 | Jiǎ | **Yang** | Wood |
| 1 | 乙 | Yǐ | Yin | Wood |
| 2 | 丙 | Bǐng | **Yang** | Fire |
| 3 | 丁 | Dīng | Yin | Fire |
| 4 | 戊 | Wù | **Yang** | Earth |
| 5 | 己 | Jǐ | Yin | Earth |
| 6 | 庚 | Gēng | **Yang** | Metal |
| 7 | 辛 | Xīn | Yin | Metal |
| 8 | 壬 | Rén | **Yang** | Water |
| 9 | 癸 | Guǐ | Yin | Water |

### 4.4 Earthly Branches Reference

| Index | Chinese | Pinyin | Animal |
|-------|---------|--------|--------|
| 0 | 子 | Zǐ | Rat |
| 1 | 丑 | Chǒu | Ox |
| 2 | 寅 | Yín | Tiger |
| 3 | 卯 | Mǎo | Rabbit |
| 4 | 辰 | Chén | Dragon |
| 5 | 巳 | Sì | Snake |
| 6 | 午 | Wǔ | Horse |
| 7 | 未 | Wèi | Goat |
| 8 | 申 | Shēn | Monkey |
| 9 | 酉 | Yǒu | Rooster |
| 10 | 戌 | Xū | Dog |
| 11 | 亥 | Hài | Pig |

### 4.5 Determining Yin/Yang Day

The daily stem determines whether the day is Yang or Yin:

- **Yang day** (even stem index: 0, 2, 4, 6, 8) → divide by **9**
- **Yin day** (odd stem index: 1, 3, 5, 7, 9) → divide by **6**

### 4.6 Hourly Branch from Solar Position

The hourly branch is the Earthly Branch for the current moment,
determined by solar position (NOT civil clock time). This is the
same calculation used for the Organ Clock (Section 5).

**Procedure:**

1. Obtain **sunrise** and **sunset** times for your date and location
   (from a sunrise/sunset table or ephemeris).
2. If the current time is between sunrise and sunset (day):
   - Divide the day period (sunrise → sunset) into **6 equal parts**
   - The 6 day branches are, in order: **辰(4), 巳(5), 午(6), 未(7), 申(8), 酉(9)**
   - Determine which sixth of the day you are in → that is your branch
3. If the current time is between sunset and next sunrise (night):
   - Divide the night period (sunset → next sunrise) into **6 equal parts**
   - The 6 night branches are, in order: **戌(10), 亥(11), 子(0), 丑(1), 寅(2), 卯(3)**
   - Determine which sixth of the night you are in → that is your branch

**Formula (day):**
```
elapsed = current_time − sunrise
part_duration = (sunset − sunrise) / 6
day_branch_position = floor(elapsed / part_duration)    [0–5]
branch_index = 4 + day_branch_position                  [4–9]
```

**Formula (night):**
```
elapsed = current_time − sunset
part_duration = (next_sunrise − sunset) / 6
night_branch_position = floor(elapsed / part_duration)   [0–5]
branch_index = [10, 11, 0, 1, 2, 3][night_branch_position]
```

**Important:** These are unequal hours. Day branches are shorter in
winter and longer in summer. Night branches are the opposite. At the
equinox, each branch is exactly 2 hours.

### 4.7 Hourly Stem via Five Rat Rule (五鼠遁)

The hourly stem cycles from a starting point determined by the daily stem.

**Formula:**
```
first_zi_stem = ((daily_stem_index mod 5) × 2) mod 10
hourly_stem_index = (first_zi_stem + hourly_branch_index) mod 10
```

**Lookup table (daily stem → first 子 Zǐ hour stem):**

| Daily Stem | Index | First Zǐ Stem | Index |
|------------|-------|---------------|-------|
| 甲 Jiǎ or 己 Jǐ | 0 or 5 | 甲 Jiǎ | 0 |
| 乙 Yǐ or 庚 Gēng | 1 or 6 | 丙 Bǐng | 2 |
| 丙 Bǐng or 辛 Xīn | 2 or 7 | 戊 Wù | 4 |
| 丁 Dīng or 壬 Rén | 3 or 8 | 庚 Gēng | 6 |
| 戊 Wù or 癸 Guǐ | 4 or 9 | 壬 Rén | 8 |

Then add the hourly branch index and take mod 10 to get the hourly stem.

### 4.8 LGBF Substitution Tables

Four substitution numbers are looked up and summed.
[SOURCE: BTR Ch.4 / TCM canonical]

#### Daily Stem Substitution (DS#)

| Stem | 甲(0) | 乙(1) | 丙(2) | 丁(3) | 戊(4) | 己(5) | 庚(6) | 辛(7) | 壬(8) | 癸(9) |
|------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **DS#** | 10 | 9 | 8 | 7 | 6 | 5 | 9 | 8 | 7 | 6 |

#### Daily Branch Substitution (DB#)

| Branch | 子(0) | 丑(1) | 寅(2) | 卯(3) | 辰(4) | 巳(5) | 午(6) | 未(7) | 申(8) | 酉(9) | 戌(10) | 亥(11) |
|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|--------|
| **DB#** | 9 | 8 | 7 | 6 | 5 | 4 | 9 | 8 | 7 | 6 | 5 | 4 |

#### Hourly Stem Substitution (HS#)

Same values as Daily Stem Substitution:

| Stem | 甲(0) | 乙(1) | 丙(2) | 丁(3) | 戊(4) | 己(5) | 庚(6) | 辛(7) | 壬(8) | 癸(9) |
|------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **HS#** | 10 | 9 | 8 | 7 | 6 | 5 | 9 | 8 | 7 | 6 |

#### Hourly Branch Substitution (HB#)

**Different from daily branch substitution** at indices 6–8:

| Branch | 子(0) | 丑(1) | 寅(2) | 卯(3) | 辰(4) | 巳(5) | 午(6) | 未(7) | 申(8) | 酉(9) | 戌(10) | 亥(11) |
|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|--------|
| **HB#** | 9 | 8 | 7 | 6 | 5 | 4 | **3** | **2** | **1** | 9 | 8 | 7 |

Note: DB# and HB# differ at indices 6 (9 vs 3), 7 (8 vs 2), 8 (7 vs 1).

### 4.9 Compute the Sum and Remainder

```
Sum = DS# + DB# + HS# + HB#
```

Then:
- **Yang day:** Remainder = Sum mod 9. If remainder = 0, use **9**.
- **Yin day:** Remainder = Sum mod 6. If remainder = 0, use **6**.

### 4.10 Remainder → Vessel Lookup

**Yang days (mod 9):**

| Remainder | Vessel | Confluent | Trigram | Law |
|-----------|--------|-----------|---------|-----|
| 1 | Yang Qiao Mai | BL-62 | Lí ☲ | Divinity |
| 2 | Yin Qiao Mai | KI-6 | Kǎn ☵ | Fall of Events |
| 3 | Yin Wei Mai | PC-6 | Xùn ☴ | Geometric Essence |
| 4 | Yin Wei Mai | PC-6 | Xùn ☴ | Geometric Essence |
| 5 | Chong Mai | SP-4 | Gèn ☶ | Arrow of Complexity |
| 6 | Yang Wei Mai | SJ-5 | Zhèn ☳ | Sole Atom |
| 7 | Dai Mai | GB-41 | Duì ☱ | Time Matrix |
| 8 | Ren Mai | LU-7 | Kūn ☷ | Kaos |
| 9 (or 0) | Du Mai | SI-3 | Qián ☰ | Synchronicity |

**Yin days (mod 6):**

| Remainder | Vessel | Confluent | Trigram | Law |
|-----------|--------|-----------|---------|-----|
| 1 | Yang Qiao Mai | BL-62 | Lí ☲ | Divinity |
| 2 | Yin Qiao Mai | KI-6 | Kǎn ☵ | Fall of Events |
| 3 | Yin Wei Mai | PC-6 | Xùn ☴ | Geometric Essence |
| 4 | Chong Mai | SP-4 | Gèn ☶ | Arrow of Complexity |
| 5 | Dai Mai | GB-41 | Duì ☱ | Time Matrix |
| 6 (or 0) | Du Mai | SI-3 | Qián ☰ | Synchronicity |

**Note:** On Yin days, only 6 of 8 vessels are accessible. Yang Wei
Mai (Sole Atom) and Ren Mai (Kaos) cannot open on Yin days.

### 4.11 Read the Derivative Law

The vessel's Law (rightmost column above) is the **Derivative Law**
for the current moment. This is the Law operating in the Astral body
through the Extraordinary Vessel system.

---

## Section 5: Organ Clock — 12-fold Solar Division

The Organ Clock determines which meridian is most active at any given
moment. It shares the same temporal substrate as the hourly branch
calculation in Section 4.6 — **they are the same computation.**
[SOURCE: TCM]

### 5.1 Procedure

The hourly branch (computed in §4.6) directly gives you the active organ:

### 5.2 Branch-to-Organ Table

| Branch | Index | Organ | Meridian | Element | Emotion (+) | Emotion (−) |
|--------|-------|-------|----------|---------|-------------|-------------|
| 子 Zǐ | 0 | Gallbladder | GB | Wood | Courage, Decision | Indecision, Resentment |
| 丑 Chǒu | 1 | Liver | LR | Wood | Kindness, Generosity | Anger, Frustration |
| 寅 Yín | 2 | Lung | LU | Metal | Courage, Righteousness | Grief, Sadness |
| 卯 Mǎo | 3 | Large Intestine | LI | Metal | Surrender, Release | Guilt, Defensiveness |
| 辰 Chén | 4 | Stomach | ST | Earth | Openness, Trust | Anxiety, Despair |
| 巳 Sì | 5 | Spleen | SP | Earth | Fairness, Trust | Worry, Mistrust |
| 午 Wǔ | 6 | Heart | HT | Fire | Love, Joy | Hatred, Arrogance |
| 未 Wèi | 7 | Small Intestine | SI | Fire | Discernment, Clarity | Insecurity, Vulnerability |
| 申 Shēn | 8 | Bladder | BL | Water | Peace, Contentment | Fear, Impatience |
| 酉 Yǒu | 9 | Kidney | KI | Water | Gentleness, Wisdom | Fear, Paranoia |
| 戌 Xū | 10 | Pericardium | PC | Fire | Love, Joy, Openness | Hurt, Jealousy |
| 亥 Hài | 11 | San Jiao | SJ | Fire | Hope, Relaxation | Hopelessness, Confusion |

### 5.3 Day and Night Sequences

**Day (sunrise → sunset):** Stomach → Spleen → Heart → Small Intestine → Bladder → Kidney

**Night (sunset → sunrise):** Pericardium → San Jiao → Gallbladder → Liver → Lung → Large Intestine

### 5.4 Anatomical Intersection

An **Anatomical Intersection** occurs when the LGBF vessel's confluent
or coupled point falls on the currently active meridian. For example:
if the LGBF opens Ren Mai (confluent LU-7, coupled KI-6) during the
Lung branch (寅, LU), the Lung meridian is simultaneously the active
organ AND the access point for the open vessel. [ANALYTICAL CONTRIBUTION]

---

## Section 6: Divine Hours — 8-fold Solar Division

The Divine Hours divide the day-night cycle into eight unequal parts:
four day hours (First Wing) and four night hours (Second Wing).
[SOURCE: DAM — BTR Ch.3, "Eight hours of sky"]

### 6.1 Procedure

1. Obtain sunrise and sunset times.
2. **First Wing (Day):** Divide (sunrise → sunset) into 4 equal parts.
3. **Second Wing (Night):** Divide (sunset → next sunrise) into 4 equal parts.

### 6.2 Divine Hours Table

| Hour | Numeral | Wing | Quality | BTR Protocols |
|------|---------|------|---------|---------------|
| I | Prima | Day | Awakening, initiation | VADUSFADAHM Proclamation, Flight of Knowledge |
| II | Seconda | Day | Rising, ascending light | Vision of the Ancient, Drawing Upon the Force |
| III | Terza | Day | Culmination, "wing touches tail" | Object Consecration, Aura Perception |
| IV | Quarta | Day | Completion, declining | Object Consecration, Spoken Thought |
| V | Quinta | Night | Transition, threshold | *Gap: no explicit BTR assignment* |
| VI | Sesta | Night | Deepening, early night | *Gap: no explicit BTR assignment* |
| VII | Settima | Night | Mystery, deep night | *Gap: no explicit BTR assignment* |
| VIII | Ottava | Night | Return, pre-dawn | *Gap: no explicit BTR assignment* |

**Hours V–VIII:** The BTR provides explicit protocol assignments only
for Hours I–IV. Hours V–VIII protocols are a **documented gap** — the
sources do not specify them. This is NOT an opportunity for invention.

### 6.3 Calculation

```
Day hour duration = (sunset − sunrise) / 4
Night hour duration = (next_sunrise − sunset) / 4
```

At the equinox (~12h day, ~12h night), each hour is approximately
3 hours. At the winter solstice in Damanhur (~8h40m day), each day
hour is approximately 2h10m and each night hour approximately 3h50m.

### 6.4 Relationship to Organ Clock

Three Divine Hours span the same duration as one Organ Clock branch
**only at the equinox**. At other times, the relationship is
proportional but not integral. The two systems share the same temporal
substrate (sunrise/sunset) but divide it differently (4+4 vs 6+6).

---

## Section 7: Lunar Phase Determination

The Primeval Law (Soul layer) is determined by the Moon's current phase
within the 6-fold Cantong qi cycle.

### 7.1 Procedure

1. From an ephemeris, determine the Moon's **geocentric ecliptic
   longitude** and the Sun's geocentric ecliptic longitude.
2. Compute the **elongation**: Moon longitude − Sun longitude,
   normalized to 0°–360°. (At New Moon, elongation ≈ 0°. At Full
   Moon, elongation ≈ 180°.)
3. Compute the **phase index**: `floor(elongation / 60) mod 6`
4. Look up the Primeval Law in the table below.

### 7.2 Phase-to-Law Table

| Phase Index | Elongation | Phase Name | Trigram | Law | Prime |
|-------------|------------|------------|---------|-----|-------|
| 0 | 0°–59° | New Moon | Kūn ☷ | Kaos | 23 |
| 1 | 60°–119° | First Crescent | Zhèn ☳ | Sole Atom | 19 |
| 2 | 120°–179° | First Quarter | Duì ☱ | Time Matrix | 29 |
| 3 | 180°–239° | Full Moon | Qián ☰ | Synchronicity | 89 |
| 4 | 240°–299° | First Wane | Xùn ☴ | Geometric Essence | 67 |
| 5 | 300°–359° | Last Quarter | Gèn ☶ | Arrow of Complexity | 17 |

### 7.3 Quick Estimation

If you do not have an ephemeris but know the Moon's visual appearance:

| Visual | Approximate Elongation | Phase |
|--------|----------------------|-------|
| Invisible (New Moon) | 0°–30° | Kūn / Kaos |
| Thin waxing crescent | 30°–90° | Zhèn / Sole Atom |
| First Quarter (half lit) | 90°–120° | Duì / Time Matrix |
| Waxing gibbous | 120°–180° | Duì→Qián / Time Matrix→Synchronicity |
| Full Moon | 170°–190° | Qián / Synchronicity |
| Waning gibbous | 190°–270° | Xùn / Geometric Essence |
| Last Quarter (half lit) | 270°–300° | Gèn / Arrow of Complexity |
| Thin waning crescent | 300°–360° | Gèn / Arrow of Complexity |

This is approximate. For precision, use an ephemeris.

---

## Section 8: Key Detection — Solar Cusps

The Gold Key (Kǎn ☵ / Fall of Events) and Silver Key (Lí ☲ / Divinity)
activate at the solar cusps — the hinges between day and night.

### 8.1 Procedure

1. Obtain **sunrise** and **sunset** times, plus the **civil twilight**
   boundaries for your location and date.
2. **Gold Key window:** From the start of morning civil twilight to
   sunrise. (Sun between −6° and 0° altitude, ascending.)
3. **Silver Key window:** From sunset to the end of evening civil
   twilight. (Sun between 0° and −6° altitude, descending.)
4. If the current time falls within either window, the corresponding
   Key is **active**.

### 8.2 Key Summary

| Key | Window | Trigram | Law | Prime |
|-----|--------|---------|-----|-------|
| Gold | Morning twilight → sunrise | Kǎn ☵ | Fall of Events | 11 |
| Silver | Sunset → evening twilight | Lí ☲ | Divinity | 31 |

### 8.3 Duration

The cusping window duration equals the length of civil twilight, which
varies by latitude and season. At Damanhur (45.4°N):
- Near equinox: ~30–35 minutes
- Near solstice: ~35–40 minutes

At higher latitudes, the window is longer; at equatorial latitudes,
shorter.

---

## Section 9: Law Unity Detection

Law Unity occurs when two or more temporal layers produce the same Law
simultaneously. This is an operatively significant alignment.

### 9.1 Two-Body Unity

**Condition:** Primeval Law (from §7, lunar phase) == Derivative Law
(from §4, LGBF vessel)

The six cyclic Primeval Laws (Kaos, Sole Atom, Time Matrix,
Synchronicity, Geometric Essence, Arrow of Complexity) can match the
Derivative Law when the LGBF opens a vessel carrying the same Law.
Since all eight Laws appear in the LGBF output but only six appear in
the cyclic Primeval rotation, Two-Body Unity is possible for the six
cyclic Laws only. Fall of Events and Divinity cannot participate in
Two-Body Unity because they never appear as Primeval Laws.

### 9.2 Key-Derivative Unity

**Condition:** An active Key's Law == the current Derivative Law (LGBF)

- **Gold Key-Derivative Unity:** LGBF opens Yin Qiao Mai (Kǎn ☵ /
  Fall of Events) during the Gold Key cusping window at sunrise.
- **Silver Key-Derivative Unity:** LGBF opens Yang Qiao Mai (Lí ☲ /
  Divinity) during the Silver Key cusping window at sunset.

Unity on Fall of Events or Divinity occurs when their vessel opens via
LGBF during the corresponding Key cusping window. These Laws participate
in the system exclusively through Key-Derivative Unity — never through
Two-Body Unity, because they are excluded from Primeval rotation.

### 9.3 Three-Body Unity

**Condition:** All three temporal BODIES are aligned simultaneously:
- **Soul** (Primeval Law) == **Astral** (Derivative Law) — i.e.,
  Two-Body Unity is active, AND
- The LGBF vessel's access point (confluent or coupled) falls on the
  **Gross** body's currently active organ meridian — i.e., Anatomical
  Intersection is active.

Three-Body Unity means Law Unity plus Anatomical Intersection: the
Soul and Astral share the same Law, and the Gross body receives the
vessel's access at the active meridian. Solar Keys are cusping EVENTS,
not bodies — they are not required for Three-Body Unity.

There are **12 configurations**: 6 confluent (vessel's confluent point
on the active meridian) and 6 coupled (vessel's coupled point on the
active meridian). Very rare — requires correct lunar phase, correct
LGBF vessel, and correct organ clock branch simultaneously.

See Compound Catalogue §3.1 (Confluent) and §3.2 (Coupled) for the
complete enumeration.

### 9.4 Summary of Unity Types

| Unity Type | Bodies | Condition | Frequency |
|------------|--------|-----------|-----------|
| Two-body | Soul + Astral | Primeval Law == Derivative Law | Uncommon |
| Key-Derivative | Key event + Astral | Key Law == LGBF Law at cusp | Rare |
| Three-body | Soul + Astral + Gross | Two-Body Unity + Anatomical Intersection | Very rare |

---

## Section 10: Divine Months — Lunisolar Calendar

The Damanhurian calendar consists of **12 regular lunar months** (New
Moon to New Moon, ~29.53 days each) plus an **intercalary 13th month**
(VADUSFADAHM) inserted when needed. [SOURCE: DAM]

### 10.1 Epoch

**New Moon of September 22, 1949**, coincident with the Autumn
Equinox of September 23, 1949. This is the origin of the Damanhurian
calendar. [DETERMINED: March 1, 2026]

### 10.2 Month Ordering (ISIS-first)

| # | Name | Tier 0 Character | Group | Great Rite | Element | Alchemical Stage |
|---|------|------------------|-------|------------|---------|-----------------|
| 1 | **ISIS** | The Gatherer | Osirian | **Autumn Equinox** | Air | Nigredo: Gather |
| 2 | **SADAM** | The Mirror-Operator | Operative | **Day of the Dead** | Earth | Nigredo: Mirror |
| 3 | **LIOTHIL** | The Helper | Falcon | — | — | Nigredo: Help |
| 4 | **EOROS** | The Director | Tappetino | **Winter Solstice** | Fire | Nigredo: Birth |
| 5 | **TASUMER** | The Builder | Operative | — | — | Albedo: Build |
| 6 | **MENON** | The Enduring One | Falcon | — | — | Albedo: Endure |
| 7 | **OSIRIS** | The Resurrected | Osirian | **Spring Equinox** | Ether | Albedo: Resurrect |
| 8 | **AGAFEST** | The Celebrant | Falcon | — | — | Albedo: Celebrate |
| 9 | **SAMMA** | The Container | Tappetino | **Divine Marriage** | — | Rubedo: Unite |
| 10 | **SET** | The Destroyer | Osirian | **Summer Solstice** | Water | Rubedo: Destroy |
| 11 | **SADAS** | The Mirror-Keeper | Falcon | — | — | Rubedo: Enter |
| 12 | **DESURIORIS** | The Sovereign | Falcon | — | — | Rubedo: Rule |
| 13 | **VADUSFADAHM** | The Activation | Tappetino | *(intercalary)* | — | Da'ath |

### 10.3 Month Groups

| Group | Members | Pattern |
|-------|---------|---------|
| **Osirian** (IAO) | ISIS (1), OSIRIS (7), SET (10) | I → O → A : Gather → Resurrect → Destroy |
| **Operative** | SADAM (2), TASUMER (5) | Mirror and Build — active work months |
| **Falcon** | LIOTHIL (3), MENON (6), AGAFEST (8), SADAS (11), DESURIORIS (12) | The five entities presiding over the cycle |
| **Tappetino** | EOROS (4), SAMMA (9), VADUSFADAHM (13) | Geometry/activation — the three structural months |

### 10.4 Six Great Rite Anchors

| Great Rite | Month | Approximate Gregorian |
|------------|-------|----------------------|
| Autumn Equinox | Month 1 (ISIS) | September 22–23 |
| Day of the Dead | Month 2 (SADAM) | ~October 31 |
| Winter Solstice | Month 4 (EOROS) | December 21–22 |
| Spring Equinox | Month 7 (OSIRIS) | March 20–21 |
| Divine Marriage | Month 9 (SAMMA) | May 24 |
| Summer Solstice | Month 10 (SET) | June 20–21 |

**No Lion's Gate.** Six Great Rites only.

### 10.5 Three-Movement Alchemical Structure

- **Nigredo** (months 1–4): ISIS → SADAM → LIOTHIL → EOROS.
  Gathering, mirroring, helping, birthing. The dark work.
- **Albedo** (months 5–8): TASUMER → MENON → OSIRIS → AGAFEST.
  Building, enduring, resurrecting, celebrating. The whitening.
- **Rubedo** (months 9–12): SAMMA → SET → SADAS → DESURIORIS.
  Uniting, destroying, entering, ruling. The reddening.

### 10.6 VADUSFADAHM Intercalation

VADUSFADAHM is the **13th month**, inserted when the lunar calendar
drifts far enough that a Great Rite would fall outside its designated
month. This is a standard lunisolar intercalation pattern — the same
structural principle as the Jewish leap month (Adar II) or the Chinese
intercalary month (閏月).

The Activation fires when the timeline needs correction: structurally
necessary, not commemorative. Full intercalation algorithm to be
determined (simplified 7-year rule in old code was a placeholder).

### 10.7 Month Determination Procedure

1. From an ephemeris, find the New Moon dates bracketing the current date.
2. The current month started at the most recent New Moon.
3. Count months from the epoch (New Moon Sep 22, 1949). Each New Moon
   starts the next month in the 12-month sequence. When 12 regular
   months have elapsed and the next New Moon does not align with its
   expected Great Rite anchor, insert VADUSFADAHM.

---

## Section 11: Sephirotic Week

Each lunar quarter-week — the period between consecutive quarter-points
(New Moon, First Quarter, Full Moon, Third Quarter) — contains 7, 8, or
9 days. Each day is named by its planet and its corresponding quality.

### 11.1 Traditional Grounding

The principle of naming calendar days by Sephiroth is traditional, not
invented. The **Sefirat HaOmer** (Counting of the Omer) is an
established Kabbalistic practice: 49 days between Pesach and Shavuot,
organized as 7 weeks of 7 days, each day named by a Sephira combination
("Chesed within Chesed," etc.). [SOURCE: Kabbalistic]. The Sephirotic
Week applies this traditional principle to a new context (lunar
quarter-weeks), and extends it to the Supernals (Binah, Chokmah, Kether)
when the astronomy permits — that extension is [ANALYTICAL CONTRIBUTION].

**Zerubavel's counterfactual** confirms the structural logic. Eviatar
Zerubavel (*The Seven Day Circle*, University of Chicago Press): "Had
they been able, with the help of some sophisticated telescopes, to
observe Uranus, Neptune, and Pluto, the week might have evolved as a
ten-day cycle." Since the IAU reclassified Pluto in 2006, the count is
exactly **9 planets = exactly 9 Sephirotic days**. The tradition
preserved the correct count before the astronomy confirmed it.

The original **shabattu** (Babylonian/Sumerian) was itself a lunar
quarter observation — the week was born from the Moon. The Sephirotic
Week returns the week to its astronomical origin.

### 11.2 The Sephirotic Days

| Day | Planet | Sephira | Quality | Frequency |
|-----|--------|---------|---------|-----------|
| 1 | Sol ☉ | Tiphareth | **Beauty** | Always (100%) |
| 2 | Luna ☽ | Yesod | **Foundation** | Always (100%) |
| 3 | Mars ♂ | Geburah | **Strength** | Always (100%) |
| 4 | Mercury ☿ | Hod | **Splendor** | Always (100%) |
| 5 | Jupiter ♃ | Chesed | **Mercy** | Always (100%) |
| 6 | Venus ♀ | Netzach | **Victory** | Always (100%) |
| 7 | Saturn ♄ | Binah | **Understanding** | ~100% |
| 8 | Uranus ♅ | Chokmah | **Wisdom** | ~65% |
| 9 | Neptune ♆ | Kether | **Crown** | ~22% |

The planetary sequence follows the traditional weekday cycle (Sun, Moon,
Mars, Mercury, Jupiter, Venus, Saturn) extended by the two
trans-Saturnian planets when the lunar quarter extends beyond seven days.
Every Sephirotic week begins at Day 1 = Sol regardless of what civil
weekday it falls on.

Planetary invisibility maps to Sephirotic day rarity: the two outermost
planets cannot be seen with the naked eye, and their corresponding
supernal days manifest only when the lunar quarter gives them room.

**Source:** The weekday planetary cycle derives from the Chaldean
planetary order (planets arranged by orbital period) via the skip-3
mechanism through the 24 planetary hours — a Hellenistic derivation
(Vettius Valens, 2nd century CE) predating the Gregorian calendar by
over a millennium. The Sephirotic day-naming principle is [SOURCE:
Kabbalistic — Sefirat HaOmer]. The planet-to-Sephira correspondences
are [SOURCE: post-GD Qabalah — modern but established]. The extension
to Uranus and Neptune, the variable week length, and the Supernal
rarity argument are [ANALYTICAL CONTRIBUTION].

### 11.3 The Three Excluded Elements

Three elements of the Tree of Life are excluded from the Sephirotic
day count. Each is excluded for a different geometric reason — they are
not spheres, and you cannot count things that are not spheres among
the Sephiroth (which literally means "spheres/numbers"):

| Exclusion | Geometric Type | Sephirotic Week Role | Astrolabium Role |
|-----------|---------------|---------------------|-----------------|
| **Malkuth** (Kingdom) | **Plane** (substrate) | Not a day — the ground on which all days play out | The manifest world the practitioner stands in |
| **Da'ath** (Knowledge / the Abyss) | **Vector** (axis) | Not a day — the galactic radial axis through Sol | VADUSFADAHM intercalary month. Every day during the 13th month is a Da'ath day |
| **Central Fire** | **Point** (pivot) | Not a day — the astronomical instant of the quarter-point | The hinge between weeks. Both destination and origin |

Three different geometric types. Three different reasons for exclusion.
None are spheres. None are days.

### 11.4 Da'ath as Galactic Vector

Da'ath is not a Sephirah because it is not a sphere. It is a **vector**
— the galactic radial axis that passes through Sol between the Galactic
Center (via Ross 154) and the galactic anticenter (via Sirius).

| Star | RA | Distance | Direction |
|------|-----|----------|-----------|
| Sirius | 06h 45m | 8.6 ly | Galactic anticenter |
| Ross 154 | 18h 50m | 9.69 ly | Galactic center |

RA separation: ~12 hours (~180°). Nearly diametrically opposed through
Sol. The BTR confirms: "two spirals that signify two opposite points of
the galaxy, the two opposite directions" (Note 16).

The "not-month" (VADUSFADAHM intercalary) corresponds to the
"not-Sephirah" (Da'ath) which is the "not-sphere" (a vector). The Abyss
is not a place you cross — it is the line that already passes through you,
through Sol/Tiphareth, where the practitioner sits. [ANALYTICAL
CONTRIBUTION — Timothy Paul Bielec, March 1, 2026]

### 11.5 The Seven Roads

The 7 Double Letter planets (Beth/Moon, Gimel/Venus, Daleth/Jupiter,
Kaph/Mars, Peh/Mercury, Resh/Saturn, Tav/Sun) are not day-names but
**roads** — the paths connecting the Sephiroth within the week. The
Continental tradition's planetary correspondences serve as connective
tissue, not as temporal labels. The skip-3 mechanism (24 planetary hours
mod 7 = 3) generates the weekday zigzag through the Tree: Sol → Luna →
Mars → Mercury → Jupiter → Venus → Saturn traces the path
Tiphareth → Yesod → Geburah → Hod → Chesed → Netzach → Binah.

For 9 planets, 24 mod 9 = 6, producing a completely different day-order.
The mathematics restructures the entire sequence. This is why the
Sephirotic solution operates at a different level (spheres, not roads)
rather than forcing the planetary hour mechanism to stretch.

### 11.6 Procedure

1. From an ephemeris, find the dates of the four quarter-points (New
   Moon, First Quarter, Full Moon, Third Quarter) bracketing the
   current date.
2. Identify the most recent quarter-point and the next one.
3. Count the number of **sunrises** (i.e., whole days) between the
   two quarter-points. This gives the week length (7, 8, or 9).
4. Count which day you are on (Day 1 = the first sunrise after the
   most recent quarter-point).
5. Look up the day name in the table above.
6. If the current date falls within the VADUSFADAHM intercalary month,
   the day carries Knowledge (Da'ath) quality regardless of count.

### 11.7 Statistical Distribution (20 years, 2015–2035)

| Week Length | Count | Percentage |
|-------------|-------|------------|
| 7 days | 344 | 34.8% |
| 8 days | 429 | **43.4%** (most common) |
| 9 days | 215 | 21.8% |

Mean: 7.38 days. Distribution is uniform across all four quarter
transitions — no particular quarter is systematically longer or shorter.
[MATHEMATICAL FACT — computed from `ephem` library, 20-year dataset]

---

## Section 12: Worked Examples

All examples use **Damanhur, Italy** (45.4°N, 7.9°E, timezone
Europe/Rome). Sunrise and sunset times are approximate values for
the given dates at this location.

---

### Example 1: Yang Day — January 1, 2000, 11:00 AM CET

**Given:** Sunrise 8:04, Sunset 16:44 (day length 8h40m = 520 min)

#### Step 1: Daily Stem-Branch

- Δ = 0 days from reference date (this IS the reference date)
- Stem: (4 + 0) mod 10 = **4 → 戊 Wù** (Yang, Earth)
- Branch: (6 + 0) mod 12 = **6 → 午 Wǔ** (Horse)

#### Step 2: Yin/Yang Day

- Stem index 4 is **even → Yang day → divide by 9**

#### Step 3: Hourly Branch

- Day branch duration = 520 / 6 ≈ **86.7 minutes** each
- Time since sunrise = 11:00 − 8:04 = **176 minutes**
- Day branch position = floor(176 / 86.7) = floor(2.03) = **2**
- Branch index = 4 + 2 = **6 → 午 Wǔ** (Heart)

#### Step 4: Hourly Stem (Five Rat Rule)

- Daily stem = 4 (戊)
- first_zi_stem = ((4 mod 5) × 2) mod 10 = (4 × 2) mod 10 = **8 → 壬 Rén**
- Hourly stem = (8 + 6) mod 10 = 14 mod 10 = **4 → 戊 Wù**

#### Step 5: Substitution Numbers

| Component | Index | Substitution |
|-----------|-------|-------------|
| DS# | Stem 4 (戊) | **6** |
| DB# | Branch 6 (午) | **9** |
| HS# | Stem 4 (戊) | **6** |
| HB# | Branch 6 (午) | **3** |
| **Sum** | | **24** |

#### Step 6: Remainder

- Yang day → 24 mod 9 = **6**

#### Step 7: Vessel and Derivative Law

- Yang remainder 6 → **Yang Wei Mai** (confluent SJ-5)
- Yang Wei Mai → Zhèn ☳ → **Sole Atom (19)**

#### Step 8: Organ Clock

- Branch 午 Wǔ (index 6) → **Heart** (Fire)
- Emotion (+): Love, Joy. Emotion (−): Hatred, Arrogance.

#### Step 9: Divine Hour

- Day hour duration = 520 / 4 = **130 minutes** each
- Time since sunrise = 176 min
- Hour position = floor(176 / 130) + 1 = 1 + 1 = **Hour II** (Seconda, Rising)

#### Step 10: Lunar Phase

- New Moon January 6, 2000. On January 1, Moon-Sun elongation ≈ **330°**
- Phase index = floor(330 / 60) mod 6 = 5 mod 6 = **5**
- Phase 5 = Gèn ☶ → **Arrow of Complexity (17)**

#### Step 11: Key Detection

- 11:00 AM is well after sunrise → no Gold Key
- Well before sunset → no Silver Key
- **No Key active**

#### Step 12: Law Unity

- Primeval Law = Arrow of Complexity (17)
- Derivative Law = Sole Atom (19)
- **17 ≠ 19 → No Unity**

#### Summary

```
Date: January 1, 2000, 11:00 AM CET
Location: Damanhur (45.4°N, 7.9°E)
Day: 戊午 Wù Wǔ (Yang/Earth day)
Hourly Pillar: 戊午 Wù Wǔ
LGBF Sum: 24, mod 9 = 6 → Yang Wei Mai → Sole Atom (19)
Organ: Heart (Fire) — Love/Joy
Divine Hour: II (Seconda) — Rising, ascending light
Lunar Phase: Last Quarter (Gèn ☶) — Arrow of Complexity (17)
Solar Keys: None active
Law Unity: None (Sole Atom ≠ Arrow of Complexity)
```

---

### Example 2: Yin Day — January 4, 2000, 2:00 PM CET

**Given:** Sunrise 8:05, Sunset 16:45 (day length 8h40m = 520 min)

#### Step 1: Daily Stem-Branch

- Δ = 3 days from reference
- Stem: (4 + 3) mod 10 = **7 → 辛 Xīn** (Yin, Metal)
- Branch: (6 + 3) mod 12 = **9 → 酉 Yǒu** (Rooster)

#### Step 2: Yin/Yang Day

- Stem index 7 is **odd → Yin day → divide by 6**

#### Step 3: Hourly Branch

- Day branch duration = 520 / 6 ≈ **86.7 minutes**
- Time since sunrise = 14:00 − 8:05 = **355 minutes**
- Day branch position = floor(355 / 86.7) = floor(4.09) = **4**
- Branch index = 4 + 4 = **8 → 申 Shēn** (Bladder)

#### Step 4: Hourly Stem (Five Rat Rule)

- Daily stem = 7 (辛)
- first_zi_stem = ((7 mod 5) × 2) mod 10 = (2 × 2) mod 10 = **4 → 戊 Wù**
- Hourly stem = (4 + 8) mod 10 = 12 mod 10 = **2 → 丙 Bǐng**

#### Step 5: Substitution Numbers

| Component | Index | Substitution |
|-----------|-------|-------------|
| DS# | Stem 7 (辛) | **8** |
| DB# | Branch 9 (酉) | **6** |
| HS# | Stem 2 (丙) | **8** |
| HB# | Branch 8 (申) | **1** |
| **Sum** | | **23** |

#### Step 6: Remainder

- Yin day → 23 mod 6 = **5**

#### Step 7: Vessel and Derivative Law

- Yin remainder 5 → **Dai Mai** (confluent GB-41)
- Dai Mai → Duì ☱ → **Time Matrix (29)**

#### Step 8: Organ Clock

- Branch 申 Shēn (index 8) → **Bladder** (Water)
- Emotion (+): Peace, Contentment. Emotion (−): Fear, Impatience.

#### Step 9: Divine Hour

- Day hour duration = 520 / 4 = **130 minutes**
- Time since sunrise = 355 min
- Hour position = floor(355 / 130) + 1 = 2 + 1 = **Hour III** (Terza, Culmination)

#### Step 10: Lunar Phase

- New Moon January 6. On January 4, elongation ≈ **350°**
- Phase index = floor(350 / 60) mod 6 = 5 mod 6 = **5**
- Phase 5 = Gèn ☶ → **Arrow of Complexity (17)**

#### Step 11: Law Unity

- Primeval Law = Arrow of Complexity (17)
- Derivative Law = Time Matrix (29)
- **17 ≠ 29 → No Unity**

#### Summary

```
Date: January 4, 2000, 2:00 PM CET
Location: Damanhur (45.4°N, 7.9°E)
Day: 辛酉 Xīn Yǒu (Yin/Metal day)
Hourly Pillar: 丙申 Bǐng Shēn
LGBF Sum: 23, mod 6 = 5 → Dai Mai → Time Matrix (29)
Organ: Bladder (Water) — Peace/Contentment
Divine Hour: III (Terza) — Culmination
Lunar Phase: Last Quarter (Gèn ☶) — Arrow of Complexity (17)
Solar Keys: None active
Law Unity: None (Time Matrix ≠ Arrow of Complexity)
```

---

### Example 3: Law Unity Event — January 2, 2000, 10:00 AM CET

**Given:** Sunrise 8:04, Sunset 16:44 (day length 8h40m = 520 min)

#### Step 1: Daily Stem-Branch

- Δ = 1 day from reference
- Stem: (4 + 1) mod 10 = **5 → 己 Jǐ** (Yin, Earth)
- Branch: (6 + 1) mod 12 = **7 → 未 Wèi** (Goat)

#### Step 2: Yin/Yang Day

- Stem index 5 is **odd → Yin day → divide by 6**

#### Step 3: Hourly Branch

- Day branch duration = 520 / 6 ≈ **86.7 minutes**
- Time since sunrise = 10:00 − 8:04 = **116 minutes**
- Day branch position = floor(116 / 86.7) = floor(1.34) = **1**
- Branch index = 4 + 1 = **5 → 巳 Sì** (Spleen)

#### Step 4: Hourly Stem (Five Rat Rule)

- Daily stem = 5 (己)
- first_zi_stem = ((5 mod 5) × 2) mod 10 = (0 × 2) mod 10 = **0 → 甲 Jiǎ**
- Hourly stem = (0 + 5) mod 10 = **5 → 己 Jǐ**

#### Step 5: Substitution Numbers

| Component | Index | Substitution |
|-----------|-------|-------------|
| DS# | Stem 5 (己) | **5** |
| DB# | Branch 7 (未) | **8** |
| HS# | Stem 5 (己) | **5** |
| HB# | Branch 5 (巳) | **4** |
| **Sum** | | **22** |

#### Step 6: Remainder

- Yin day → 22 mod 6 = **4**

#### Step 7: Vessel and Derivative Law

- Yin remainder 4 → **Chong Mai** (confluent SP-4)
- Chong Mai → Gèn ☶ → **Arrow of Complexity (17)**

#### Step 8: Organ Clock

- Branch 巳 Sì (index 5) → **Spleen** (Earth)
- Emotion (+): Fairness, Trust. Emotion (−): Worry, Mistrust.

#### Step 9: Divine Hour

- Day hour duration = 520 / 4 = **130 minutes**
- Time since sunrise = 116 min
- Hour position = floor(116 / 130) + 1 = 0 + 1 = **Hour I** (Prima, Awakening)

#### Step 10: Lunar Phase

- New Moon January 6. On January 2, elongation ≈ **338°**
- Phase index = floor(338 / 60) mod 6 = 5 mod 6 = **5**
- Phase 5 = Gèn ☶ → **Arrow of Complexity (17)**

#### Step 11: Law Unity Check

- Primeval Law = **Arrow of Complexity (17)**
- Derivative Law = **Arrow of Complexity (17)**
- **17 == 17 → TWO-BODY UNITY**

#### Step 12: Key Check

- 10:00 AM is well past sunrise → no Gold Key active
- Not near sunset → no Silver Key active
- This is a **Two-body Unity** (not Three-body)

#### What This Means

At this moment, the slow rhythm (Moon → Gèn → Arrow of Complexity) and
the fast rhythm (LGBF → Chong Mai → Gèn → Arrow of Complexity) produce
the same Law simultaneously. The Penetrating Vessel (Chong Mai) is open
at SP-4, and the Sephirotic body is in the Arrow of Complexity's lunar
phase. Both layers say: this is a moment where complexity increases,
where the arrow points toward the exit of Form. The perception pair is
Curiosity and Expansion (+) or Eternal Reduction (−).

#### Summary

```
Date: January 2, 2000, 10:00 AM CET
Location: Damanhur (45.4°N, 7.9°E)
Day: 己未 Jǐ Wèi (Yin/Earth day)
Hourly Pillar: 己巳 Jǐ Sì
LGBF Sum: 22, mod 6 = 4 → Chong Mai → Arrow of Complexity (17)
Organ: Spleen (Earth) — Fairness/Trust
Divine Hour: I (Prima) — Awakening
Lunar Phase: Last Quarter (Gèn ☶) — Arrow of Complexity (17)
Solar Keys: None active
*** TWO-BODY LAW UNITY: Arrow of Complexity (17) ***
```

---

## Section 13: Cross-Dimensional Resonance Detection

Beyond structural compounds (Section 11), the Astrolabium detects
**thirteen cross-dimensional resonances** — alignments between
interpretive qualities that span different temporal layers. Nine
produce Boolean (active/inactive) results; four produce state values.
All lookup tables needed for pen-and-paper detection are provided here.

**Source attribution:** Resonance type definitions and lookup tables are
[ANALYTICAL CONTRIBUTION]. The underlying data (Wu Xing assignments,
Chia correspondences, Adonaj-Ba centers) are [SOURCE: TCM] and [SOURCE:
DAM] as tagged in Sections 1–3. The Plum Blossom Alchemy element mapping
is [ANALYTICAL CONTRIBUTION — Timothy Paul Bielec, ~2013] derived from
[SOURCE: TCM] canonical correspondences (EV → confluent point → host
meridian → Wu Xing element, with Six Qi fire distinction from the
Huáng Dì Nèi Jīng).

### 13.1 Elemental Resonances (Type A — Deterministic)

Three resonances compare Wu Xing elements across layers. All use exact
matching — either the elements are the same or they are not.

**Hierarchy:** R_WX_03 (Plum Blossom) is the **primary** elemental bridge.
Its derivation passes through the practitioner's body (EV → confluent point
→ host meridian → Wu Xing element), threading the 8-trigram system directly
to TCM. R_WX_01 and R_WX_02 use the canonical I Ching trigram-element
associations. Both are tracked because they produce different resonance
patterns.

**R_WX_01: Canonical Trigram-Organ Wu Xing Match.**
Compare the Primeval trigram's canonical Wu Xing (Table 13A) with the active
organ's Wu Xing element (from Section 3, Table 3.1). Cosmological mapping.

**Table 13A — Trigram Canonical Wu Xing**

| Trigram | Wu Xing |
|---------|---------|
| Qián ☰ | Metal |
| Kūn ☷ | Earth |
| Zhèn ☳ | Wood |
| Xùn ☴ | Wood |
| Kǎn ☵ | Water |
| Lí ☲ | Fire |
| Gèn ☶ | Earth |
| Duì ☱ | Metal |

Detection: `trigram_wu_xing == organ_element` → active.

**R_WX_02: Canonical Vessel-Organ Wu Xing Match.**
The Derivative vessel's Law → that Law's trigram → canonical Wu Xing
(Table 13A) compared with the active organ's element. Cosmological mapping.

Detection: Look up the Derivative vessel's Law (Section 4), find
that Law's trigram (Section 1.1), find that trigram's canonical Wu Xing
(Table 13A). Compare with organ element. Same element → active.

**R_WX_03: Plum Blossom Wu Xing Match (PRIMARY BRIDGE).**
The Primeval trigram's Plum Blossom assignment (from Section 2, Table
2.2) mapped to a Wu Xing element via Table 13B, compared with the
active organ's element. The derivation chain (EV → confluent point →
host meridian → Wu Xing) passes through the body.

**Table 13B — Plum Blossom to Wu Xing Mapping**

| Plum Blossom Assignment | Wu Xing |
|------------------------|---------|
| Imperial Fire | Fire |
| Min. Fire Yang | Fire |
| Min. Fire Yin | Fire |
| Yang Water | Water |
| Yin Water | Water |
| Metal | Metal |
| Earth | Earth |
| Wood | Wood |

Detection: `plum_blossom_wu_xing == organ_element` → active.

### 13.2 Qualitative Resonances (Type B — Graded)

Three resonances compare interpretive qualities. Results are graded
**EXACT** (strongest), **NATURAL** (recognizable affinity), or **NONE**
(no match). The lookup tables encode pre-authored semantic judgments.

**R_CLR_01: Color Affinity.**
Compare the Primeval Law's color (Section 1.1) with the Chia color for
the active organ's Wu Xing element (Section 3, Table 3.2).

**Table 13C — Color Affinity Grades**

| Law Color | Chia Color (Element) | Grade |
|-----------|---------------------|-------|
| Green (Sole Atom) | Green (Wood) | **EXACT** |
| White (Divinity) | White (Metal) | **EXACT** |
| Yellow Gold (Kaos) | Yellow (Earth) | NATURAL |
| Orange (Synchronicity) | Red (Fire) | NATURAL |
| Indigo (Fall of Events) | Blue/Black (Water) | NATURAL |
| Azure Blue (Arrow of Complexity) | Blue/Black (Water) | NATURAL |
| Silver (Time Matrix) | White (Metal) | NATURAL |
| Brick Red (Geometric Essence) | Red (Fire) | NATURAL |

Any combination not listed = NONE. Active when grade ≠ NONE.

**R_EPR_01: Emotion-Perception Resonance.**
Compare the Chia emotional quality (positive or negative) for the
active organ's element with the Primeval Law's perception pair.

**Table 13D — Emotion-Perception Grades**

| Law | Element | Polarity | Grade | Rationale |
|-----|---------|----------|-------|-----------|
| Divinity | Fire | neg | **EXACT** | Both: "Hatred" |
| Divinity | Fire | pos | **EXACT** | Both: "Love/Joy" |
| Sole Atom | Wood | pos | NATURAL | Kindness ≈ Renewal |
| Kaos | Earth | neg | NATURAL | Worry ≈ Demolition |
| Fall of Events | Water | neg | NATURAL | Fear ≈ Loneliness |
| Arrow of Complexity | Metal | neg | NATURAL | Grief ≈ Reduction |
| Time Matrix | Metal | neg | NATURAL | Grief ≈ Pain/Suffering |
| Synchronicity | Fire | pos | NATURAL | Love ≈ Coherent force |

Any combination not listed = NONE. Active when grade ≠ NONE.

**R_ABD_01: Adonaj-Ba Proximity.**
Compare the Primeval Law's Adonaj-Ba center (Section 1.1) with the
active organ. Grades reflect anatomical relationship.

**Table 13E — Adonaj-Ba Organ Proximity Grades**

| Adonaj-Ba | Organ | Grade |
|-----------|-------|-------|
| Heart | Heart | **EXACT** |
| Solar Plexus | Stomach | **EXACT** |
| Heart | Sm Intestine | ADJACENT |
| Heart | Pericardium | ADJACENT |
| Solar Plexus | Spleen | ADJACENT |
| Sexual Organs | Kidney | ADJACENT |
| Sexual Organs | Bladder | ADJACENT |
| Sacrum | Kidney | ADJACENT |
| Sacrum | Bladder | ADJACENT |
| Throat | Lung | ADJACENT |
| Solar Plexus | Liver | PROXIMAL |
| Solar Plexus | Gallbladder | PROXIMAL |
| Sacrum | Lg Intestine | PROXIMAL |
| Crown | San Jiao | PROXIMAL |
| Third Eye | Liver | PROXIMAL |
| Third Eye | Gallbladder | PROXIMAL |
| Throat | Lg Intestine | PROXIMAL |
| Mobile 8th | San Jiao | PROXIMAL |

Any combination not listed = NONE. Active when grade ≠ NONE.
Grade hierarchy: EXACT > ADJACENT > PROXIMAL > NONE.

### 13.3 Rhythmic Resonances (Type A — Deterministic)

**R_LUN_01: Waxing-Wing Alignment.**
Compare lunar phase direction with the solar wing.

| Condition | Result |
|-----------|--------|
| Waxing Moon + Day Wing | **ALIGNED** |
| Waning Moon + Night Wing | **ALIGNED** |
| Waxing Moon + Night Wing | Not aligned |
| Waning Moon + Day Wing | Not aligned |

Waxing = phases 1, 2, 3 (New Moon through Full Moon).
Waning = phases 4, 5, 0 (Full Moon through New Moon).
Day Wing = sunrise to sunset. Night Wing = sunset to sunrise.

**R_LUN_02: Yang Count (State Value).**
Not a Boolean resonance. Track the yang line count from the current
phase's trigram:

| Phase Index | Trigram | Yang Lines |
|-------------|---------|-----------|
| 0 (New Moon) | Kūn ☷ | 0 |
| 1 (First Crescent) | Zhèn ☳ | 1 |
| 2 (First Quarter) | Duì ☱ | 2 |
| 3 (Full Moon) | Qián ☰ | 3 |
| 4 (First Wane) | Xùn ☴ | 2 |
| 5 (Last Quarter) | Gèn ☶ | 1 |

Record the value (0–3). It traces the energetic wave through the month.

### 13.4 Calendrical Resonances

**R_SPH_01: Sephirotic-Quest Match.**
Compare the Sephirotic day's planet (Section 10.3) with the Primeval
Law's Quest Tarot Continental attribution.

**Table 13F — Quest Tarot Continental Attributions**

| Law | Quest Tarot | Continental Attribution |
|-----|-------------|------------------------|
| Synchronicity | Magician | Air (Mother — Aleph) |
| Sole Atom | Justice | Cancer (Simple — Cheth) |
| Divinity | Hierophant | Aries (Simple — Heh) |
| Geometric Essence | Priestess | Moon (Double — Beth) |
| Time Matrix | Emperor | Jupiter (Double — Daleth) |
| Kaos | Death/Renewal | Water (Mother — Mem) |
| Fall of Events | World | Sun (Double — Tav) |
| Arrow of Complexity | Star | Mercury (Double — Peh) |

**Table 13G — Quest Attribution to Sephirotic Planet Matching**

Only planetary attributions (not elements/zodiacal signs) can match
Sephirotic planets. The matchable Quest-Law-Planet triples:

| Law | Quest Attribution | Matches Sephirotic Planet |
|-----|------------------|--------------------------|
| Geometric Essence | Moon | Luna (Day 2) |
| Time Matrix | Jupiter | Jupiter (Day 5) |
| Fall of Events | Sun | Sol (Day 1) |
| Arrow of Complexity | Mercury | Mercury (Day 4) |

Laws with elemental or zodiacal Quest attributions (Synchronicity/Air,
Sole Atom/Cancer, Divinity/Aries, Kaos/Water) **never** match a
Sephirotic planet.

Detection: Check Table 13G. If the Primeval Law's matching planet
equals today's Sephirotic planet → active.

**R_SEA_01: Season-Great Rite Alignment.**
Compare the Chia season for the active organ's element with the current
month's Great Rite seasonal position.

**Table 13H — Chia Element Seasons**

| Wu Xing Element | Chia Season |
|----------------|-------------|
| Wood | Spring |
| Fire | Summer |
| Earth | Late Summer |
| Metal | Autumn |
| Water | Winter |

**Table 13I — Great Rite Season Alignments**

| Great Rite | Season(s) that match |
|------------|---------------------|
| Autumn Equinox | Autumn |
| Day of the Dead | Autumn |
| Winter Solstice | Winter |
| Spring Equinox | Spring |
| Divine Marriage | Summer, Late Summer |
| Summer Solstice | Summer |

Detection: Look up the organ's Chia season (Table 13H). Look up the
current month's Great Rite (if any) and find matching seasons
(Table 13I). If the Chia season appears → active. Months without
Great Rites never trigger this resonance.

### 13.5 Calendrical State Values

Three additional values are extracted from the calendar, not compared:

**R_CAL_01: Alchemical Stage.**

| Months | Stage |
|--------|-------|
| 1–4 | Nigredo |
| 5–8 | Albedo |
| 9–12 | Rubedo |
| 13 | Da'ath |

**R_CAL_02: Month Group.**

| Months | Group |
|--------|-------|
| 1 (ISIS), 4 (EOROS), 7 (OSIRIS), 10 (SET) | Osirian |
| 2 (SADAM), 5 (TASUMER), 8 (AGAFEST), 11 (SADAS) | Falcon |
| 3 (LIOTHIL), 6 (MENON), 9 (SAMMA), 12 (DESURIORIS) | Operative |
| 13 (VADUSFADAHM) | Tappetino |

**R_CAL_03: IAO Position.**

| Month | IAO |
|-------|-----|
| 1 (ISIS) | I |
| 7 (OSIRIS) | O |
| 10 (SET) | A |
| All others | — |

### 13.6 Resonance Detection Procedure (Pen and Paper)

After completing the structural compound checks (Section 11), detect
resonances in this order:

1. **Elemental** (~30 seconds): Look up Primeval trigram Wu Xing
   (Table 13A). Compare with organ element. Check Derivative vessel's
   trigram Wu Xing. Check Plum Blossom mapping (Table 13B).

2. **Qualitative** (~60 seconds): Look up Law color and organ Chia
   color (Table 13C). Check emotion-perception (Table 13D). Check
   Adonaj-Ba proximity (Table 13E).

3. **Rhythmic** (~15 seconds): Check waxing/waning vs. day/night wing.
   Record yang count.

4. **Calendrical** (~45 seconds): Check Sephirotic-Quest match
   (Tables 13F–G). Check Season-Great Rite (Tables 13H–I). Record
   alchemical stage, month group, IAO position.

**Total additional time: ~2.5 minutes.** The full computation
(Sections 4–12 + Section 13) takes approximately 13–14 minutes.

### 13.7 Worked Example — Resonance Detection

Continuing Example 1 from Section 12 (January 2, 2000, 10:00 AM,
Damanhur):

**State from Section 12:**
- Primeval trigram: Gèn ☶ (phase 5, Arrow of Complexity)
- Organ: Spleen (Earth)
- Wing: Day
- Waxing: No (phase 5 = waning)
- Sephirotic day planet: (not computed in original example — would
  need the lunar quarter lookup)
- Month: (divine month not computed in original example)

**Elemental:**
- Trigram Wu Xing: Gèn = **Earth** (Table 13A)
- Organ element: **Earth**
- Earth == Earth → **R_WX_01 ACTIVE**
- Derivative vessel (Chong Mai) → Arrow of Complexity → Gèn → Earth
- Earth == Earth → **R_WX_02 ACTIVE**
- Plum Blossom of Gèn: Earth → Earth (Table 13B)
- Earth == Earth → **R_WX_03 ACTIVE** (triple elemental match)

**Qualitative:**
- Law color: Azure Blue (Arrow of Complexity)
- Chia color for Earth: Yellow
- Azure Blue : Yellow → not in Table 13C → **NONE**
- Emotion-Perception: Arrow of Complexity × Earth → not in Table 13D
  → **NONE**
- Adonaj-Ba: Arrow of Complexity → Third Eye
- Third Eye : Spleen → not in Table 13E → **NONE**

**Rhythmic:**
- Waning + Day Wing → **not aligned**
- Yang count: Gèn = **1**

**Result:** Three elemental resonances active (triple Wu Xing Earth
match), zero qualitative, zero rhythmic Boolean. This is a moment of
concentrated Earth quality — the cosmic principle (Gèn/Earth), the
deep vessel (Chong Mai via Gèn/Earth), and the body's surface organ
(Spleen/Earth) all share the same elemental character.

---

## Appendix A: Complete Substitution Tables

For quick reference during pen-and-paper calculation.

### A.1 Daily Stem Substitution (DS#)

```
甲 Jiǎ   (0) = 10       己 Jǐ    (5) = 5
乙 Yǐ    (1) = 9        庚 Gēng  (6) = 9
丙 Bǐng  (2) = 8        辛 Xīn   (7) = 8
丁 Dīng  (3) = 7        壬 Rén   (8) = 7
戊 Wù    (4) = 6        癸 Guǐ   (9) = 6
```

Pattern: 10, 9, 8, 7, 6, 5, 9, 8, 7, 6

### A.2 Daily Branch Substitution (DB#)

```
子 Zǐ    (0) = 9        午 Wǔ    (6) = 9
丑 Chǒu  (1) = 8        未 Wèi   (7) = 8
寅 Yín   (2) = 7        申 Shēn  (8) = 7
卯 Mǎo   (3) = 6        酉 Yǒu   (9) = 6
辰 Chén  (4) = 5        戌 Xū   (10) = 5
巳 Sì    (5) = 4        亥 Hài  (11) = 4
```

Pattern: 9, 8, 7, 6, 5, 4 — repeats twice

### A.3 Hourly Stem Substitution (HS#)

**Same as Daily Stem Substitution** (A.1 above).

### A.4 Hourly Branch Substitution (HB#)

```
子 Zǐ    (0) = 9        午 Wǔ    (6) = 3  ← DIFFERENT
丑 Chǒu  (1) = 8        未 Wèi   (7) = 2  ← DIFFERENT
寅 Yín   (2) = 7        申 Shēn  (8) = 1  ← DIFFERENT
卯 Mǎo   (3) = 6        酉 Yǒu   (9) = 9
辰 Chén  (4) = 5        戌 Xū   (10) = 8
巳 Sì    (5) = 4        亥 Hài  (11) = 7
```

Pattern: 9, 8, 7, 6, 5, 4, **3, 2, 1**, 9, 8, 7

**The three bold values (午=3, 未=2, 申=1) are where the hourly table
differs from the daily table (午=9, 未=8, 申=7).**

---

## Appendix B: Remainder → Vessel Lookup (Large Format)

### B.1 Yang Days (Sum mod 9)

```
Remainder 1 → Yang Qiao Mai  (BL-62)  → Lí ☲   → Divinity (31)
Remainder 2 → Yin Qiao Mai   (KI-6)   → Kǎn ☵  → Fall of Events (11)
Remainder 3 → Yin Wei Mai    (PC-6)   → Xùn ☴  → Geometric Essence (67)
Remainder 4 → Yin Wei Mai    (PC-6)   → Xùn ☴  → Geometric Essence (67)
Remainder 5 → Chong Mai      (SP-4)   → Gèn ☶  → Arrow of Complexity (17)
Remainder 6 → Yang Wei Mai   (SJ-5)   → Zhèn ☳ → Sole Atom (19)
Remainder 7 → Dai Mai        (GB-41)  → Duì ☱  → Time Matrix (29)
Remainder 8 → Ren Mai        (LU-7)   → Kūn ☷  → Kaos (23)
Remainder 9 → Du Mai         (SI-3)   → Qián ☰ → Synchronicity (89)
(Remainder 0 = Remainder 9)
```

### B.2 Yin Days (Sum mod 6)

```
Remainder 1 → Yang Qiao Mai  (BL-62)  → Lí ☲   → Divinity (31)
Remainder 2 → Yin Qiao Mai   (KI-6)   → Kǎn ☵  → Fall of Events (11)
Remainder 3 → Yin Wei Mai    (PC-6)   → Xùn ☴  → Geometric Essence (67)
Remainder 4 → Chong Mai      (SP-4)   → Gèn ☶  → Arrow of Complexity (17)
Remainder 5 → Dai Mai        (GB-41)  → Duì ☱  → Time Matrix (29)
Remainder 6 → Du Mai         (SI-3)   → Qián ☰ → Synchronicity (89)
(Remainder 0 = Remainder 6)
```

**On Yin days, Yang Wei Mai (Sole Atom) and Ren Mai (Kaos) are
inaccessible.**

---

## Appendix C: Source Attribution Index

Every table and mapping in this guidebook, with its epistemic source.

### C.1 From Damanhurian Teaching [SOURCE: DAM]

| Item | Location | Detail |
|------|----------|--------|
| Eight Primeval Law names and descriptions | §1.1, Eight Laws Source Text | Falco Tarassaco's teaching |
| Adonaj-Ba body centers | §1.1, Quest document | Body center for each Law |
| Quest names (full) | §1.1, The 8 Quests document | "Act in Order to Be", etc. |
| Colors | §1.1, Quest document | arancio, verde, bianco, etc. |
| Perception pairs | §1.2, Quest document | +/− emotional poles |
| Three Reservoirs | §1.3, Magic Levels and Man Tanks | Will/Memory/Energy → Law |
| Divine Hour qualities I–IV | §6.2 | BTR Ch.3 protocol assignments |
| Hours V–VIII: gap documented | §6.2 | Sources do not specify |
| Divine Month names | §10.2 | The Damanhurian calendar |
| Great Rite anchors | §10.4 | Six Great Rites |

### C.2 From Traditional Chinese Medicine [SOURCE: TCM]

| Item | Location | Detail |
|------|----------|--------|
| Heavenly Stems table | §4.3 | Standard 10-stem system |
| Earthly Branches table | §4.4 | Standard 12-branch system |
| Yin/Yang day determination | §4.5 | Even/odd stem index |
| Five Rat Rule | §4.7 | 五鼠遁 hourly stem formula |
| LGBF substitution tables | §4.8 | Standard LGBF values |
| LGBF remainder → vessel tables | §4.10 | Li Shizhen tradition |
| Vessel-Trigram mapping | §3.1 | Qijing Bamai Kao (1572) |
| Organ clock correspondences | §5.2 | Standard TCM organ clock |
| Vessel confluent/coupled points | §3.1 | Standard acupuncture |

### C.3 From Neidan / Cantong qi [SOURCE: Neidan]

| Item | Location | Detail |
|------|----------|--------|
| 6+2 architecture | §2 | Cantong qi lunar trigram cycle |
| Kan/Li as alchemical operators | §2.2 | Wei Boyang tradition |
| Reversal logic (nì 逆) | §2.2 | Work with container at cusp |

### C.4 From Plum Blossom Alchemy [ANALYTICAL CONTRIBUTION — Timothy Paul Bielec, ~2013]

| Item | Location | Detail |
|------|----------|--------|
| Plum Blossom element mapping | §2 | EV → confluent point → host meridian → Wu Xing element derivation |
| Water gate identification | §2.2 | Kǎn/Lí carry Water in Plum Blossom system |
| Gold/Silver Key sunrise/sunset | §2.2 | Water gate practice at solar cusps |

### C.5 Other Analytical Contributions [ANALYTICAL CONTRIBUTION]

| Item | Location | Detail |
|------|----------|--------|
| Trigram → Law mapping | §1.1 | Timothy's synthesis (2013) |
| Prime → Law mapping | §1.1 | Constraint propagation derivation |
| Quest short names | §1.1 | ACTION, CONTINUITY, etc. |
| Neidan reversal applied to cusps | §2.2 | Gold Key = Fall of Events, Silver Key = Divinity |
| Sophie Germain / twin prime bridges | §2.3 | Structural number theory observation |
| Earlier/Later Heaven parallel | §2.4 | Primeval/Derivative = Xiantian/Houtian |
| Anatomical Intersection concept | §5.4 | LGBF point on active meridian |
| Sephirotic Week day-naming | §11.1 | Traditional planet-quality correspondences applied to lunar quarter days |
| Sephirotic Week planetary cycle | §11.1 | Weekday order (Sol→Saturn) + trans-Saturnians (Uranus, Neptune) |
| Day 0 = Knowledge | §11.1 | VADUSFADAHM intercalary days carry Knowledge quality |
| Three-movement alchemical staging | §10.5 | Nigredo/Albedo/Rubedo monthly structure |
| Month groupings | §10.3 | Osirian/Operative/Falcon/Tappetino |
| ISIS-first calendar ordering | §10.2 | Epoch and month sequence |

### C.6 Mathematical Facts [MATHEMATICAL FACT]

| Item | Location | Detail |
|------|----------|--------|
| Stem-branch arithmetic | §4.2 | Modular arithmetic from reference date |
| LGBF sum and remainder | §4.9 | Deterministic calculation |
| Lunar elongation → phase | §7.1 | Geometric computation |
| Sephirotic week statistics | §11.3 | 20-year ephem computation |

---

## Appendix D: Design Notes — How We Got Here

This appendix records the key learnings and corrections accumulated
across the derivation sessions (January–March 2026). Every entry
corresponds to a problem encountered, a correction made, or an insight
that resolved a structural question. A practitioner building from this
specification should understand not only WHAT the system is but WHY
certain choices were made.

### D.1 The Civil Time Violation (January 2026)

The single most damaging error in the project's history. The initial
implementation used civil clock time ("03:00-05:00") for the Earthly
Branch hours — importing the TCM organ clock from modern clinical
practice, where practitioners use wall clocks. But the Earthly Branch
system predates mechanical clocks by millennia. The branches are a
**12-fold solar position division**, not a clock-time lookup. At
Damanhur's latitude (45.4°N), the winter solstice day is ~8h40m: the
"equal two-hour branches" are off by 40 minutes at the extremes.

**The fix:** ALL hourly calculations now derive from sunrise/sunset at
the practitioner's latitude and longitude. No function signature omits
location parameters. This constraint required a complete specification
rewrite (v2.1 and v2.2 of the tech spec were contaminated and are
permanently retired). See `ASTROLABIUM_PROJECT_MIDMORTEM.md` for the
full error history.

**The lesson:** If a traditional system was designed before a modern
convenience (clocks, calendars, time zones), do not retrofit the modern
convenience onto it. Compute from the original substrate.

### D.2 The 6+2 Architecture (February–March 2026)

The initial mapping placed all 8 trigrams in the lunar cycle. But the
Cantong qi tradition (Wei Boyang, c. 142 CE) specifically **excludes**
Kǎn ☵ and Lí ☲ from the monthly rotation. They are the alchemical
operators — true lead and true mercury — not cyclic phases. Forcing them
into the lunar rotation created an 8-phase system that departed from its
own cited source.

**The fix:** 6 cyclic trigrams carry 6 Laws through the lunar month at
60° intervals. Kǎn and Lí stand outside the rotation as the Gold and
Silver Keys, activating at the solar cusps (sunrise and sunset). This
honors the Cantong qi tradition while solving the mapping problem more
elegantly: the Keys find their natural home at the daily solar hinges
rather than being forced into the lunar rotation.

**The lesson:** When citing a source tradition, honor it. If the
tradition says "these two are excluded," do not include them.

### D.3 Neidan Reversal Logic (March 2026)

The Gold and Silver Key assignments follow **nì** (逆, reversal) — the
Neidan principle that the practitioner works with the container at the
moment its contents would naturally escape:

- **Gold Key (Kǎn ☵, sunrise):** Yang is ascending — work with Kǎn
  (the container of true yang / True Lead) to capture it.
- **Silver Key (Lí ☲, sunset):** Yin is descending — work with Lí
  (the container of true yin / True Mercury) to hold it.

This is not an arbitrary assignment. It follows directly from alchemical
principle: at the moment of maximum loss, the adept applies the
corresponding container. The cusping window (civil twilight) provides
the operative timeframe.

### D.4 The Kǎn/Zhèn Vessel-Law Swap (March 2026)

The vessel-trigram mapping from Li Shizhen (Qijing Bamai Kao, 1572)
assigns **Kǎn ☵ to Yin Qiao Mai** and **Zhèn ☳ to Yang Wei Mai**. An
early version of the guidebook had these swapped — Kǎn carrying Sole
Atom (19) and Zhèn carrying Fall of Events (11). The error was caught
by checking the complete derivation chain: Vessel → Trigram (Li Shizhen)
→ Trigram → Law (Master Table). The correction was propagated across all
files.

**The lesson:** When a mapping passes through a derivation chain
(A → B → C), verify each link independently. Errors compound silently.

### D.5 The Sephirotic Week Day Ordering (March 2026)

Initial versions named the days ascending the Tree of Life: Day 1 =
Yesod (Foundation), Day 2 = Hod (Splendor), etc. This produced days
that did not follow any established planetary sequence.

The corrected version uses the **traditional weekday planetary cycle**
(Sun → Moon → Mars → Mercury → Jupiter → Venus → Saturn), which IS
a Sephirotic sequence — it traces the path Tiphareth → Yesod → Geburah
→ Hod → Chesed → Netzach → Binah through the Tree via the skip-3
planetary hours mechanism (Vettius Valens, 2nd century CE).

The English qualities come from each planet's traditional Sephirotic
correspondence: Sol = Tiphareth = Beauty, Luna = Yesod = Foundation,
etc. The Sephirotic naming is PRESERVED but arrives through the
traditional planetary mechanism rather than through an ascending-Tree
walk.

**The lesson:** Do not invent a new ordering when a traditional one
exists that encodes the same structure.

### D.6 The Calendar Architecture (March 2026)

The month ordering was determined by the Osirian divine family (ISIS,
OSIRIS, SET, EOROS) holding the four cardinal Great Rites, confirmed by
the Stellar Navigation Proof (ISIS = Alpha Centauri, EOROS = Ross 154,
OSIRIS = Sol, SET = Sirius). The mythological sequence (SET kills
OSIRIS → ISIS gathers his body → EOROS is born to avenge him) determined
the inter-rite spacing. Three-movement alchemical staging (Nigredo,
Albedo, Rubedo) divided the year into four-month blocks.

The epoch — **New Moon of September 22, 1949** — is the cleanest
possible conjunction: the New Moon falls ~24 hours before the Autumn
Equinox. Oberto Airaudi was born May 29, 1950 = Year 1, Month 9
(SAMMA / Divine Marriage). The calendar was verified by computing all
six Great Rite anchors for Year 1 — all align without intercalation.

### D.7 Da'ath as Galactic Vector (March 2026)

The traditional Qabalistic literature does not adequately explain why
Da'ath is excluded from the Sephirotic count. The resolution is
geometric: Da'ath is not a sphere but a **vector** — the galactic
radial axis through Sol, between Ross 154 (toward the Galactic Center)
and Sirius (toward the galactic anticenter). You cannot count a vector
among spheres any more than you can count a road among cities.

This resolved the "not-Sephirah" problem for the Sephirotic Week and
clarified the three geometric types of exclusion (plane, vector, point)
that keep Malkuth, Da'ath, and the Central Fire out of the day count.

### D.8 The Traditional Grounding of the Sephirotic Week (March 2026)

The Sefirat HaOmer (Counting of the Omer) provides Kabbalistic precedent
for naming calendar days by Sephiroth. The original Babylonian shabattu
was a lunar quarter observation. Zerubavel's counterfactual (9 planets =
9 days if telescopes existed) tightens the count. The Navagraha system
(India) shows that other traditions had 9 celestial bodies but chose not
to extend the week — the extra bodies (Rahu, Ketu) are invisible, just
as Uranus and Neptune are invisible to the naked eye.

These discoveries upgraded the epistemic status of the Sephirotic Week:
the PRINCIPLE of Sephirotic day-naming is [SOURCE: Kabbalistic], not
[ANALYTICAL CONTRIBUTION]. The specific application to variable-length
lunar quarter-weeks and the Supernal extension remain [ANALYTICAL
CONTRIBUTION].

### D.9 The Prime-Law Mapping (February 2026)

The eight primes (89, 19, 31, 67, 29, 11, 23, 17) map uniquely to the
eight Laws through constraint propagation from the Quest-Tarot pairings.
Two single-prime anchor cards (Hierophant → 31 → Divinity; Emperor →
29 → Time Matrix) determine all other assignments. The mapping is
**forced by the mathematics** — no arbitrary choices required.

Three structural bridges connect cyclic and permanent registers:
- Sophie Germain pair: 2(11)+1 = 23. Fall generates Kaos.
- Twin primes (29, 31): Time Matrix twins with Divinity.
- Twin primes (17, 19): Arrow twins with Sole Atom.

Full derivation: `docs/eight-threads-on-the-loom-of-maat.md`.

### D.10 What the Madman in the Cave Actually Needs

This guidebook was written so that a single practitioner — equipped with
pen, paper, an ephemeris (for lunar longitudes and quarter-phase dates),
and a sunrise/sunset table (for their latitude) — can compute every
temporal layer of the Astrolabium by hand. No computer. No software.
No internet. The tables in this document are complete and self-contained.

The computation for any given moment requires approximately:
- 2 minutes for the daily stem-branch (simple modular arithmetic)
- 2 minutes for the hourly branch (division of elapsed time)
- 1 minute for the Five Rat Rule (one lookup, one addition)
- 2 minutes for the LGBF sum and vessel lookup (four lookups, one sum)
- 1 minute for the organ clock (direct from hourly branch)
- 1 minute for the divine hour (simple division)
- 1 minute for the lunar phase (elongation lookup)
- 30 seconds for key detection (compare with sunrise/sunset)
- 30 seconds for unity check (compare two Laws)

**Total: ~14 minutes per moment** (11 minutes for the structural
state + ~3 minutes for resonance detection in Section 13). A skilled
practitioner will get faster with practice. The computation is fully
deterministic — two practitioners working independently at the same
moment and location will produce identical results.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 1, 2026 | Initial guidebook. Corrects Zhèn/Kǎn Law assignments, vessel-trigram mapping, calendar model. Supersedes trigram_law_architecture.md and astrolabium_periodic_table_v2_7.md as the single specification. |
| 1.1 | March 1, 2026 | Sephirotic Week rewritten: fixed planetary cycle (Sol→Neptune) following traditional weekday order with English quality names from traditional planet-Sephira correspondences. |
| **2.0** | **March 1, 2026** | **LOCKED.** Sephirotic Week expanded with traditional grounding (Sefirat HaOmer, Zerubavel), Da'ath-as-galactic-vector, three geometric types of exclusion, seven roads. New Appendix D: Design Notes documenting all key learnings from the derivation sessions. Status changed from DRAFT to LOCKED. |
| 2.1 | March 2, 2026 | Section 13 added: Cross-Dimensional Resonance Detection. Complete lookup tables for all 13 resonance types (9 Boolean + 4 state-value). Tables 13A–I. Worked example continuing Example 1. Total pen-and-paper time now ~14 minutes per query. |
| **2.2** | **March 2, 2026** | **Plum Blossom / Water hinge reframing.** Source attribution corrected: `[SOURCE: Wu Mei]` → `[SOURCE: Plum Blossom Alchemy]` (Timothy's analytical derivation from TCM, not lineage teaching). Section 13.1 hierarchy note: R_WX_03 (Plum Blossom) labeled PRIMARY BRIDGE. R_WX_01/R_WX_02 labeled "canonical." Appendix C.4 rewritten with full Plum Blossom Alchemy provenance. |

---

## What This Document Supersedes

This guidebook is the sole specification for the Astrolabium. The
following documents are superseded:

- `trigram_law_architecture.md` — Replaced by §1–§2
- `astrolabium_periodic_table_v2_7.md` — Replaced by full guidebook
- `astrolabium_periodic_table_v2_6.md` — Already superseded
- All `astrolabium/code/src/*.py` — To be torched and rebuilt from this
  guidebook (Phase 3)
- All `astrolabium/code/tests/*.py` — To be rewritten from §12 worked
  examples (Phase 3)

The following remain valid and are referenced (not replaced):

- `astrolabium/docs/sources/*` — Primary source material (read-only)
- `docs/eight-threads-on-the-loom-of-maat.md` — Upstream derivation
- `docs/Appendix_B_v3.md` — Stream 1 Names of Power (unaffected)
- `astrolabium/docs/specs/astrolabium_data_schemas.md` — Design
  document whose vessel-trigram mapping (§6) is the authority for §3

---

*Compiled and locked March 1, 2026. Every table verified against source
documents. Every correspondence chain documented. Every derivation
recorded. A practitioner with this book, a pen, an ephemeris, and a
sunrise table can compute the alchemical quality of any moment in
history or future. The madman in the cave needs nothing else.*
