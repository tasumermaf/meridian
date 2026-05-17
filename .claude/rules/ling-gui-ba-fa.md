# Ling Gui Ba Fa (靈龜八法)

> The Sacred Turtle Eight Methods. Chinese chronoacupuncture for
> determining which Extraordinary Vessel is currently open. The Astral
> body's clock.

---

## Name

**靈龜八法** — *Líng Guī Bā Fǎ* — "Sacred Turtle Eight Methods" or
"Spirit Turtle Eight Methods." The "turtle" is the Lo Shu turtle, the
mythical creature that bore the magic square of order 3 on its shell —
the numerological pattern that organizes the timing.

[SOURCE: TCM — classical chronoacupuncture lineage. Transmission via
the *Zhēn Jiǔ Dà Chéng* (Great Compendium of Acupuncture and
Moxibustion, 1601, Yáng Jìzhōu) and later refinements through the
twentieth century.]

## The Eight Extraordinary Vessels

LGBF rotates through the eight **Extraordinary Vessels** (*qí jīng bā
mài*, 奇經八脈) — the eight "extraordinary" or "ancestral" channels of
TCM that operate outside the regular twelve-meridian organ system.
Each vessel has a designated **confluent point** (the master point
that opens it) and a **coupled point** (the paired point that augments
it).

| # | Vessel (Chinese)             | Pinyin         | English                | Confluent | Coupled  |
|---|------------------------------|----------------|------------------------|-----------|----------|
| 1 | 衝脈                         | Chōng Mài      | Penetrating Vessel     | SP-4      | PC-6     |
| 2 | 任脈                         | Rèn Mài        | Conception Vessel      | LU-7      | KI-6     |
| 3 | 督脈                         | Dū Mài         | Governing Vessel       | SI-3      | BL-62    |
| 4 | 帶脈                         | Dài Mài        | Belt Vessel            | GB-41     | TE-5     |
| 5 | 陽蹻脈                       | Yáng Qiāo Mài  | Yang Heel Vessel       | BL-62     | SI-3     |
| 6 | 陰蹻脈                       | Yīn Qiāo Mài   | Yin Heel Vessel        | KI-6      | LU-7     |
| 7 | 陽維脈                       | Yáng Wéi Mài   | Yang Linking Vessel    | TE-5      | GB-41    |
| 8 | 陰維脈                       | Yīn Wéi Mài    | Yin Linking Vessel     | PC-6      | SP-4     |

The vessels pair: 1↔8, 2↔6, 3↔5, 4↔7 (confluent ↔ coupled symmetry).
This pairing is what enables **Anatomical Intersection** detection
(see `.claude/rules/temporal-bodies.md`).

Source database: `docs/sources/Complete_Database__8_EV.md`.

## The Vessel → Derivative Law mapping

Each vessel carries one **Derivative Law** — the Astral-layer reading
the LGBF formula produces. The eight Derivative Laws differ from the
six cyclic Primeval Laws + two Permanent Laws of the Soul/Keys
architecture. They are a parallel eight-fold system specific to the
Astral body.

[Mapping in `astrolabium/data/registers.json` — `lgbf_vessels` register.]

| Vessel              | Derivative Law             |
|---------------------|----------------------------|
| Chōng Mài (1)       | Geometric Essence          |
| Rèn Mài (2)         | Sole Atom                  |
| Dū Mài (3)          | Synchronicity              |
| Dài Mài (4)         | Time Matrix                |
| Yáng Qiāo Mài (5)   | Fall of Events             |
| Yīn Qiāo Mài (6)    | Divinity                   |
| Yáng Wéi Mài (7)    | Arrow of Complexity        |
| Yīn Wéi Mài (8)     | Kaos                       |

The eight Laws are the same eight that appear in the prime-law
correspondence (see palette derivation). The mapping itself is
[ANALYTICAL CONTRIBUTION] — Damanhurian sources do not directly assign
Laws to TCM vessels; the assignment was synthesized from the
qualitative character of each vessel (e.g., the Dū Mài's role as
governor of all yang channels maps to Synchronicity's selective
coherence function) and is documented in
`docs/specs/operators_manual.md`.

## The Formula

The active vessel is determined by a substitution-arithmetic formula
that combines:

1. The **day's Heavenly Stem** (1 of 10)
2. The **day's Earthly Branch** (1 of 12)
3. The **hour's Heavenly Stem** (derived from day stem + hour branch)
4. The **hour's Earthly Branch** (from solar position — `(lat, lon, tz)`-dependent)

