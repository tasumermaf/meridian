# The Vedic Yuga / Kalpa Layer

> Nested cosmological cycles inherited from Sanskrit tradition. From the
> 432,000-year Kali Yuga up through Mahā Yuga, Manvantara, and the
> 4.32-billion-year Kalpa — the "Day of Brahmā." The deep-time frame the
> Astrolabium reports beneath every other layer.

---

## What this layer is

The Sanskrit cosmological system situates ordinary historical time inside
a hierarchy of nested cycles of immense duration. The Astrolabium's
shorter layers — day, lunar month, solar year, sexagenary cycle, even
the 25,772-year precessional Great Year — are all instants when read
against the yuga frame. This layer's purpose is **cosmological humility**:
it is the longest-period component of the instrument and it reports the
moment as a position within scales that exceed any human reference.

The layer is implemented in `astrolabium/src/engine/vedic_yuga.py`. The
math is deterministic — no ephemeris, no astronomical computation, no
dependency on time of year. Just the canonical Sanskrit year counts and
a single anchor date (the traditional start of the current Kali Yuga).
That makes the layer trivially fast and trivially reproducible: the same
dt produces the same yuga position to floating-point precision every
time.

Entry points:

- `get_vedic_time(dt)` — composite state: current yuga, years into Mahā
  Yuga, Manvantara / Kalpa position, the canonical constants.
- `current_yuga(dt)` — which yuga we are in, fraction through, years
  remaining.
- `years_into_kali_yuga(dt)` — years since Feb 18, 3102 BCE.
- `years_into_maha_yuga(dt)` — position inside the current 4.32-million-year cycle.
- `years_into_kalpa(dt)` — position inside the current 4.32-billion-year Day of Brahmā.

[SOURCE: Sanskrit cosmology — Sūrya Siddhānta (4th–5th century CE),
Bhāgavata Purāṇa, Viṣṇu Purāṇa, and the Manusmṛti tradition. The year
counts and ratios are canonical and reproduced consistently across the
classical sources.]

---

## The nested hierarchy

Read top-down (immediate to cosmic) and the scales escalate by orders of
magnitude. The Astrolabium reports the layers the practitioner can
plausibly inhabit and frames the rest as context.

```
day                         ~24 hours
lunar month                 ~29.5 days
solar year                  ~365.24 days
60-yr sexagenary cycle      60 years          (Chinese; see stem-branch)
Great Year (precession)     ~25,772 years     (see stellar-layer.md)
Kali Yuga                   432,000 years     ← THIS LAYER STARTS HERE
Mahā Yuga                   4,320,000 years   (10 × Kali)
Manvantara                  ≈ 308,448,000 yr  (71 Mahā Yuga + 1 sandhya)
Kalpa = Day of Brahmā       ≈ 4.32 billion yr (14 Manvantara + 1 sandhya)
Year of Brahmā              ≈ 3.1 trillion yr (360 days + 360 nights of Brahmā)
Life of Brahmā              ≈ 311 trillion yr (100 years of Brahmā)
```

The Astrolabium reports the layers from Kali Yuga up through Kalpa
directly. The Year and Life of Brahmā are documented here but are not
returned by the engine — they exist as the outer frame the practitioner
should know is there, but their numerical position is not operationally
useful.

[MATHEMATICAL FACT — every count in the table above is deterministic
from the canonical definitions.]

---

## The four yugas

The Mahā Yuga is composed of four sub-ages whose durations are in the
ratio **4 : 3 : 2 : 1**. The unit is **432,000 years** — the "Kali unit"
— and every other yuga duration is a multiple of it.

| Yuga          | Sanskrit | Years     | × Kali | Ratio | Quality (traditional) |
|---------------|----------|-----------|--------|-------|------------------------|
| **Satya / Kṛta** | सत्य/कृत  | 1,728,000 | 4×     | 4     | Golden age — dharma at 100%   |
| **Treta**        | त्रेता    | 1,296,000 | 3×     | 3     | Silver age — dharma at 75%    |
| **Dvāpara**      | द्वापर   |   864,000 | 2×     | 2     | Bronze age — dharma at 50%    |
| **Kali**         | कलि      |   432,000 | 1×     | 1     | Iron age — dharma at 25%      |
|                  |          | **4,320,000** | **10×** |    | **= 1 Mahā Yuga**             |

