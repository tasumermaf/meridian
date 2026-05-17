# The Divine Calendar

> Thirteen lunar months, six Great Rites anchored to astronomical
> events, the Sephirotic Week within each lunar quarter, the
> three-movement alchemical year. The macro-temporal frame inside
> which all the other layers operate.

---

## The Year

The **Divine Year** begins at the **New Moon nearest the Autumn
Equinox** of the Gregorian year. Year 1 was 1949 (the founding year
of the Damanhurian lineage from which this calendrical system
descends). The current Divine Year is computed as
`anchor_gregorian_year − 1949 + 1`.

The year contains either **12 or 13 lunar months**, depending on how
many New Moons fall between two consecutive Autumn-Equinox-adjacent
NMs. A year with 13 lunations includes the intercalary month
**VADUSFADAHM** in slot 13. Intercalation happens in approximately
**36.6% of years**, matching the Metonic distribution.

```
Epoch:       New Moon Sep 22, 1949 12:20:56 UTC
Year start:  NM nearest to Autumn Equinox of the Gregorian year
Month:       New Moon to New Moon (29 or 30 days per lunation)
Intercalary: When year contains 13 lunations → Month 13 = VADUSFADAHM
Sephirotic:  Each lunar quarter (NM→FQ→FM→LQ→NM) = 7-9 days
             Day 1 = Tiphareth/Sol, Day 9 = Kether/Neptune
Divine Year: anchor_gregorian_year - 1949 + 1   (Year 1 = 1949)
```

## The Twelve Regular Months

| #  | Name        | Element        | Tier 0 Character (one-line)             | Great Rite          |
|----|-------------|----------------|------------------------------------------|---------------------|
| 1  | **ISIS**       | Air            | The Gatherer                          | Autumn Equinox      |
| 2  | **SADAM**      | Earth          | The Mirror-Operator                   | Day of the Dead     |
| 3  | **LIOTHIL**    | —              | The Helper                            | —                   |
| 4  | **EOROS**      | Fire           | The Director (Horus)                  | Winter Solstice     |
| 5  | **TASUMER**    | —              | The Builder                           | —                   |
| 6  | **MENON**      | —              | The Enduring One                      | —                   |
| 7  | **OSIRIS**     | Ether          | The Resurrected                       | Spring Equinox      |
| 8  | **AGAFEST**    | —              | The Celebrant                         | —                   |
| 9  | **SAMMA**      | —              | The Container (Rhombus)               | Divine Marriage     |
| 10 | **SET**        | Water          | The Destroyer                         | Summer Solstice     |
| 11 | **SADAS**      | —              | The Mirror-Keeper                     | —                   |
| 12 | **DESURIORIS** | —              | The Sovereign                         | —                   |
| 13 | **VADUSFADAHM** | —             | The Activation (intercalary)          | —                   |

For full interpretive character of each name see
`.claude/rules/names-of-power.md`.

## The Six Great Rites

Six rites anchor to specific astronomical/calendrical events:

| Rite                | Anchor                                      | Month     |
|---------------------|---------------------------------------------|-----------|
| **Autumn Equinox**  | sun crosses celestial equator (descending)  | ISIS      |
| **Day of the Dead** | early November (traditional)                | SADAM     |
| **Winter Solstice** | sun's lowest declination                    | EOROS     |
| **Spring Equinox**  | sun crosses celestial equator (ascending)   | OSIRIS    |
| **Divine Marriage** | May 24 (anniversary of the lineage's marriage rite) | SAMMA |
| **Summer Solstice** | sun's highest declination                   | SET       |

**There is no Lion's Gate.** That is a Theosophical/New Age construct
not part of this calendrical system. If a user asks about it, you can
acknowledge it exists in other systems and explain that the Damanhurian
calendar does not include it.

The six rites are spaced approximately seven weeks apart. Together
they form the cosmological-ritual frame of the Divine Year.

## The Three-Movement Alchemical Year

The twelve regular months group into three alchemical movements of
four months each:

| Movement   | Months                                | Function                                |
|------------|---------------------------------------|------------------------------------------|
| **Nigredo** | ISIS, SADAM, LIOTHIL, EOROS          | Gather → Mirror → Help → Birth          |
| **Albedo**  | TASUMER, MENON, OSIRIS, AGAFEST      | Build → Endure → Resurrect → Celebrate  |
| **Rubedo**  | SAMMA, SET, SADAS, DESURIORIS        | Unite → Destroy → Enter → Rule          |

This follows the classical alchemical sequence (blackening → whitening
→ reddening) mapped onto the Autumn-to-Autumn arc of the Divine Year.
[ANALYTICAL CONTRIBUTION — the specific verb-mapping per month is a
synthesis between the Damanhurian Tier 0 character of each Name and the
classical alchemical sequence.]

## VADUSFADAHM — the intercalary 13th month

When a Divine Year contains 13 lunations between its start NM and the
next year's start NM, VADUSFADAHM is inserted as Month 13.
Astronomical computation determines this; there is no fixed rule like
"every seven years." `astrolabium/src/engine/calendar.py` runs the
counting directly via `ephem`.

**VADUSFADAHM** is the **activation formula** of the Sacred Language.
The word decomposes as VAD ("Power") + USFAD ("Conscience, Aware,
Precise, Diligent") + AM ("Personal name"). It carries the
**conscience suffix** of the entire Sacred Language system — the
quality of awareness inserted between cycles. Inserting it as the
intercalary month places that quality of awareness *between* the
twelve normal months and the start of the next year. It is the
Astrolabium calendar's pause for reflection before the gathering of
ISIS begins again.

[SOURCE: Damanhurian — Sacred Language dictionary, Names of Power
analysis. See `.claude/rules/names-of-power.md`.]

## The Sephirotic Week

Each lunar quarter — from New Moon to First Quarter, First Quarter to
Full Moon, Full Moon to Last Quarter, Last Quarter to next New Moon —
contains **7 to 9 days**, depending on the precise timing of the
quarter cusps. The Astrolabium names these days using the **Hellenistic
planetary weekday** ordering, extended through the supernal Sephiroth.

| Day | Sephirah     | Planet      | Hex (palette)        |
|-----|--------------|-------------|----------------------|
| 1   | Tiphareth    | Sol ☉       | (gold)               |
| 2   | Yesod        | Luna ☽      | (silver)             |
| 3   | Geburah      | Mars ♂      | (red)                |
| 4   | Hod          | Mercury ☿   | (orange)             |
| 5   | Chesed       | Jupiter ♃   | (blue)               |
| 6   | Netzach      | Venus ♀     | (green)              |
| 7   | Binah        | Saturn ♄    | (dark blue)          |
| 8   | Chokmah      | Uranus ♅    | (extended — gray)    |
| 9   | Kether       | Neptune ♆   | (extended — white)   |

The first seven days reproduce the traditional Hellenistic planetary
weekday exactly (Sun-day, Moon-day, Mars-day = Tuesday, Mercury-day =
Wednesday, Jupiter-day = Thursday, Venus-day = Friday, Saturn-day =
Saturday). The **Chaldean skip-3 mechanism** is the classical
algorithm that produced this ordering from the seven classical planets
by spacing them around a heptagram.

Days 8 and 9 extend the sequence into the modern planets (Uranus and
Neptune) at the supernal Sephiroth (Chokmah and Kether), filling out
the seven-to-nine-day window. These extensions are [ANALYTICAL
CONTRIBUTION] — the Hellenistic source material only specifies seven
days. The extension is consistent with the standard Tree of Life
planet-Sephirah mapping used in Western Mystery tradition.

[SOURCE: Hellenistic / Western Mystery + ANALYTICAL CONTRIBUTION
(extension to days 8-9)]

## Year Numbering Examples

| Gregorian year start ≈ | Anchor NM (UTC, approx)      | Divine Year |
|------------------------|------------------------------|-------------|
| 1949 Autumn Equinox     | 1949-09-22 12:20:56          | **1**       |
| 1950 Autumn Equinox     | 1950-09-12                   | **2**       |
| 2025 Autumn Equinox     | (Sep 21 NM nearest Sep 22)   | **77**      |
| 2026 Autumn Equinox     | (Sep 10 NM nearest Sep 22)   | **78**      |

The engine computes the exact NM via `ephem` — no lookup table. See
`astrolabium/src/engine/calendar.py`.

## Year Composition Examples

A user might want to know: *"how many days is this Divine Year? How
many months? Is VADUSFADAHM in it?"* The engine answers all three via
`calendar.get_divine_year(dt)`.

| Divine Year | Months | Intercalary? | Total days |
|-------------|--------|--------------|------------|
| (a typical 12-month year) | 12    | No           | ~354       |
| (a typical 13-month year) | 13    | Yes          | ~384       |

The instrument confirms intercalation directly from the NM count, not
from a 7-year cycle approximation. The pre-2026 implementations used a
simplified 7-year rule; this has been replaced.

## What never to do

- Never report a Divine Year without computing it from the New Moon
  nearest the Autumn Equinox. Calendar-year approximations are wrong.
- Never assume VADUSFADAHM is present without checking. Most years
  do not contain it.
- Never report the Sephirotic Week day from a count starting at the
  Gregorian week. The week count restarts at each lunar quarter cusp.
- Never present the alchemical three-movement structure as
  [SOURCE: Damanhurian]. The Nigredo/Albedo/Rubedo mapping is
  classical alchemical, applied analytically; the Damanhurian sources
  describe a 13-month year and Name characters, not necessarily this
  particular alchemical projection.

## Cross-references

- `.claude/rules/names-of-power.md` — Tier 0 character of each month
- `.claude/rules/temporal-bodies.md` — how the calendar relates to
  the moment-by-moment layers
- `.claude/rules/divine-hours.md` — the daily hour structure inside
  any given calendar day
- `astrolabium/src/engine/calendar.py` — the calendar engine
- `docs/specs/operators_manual.md` — Part 1 user-facing presentation
- `docs/specs/guidebook.md` — Part 2 computational tables
