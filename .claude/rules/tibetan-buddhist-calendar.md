# The Tibetan Buddhist Calendar

> Twelve lunisolar months by Phugpa reckoning, anchored by Losar at the
> first New Moon after Feb 10. The fourth month is **Saga Dawa**, the
> Buddha-month, in which Vesak falls and from which the dragon-root
> regeneration thesis is read.

---

## What this layer is

The Tibetan Buddhist calendar is a **lunisolar** system: months begin at
the astronomical New Moon, and the year drifts against the Gregorian
calendar from one cycle to the next. The Astrolabium uses **Phugpa
reckoning** — the calendar system developed at Phugpa Monastery in the
15th century and now the most widely used Tibetan monastic calendar.

The layer is implemented in
`astrolabium/src/engine/festivals.py`. The two entry points are:

- `get_tibetan_month(dt)` — returns the Tibetan lunar month containing
  the given datetime, with month number, transliteration, Tibetan-script
  name, English gloss, start/end New Moons, and the convenience flag
  `is_saga_dawa`.
- `TIBETAN_MONTH_NAMES` — the twelve-name table, in order.

Festivals with Tibetan-calendar anchors (Saga Dawa, Losar, Chotrul
Duchen, Vesak) flow through the same `festivals.py` resolver as
solar-date and Chinese-lunar festivals; the dispatcher selects the
right anchor type from `data/sacred_festivals.json`.

[SOURCE: Tibetan Buddhist tradition (Phugpa monastic calendar). The
month names, Saga Dawa identification, and Vesak placement are
canonical. ANALYTICAL CONTRIBUTION: the dragon-root regeneration
framing of Saga Dawa, sourced from the Mama Food Forest text
*Awakening the Root of the Dragon* (May 17, 2026), is the specific
interpretive lens this rules file surfaces.]

## The Tibetan Year — Phugpa reckoning

The Tibetan year begins at **Losar** — the first day of the first
Tibetan lunar month. By Phugpa convention this is the **first New
Moon on or after Feb 10** of the Gregorian year. Losar therefore
typically falls between **mid-February and early March**.

```
Year start:    Losar — first New Moon after Feb 10 (Phugpa)
Month:         New Moon to New Moon (29 or 30 days per lunation)
Intercalary:   Inserted when the lunar count requires it; supported
               in the engine via the 13-slot walk in get_tibetan_month
Display drift: Skipped/doubled days exist in Phugpa display
               convention; the engine does not surface these
```

The engine determines which lunation a given moment falls in by walking
New Moons forward from Losar. This means that if you ask about a moment
in **January**, the engine correctly reports the Tibetan calendar of the
*previous* Gregorian year — Losar has not yet occurred for the current
Gregorian year.

## The Twelve Tibetan Months

The table below gives the transliteration the engine returns, the
Tibetan-script form, and the traditional **Sanskrit asterism name**
that classical Tibetan astronomy attaches to each lunar month (these
asterisms are the same nakṣatra-equivalents inherited from the Indian
Kālacakra tradition).

| #  | Transliteration       | Tibetan         | Asterism / Note          |
|----|-----------------------|-----------------|--------------------------|
| 1  | **Dawa Dangpo**       | ཟླ་བ་དང་པོ་       | Mchu — Losar / Chotrul Duchen |
| 2  | **Dawa Nyipa**        | ཟླ་བ་གཉིས་པ་       | Dbo                      |
| 3  | **Dawa Sumpa**        | ཟླ་བ་གསུམ་པ་       | Nag-pa                   |
| 4  | **Dawa Zhipa**        | ཟླ་བ་བཞི་པ་        | **Saga Dawa** — Vesak    |
| 5  | **Dawa Ngapa**        | ཟླ་བ་ལྔ་པ་         | Snron                    |
| 6  | **Dawa Drukpa**       | ཟླ་བ་དྲུག་པ་        | Chu-stod                 |
| 7  | **Dawa Dunpa**        | ཟླ་བ་བདུན་པ་       | Gro-bzhin                |
| 8  | **Dawa Gyepa**        | ཟླ་བ་བརྒྱད་པ་      | Khrums                   |
| 9  | **Dawa Gupa**         | ཟླ་བ་དགུ་པ་        | Tha-skar                 |
| 10 | **Dawa Chupa**        | ཟླ་བ་བཅུ་པ་        | Smin-drug                |
| 11 | **Dawa Chu Chigpa**   | ཟླ་བ་བཅུ་གཅིག་པ་   | Mgo                      |
| 12 | **Dawa Chu Nyipa**    | ཟླ་བ་བཅུ་གཉིས་པ་   | Rgyal                    |

