# Heliacal Risings

> A star's first dawn appearance after a period of invisibility, when
> it has been "swallowed by the Sun" — too close in the sky to be
> seen against twilight. The Deep Sky layer of the Astrolabium.

---

## What a heliacal rising is

A bright star is visible at night for most of the year. Each year,
however, there is a span — weeks for the brightest stars, a month or
more for fainter ones — when the Sun lies too close to the star's
position in the sky. During this interval the star rises and sets
nearly with the Sun and is drowned in solar glare. It is, in the old
phrase, **swallowed by the Sun**.

The **heliacal rising** (Greek *hēlios* + the rising of) is the first
morning the star reappears: the first dawn on which it clears the
eastern horizon with the Sun still far enough below it that the
star's light wins. After this morning, the star will rise a little
earlier each day, climbing back into the night sky.

A complementary event, the **heliacal setting**, is the last evening
the star is visible at sunset before disappearing into the Sun's
glare. The engine does not compute heliacal settings explicitly; the
focus is on the rising as the calendar-anchoring event most
traditions used.

[SOURCE: classical astronomy — Hesiod, *Works and Days*, c. 700 BCE,
on Pleiades; Ptolemy, *Almagest* IX, on the geometry; modern treatment
in Schaefer, *Vistas in Astronomy* 36 (1993) 311–361.]

## Why it mattered historically

Heliacal risings were the **precise calendar anchors** of every
premodern agricultural and seafaring civilization. They are
self-correcting in a way that lunar months and civil years are not:
the star's position against the Sun is a fact of the solar system,
unaffected by which king last reformed the calendar or which
intercalary month a priesthood last inserted.

**Sirius and Egypt.** The heliacal rising of Sirius (Egyptian
*Sopdet*, Greek *Sothis*) at Memphis (~30°N) fell around mid-July to
early August in the Old Kingdom era and coincided with the annual
inundation of the Nile. The Egyptian civil year of 365 exact days
drifted against the true solar year by about one day every four
years. Sirius's heliacal rising, anchored to the actual Earth-Sun
geometry, drifted with it — and the **Sothic cycle of 1,460 Julian
years** (the period over which the civil calendar and the Sothic
calendar realigned) is the single longest-baseline calendar
verification mechanism in antiquity. Censorinus records that the
Sothic cycle reset in 139 CE; back-projection gives reset points at
1322 BCE and 2782 BCE, the second of which sits near the
construction of the Great Pyramid. [SOURCE: Censorinus, *De Die
Natali* 21; Parker, *The Calendars of Ancient Egypt* (1950).]

**The Pleiades and Mediterranean sailing.** Hesiod, *Works and Days*
383–387: harvest when the Pleiades rise, plow when they set. At
classical Greek latitudes (~38°N) the Pleiades' heliacal rising
fell in mid-May; their heliacal setting in late October. The
**sailing season** was bounded by these two events. The Roman
*mare clausum* — the closed sea, when navigation was officially
suspended — ran from Pleiades-setting to Pleiades-rising.

**Spica and temperate Europe.** The heliacal rising of Spica
(Latin *spica* = "ear of grain," the sheaf the Virgin holds) was
read in temperate northern latitudes as the marker for **spring
planting**. The name itself encodes the agricultural reading: the
star and the crop arrive together.

**Pleiades in the Andes.** The *nuyt-yaku* observation — Quechua for
"clean Pleiades" versus "dim Pleiades" — was used by Andean farmers
to predict El Niño years. A bright Pleiades at June heliacal rising
forecasted a normal harvest; a dim Pleiades forecasted drought and
delayed planting. Modern atmospheric science confirms: in El Niño
years, high-altitude cirrus over the Andes dims the cluster's
appearance at heliacal rising. The cultural practice tracks a real
meteorological signal. [SOURCE: Orlove et al., *Nature* 403 (2000)
68–71.]

