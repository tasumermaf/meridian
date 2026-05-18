# The Cross-Tradition Sacred Festival Registry

> A registry of 32 festivals from 10+ traditions, resolved at query
> time against the practitioner's Gregorian moment. The Astrolabium's
> way of acknowledging that the lunar calendar it computes is one
> among many — and that any given day on the civil clock is also a
> sacred day in some living lineage.

---

## What the registry is

The Cross-Tradition Sacred Festival Registry overlays Gregorian civil
time with festival anchors from a deliberately broad spectrum of
contemplative traditions: **Tibetan Buddhist, Hindu, Sikh, Jain,
Chinese, Christian (Western), Celtic / Pagan, Islamic, Jewish, Mexican
syncretic, Persian / Zoroastrian / Bahá'í, Theravada Buddhist, and
Damanhurian.** It was added in Sprint A Phase 3 as the calendar layer's
ecumenical complement — the Divine Calendar gives the Damanhurian frame;
the festival registry gives the rest of the world's frames the same
moment is also occurring inside.

The registry is **informational, not prescriptive.** It tells the
practitioner: *today is also the third day of Saga Dawa, or the day
after Beltane, or three weeks before Vesak.* What the practitioner
does with that information is their own concern.

The data lives at `astrolabium/data/sacred_festivals.json` (32
festivals, version 1.0). The engine is at
`astrolabium/src/engine/festivals.py`. The design pattern is consistent
with the rest of the Astrolabium: stored anchors, computed dates,
never stored dates. Festival dates drift; anchor rules do not.

[SOURCE: per-festival source notes; ANALYTICAL CONTRIBUTION for the
multi-tradition registry design and proximity-query semantics.]

## Why a multi-tradition registry

The Astrolabium already tells the practitioner what Damanhurian month
they're in, what Primeval Law is active, what organ has the dispatcher
position. Adding a festival registry from other traditions completes
the temporal picture without colonising it. **Knowing that today is
Yom Kippur changes what the moment is for someone — even if the
practitioner is not Jewish.** Knowing it is Saga Dawa changes the
field a Buddhist practitioner is moving inside. The registry surfaces
that information without claiming the practitioner is obligated by it.

This is also how the instrument honours the principle that no single
tradition owns the calendar. The Damanhurian Great Rites have
parallels and counter-parallels in every contemplative system that
ever paid attention to the sky. The registry makes those parallels
visible.

## The anchor types

Eight anchor types are supported. Each resolves a festival's date for
a given Gregorian year. The engine dispatches on the festival's
`anchor_type` field; the rule and any parameters live in `anchor_data`.

### `solar_date`

Fixed Gregorian month and day. The simplest anchor — the festival
falls on the same civil date every year.

```
solar_date  →  e.g., Divine Marriage = May 24
            →  Day of the Dead = November 2
            →  Beltane = May 1
            →  Imbolc = February 1 (conventional)
            →  Lughnasadh = August 1
            →  Samhain = October 31
```

The Imbolc anchor carries a `rationale` field noting that the
astronomical cross-quarter day actually falls Feb 3–5, but observance
has settled on Feb 1–2. This is an honest disclosure pattern that the
registry uses whenever a tradition's observed date differs from its
astronomical anchor.

### `solar_term`

Anchored to one of the 24 Chinese solar terms (节气 *jiéqì*). The
engine finds the moment in the target year when the Sun's tropical
ecliptic longitude crosses the term's degree (Qīngmíng = 15°, Xiàzhì
= 90°, Qiūfēn = 180°, Dōngzhì = 270°, Chūnfēn = 0°, and so on).

This is the most astronomically precise anchor type the registry
supports. It is shared by:

```
solar_term  →  Qingming (清明 — Tomb-Sweeping, term 4 at 15°)
            →  Dongzhi (冬至 — Winter Solstice, term 21 at 270°)
            →  Nowruz (Persian New Year, anchored to Chūnfēn / 0°)
            →  Damanhurian Autumn Equinox (Qiūfēn / 180°)
            →  Damanhurian Spring Equinox (Chūnfēn / 0°)
            →  Damanhurian Summer Solstice (Xiàzhì / 90°)
            →  Damanhurian Winter Solstice (Dōngzhì / 270°)
```