*Dawa* (ཟླ་བ་) means "moon" and "month." *Dangpo, nyipa, sumpa,
zhipa* are the ordinals (first, second, third, fourth). Saga Dawa is
the proper name for the fourth month, derived from the lunar mansion
in which the month's full moon falls.

## Losar — Tibetan New Year (Month 1, Day 1)

Losar (ལོ་གསར་, *lo gsar*, "new year") is the first day of Dawa
Dangpo. By Phugpa convention, the engine resolves Losar as the **first
New Moon on or after Feb 10** of the relevant Gregorian year.

| Gregorian year | Losar (approx, UTC) | Tibetan year designation |
|----------------|---------------------|--------------------------|
| 2025           | Feb 28              | Wood-Snake               |
| 2026           | Feb 17              | Fire-Horse               |
| 2027           | Feb 7 (precedes Feb 10 anchor → falls back) | — |

Note: when Losar falls *before* Feb 10 in a given Gregorian year (rare,
roughly once per Metonic cycle), the simple "first NM after Feb 10"
anchor over-shoots by one lunation. This is a known limitation of the
current Phugpa approximation. For most years the anchor is correct;
edge years should be cross-checked against a published Tibetan
calendar before any operative use.

## Saga Dawa — the Buddha-month (Month 4)

The single most important month of the Tibetan calendar. **Saga Dawa**
(ས་ག་ཟླ་བ་) means *"the month when the Saga star appears"* — Saga
being the Tibetan name for the lunar asterism that the Indian
tradition calls **Viśākhā** (Skt. विशाखा) and that Chinese astronomy
calls **Dī** (氐, mansion 2 in the 28-mansion / 二十八宿 system). All
three traditions identify the same star group; all three call it
some variant of "the Root."

Saga Dawa is **the Buddha-month** because the Mahāyāna and
Theravāda traditions converge on the claim that **Śākyamuni's birth,
enlightenment, and parinirvāṇa all occurred on the full moon of the
Vaiśākha lunar month** — and the Vaiśākha full moon is **Vesak**, the
high day of Saga Dawa.

```
Saga Dawa 2026:  May 17 – June 14   (Tibetan Month 4, Phugpa)
Vesak 2026:      May 31 (full moon inside Saga Dawa)
```

The engine flags any moment falling in Tibetan Month 4 with
`is_saga_dawa: True` so downstream readers can surface
Saga-Dawa-specific framing.

### The Root Mansion connection — the stellar bridge

The asterism name is what gives Saga Dawa its identity. The Indian
**Viśākhā** is one of the 27 nakṣatras; the Chinese **氐 Dī** is the
second of the 28 mansions (二十八宿). Both name the same group of
stars in Libra (α, β, γ, ι Librae in modern catalogue terms). Both
traditions translate the name with the same root sense: **"root,"
"base," "the place where things begin."**

This is the practical cross-reference into the Astrolabium's
**Stellar Layer** (the Chinese 28-mansion architecture). When the
engine reports `is_saga_dawa: True`, it is also reporting that the
current Tibetan month is the month-of-the-Root-Mansion — the same
celestial coordinate the Chinese system flags as 氐 Dī. The Tibetan
calendar layer and the Stellar Layer agree on this identification by
construction; the agreement is the architecture, not a coincidence.

[SOURCE: Tibetan + Indian + Chinese astronomical tradition; the
Sanskrit/Tibetan/Chinese identification of the asterism is canonical
and documented in the Mama Food Forest text *Awakening the Root of
the Dragon* (May 17, 2026).]

### The dragon-root regeneration thesis

The Mama Food Forest text reframes Saga Dawa beyond the standard
Buddha-month framing. The proposal: **true regeneration is not only
ecological — it is the reawakening of the dragon root.** Humanity's
reconnection to land, body, breath, awareness. When the dragon root
awakens:

- **Mountains hold spirit.** They are not inert geology.
- **Waters carry energy.** They are not transport medium.
- **Soil is alive.** It is not substrate.
- **Plants hold awareness.** They are not biomass.

This is the [ANALYTICAL CONTRIBUTION] framing the Astrolabium
surfaces when reporting Saga Dawa. The dragon-root reading does not
displace the canonical Buddha-month reading; it sits beside it,
naming the same merit-generative quality of the month in
ecological-cybernetic terms that connect to Stream 4 (TASUMER MAF).

[SOURCE: Mama Food Forest — *Awakening the Root of the Dragon*,
May 17, 2026, Chinese + English text. ANALYTICAL CONTRIBUTION: the
cross-reference between this regeneration framing and Stream 4's
cybernetic regeneration work.]

### Traditional practices during Saga Dawa

The classical observances during Saga Dawa, in particular around
Vesak:

- **Circumambulation** (*kora*) of sacred mountains, monasteries,
  and stūpas — most famously Mount Kailash, where the Saga Dawa
  Festival itself draws pilgrims to the south face for the
  flag-raising at Tarboche.
- **Lamp offerings** in monasteries and home shrines.
- **Vow observance** — practitioners commonly take the
  one-day eight precepts (*nyung-nä*) on the Vesak full moon.
- **Liberating life** (*tshe thar*) — the freeing of animals
  destined for slaughter.
- **Meditation, recitation, and study** — the entire month is
  treated as a heightened-merit window for any contemplative or
  generosity practice.
- **Tree planting and earth-tending** — the Saga Dawa regeneration
  lineage emphasized in the Mama Food Forest text.

### The merit multiplier

Traditional Tibetan teaching holds that **virtuous actions performed
during Saga Dawa generate merit at a 100,000× multiplier**, with the
full-moon day (Vesak) carrying the peak. The multiplier appears in
classical texts and is universally cited in contemporary Tibetan
teaching cycles.

**Mark this honestly.** [SOURCE: Tibetan Buddhist tradition.] It is
NOT a [VERIFIED] number in the engineering sense — there is no
metrological procedure that would test it. The Astrolabium surfaces
the multiplier as a tradition belief that informs the *quality* with
which a practitioner approaches the month; it does not report it as
a falsifiable claim.

## Other Tibetan Holy Days

The festival registry currently tracks the following Tibetan-anchored
festivals (in addition to Saga Dawa as the whole-month observance):

| Festival           | Anchor                                        | Month |
|--------------------|-----------------------------------------------|-------|
| **Losar**          | First day of Dawa Dangpo                      | 1     |
| **Chotrul Duchen** | Full moon of Dawa Dangpo (Day of Miracles)    | 1     |
| **Vesak**          | Full moon of Dawa Zhipa (inside Saga Dawa)    | 4     |
| **Saga Dawa**      | Entire month range (Dawa Zhipa, NM-to-NM)     | 4     |

**Chotrul Duchen** (མཆོད་འཕྲུལ་དུས་ཆེན་, *mchod 'phrul dus chen*,
"Great Day of Miracles") commemorates the fifteen days during which
the Buddha is said to have performed miracles to confound six rival
teachers. The full moon of the first Tibetan month — typically late
February or early March.

**Vesak** is the single full-moon day of Saga Dawa. Vesak and Saga
Dawa are not the same thing. **Saga Dawa is the month; Vesak is the
day.** The engine resolves them separately and a practitioner asking
about either gets a distinct answer.

Future expansion: the festival registry can be extended to cover the
**four great deeds days** (Chotrul Duchen, Saga Dawa Vesak, Chokhor
Duchen / First Turning of the Wheel, and Lhabab Duchen / Descent from
Tushita) and the **dakini days / protector days** keyed to lunar tithis
within each month. The architecture supports it; the data file does
not yet enumerate them.

## Phugpa vs other variants

Three significant Tibetan calendar variants exist. They differ on
**day skips and day doublings** (which calendar dates appear or
disappear from a printed calendar) but **agree on which lunar month
a given moment falls in.** This is why the Astrolabium uses Phugpa
by default and notes the variants in this rules file only — the
month-level answer is variant-invariant for our purposes.