These are four examples; analogous heliacal-rising calendars exist
across Mesoamerica (Venus heliacal cycle in the Dresden Codex),
Polynesia (Pleiades navigation), Australian Aboriginal traditions,
ancient China (the Twenty-Eight Mansions are themselves built around
reference-star visibility), and the Old Norse rune-stick calendars.

## The astronomical mechanism

Three quantities determine the date of a star's heliacal rising at a
given location:

1. **The star's declination** (Dec) — its angular distance north or
   south of the celestial equator. Fixed against the stars; changes
   only with the slow drift of precession over millennia.
2. **The observer's latitude** — sets the geometry of the local
   horizon relative to the celestial equator. A star with declination
   +20° culminates much higher in the sky for an observer at 40°N
   than for one at 60°N; its rising azimuth and the steepness of its
   apparent path through twilight differ accordingly.
3. **The Sun's position** — moves ~1° per day along the ecliptic.
   When the Sun's right ascension lies close to the star's RA, the
   star is swallowed; as the Sun moves away (eastward through the
   zodiac), the star reappears at dawn first, then earlier and
   earlier through the year.

The heliacal rising occurs on the morning when, at the start of
nautical or civil twilight, the star is just above the eastern
horizon while the Sun is still below by an angular margin sufficient
for the star's light to register against the brightening sky. That
margin is the **arcus visionis**.

[MATHEMATICAL FACT — geometric. The exact date depends on
atmospheric extinction (worse at low altitudes), the star's
brightness, the observer's visual acuity, and local horizon
obstruction. Schaefer's algorithm models all of these; the engine
implements a simpler geometric check sufficient for calendrical use.]

## The arcus visionis

The **arcus visionis** is the angular distance the Sun must be below
the horizon for a star at the horizon to be visible. It is the
single most important parameter in heliacal-rising computation, and
it **varies with the star's brightness**.

| Star type                     | Typical arcus visionis |
|-------------------------------|------------------------|
| Sirius (-1.46 mag)            | ~8°                    |
| 1st magnitude stars           | ~10–12°                |
| Pleiades cluster (~2.9 mag)   | ~12–13°                |
| Mid-magnitude (3rd–4th mag)   | ~15–17°                |
| Faint naked-eye (5th–6th mag) | ~18° or more           |

The engine uses **13° as `DEFAULT_ARCUS_VISIONIS_DEG`**. This is
appropriate for bright naked-eye stars — most of the catalog — and
slightly conservative for Sirius (which is detectable at ~8° solar
depression, but reliably "first visible" closer to 10–12° once
extinction is accounted for). Callers who care about the historical
reconstruction for a specific star at a specific latitude should
override the default with a star-specific value derived from
Schaefer's tables.

[SOURCE: Schaefer (1993), Table 1, fits Ptolemy's *Phaseis*
observations to magnitude and zenith distance.]

The 13° default is a calendrical compromise, not a per-star truth.
The engine signals which value was used by returning
`arcus_visionis_deg_used` in the result dict; consumers should
display this when reporting the date.

## The 22 stars in the catalog — by significance

### Agricultural-year anchors

**Sirius (α CMa, -1.46 mag, Canis Major).** The brightest star in
the night sky. Egyptian agricultural year start; Sothic cycle
anchor; Greek *Kynos epitole*; Chinese Tianlang ("celestial wolf");
Polynesian navigation reference. At Memphis (30°N) the heliacal
rising historically fell in mid-July; at modern latitudes the date
has drifted slightly due to precession but the star remains the
canonical heliacal case.

**Pleiades (η Tau / Alcyone, 2.86 mag, Taurus).** The cluster as a
whole rises and sets coherently — the engine treats Alcyone (the
brightest member) as the reference. Hesiod's marker; Beltane fires
in Celtic tradition (heliacal rising near May 1 at ~50°N two
millennia ago); Andean *nuyt-yaku*; Subaru in Japan; Krittikā in
the Vedic *nakṣatra* system; Chinese mansion 17 (Mǎo 昴, the Hairy
Head). The single most cross-cultural heliacal marker after Sirius.