Each of the four has a numerical substitution value. The four values
are summed, and the sum is taken modulo 9 (yang days) or modulo 6 (yin
days).

```
Sum = Day_Stem_Sub + Day_Branch_Sub + Hour_Stem_Sub + Hour_Branch_Sub

Yang days (even stem index: Jiǎ=0, Bǐng=2, Wù=4, Gēng=6, Rén=8):
    Remainder = Sum mod 9

Yin days (odd stem index: Yǐ=1, Dīng=3, Jǐ=5, Xīn=7, Guǐ=9):
    Remainder = Sum mod 6

Remainder 0 = use the divisor value (9 or 6)
Remainder maps to one of the 8 vessels via lookup table.
```

The substitution tables are in `astrolabium/src/engine/stem_branch.py`
and documented in `docs/specs/guidebook.md` (Part 2 of Book II) for
manual computation.

## Stem-Branch Reference

The 60-day **sexagenary cycle** combines 10 Heavenly Stems with 12
Earthly Branches in a 60-day rotation. The Astrolabium uses this
fixed reference point:

- **Reference date:** January 1, 2000 = **Wù Wǔ** (Heavenly Stem 5, Earthly Branch 7)

From that anchor, any date can be computed by counting days forward
or backward modulo 60. The day calculation is location-independent —
the same calendar day has the same stem-branch everywhere on Earth.

**The hourly branch IS location-dependent.** The hourly branch is
the Earthly Branch corresponding to the time-of-day band determined by
solar position. Sunrise and sunset bracket the day wing; the day wing
is divided into six branches (寅 Yín, 卯 Mǎo, 辰 Chén, 巳 Sì, 午 Wǔ,
未 Wèi); the night wing into the other six (申 Shēn, 酉 Yǒu, 戌 Xū,
亥 Hài, 子 Zǐ, 丑 Chǒu).

The **Five Rat Rule** (五鼠遁) determines the hourly stem from the
daily stem. The Rat (子 Zǐ) is the first branch and the first hour of
the day in the classical scheme; the rule names which Heavenly Stem
the Rat hour carries on each of the five day-stem classes.

## What "open" means

When LGBF says a vessel is "open," it means: this is the window during
which **acupuncture, breathwork, meditation, or qi-cultivation
targeting this vessel will have the strongest effect**. Classical
practice schedules treatments around vessel openings. In the
Astrolabium, the open vessel is simply read and reported — what the
practitioner does with the reading is theirs.

The vessel rotates approximately every **two hours** (one Earthly
Branch's worth of time-of-day), though the exact rotation time is
fractional and depends on the day's stem-branch arithmetic.

## The Plum Blossom Bridge

The eight vessels each have a **confluent point** that sits on one of
the twelve regular meridians (Lung, Large Intestine, Stomach, etc.).
The confluent point's host meridian carries a Wu Xing element
(Wood/Fire/Earth/Metal/Water). This is the path by which an Astral
body event (open vessel) translates into a Gross body location
(meridian, organ, element).

When the active **organ window** (Gross) is the host meridian of the
**open vessel's** (Astral) confluent point — Anatomical Intersection
holds. This is the **Plum Blossom Alchemy** bridge documented in
`.claude/rules/plum-blossom-alchemy.md`.

## What never to do

- Never compute LGBF without location. The hour-branch term in the
  formula depends on solar position.
- Never substitute mod 8 for the mod 9 / mod 6 rule. The yang/yin
  distinction is not optional.
- Never report the vessel by Western anatomy alone. The vessel is
  Chinese-named for a reason; the Chinese name encodes the function
  (e.g., Dài Mài, the Belt Vessel, encircles the waist and binds the
  twelve regular channels; this matters when the practitioner is
  reading the reading).

## Cross-references

- `.claude/rules/temporal-bodies.md` — vessel as the Astral layer
- `.claude/rules/plum-blossom-alchemy.md` — the EV → meridian → element
  bridge
- `.claude/rules/trigram-laws.md` — how the eight Derivative Laws
  relate to the 6+2 Soul/Keys architecture
- `docs/sources/Complete_Database__8_EV.md` — full vessel reference
- `docs/sources/Comprehensive_Timing_v2_2.md` — timing protocol detail
- `docs/specs/guidebook.md` — manual computation tables and examples