| Variant      | Used by                                      | Difference from Phugpa |
|--------------|----------------------------------------------|------------------------|
| **Phugpa**   | Gelug, most Kagyu, most Nyingma              | (default / baseline)   |
| **Tsurpu**   | Karma Kagyu                                  | Different tithi-to-date mapping for some days |
| **Bhutanese** | Bhutan state, some Drukpa Kagyu lineages    | Distinct Losar in some years |

If a practitioner specifies they're following Tsurpu or the Bhutanese
calendar, acknowledge the variant and explain that the Astrolabium's
month-level reading agrees with their calendar even when daily display
dates differ. If a practitioner asks for tithi-precise day arithmetic
within a Tibetan month, flag that this is outside the current engine's
scope — they should consult a published calendar from their lineage.

## Operational use in the Astrolabium

When the engine reports the current Tibetan month, the state object
includes the month number, the transliteration, the Tibetan script,
the English gloss, the New Moon boundaries, and the `is_saga_dawa`
flag. A user looking at their state for May 18, 2026 will see:

```
Tibetan month: 4 — Dawa Zhipa (Saga Dawa)
               Tibetan script: ཟླ་བ་བཞི་པ་
               Month window: May 17 – June 14, 2026 (UTC)
               Saga Dawa: True
               Vesak (full moon): May 31, 2026
```

The Saga-Dawa-active state is meant to inform downstream readings the
same way the Damanhurian Tier 0 month character does: it dresses every
other layer the practitioner reads. An organ-clock reading during
Saga Dawa carries the Saga-Dawa quality of root-awakening; a
twilight-window reading on Vesak carries the Vesak quality of
Buddha-day intensification.

The instrument does not tell the practitioner what to feel. It tells
them which quality is dressing the moment, so the practitioner can
recognize what kind of moment this is.

## Common errors

- **Confusing Saga Dawa (the month) with Vesak (the day).** Saga Dawa
  is the entire fourth Tibetan lunar month (≈29-30 days). Vesak is the
  single full-moon day inside it. The engine returns them as separate
  festival entries.
- **Treating the 100,000× merit multiplier as [VERIFIED].** It is
  [SOURCE: Tibetan tradition], a belief that informs practice. Do not
  promote it to a falsifiable claim.
- **Reporting a fixed Gregorian date range for Saga Dawa across years.**
  The calendar is lunisolar; Saga Dawa drifts. 2026: May 17 – June 14.
  2027 will be different. Always compute, never hard-code.
- **Asking about a January date and getting confused by which Tibetan
  year applies.** January moments fall before that Gregorian year's
  Losar, so the engine correctly reports them as belonging to the
  *previous* Tibetan year. This is the intended behavior.
- **Conflating Saga Dawa's Root Mansion with the Western mansion of
  the same number.** The 28 Chinese mansions and the 27/28 Indian
  nakṣatras are not numbered the same way and do not align with
  Western zodiacal divisions. The Root identification (Viśākhā / 氐 Dī)
  is what's stable; the mansion *number* is a system-internal label.
- **Reporting Phugpa-display day dates (with skips and doublings)
  using only the engine's lunation-walk logic.** The engine resolves
  *which lunar month* a moment is in, not the exact tithi-date that a
  Phugpa printed calendar would show. For day-precise tithi work,
  consult a published lineage calendar.

## Cross-references

- `.claude/rules/divine-calendar.md` — the Damanhurian calendar layer,
  which the Tibetan calendar sits beside (not above or below)
- `.claude/rules/names-of-power.md` — Tier 0 character of the
  Damanhurian months, for comparison with the Tibetan month
  characterizations
- `.claude/rules/stellar-layer.md` (if present) — the Chinese
  28-mansion architecture, of which 氐 Dī is mansion 2 and the
  cross-tradition Root identification with Saga Dawa
- `astrolabium/src/engine/festivals.py` — `get_tibetan_month`,
  `TIBETAN_MONTH_NAMES`, and the festival resolver
- `astrolabium/data/sacred_festivals.json` — festival entries for
  Losar, Chotrul Duchen, Vesak, Saga Dawa
- Mama Food Forest, *Awakening the Root of the Dragon*, May 17, 2026
  — the source for the dragon-root regeneration framing