**Spica (α Vir, 0.97 mag, Virgo).** Spring planting in temperate
Europe; reference star of Chinese mansion 0 (Jiǎo 角, the Horn) and
of Indian Citrā nakshatra. Hipparchus used Spica's heliacal-setting
observations to discover precession around 130 BCE.

### The four Royal Stars of Persia (~3000 BCE)

The Persian Achaemenid astronomy identified four "Royal Stars" or
"Watchers," each marking one of the four cardinal directions of the
sky in the third millennium BCE (when precession had positioned
them as quasi-cardinal anchors).

| Watcher              | Star       | Direction | Approx. season anchor |
|----------------------|------------|-----------|-----------------------|
| Eastern Watcher      | Aldebaran  | East      | Spring equinox        |
| Northern Watcher     | Regulus    | North     | Summer solstice       |
| Western Watcher      | Antares    | West      | Autumn equinox        |
| Southern Watcher     | Fomalhaut  | South     | Winter solstice       |

The four-watcher scheme is precession-dependent and has drifted out
of alignment in the millennia since. The Astrolabium catalog
includes all four for cultural reference and for heliacal
calendrical use, but **does not** present them as currently-cardinal.

**Aldebaran (α Tau, 0.85 mag, Taurus).** Bull's Eye; Chinese mansion
18 (Bì 畢, the Net); Rohiṇī nakshatra. Late-spring marker in
northern temperate latitudes.

**Regulus (α Leo, 1.40 mag, Leo).** The "Little King." Late-summer
heliacal marker; lies almost exactly on the ecliptic (declination
~+12° currently); occasionally occulted by the Moon.

**Antares (α Sco, 1.06 mag, Scorpius).** The "rival of Mars" — red
supergiant whose color competes with Mars when Mars passes through
Scorpius. Reference star of Chinese mansion 4 (Xīn 心, the Heart);
Jyeṣṭhā nakshatra. Mid-summer marker.

**Fomalhaut (α PsA, 1.16 mag, Piscis Austrinus).** Southern Watcher;
isolated bright star in the autumn northern-hemisphere sky.

### The Summer Triangle and the Qixi myth

Three first-magnitude stars form a vast triangle high overhead in
the northern summer sky. Two of them are the lovers of the **Qīxī
Festival** (七夕, "Seventh Evening") — the Chinese romance celebrated
on the seventh night of the seventh lunar month.

**Vega (α Lyr, 0.03 mag, Lyra).** The Weaver Girl (Zhīnǚ 織女). Fifth-
brightest star in the night sky. Will be the pole star around
14,000 CE due to precession; last held that role around 12,000 BCE.

**Altair (α Aql, 0.77 mag, Aquila).** The Cowherd (Niúláng 牛郎).
Separated from the Weaver Girl by the Milky Way; the two meet across
the Magpie Bridge on the night of Qīxī. Śravaṇa nakshatra.

**Deneb (α Cyg, 1.25 mag, Cygnus).** The tail of the Swan; the third
vertex of the Summer Triangle. Will become a near-pole star around
10,000 CE.

### Pole stars across the precessional cycle

**Polaris (α UMi, 1.98 mag, Ursa Minor).** The current pole star,
closest approach to the celestial pole around 2100 CE. Circumpolar
at most northern latitudes — **never rises, never sets — no heliacal
rising applies**.

**Thuban (α Dra, 3.65 mag, Draco).** The pole star around 2787 BCE.
Aligned with the descending passage of the Great Pyramid of Giza,
which was constructed to point at Thuban at lower culmination.
Dim by modern naked-eye standards but historically critical for
Egyptian Old Kingdom astronomy.

### Chinese-mansion reference stars

Five named-star catalog entries are also reference stars of the 28
Lunar Mansions. The mansion system and the heliacal-rising layer
share these anchor points; consult `.claude/rules/28-lunar-mansions.md`
for mansion context.