The 4:3:2:1 ratio is a structural feature of the system. Each yuga's
duration is the previous one minus 432,000 years. The 432,000 figure
itself is the fundamental atomic unit of Vedic deep-time arithmetic.

[SOURCE: Sūrya Siddhānta, Mahābhārata, Viṣṇu Purāṇa, Bhāgavata Purāṇa.]
[MATHEMATICAL FACT — the 4:3:2:1 ratio and the 432,000 unit are
deterministic from the tradition's definitions.]

---

## Why 4,320,000 — the Sūrya Siddhānta sacred year

The Mahā Yuga total — **4,320,000 years** — is not arbitrary. In the
Sūrya Siddhānta this is the number of revolutions that produce exact
integer counts for the major astronomical periods within a single
"divine year" (*divya-varṣa*) framework. The Sanskrit astronomers built
the yuga numbers to make solar, lunar, planetary, and stellar periods
synchronize exactly at the start and end of each Mahā Yuga, with all
celestial bodies returning to mean longitude zero simultaneously.

The 432,000 unit appears throughout the system. It also appears in
unexpected places in other cultures — the number of years of pre-flood
Babylonian kingship in Berossos' chronicle (432,000 years across ten
kings), the number of stanzas in some recensions of the Ṛgveda
multiplied through by relevant factors, and the count of warriors in
some Norse Valhalla traditions. The pattern of 432,000 as a sacred
"cosmic-year" unit is cross-cultural, though the Astrolabium does not
make claims about how the cross-cultural occurrences are related.

[SOURCE: Sūrya Siddhānta — explicit. The cross-cultural pattern of
432,000 is documented in comparative religion literature; the relation
is an open question and is [ANALYTICAL CONTRIBUTION] when proposed.]

---

## Manvantara — the age of a Manu

A **Manvantara** is the reign of one **Manu** (the cosmic ancestor /
progenitor of humanity for that age). The duration is:

```
1 Manvantara = 71 × Mahā Yuga + 1 sandhya (transitional Satya Yuga)
             = 71 × 4,320,000 + 1,728,000
             = 308,448,000 years
             ≈ 308.6 million years
```

The sandhya (Skt. *sandhi* — "junction") is a transitional twilight
period at each Manvantara's start, of duration equal to one Kṛta /
Satya Yuga. It represents the cosmological re-ordering between the
reign of one Manu and the next.

A Kalpa contains **14 Manvantaras**. Each is presided over by a
different Manu with a distinct cosmological role. The seven Manus that
have already presided in the current Kalpa, in order, are:

| #  | Manu                | Sanskrit         | Status                |
|----|---------------------|------------------|------------------------|
| 1  | Svāyambhuva         | स्वायम्भुव        | past                  |
| 2  | Svārociṣa           | स्वारोचिष        | past                  |
| 3  | Uttama              | उत्तम            | past                  |
| 4  | Tāmasa              | तामस             | past                  |
| 5  | Raivata             | रैवत             | past                  |
| 6  | Cākṣuṣa             | चाक्षुष           | past                  |
| **7**  | **Vaivasvata**      | **वैवस्वत**       | **current — us**      |
| 8  | Sāvarṇi             | सावर्णि           | future                |
| 9  | Dakṣa Sāvarṇi       | दक्ष सावर्णि      | future                |
| 10 | Brahma Sāvarṇi      | ब्रह्म सावर्णि    | future                |
| 11 | Dharma Sāvarṇi      | धर्म सावर्णि      | future                |
| 12 | Rudra Sāvarṇi       | रुद्र सावर्णि     | future                |
| 13 | Deva Sāvarṇi        | देव सावर्णि       | future                |
| 14 | Indra Sāvarṇi       | इन्द्र सावर्णि    | future                |

**Vaivasvata Manu** — "the son of Vivasvat (the Sun)" — is the current
Manu. He is the cosmological figure equivalent to Noah / Ziusudra /
Utnapishtim: the lawgiver who survives the great flood at the end of
the previous Manvantara and re-founds humanity. The Manusmṛti is
attributed to him.