The four Damanhurian Great Rite solstice/equinox observances and the
Chinese Dongzhi festival share the same solar-term anchor — they are
the same astronomical event observed by different traditions. The
registry surfaces all of them on the same day because they are all
present on the same day.

### `lunar_month_day`

Chinese lunisolar anchor — the Nth day of the Mth lunar month, where
the first lunar month begins at the New Moon nearest Lìchūn
(Beginning of Spring, ~Feb 4).

```
lunar_month_day  →  Qixi (七夕) = lunar 7/7
                 →  Mid-Autumn (中秋节) = lunar 8/15 (full moon)
```

The engine's implementation is a practical approximation: it does not
handle Chinese intercalary months in the strict Phugpa or Time-Granted
sense. For typical festival lookup this is sufficient; for full
luni-solar calendar arithmetic it is not. The simplification is
acknowledged in the code's docstring.

### `tibetan_lunar_month_full`

Tibetan calendar (Phugpa reckoning) — a specific day within a
specified Tibetan lunar month. The `day` field can be `"full_moon"`
or `"first"`.

```
tibetan_lunar_month_full  →  Vesak = Tibetan month 4, day = full_moon
                          →  Losar = Tibetan month 1, day = first
                          →  Chotrul Duchen = Tibetan month 1, day = full_moon
```

Tibetan month 1 (Losar / Tibetan New Year) begins at the first New
Moon after approximately February 10 of the Gregorian year — this is
the Phugpa anchoring rule the engine uses. Tibetan month 4 begins
three lunations later, which places it in May/June and matches
documented Saga Dawa 2026 dates (May 17 – June 14).

### `tibetan_lunar_month_range`

The entire Tibetan lunar month — not a specific day within it, but
the full 29–30 day span. Currently used by **Saga Dawa**, which is
the only registered festival observed as a full month rather than as
a single day.

```
tibetan_lunar_month_range  →  Saga Dawa = entire Tibetan month 4
```

When the engine resolves a `tibetan_lunar_month_range` festival it
returns both `start_datetime` and `end_datetime` covering the full
lunation. The proximity query treats any moment inside that range as
`status: "active"` regardless of the 14-day window.

### `computed`

Rule-based luni-solar anchors that need their own tradition-specific
calendar arithmetic. The engine **currently approximates these via
the stored `gregorian_window` midpoint** — an honest deferral, not a
hidden compromise. The window is what the documented observance
window is for a typical year; the midpoint gives a usable
approximate date that the proximity query will surface during the
correct general period.

Refinement of these anchors to their proper computation is queued for
a follow-up sprint. The approximations affect:

```
computed  →  Easter (Western)  — needs Paschal full moon algorithm
          →  Diwali  — needs Hindu Vedic calendar (Kartika new moon)
          →  Holi  — needs Hindu Vedic calendar (Phalguna full moon)
          →  Navratri  — needs Hindu Vedic calendar (Ashvin Shukla)
          →  Eid al-Fitr  — needs Hijri month tracking (Shawwal)
          →  Eid al-Adha  — needs Hijri month tracking (Dhu al-Hijjah)
          →  Passover  — needs Jewish calendar (15 Nisan)
          →  Yom Kippur  — needs Jewish calendar (10 Tishrei)
          →  Rosh Hashanah  — needs Jewish calendar (1-2 Tishrei)
          →  Chinese New Year (Chunjie)  — partial; uses lichun rule
          →  Magha Puja, Asalha Puja  — need Theravada lunar arithmetic
```

For festivals whose `gregorian_window` is `"varies"` (Eid al-Fitr,
Eid al-Adha because the Islamic lunar calendar drifts ~11 days/year),
the current implementation returns `None` — the festival will not
appear in proximity results until proper Hijri arithmetic is added.
This is the correct behaviour: better to be silent than to surface a
wrong date for a tradition that takes its calendar seriously.

### `fixed_window`

Reserved for festivals where the only available anchor is a known
Gregorian window without finer luni-solar logic. Currently no
registered festival uses this anchor; the engine treats it identically
to `computed` (window-midpoint) as a forward-compatibility path.

## Saga Dawa — the worked example

Saga Dawa illustrates how the registry handles the most demanding
anchor type — a full Tibetan lunar month, with an associated lunar
mansion, with classical merit semantics, with an internal anniversary
(Vesak) that is itself a separately registered festival.