| Star            | Chinese mansion              |
|-----------------|------------------------------|
| Spica           | 0 — Jiǎo 角 (Horn)           |
| Antares         | 4 — Xīn 心 (Heart)           |
| Pleiades        | 17 — Mǎo 昴 (Hairy Head)     |
| Aldebaran       | 18 — Bì 畢 (Net)             |
| Orion's Belt    | 20 — Shēn 參 (Three Stars)   |

The catalog entry for **Betelgeuse (α Ori)** stands proxy for the
Three Stars asterism in heliacal-rising computation, since its
brightness (0.50 mag) gives a more robust visibility threshold than
Alnilam or the other Belt stars at ~1.7 mag.

### Southern beacons

**Canopus (α Car, -0.74 mag, Carina).** Second-brightest star in
the night sky after Sirius. Invisible from most of Europe (south of
~37°N required). Primary navigational reference for the southern
sky; used by Polynesian wayfinders and Arab navigators (Arabic
*Suhayl*).

**Achernar (α Eri, 0.46 mag, Eridanus).** End of the celestial river
Eridanus; far southern declination, invisible from most of Europe.

**α Centauri (Rigil Kentaurus, -0.27 mag, Centaurus).** Third-
brightest star in the night sky; closest stellar system to the Sun
at 4.37 light-years. Visible only from southern latitudes.

### Remaining catalog entries

**Betelgeuse (α Ori, 0.50 mag).** Red supergiant in Orion's
shoulder; expected to supernova within the next ~100,000 years.

**Rigel (β Ori, 0.13 mag).** Blue supergiant in Orion's foot;
brightest star in Orion despite the β designation.

**Capella (α Aur, 0.08 mag).** Sixth-brightest star; brightest
within 30° of the north celestial pole. Late-autumn marker in
temperate northern latitudes.

**Procyon (α CMi, 0.34 mag).** The name means "before the dog" — it
rises shortly before Sirius. Eighth-brightest star.

**Arcturus (α Boo, -0.05 mag).** Fourth-brightest star. Spring
marker in northern temperate latitudes; Svāti nakshatra; Greek
"bear-guardian."

**Alphecca (α CrB, 2.23 mag).** Brightest star of the Northern
Crown — Ariadne's crown in Greek mythology.

**Alkaid (η UMa, 1.86 mag).** Last star in the handle of the Big
Dipper. Circumpolar at northern latitudes — **no heliacal rising
applies** at most temperate and high latitudes.

## Sirius and the Sothic cycle