[SOURCE: Bhāgavata Purāṇa (Canto 8), Viṣṇu Purāṇa, Manusmṛti.]

---

## Kalpa — the Day of Brahmā

A **Kalpa** is the longest cycle the Astrolabium reports as a numeric
position. The duration is:

```
1 Kalpa = 14 × Manvantara + 1 initial sandhya
        = 14 × 308,448,000 + 1,728,000
        = 4,320,000,000 years (canonical rounding)
        ≈ 4.32 billion years
```

The Kalpa is also called the **Day of Brahmā** (*Brahma-divasa*) — one
"day" in the cosmological life of the creator-deity. A Brahmā-night of
equal duration follows each Brahmā-day, during which the universe is
dissolved (*pralaya*) and re-manifested.

Each Kalpa carries a traditional name. The current Kalpa is the
**Shvetavārāha Kalpa** (श्वेतवाराह कल्प) — the "White Boar Kalpa,"
named for Viṣṇu's third avatāra (Varāha, the boar) who lifted the
earth out of the cosmic waters at the start of this Day of Brahmā.

[SOURCE: Bhāgavata Purāṇa, Viṣṇu Purāṇa.]

The numerical coincidence with modern cosmology is striking: the age of
the Earth is ≈ 4.54 billion years, which is within an order of magnitude
of one Kalpa. The Sanskrit tradition arrived at the 4.32-billion-year
figure through pure ratio arithmetic from the 432,000 Kali unit, with
no observational geological access. The Astrolabium notes the
coincidence as a [SOURCE: Sanskrit cosmology] number without claiming
any predictive relation to modern geology.

---

## Where we are — May 2026

The classical Vaishnava reckoning places this moment precisely:

```
Kalpa                   Shvetavārāha (White Boar) — current
Manvantara              7 of 14    — Vaivasvata Manu (son of the Sun)
Mahā Yuga               28 of 71   (within the current Manvantara)
Yuga                    Kali Yuga  (last quarter of the current Mahā Yuga)

Kali Yuga elapsed       ≈ 5,127 years  (Feb 18, 3102 BCE → May 18, 2026)
Kali Yuga total         432,000 years
Kali Yuga fraction      ≈ 0.01187   (≈ 1.187% complete)
Kali Yuga remaining     ≈ 426,873 years
```

The instrument's reading for May 18, 2026 reports:

- We are **1.187% of the way through the current Kali Yuga**.
- The current Kali Yuga is **the last quarter** of the current Mahā Yuga.
- The current Mahā Yuga is **the 28th of 71** in the current Manvantara.
- The current Manvantara is **the 7th of 14** in the current Kalpa.
- The current Kalpa is **the Shvetavārāha** (White Boar) Kalpa.
- We are roughly **two billion years into a 4.32-billion-year Day of Brahmā**.

The framing the Astrolabium surfaces: every layer above the Kali Yuga
unit — Mahā Yuga, Manvantara, Kalpa — is a context the practitioner
cannot directly experience. The Kali Yuga itself (432,000 years) is
already 6,000× longer than recorded human history. The instrument
returns these numbers so the practitioner can locate the present moment
inside scales that are not human, and so the question *"what is now?"*
has an honest cosmological answer.

[MATHEMATICAL FACT — every number above is a direct consequence of the
canonical constants and the 3102 BCE anchor. The engine returns them
to floating-point precision.]

---

## The 3102 BCE anchor

The classical anchor for the start of the current Kali Yuga is **midnight
between February 17 and February 18, 3102 BCE (Julian calendar)**. In
astronomical year numbering (where 1 BCE = year 0, so 3102 BCE = year
−3101), this is **year −3101.13** approximately. The engine stores this
as `KALI_YUGA_START_YEAR_ASTRO = -3101.13`.

Two traditions converge on this date:

- **Mahābhārata tradition:** Kali Yuga began with **Kṛṣṇa's departure
  from the world** (his return to Vaikuṇṭha after the Mahābhārata war).
  The traditional date for this is exactly Feb 18, 3102 BCE.