```json
{
  "id": "saga_dawa",
  "name_native": "ས་ག་ཟླ་བ་",
  "name_native_transliteration": "Sa-ga zla-ba",
  "anchor_type": "tibetan_lunar_month_range",
  "anchor_data": {
    "tibetan_month": 4,
    "duration": "full_month"
  },
  "associated_lunar_mansion": 2,
  "duration_days": 30,
  "merit_multiplier_classical": 100000
}
```

**Saga Dawa 2026 = May 17 – June 14.** The engine arrives at this
range by finding the first New Moon after Feb 10, 2026 (= Losar,
the start of Tibetan month 1), then adding three lunations (Tibetan
months 2, 3, 4 begin). The fourth New Moon is Saga Dawa's opening;
the fifth New Moon is its close.

The month commemorates the birth, enlightenment, and parinirvana of
Shakyamuni Buddha. "Saga" refers to the star or mansion under which
the Buddha is said to have been born — Viśākhā in the Indian system,
Lunar Mansion 2 (Root / 氐 *Dǐ*) in the Chinese 28-mansion system.
The full month is sacred; the full moon day within it (Vesak / Buddha
Day) is the most auspicious single point.

**Vesak is a separately registered festival.** During Saga Dawa the
proximity query will surface both — Saga Dawa as a range-active
festival and Vesak as its full-moon centrepiece. They are not
duplicates; they are layered observances, and the registry preserves
both.

[SOURCE: Tibetan Buddhist tradition; documented dates per Mama Food
Forest text, May 2026.]

## The complete festival list

Grouped by tradition for orientation. Each carries a `source_note` in
the JSON; cite that note when discussing the festival in any user-
facing context.

### Damanhurian (6 — the Great Rites)

| Festival                | Anchor          | Falls in Divine Month  |
|-------------------------|------------------|------------------------|
| Autumn Equinox          | solar_term Qiūfēn | 1 ISIS               |
| Day of the Dead         | solar_date 11/2  | 2 SADAM                |
| Winter Solstice         | solar_term Dōngzhì | 4 EOROS              |
| Spring Equinox          | solar_term Chūnfēn | 7 OSIRIS             |
| Divine Marriage         | solar_date 5/24  | 9 SAMMA                |
| Summer Solstice         | solar_term Xiàzhì | 10 SET                |

These mirror the Great Rite definitions in `divine-calendar.md`. They
are listed in the registry as well as in the Divine Calendar because
the registry is the engine's single source of truth for cross-tradition
festival proximity. The Divine Calendar's Great Rites are the **same**
events appearing in the **same instrument** from a different angle.

### Tibetan Buddhist (3)

| Festival          | Anchor                     | Notes                              |
|-------------------|----------------------------|------------------------------------|
| Losar (ལོ་གསར་)   | tibetan_lunar_month_full   | New Year, first day of month 1     |
| Chotrul Duchen    | tibetan_lunar_month_full   | Full moon month 1, merit ×100,000  |
| Saga Dawa         | tibetan_lunar_month_range  | Full month 4, merit ×100,000       |

### Buddhist (Theravada / pan-tradition) (3)

| Festival                       | Anchor                     | Notes                                   |
|--------------------------------|----------------------------|-----------------------------------------|
| Vesak (Vaiśākha Purnima)       | tibetan_lunar_month_full   | Buddha Day; full moon Tibetan month 4   |
| Magha Puja (มาฆบูชา)            | computed (window approx)   | Full moon 3rd lunar month               |
| Asalha Puja (อาสาฬหบูชา)         | computed (window approx)   | Full moon 8th lunar month; Vassa start  |

### Hindu / Sikh / Jain (3)

| Festival              | Anchor                  | Notes                                   |
|-----------------------|-------------------------|-----------------------------------------|
| Diwali (दीपावली)       | computed (window approx) | Festival of Lights; Lakshmi Puja        |
| Holi (होली)            | computed (window approx) | Festival of Colors; Phalguna full moon  |
| Navratri (नवरात्रि)     | computed (window approx) | Nine nights, Divine Mother              |

### Chinese (5)

