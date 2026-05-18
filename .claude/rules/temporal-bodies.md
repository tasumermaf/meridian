# The Five Temporal Bodies

> The architectural structure the Astrolabium reads. Three bodies of
> the practitioner (Soul, Astral, Gross), a permanent-Law layer
> (Solar Keys) that activates only at the two solar cusps, and a
> Stellar Layer (mansions, terms, festivals, Tibetan calendar) that
> situates the moment in the longest cycles. Added May 2026 in
> response to the *Living Time Keepers* and *Saga Dawa* source
> documents.

---

## Why "bodies"

The Damanhurian tradition distinguishes three bodies that operate the
practitioner: a Soul body (slowest, deepest), an Astral body (middle),
and a Gross body (the physical organism, fastest in time-scale).
[SOURCE: Damanhurian]. The Astrolabium reads each body's currently
active state simultaneously and reports them as five parallel layers.

The "fourth body" is not really a body — it is the **Solar Keys**
layer, which represents the two Permanent Laws (Divinity and Fall of
Events) that are not in the cyclic six. The Keys activate only at the
sunrise and sunset cusps, briefly each day. Treating them as their own
layer lets the engine detect when their activation amplifies whatever
the other three layers are doing.

The **fifth body** is the **Stellar Layer**, added in May 2026. It
situates the moment within architectures slower and deeper than the
lunar month: the position of the Sun, Moon, and visible planets in the
28 Chinese Lunar Mansions; the current and upcoming Chinese 24 Solar
Term; the cross-tradition sacred festival calendar; and the Tibetan
lunar month (Phugpa). See `.claude/rules/stellar-layer.md` for the
architectural overview.

## The Layer Table

| Body         | Layer            | Rhythm           | Period          | Source for state                                       |
|--------------|------------------|------------------|-----------------|--------------------------------------------------------|
| **Stellar**  | Mansions / Terms / Festivals / Tibetan Month | Stellar + Solar + Lunisolar | ~13 days (term, mansion of sun) / 1-30 days (festival proximity) / ~30 days (Tibetan month) | Sun/Moon/planet ecliptic longitudes; festival anchor resolution |
| **Soul**     | Primeval Law     | Lunar            | ~4.9 days/phase | Moon phase index → trigram → Law (6 cyclic)            |
| **Solar Keys** | Permanent Laws  | Solar cusps      | Daily, brief    | Sunrise → Gold Key / Sunset → Silver Key (with cusping window) |
| **Astral**   | Derivative Law   | LGBF             | ~2 hours/vessel | Stem-branch substitution + solar branch → vessel → Law |
| **Gross**    | Organ Clock      | Solar            | ~2 hours/organ  | Solar position → Earthly Branch → organ                |

### Soul Layer — Primeval Law

The moon's phase determines which of the **six cyclic Primeval Laws** is
currently active. The lunar month is divided into six ~4.9-day phases,
each carried by a different trigram:

| Phase                             | Trigram   | Law                  |
|-----------------------------------|-----------|----------------------|
| New Moon (0° elongation)          | Kūn ☷    | **Kaos**             |
| Waxing Crescent                   | Zhèn ☳   | **Arrow of Complexity** |
| First Quarter / Waxing Gibbous    | Duì ☱    | **Time Matrix**      |
| Full Moon (180° elongation)       | Qián ☰   | **Synchronicity**    |
| Waning Gibbous                    | Xùn ☴    | **Geometric Essence** |
| Last Quarter / Waning Crescent    | Gèn ☶    | **Sole Atom**        |

The mapping comes from the *Cantong qi* (參同契), the foundational
Daoist alchemical text. The six trigrams here are exactly the ones that
do **not** include Water; the two excluded trigrams (Kǎn ☵ and Lí ☲)
are the Solar Keys. See `.claude/rules/trigram-laws.md` for the full
architecture and `docs/specs/trigram_law_architecture.md` for the spec.

[SOURCE: Damanhurian (the eight Primeval Laws) + Cantong qi (the
trigram assignments) + ANALYTICAL CONTRIBUTION (the 6+2 architecture
mapping the cyclic six to lunar phases and the two Keys to solar
cusps)]

### Solar Keys Layer — Permanent Laws

Two **Permanent Laws** that activate only at the solar cusps:

| Key         | Trigram   | Permanent Law          | Cusp        |
|-------------|-----------|------------------------|-------------|
| **Gold Key**   | Kǎn ☵    | **Fall of Events**     | Sunrise     |
| **Silver Key** | Lí ☲     | **Divinity**           | Sunset      |

A Key is "active" during its **cusping window** — the civil twilight
duration that brackets the exact sunrise or sunset instant at the
practitioner's location. The window varies by latitude and season; at
Damanhur (45°N), it runs roughly 25–35 minutes; near the equator,
shorter; at high latitudes, much longer.

The Permanent Laws are not cyclic. They do not rotate with the moon.
They are always *available* — accessible at any cusp on any day. What
the engine reports is whether right now is a cusping window.

[SOURCE: Damanhurian (the Permanent Laws) + Cantong qi (Kǎn and Lí
as the alchemical operators) + ANALYTICAL CONTRIBUTION (mapping these
two to the daily solar cusps as the "Keys")]

### Astral Layer — Derivative Law via LGBF