- **Sūrya Siddhānta tradition:** The 4th–5th century CE astronomical
  text states that all the planets and the lunar node Rāhu were in mean
  conjunction at celestial longitude zero at this moment, marking the
  start of the current great age.

Modern back-calculation does not confirm the planetary conjunction (the
real planets were not at longitude zero in Feb 3102 BCE), but the
**date itself is the anchor** the tradition uses, and the Astrolabium
uses it without correction. The 432,000-year arithmetic anchors to it
literally.

[SOURCE: Sūrya Siddhānta and Mahābhārata. The Feb 18 / Feb 17 distinction
varies by which midnight is meant; the engine uses Feb 18 as the
canonical day.]

---

## Variant interpretations — what we do NOT implement

Two prominent modern revisions exist. The Astrolabium uses the
**classical Sūrya Siddhānta reckoning** by default; the variants are
documented here for completeness.

### Sri Yukteswar's "Holy Science" cycle (1894)

Swami Sri Yukteswar Giri, in *The Holy Science*, proposes that the
"yuga cycle" is in fact a **24,000-year cycle** — much shorter than the
classical 4,320,000-year Mahā Yuga — and that the 24,000 years is half
the (then-current) estimate of the precessional Great Year. Within this
much-shorter cycle, the Yukteswar revision claims we are currently
**ascending into Dvāpara Yuga** (since approximately 1699 CE) rather
than deep in Kali Yuga.

The Yukteswar framework is influential in 20th-century yoga lineages
(especially Kriya Yoga via Yogananda) and in the Theosophical-adjacent
"ascension" literature. It is a **19th-century interpretive revision**,
not the classical canon. The Astrolabium does not implement it.

[SOURCE: Sri Yukteswar Giri, *The Holy Science* (Kaivalya Darśanam),
1894. ANALYTICAL CONTRIBUTION — the note that Yukteswar is a 19th-century
revision rather than classical Sūrya Siddhānta canon is the Astrolabium's
own framing. The Yukteswar reading is internally consistent and not
"wrong" inside its own frame; it is simply not the calendar the
Astrolabium uses.]

### Theosophical / New Age adaptations

The 19th-century Theosophical literature (Blavatsky, Leadbeater) and its
20th-century New Age descendants produced a variety of yuga-cycle
schemes — some keyed to the precession of the equinoxes, some to a
12,000-year "great year," some to ages keyed to zodiacal sign-shifts
("Age of Aquarius"). These are syncretic and do not preserve the
classical 4:3:2:1 ratio or the 432,000-year unit. The Astrolabium does
not implement any of these schemes in this layer; the precessional
"Great Year" lives in `stellar-layer.md` as its own separately-named
component, not labeled as a yuga.

[ANALYTICAL CONTRIBUTION — distinguishing the Sanskrit yuga cycles from
the precessional ages is the Astrolabium's choice. They are different
periodicities and should not be conflated.]

---

## Why this layer matters operationally

The Astrolabium's shorter layers (organ clock, divine hour, lunar phase,
lunar mansion, solar term) describe **quality of the moment** at human
scales. The deep-time layer does something different. It does not
prescribe what the practitioner should *do*; it tells them **where they
stand**.

The current historical moment is:

- **1.2% of the way through ONE 432,000-year Kali Yuga.**
- which is itself **the last quarter of a 4.32-million-year Mahā Yuga.**
- which is itself **the 28th of 71 in a 308.6-million-year Manvantara.**
- which is itself **the 7th of 14 in a 4.32-billion-year Day of Brahmā.**