| Festival                    | Anchor                | Notes                                |
|-----------------------------|------------------------|--------------------------------------|
| Spring Festival (春节)       | computed (lichun anchor) | Chinese New Year, 15 days         |
| Qingming (清明节)            | solar_term Qīngmíng    | Tomb-sweeping; solar term 4         |
| Qixi (七夕)                  | lunar_month_day 7/7    | Weaver Girl & Cowherd               |
| Mid-Autumn (中秋节)          | lunar_month_day 8/15   | Full moon, mooncakes                |
| Dongzhi (冬至)               | solar_term Dōngzhì     | Winter solstice                     |

### Christian (Western) (1)

| Festival              | Anchor                  | Notes                                   |
|-----------------------|--------------------------|----------------------------------------|
| Easter                | computed (window approx) | First Sunday after Paschal full moon   |

### Celtic / Pagan (4 — the cross-quarter days)

| Festival                  | Anchor             | Notes                                  |
|---------------------------|---------------------|----------------------------------------|
| Imbolc (St Brigid's Day)  | solar_date 2/1      | Mid-point Winter Solstice → Equinox    |
| Beltane (Bealtaine)       | solar_date 5/1      | Mid-point Equinox → Summer Solstice    |
| Lughnasadh (Lammas)       | solar_date 8/1      | Mid-point Solstice → Autumn Equinox    |
| Samhain (Halloween)       | solar_date 10/31    | Mid-point Equinox → Winter Solstice    |

### Islamic (2)

| Festival                       | Anchor                   | Notes                                   |
|--------------------------------|--------------------------|-----------------------------------------|
| Eid al-Fitr (عيد الفطر)         | computed (Hijri — deferred) | First day of Shawwal                  |
| Eid al-Adha (عيد الأضحى)        | computed (Hijri — deferred) | 10th of Dhu al-Hijjah                 |

### Jewish (3)

| Festival                  | Anchor                | Notes                            |
|---------------------------|------------------------|----------------------------------|
| Rosh Hashanah (ראש השנה)  | computed (window approx) | First two days of Tishrei      |
| Yom Kippur (יום כיפור)    | computed (window approx) | 10 Tishrei                      |
| Passover (פסח)             | computed (window approx) | 15 Nisan, 7–8 days              |

### Mexican / Catholic / pre-Columbian syncretic (1)

| Festival                       | Anchor          | Notes                                       |
|--------------------------------|------------------|---------------------------------------------|
| Day of the Dead (Día de los Muertos) | solar_date 11/2 | Same civil date as the Damanhurian Rite |

### Persian / Zoroastrian / Bahá'í (1)

| Festival              | Anchor                   | Notes                                  |
|-----------------------|---------------------------|----------------------------------------|
| Nowruz (نوروز)        | solar_term Chūnfēn        | 13 days; spring equinox + 12 days      |

## Status semantics — active, upcoming, past

`get_festival_proximity(dt, window_days=14)` classifies every festival
within range into one of three statuses based on `dt`'s relationship
to the festival's `start_datetime` and `end_datetime`.

| Status      | Condition                          | Meaning                                |
|-------------|------------------------------------|----------------------------------------|
| `active`    | `start ≤ dt ≤ end`                 | The moment is inside the festival      |
| `upcoming`  | `dt < start`                       | The festival is ahead                  |
| `past`      | `dt > end`                         | The festival has ended                 |

`distance_days` is the signed-positive distance to the nearest edge:
zero for an active festival, days-until for an upcoming one, days-since
for a past one. Results are sorted by `distance_days` ascending —
active festivals appear first (distance 0), then nearest upcoming or
past.

The proximity query also deduplicates: if the same festival resolves
under multiple years (when `dt` is near a year boundary and the
engine checks both years), only the closest occurrence is returned.

## The 14-day default proximity window

The default `window_days = 14` is the **lunar-quarter half-window**.
Half of one lunar quarter (a quarter is 7.4 days; doubled and rounded
gives 14) is the natural temporal radius for "this season's
observances." Inside 14 days the practitioner is plausibly *preparing
for* an upcoming festival or *still inside the wake of* a past one.

Outside 14 days the festival is no longer contextual. The instrument
will not surface Vesak in early January, even though Vesak exists in
the calendar — it is too far away to be relevant to the moment being
read.

Callers can override the window. Two weeks is the **interpretive
horizon**, not a fixed law. A 30-day query is reasonable for
seasonal planning; a 1-day query is reasonable for "is today a
festival?" queries.

## Integration with the four temporal bodies

The festival registry is a **calendar-layer contextualisation**. It
operates at the same scale as the Divine Month and Sephirotic Week —
it tells the practitioner *what kind of period this is*, not *what
the instantaneous state of the qi is*. The four temporal bodies
(Soul, Solar Keys, Astral, Gross) continue to compute exactly as
specified in `.claude/rules/temporal-bodies.md`. The festival layer
sits beside them, not above them.

A reading on May 17, 2026 might surface as:

```
Divine Month:    9 — SAMMA (The Container / Rhombus)
Soul body:       Sole Atom (Last Quarter, Gèn ☶)
Solar Keys:      neither active
Astral body:     Yin Wei vessel (LGBF derivative)
Gross body:      Heart organ window
Festivals:
  active   → Saga Dawa (day 1 of 30)
  upcoming → Divine Marriage (in 7 days)
  upcoming → Vesak (in 14 days)
```

The festival layer does not change what the other bodies report. It
adds a **frame**: the same Heart-organ reading on the first day of
Saga Dawa carries a different weight than the same reading two months
later in the same lunar phase. The instrument supplies the frame; the
practitioner does the interpretation.

This is the same operating principle as the Tier 0 character of each
Divine Month — the qualities dress the moment without dictating its
content. A festival from another tradition dresses the moment the
same way, except the tradition doing the dressing is acknowledged
rather than implicit.

## Provenance — honour the tradition

Every festival has a `source_note` field in the JSON. When discussing
a festival in any output, surface the source. Examples:

```
Saga Dawa  →  [SOURCE: Tibetan Buddhist tradition. Mama Food Forest text May 2026.]
Vesak      →  [SOURCE: Buddhist tradition; UN-recognized international observance since 1999]
Diwali     →  [SOURCE: Hindu / Vedic calendrical tradition]
Easter     →  [SOURCE: Christian tradition; Council of Nicaea 325 CE definition]
Nowruz     →  [SOURCE: Zoroastrian / Persian tradition; UN International Day of Nowruz]
```

Do not flatten festivals into "ancient sacred days" or "wisdom
traditions." Name the tradition the festival belongs to. Use the
native script when the festival has one — ས་ག་ཟླ་བ་ for Saga Dawa,
दीपावली for Diwali, عيد الفطر for Eid al-Fitr, יום כיפור for Yom
Kippur, 七夕 for Qixi. Provide the transliteration where the JSON
provides one.

The registry honours these traditions by representing them on their
own terms, in their own scripts, with their own anchor rules. The
Astrolabium is not converting other calendars into the Damanhurian
calendar. It is reporting them alongside it.

## The `merit_multiplier_classical` convention

Two Tibetan Buddhist festivals — **Saga Dawa** and **Chotrul Duchen**
— carry a `merit_multiplier_classical` of **100,000**. This is the
classical Tibetan teaching that virtuous actions performed on these
days are multiplied 100,000-fold in karmic effect. The convention is
*classical* — it represents what the Tibetan tradition teaches, not
what the Astrolabium asserts about karma.

The field is `merit_multiplier_classical` rather than just
`merit_multiplier` precisely to mark this provenance: the number is
reported because the tradition reports it. The registry surfaces it
without endorsing or rejecting the underlying cosmological claim.

If additional festivals carry classical merit multipliers from their
respective traditions (some Hindu traditions ascribe magnified karmic
weight to certain tithis), they should be added with the same field
name and the same `_classical` qualifier.

[SOURCE: Tibetan Buddhist tradition.]

## Known limitations

The current implementation is honest about three areas of
approximation.

**1. Computed-anchor festivals use window midpoints.** Easter, Diwali,
Holi, Navratri, Passover, Yom Kippur, Rosh Hashanah, Magha Puja,
Asalha Puja, Chunjie — all currently resolve to the midpoint of their
documented `gregorian_window`. This is sufficient to surface them in a
14-day proximity query during the correct season; it is not sufficient
to pin them to their tradition-canonical exact dates. Refinement —
the true Paschal full moon algorithm, Hindu Vedic calendar arithmetic
(amanta vs purnimanta reckoning), Hijri month tracking — is queued
for a follow-up sprint.

**2. The Chinese lunar arithmetic ignores intercalary months.** The
`lunar_month_day` resolver counts lunations from the New Moon nearest
Lìchūn without checking whether the Chinese calendar inserts an
intercalary month before reaching the target. For Qixi (7/7) and
Mid-Autumn (8/15) the error is at most one lunation in intercalary
years.

**3. Tibetan calendar uses simplified Phugpa lunation counting.** The
full Phugpa system handles "skipped days" and "doubled days" that
affect display-calendar ordering. The current implementation treats
months as consecutive lunations, which is correct for *which* lunar
month a given moment falls inside but does not reproduce the full
Tibetan day-numbering scheme. For festival proximity this is the
right trade-off; for issuing Tibetan calendar dates it is not.

When any of these limitations matter for a specific user query, mark
the response with the limitation. The instrument's reputation is built
on naming what it does not yet do precisely.

## Common errors

**Do not claim a festival from another tradition is Damanhurian
because it falls near a Great Rite.** Imbolc, Beltane, Lughnasadh,
and Samhain (the four Celtic cross-quarter days) bracket the
Damanhurian Great Rites in the solar year, but they are **separate
traditions with parallel observances**. The Celtic calendar is
pre-Christian Irish; the Damanhurian calendar descends from Falco's
1949 lineage; they share the solar wheel but not the cosmology.
Likewise the Mexican Day of the Dead and the Damanhurian Day of the
Dead share a civil date (November 2) and a thematic concern (the
dead) but are independent observances. The registry includes both
because both are real. Do not collapse them.

**Do not surface festivals as if practitioners must observe them.**
The registry is informational. A Christian visitor whose state report
notes Saga Dawa is active is receiving useful temporal context, not
an instruction to observe Saga Dawa. The same applies in reverse: a
Buddhist visitor whose state report notes Passover is upcoming
receives the same kind of context. Never frame any festival as
obligatory on the practitioner.

**Do not romanticise festivals into generic "sacred time."** Each
festival commemorates something specific. Saga Dawa commemorates the
Buddha's birth, enlightenment, and parinirvana. Yom Kippur is the Day
of Atonement. Easter celebrates the resurrection. These are not
interchangeable spiritual signifiers. When a festival is mentioned,
its commemoration is mentioned with it.

**Do not modify the `merit_multiplier_classical` value or add
multipliers from your own analysis.** The classical 100,000 figure
for Saga Dawa and Chotrul Duchen comes from Tibetan tradition. New
multipliers may be added only when documented in a source tradition,
never as analytical contribution.

**Do not report a festival's date from a `computed`-anchor entry
without flagging the approximation.** When Easter, Diwali, Passover,
or any other computed-window festival surfaces in a proximity result,
the response should acknowledge that the date is approximate to the
documented window's midpoint, and that the canonical computation is a
follow-up refinement.

**Do not refuse to report festivals whose window is `"varies"`.** The
engine returns `None` for these (Eid al-Fitr and Eid al-Adha) and the
proximity query simply omits them. This is correct behaviour. Do not
fabricate dates to fill the gap; do not apologise for the omission in
every response. If a user asks specifically about an Islamic
observance, name the limitation and point at the deferred-sprint
status.

## Cross-references

- `.claude/rules/divine-calendar.md` — the Damanhurian frame inside
  which the festival registry overlays. The Great Rites are listed in
  both places; the registry is the engine's source of truth.
- `.claude/rules/names-of-power.md` — Tier 0 character of each Divine
  Month, which dresses the moment in parallel with festival proximity.
- `.claude/rules/trigram-laws.md` — the 6+2 Cyclic + Solar Key
  architecture that the festival registry sits beside.
- `.claude/rules/temporal-bodies.md` — the four-body model into which
  festival proximity feeds as a calendar-layer frame.
- `astrolabium/data/sacred_festivals.json` — the registry data file
  (32 festivals, version 1.0).
- `astrolabium/src/engine/festivals.py` — the engine: resolver
  functions per anchor type, the proximity query, and the Tibetan
  month helper.
- `astrolabium/src/engine/solar_terms.py` — the 24 Chinese solar
  terms used by both the `solar_term` resolver and the Chinese
  lunisolar arithmetic.