The Egyptian civil calendar had exactly 365 days: twelve months of
30 days plus five epagomenal days. The tropical year is
approximately 365.2422 days. The civil calendar therefore drifted
against the seasons by one day every four years, completing a full
365-day cycle every **4 × 365 = 1,460 Julian years** (the integer
approximation; the true Sothic cycle is closer to 1,456 years
because of slow changes in Sirius's apparent motion).

Over this cycle the date of Sirius's heliacal rising in the civil
calendar shifted from First of Thoth (New Year's Day in the Sothic
alignment) progressively through every month of the year and back.
The cycle's known reset in 139 CE allows back-projection to 1322 BCE
and 2782 BCE — datings that have been used to anchor the absolute
chronology of the Egyptian Middle and Old Kingdoms.

[SOURCE: Censorinus, *De Die Natali* 21.10; Parker, *The Calendars
of Ancient Egypt* (1950); Krauss, *Sothis- und Monddaten* (1985).]

At Memphis (30.0°N) in 2787 BCE, the engine's computation places
Sirius's heliacal rising around July 17 (Julian-equivalent). At
the same latitude today, precession has shifted Sirius's
declination from approximately -16°35′ at J2000 to slowly evolving
values; the modern heliacal rising at 30°N falls in early August.
The date is not static.

## Precession and the drift of heliacal dates

The Earth's rotational axis precesses with a period of approximately
26,000 years. Over the timescale of recorded civilizations
(roughly 5,000 years), every star's right ascension and declination
have shifted measurably, and with them the dates of heliacal risings.

**The Pleiades case is illustrative.** For Hesiod's Greek audience
(~700 BCE, ~38°N), the Pleiades' heliacal rising fell in mid-May.
By the Roman late Republic (~50 BCE) it had moved to late May. For
a modern observer at the same latitude, it now falls in **late June**
— almost six weeks later than in Hesiod's day. The agricultural
correspondence Hesiod recorded ("harvest at Pleiades-rising") no
longer aligns with modern temperate-zone wheat harvest, which falls
in July–August. The star didn't move relative to its rural calendar
function; the calendar function moved because the sky did.

[MATHEMATICAL FACT — general precession at ~50.29 arcseconds per
Julian year, ~1° every 71.6 years, ~5° every 358 years.]

The engine computes against modern (J2000.0) star positions and
the current Sun. For historical heliacal-rising reconstruction, the
star's position must be precessed back to the epoch of interest,
which the engine does not do by default. Consumers needing
millennium-scale historical accuracy should consult a dedicated
historical-astronomy package (e.g., Skyfield with proper-motion
plus precession corrections).

## How the engine computes heliacal risings

The implementation in `astrolabium/src/engine/heliacal.py` follows
a deliberately simple geometric algorithm. It is sufficient for
forward calendrical use (the next heliacal rising of a star at a
modern location) and is not intended as a high-precision historical
astronomy tool.

```python
from astrolabium.engine import heliacal
from datetime import datetime
import pytz

dt = pytz.utc.localize(datetime(2026, 5, 18))
state = heliacal.heliacal_state(
    lat=45.0750,    # Damanhur
    lon=7.7569,
    tz="Europe/Rome",
    dt=dt,
    window_days=60,
)
```

The algorithm:

1. For each catalog star, construct an `ephem.FixedBody` at its
   J2000.0 RA and Dec.
2. Construct an `ephem.Observer` at the user's lat/lon, with
   `pressure = 0` (no atmospheric refraction modeling — the goal is
   geometric clarity, not survey-grade precision).
3. For a candidate morning, find sunrise time at the location.
4. Step back `arcus_visionis_deg * 4` minutes (the Sun moves 15° per
   hour, so 4 minutes per degree of solar depression).
5. At that observation time, compute the star's altitude and
   azimuth.
6. The star is **heliacally visible** if its altitude is above the
   horizon (alt > 0°) and its azimuth is broadly eastern
   (45° < az < 135°).
7. Scan forward day by day. The first morning the star transitions
   from invisible-yesterday to visible-today is the heliacal rising.

The transition logic in `next_heliacal_rising` handles the case
where the star is already visible at the query date: it walks
forward until invisible, then forward again until visible. The
result is always the **next** rising, never the most recent past one.

The azimuth band (45°–135°, "generously eastern") is wide enough to
accommodate stars rising at sharply oblique angles at high
latitudes. It is the band's width — not the arcus visionis — that
makes the algorithm robust at high-latitude observation sites where
heliacal-rising azimuths can wander far from due east.

`heliacal_state` returns:

```python
{
    "upcoming": [...],                     # within window_days
    "sirius_next_heliacal_rising": dt,     # always computed
    "window_days": 60,
}
```

The Sirius field exists because Sirius is the canonical heliacal
case — orchestrator presentations that include the Stellar Layer
should surface Sirius's next rising even if it lies outside the
default window.

## Interpreting the upcoming_heliacal_risings output

The upcoming-risings list is **not a list of directives**. A
heliacal rising is a **moment**, often celebratory or seasonally-
marking, but the practitioner's relationship to that moment is
theirs to determine. The same astronomical event may mean *new
agricultural cycle* in one tradition, *sailing season opens* in
another, *temple festival* in a third, and *nothing in particular*
in a fourth.

What the engine reports:

- **The star** (with cultural alt-names so the practitioner can
  recognize their tradition's reading)
- **The date** of the next heliacal rising at the location
- **The arcus visionis** used (so the date can be interpreted in
  light of the visibility margin assumed)
- **The cultural attestation** from the catalog `significance` and
  `heliacal_significance` fields, where one exists

What the engine does **not** report:

- A judgment of whether the rising is auspicious or inauspicious
- A directive about what the practitioner should do
- A claim that any specific tradition's reading applies to the
  current observer

Orchestrator presentations should preserve this distinction. The
star rises; the meaning is made.

## Common errors

- **Never compute a heliacal rising for a circumpolar star at high
  latitudes.** Polaris, at declination +89.26°, never sets at any
  northern latitude — its altitude is always approximately equal to
  the observer's latitude. The "heliacal" concept presupposes a
  period of invisibility, which circumpolar stars do not have. The
  `upcoming_heliacal_risings` function explicitly skips Polaris and
  Alkaid for this reason. Add other stars to the skip-list if the
  observer's latitude makes them circumpolar (rule of thumb: a star
  is circumpolar at latitude φ if its declination > 90° − φ).

- **Never use sidereal star positions for the Sun.** The Sun is a
  tropical body — its position is given as a tropical ecliptic
  longitude in `ephem` and must remain tropical for sunrise / sunset
  computation. Mixing a sidereally-corrected star position with a
  tropically-positioned Sun is fine because the visibility check is
  geometric (altitude, azimuth) and both bodies are computed in the
  same equatorial frame by `ephem`. The Lahiri ayanamsa correction
  that governs the 28 Mansion lookup is **not** applied here — it
  would be a category error.

- **Never treat the 13° default arcus visionis as a star-specific
  truth.** It is a calendrical compromise. Sirius is detectable at
  ~8°; the Pleiades cluster needs ~12–13°; a 4th-magnitude star may
  need 17° or more. Historical practices used star-specific values
  informed by careful observation, often calibrated by generations
  of practitioners. The engine's default is a serviceable
  approximation, not a reconstruction of any particular tradition's
  threshold.

- **Never present a modern heliacal rising date as the date a
  historical text would have recorded.** The Pleiades' heliacal
  rising at 38°N has drifted six weeks since Hesiod. Hesiod's
  "mid-May" is the modern "late June" at the same latitude. The
  engine computes for the current epoch; historical reconstruction
  requires explicit precession correction.

- **Never ignore the observer's location.** A heliacal rising is a
  local event. Sirius's rising at Cairo is not the same date as its
  rising at Reykjavík (where it occurs much later in the year, if
  at all in some years). The function signatures all require
  `(lat, lon, tz)` for this reason.

- **Never report a heliacal rising without the arcus visionis used.**
  Two computations of the same rising with different arcus values
  can differ by a week or more. The returned
  `arcus_visionis_deg_used` field exists specifically so consumers
  can disclose the assumption.

- **Never confuse heliacal rising with cosmical rising or with
  acronychal rising.** *Heliacal rising* = first dawn visibility
  (the engine's case). *Cosmical rising* = the star rises with the
  Sun (the star is at the eastern horizon at sunrise — invisible).
  *Acronychal rising* = the star rises as the Sun sets (visible all
  night, the opposite of the heliacal-rising condition). The three
  events are distinct points in the star's annual visibility cycle.

## Cross-references

- `.claude/rules/28-lunar-mansions.md` — the sidereal stellar
  architecture; five heliacal-catalog stars (Spica, Antares,
  Pleiades, Aldebaran, Orion's Belt) are also mansion reference
  stars
- `.claude/rules/divine-hours.md` — local solar time; heliacal
  computation requires location for the same reason
- `.claude/rules/temporal-bodies.md` — heliacal events do not
  belong to the four-body schema (Soul, Astral, Gross, Stellar);
  they are punctual astronomical anchors layered atop it
- `astrolabium/data/named_stars.json` — the canonical 22-star
  catalog (positions, magnitudes, cultural attestations)
- `astrolabium/src/engine/heliacal.py` — the computation engine
- `docs/specs/operators_manual.md` — Part 1, user-facing Deep Sky
  presentation
- `docs/specs/guidebook.md` — Part 2, technical reference and
  worked examples for heliacal-rising dates at the principal
  practitioner latitudes