This is the **Deep-Cycle Layer** the Living Time Keepers paper (Xue Mei,
Section VI item #6) called for. The instrument needs a cosmic-timescale
component or it cannot honestly answer the question *"what is now?"* at
the scales that matter to a serious practitioner. The yuga / kalpa layer
provides it.

The framing is cosmological humility. The shorter layers urge the
practitioner toward attention; the yuga layer reminds them that all
attention is local to a moment within scales they cannot inhabit. Both
framings are present in the instrument simultaneously.

---

## Common errors

- **Confusing yuga (cosmic) with the 60-year sexagenary cycle.** Both
  appear in traditional Asian timekeeping. The sexagenary cycle is 60
  years; the Kali Yuga is 432,000. They operate at completely different
  scales and serve different purposes. See `stem-branch` for the
  sexagenary cycle.
- **Treating the Day of Brahmā as a literal 24-hour day.** The "day"
  is metaphorical. Brahmā's day = 4.32 billion years of cosmological
  manifestation, followed by an equal night of cosmological dissolution.
  The unit is "day" because the tradition models cosmological time as
  Brahmā's day-night alternation, not because it shares anything with
  the diurnal cycle.
- **Claiming the Kali Yuga "has been going badly" because of the
  tradition's name for it.** The classical tradition does describe Kali
  Yuga as the age of *dharma's decline* (dharma at 25% versus 100% in
  Satya Yuga, with social, ecological, and spiritual degradation as
  side effects). **These are interpretive claims of the tradition, not
  empirical claims the Astrolabium endorses.** [SOURCE: Sanskrit
  cosmology] for the framing, not [VERIFIED] for any historical claim.
  The instrument reports the position; it does not predict the quality.
- **Conflating the Vedic four-yuga cycle with the Greek / Hesiodic Five
  Ages.** Hesiod's *Works and Days* (~700 BCE) describes a sequence of
  Gold → Silver → Bronze → Heroic → Iron ages. The shape resembles the
  Vedic 4:3:2:1 (decline through metals) but the **numbers, durations,
  and structural role are different**. Hesiod has five ages, no
  numerical durations, and an explicit Heroic-age interpolation that
  breaks the metal-degradation pattern. The Vedic yugas have four ages,
  exact durations, and the 4:3:2:1 ratio. **They are not the same
  system.** Comparative-mythology scholarship treats them as
  independently developed cyclic-age cosmologies that may share an
  Indo-European root, but the Astrolabium does not implement the
  Hesiodic Five Ages and does not equate them.
- **Treating 432,000 as numerologically magic.** The 432,000 number is
  the structural atom of the Sanskrit deep-time system. It also appears
  in Berossos, in some Vedic stanza counts, and in scattered other
  places. The Astrolabium reports the number as **the Kali Yuga
  duration**, not as a mystical key. Cross-cultural occurrences are
  noted but not endorsed as significant beyond the Sanskrit cosmology
  itself.
- **Reporting we are "halfway through Kali Yuga" or "near the end."**
  We are at **1.187% of the way through**. ~426,873 years remain in
  the current Kali Yuga. Any reading that places the current moment
  near a Kali-Yuga boundary contradicts the classical arithmetic.

---

## Cross-references

- `.claude/rules/stellar-layer.md` — the yuga layer is the **longest-period
  component** the stellar layer reports. The precessional Great Year
  (≈25,772 years) is a fine-grained subdivision compared to the Kali
  Yuga (432,000 years), which is itself the smallest yuga unit.
- `.claude/rules/tappetino-proof.md` — the rhombic-dodecahedron
  12-fold architecture and the Sanskrit cosmology share a deep
  preoccupation with **12-fold structural arithmetic**. The Kalpa
  contains 14 Manvantaras (not 12), but the Mahā-Yuga 4:3:2:1 ratio
  decomposes the Mahā Yuga into 10 Kali units, and the broader
  cross-cultural 432,000 pattern is implicated in the 12-fold
  cosmologies the Tappetino Proof analyzes.
- `.claude/rules/how-to-use-this-instrument.md` — guidance on how
  deep-time layers are surfaced alongside the immediate layers in the
  practitioner's reading. The yuga layer is reported as **context**, not
  as **prescription**.
- `astrolabium/src/engine/vedic_yuga.py` — the engine itself, with
  full documentation of the constants and the canonical arithmetic.
- *Sūrya Siddhānta* (4th–5th century CE) — primary classical source
  for the yuga durations and the 3102 BCE Kali Yuga anchor.
- *Bhāgavata Purāṇa*, Canto 8 — primary classical source for the
  Manvantara structure and the seven Manus.