The **eight Extraordinary Vessels** rotate through an opening schedule
governed by the **Ling Gui Ba Fa** (靈龜八法, Sacred Turtle Eight
Methods) formula. The schedule depends on both date (the daily
stem-branch from a 60-day sexagenary calendar) and hour (the hourly
branch, which is itself derived from solar position at the
practitioner's location).

Each vessel carries a Derivative Law. The mapping is in
`.claude/rules/ling-gui-ba-fa.md`. The vessel rotates roughly every
two hours (one Earthly Branch worth of time-of-day).

[SOURCE: TCM (LGBF transmission lineage) + ANALYTICAL CONTRIBUTION
(the vessel → Law mapping)]

### Gross Layer — Organ Clock

The classical **Organ Clock** of Traditional Chinese Medicine maps
each of the 12 Earthly Branches to an organ window. The Branch
sequence is determined by solar position — the day is divided into
12 equal arcs from local midnight, and each arc activates a specific
organ.

| Branch | Pinyin | Organ                 | Element  |
|--------|--------|-----------------------|----------|
| 子     | Zǐ     | Gall Bladder          | Wood     |
| 丑     | Chǒu   | Liver                 | Wood     |
| 寅     | Yín    | Lung                  | Metal    |
| 卯     | Mǎo    | Large Intestine       | Metal    |
| 辰     | Chén   | Stomach               | Earth    |
| 巳     | Sì     | Spleen                | Earth    |
| 午     | Wǔ     | Heart                 | Fire     |
| 未     | Wèi    | Small Intestine       | Fire     |
| 申     | Shēn   | Bladder               | Water    |
| 酉     | Yǒu    | Kidney                | Water    |
| 戌     | Xū     | Pericardium           | Fire*    |
| 亥     | Hài    | San Jiao              | Fire*    |

\* Pericardium and San Jiao are the two "ministerial fire" organs in
the Six Qi system, distinguished from the "sovereign fire" of the
Heart. Inner alchemy traditions assign different practices to each.
[SOURCE: TCM — Huáng Dì Nèi Jīng, Mantak Chia Neidan transmission]

## The Unified Substrate

The four layers share a single astronomical foundation:

```
SUNRISE --- MIDDAY --- SUNSET --- MIDNIGHT --- SUNRISE
   |<- First Wing (4 Divine Hours) ->|         |<- Second Wing (4 Divine Hours) ->|
       6 Organ Windows (2 each per hour)           6 Organ Windows
       6 Earthly Branches                          6 Earthly Branches
                ↑ same calculation ↑
```

The Organ Clock branch and the LGBF hourly branch use the **same
function** in the engine: `stem_branch.get_earthly_branch_from_solar(dt,
lat, lon, tz)`. The Divine Hours derive their division from the same
sunrise/sunset boundaries. The Soul layer (lunar) ticks independently
on its longer rhythm but shares the same engine's ephem-driven lunar
phase calculation.

This shared substrate is the analytical contribution that made a single
unified instrument possible. Premodern systems each implemented their
own clock; the Astrolabium recognizes that they were all measuring
slices of the same astronomical fact.

## Compound Detection — the Resonant Moments

The engine evaluates four formal predicates and reports any that hold:

### Two-Body Law Unity

**Definition:** Primeval Law (Soul) == Derivative Law (Astral).

When the lunar phase's Law and the open Extraordinary Vessel's Law
agree, the practitioner has a window where the slow rhythm (months) and
the fast rhythm (hours) are saying the same thing. These windows are
relatively common — several per lunar quarter — and offer a "double
underline" on whatever quality is active.

### Key-Amplified Law Unity

**Definition:** Two-Body Unity holds AND the current moment is within
a Solar Key cusping window.

Rarer. When the sunrise (or sunset) cusp brackets a Two-Body Unity, the
Solar Key's Permanent Law is also active — three layers in agreement,
plus the cosmological gravity of a daily threshold. The Cantong qi
treats sunrise and sunset as the moments when the alchemical fire is
most precisely controllable. Two-Body Unity *during* a Key cusp is the
hour the tradition treats as ritually weightiest.

### Key-Derivative Unity

**Definition:** A Solar Key's Law equals the current Derivative Law,
during cusping.

When the Astral layer agrees with the Permanent Law that the active Key
carries. Often co-occurs with Two-Body Unity but not always — a strict
detection runs them independently.

### Anatomical Intersection

**Definition:** The currently open Extraordinary Vessel's confluent or
coupled point lies on the currently active organ-clock meridian.

A bridge from the Astral layer to the Gross layer through the
practitioner's body. When the open vessel has its access point on
the open meridian, the practitioner is at an unusually clean route
from the vessel's qi state to the meridian's organ window. This is the
**Plum Blossom Alchemy** bridge — see
`.claude/rules/plum-blossom-alchemy.md` for the full derivation.

## What this gives the practitioner

A reading at any moment, for any location, returns:

- The active Primeval Law (Soul)
- Whether a Solar Key is currently cusping (Keys)
- The open Extraordinary Vessel and its Derivative Law (Astral)
- The active organ window and its element (Gross)
- The Divine Hour number (1–8) and wing (day or night)
- The current Divine Month, the Sephirotic Week day, the Great Rite
  proximity
- Any compounds the engine detected — Unity, Key-Amplified, Key-Derivative,
  Anatomical Intersection — with the specific layers involved

The practitioner reads the whole layered state and decides what, if
anything, to do with it. The Astrolabium does not advise. It displays.
