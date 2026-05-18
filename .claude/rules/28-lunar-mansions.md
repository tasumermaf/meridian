# The 28 Lunar Mansions (二十八宿)

> The sidereal Chinese stellar architecture. Twenty-eight non-uniform
> arcs of the ecliptic, anchored to actual reference stars, organized
> into four celestial palaces. The Stellar Layer of the Astrolabium.

---

## What the system is

**二十八宿** — *Èrshíbā Xiù* — "Twenty-Eight Lodgings" or "Twenty-Eight
Mansions." A division of the ecliptic (the great circle the Sun, Moon,
and planets travel along) into **twenty-eight unequal arcs**, each
anchored to a specific reference star. The Sun spends roughly thirteen
days in each mansion; the Moon, slightly less than a day in each
(hence "lunar" mansions — the Moon visits all twenty-eight in a single
sidereal month of 27.32 days).

The mansions are **non-uniform**. They range from about 3° wide (Zī
觜, Turtle Beak, the head of Orion) to about 27° wide (Jǐng 井, the
Well, in Gemini). The widths reflect the actual stellar geography the
Chinese astronomers were anchoring to, not an abstract equal division.
This is the central architectural difference from the Western tropical
zodiac, which carves the ecliptic into twelve equal 30° slices
regardless of where the stars actually are.

[SOURCE: Chinese classical astronomy — Han through Ming canon. The
twenty-eight mansion system is documented in the *Shǐjì* (Records of
the Grand Historian, c. 94 BCE), the *Hàn Shū* astronomical
treatises, and the Ming-dynasty *Míngshǐ Tiānwén Zhì*. Reference star
identifications follow the canonical asterism mapping in the *Yítiānyí*
(Yuan/Ming celestial globe tradition).]

The Astrolabium uses the Chinese mansion convention as its default.
Related 27-mansion and 28-mansion systems exist in the Indian
*nakṣatra* tradition and Tibetan *gyukar* reckoning; differences are
noted in the cross-traditions section below. The engine does not
attempt to harmonize them — the Chinese definitions are what
`stellar.py` reads.

## The Four Palaces

The twenty-eight mansions are grouped into **four celestial palaces**,
each covering seven consecutive mansions, one cardinal direction, one
season, and one Wǔ Xíng element. The palaces are also called the four
**Heavenly Animals** — vast figural asterisms spanning a quarter of
the sky each.

| Palace                | Chinese      | Pinyin              | Direction | Season | Wu Xing | Mansions |
|-----------------------|--------------|---------------------|-----------|--------|---------|----------|
| Azure Dragon East     | 東方蒼龍     | Dōngfāng Cānglóng   | East      | Spring | Wood    | 1–7      |
| Black Tortoise North  | 北方玄武     | Běifāng Xuánwǔ      | North     | Winter | Water   | 8–14     |
| White Tiger West      | 西方白虎     | Xīfāng Báihǔ        | West      | Autumn | Metal   | 15–21    |
| Vermillion Bird South | 南方朱雀     | Nánfāng Zhūquè      | South     | Summer | Fire    | 22–28    |

[SOURCE: Chinese classical astronomy. The four-palace scheme is
documented from at least the Warring States period; the figural
animals are visible carvings on the Han-era Five Beasts Mirror series
and the Zēng Hóu Yǐ lacquer chest (433 BCE), the oldest dated artifact
showing the twenty-eight-mansion + four-animal architecture
together.]

The **direction–season–element** mapping follows the standard Chinese
correspondences (East/Spring/Wood, etc.). The Black Tortoise is the
only one of the four animals composed of two creatures (a tortoise
entwined with a snake); the other three are single beasts.

The palace assignment is **not arbitrary geography**. The four animals
are read in the sky in the same direction the body lies on the
ground: when the Azure Dragon rises in the east at dusk, that is
spring; when the Vermillion Bird culminates due south at dusk, that is
summer. The system is a giant celestial clock keyed to seasonal
agriculture.

## The Twenty-Eight Mansions

The mansions are listed below in canonical order, starting with Jiǎo
(Horn) — the first mansion of the Azure Dragon, anchored at Spica.
This is the order the Moon and Sun traverse them in apparent motion
along the ecliptic (west-to-east, against the diurnal rotation).

### Azure Dragon Palace (East, Spring, Wood)

| # | Chinese | Pinyin | English          | Animal              | Reference Star          | Width  |
|---|---------|--------|------------------|---------------------|-------------------------|--------|
| 1 | 角      | Jiǎo   | Horn             | Jiao (hornless dragon) | Spica (α Vir)         | 12°    |
| 2 | 亢      | Kàng   | Neck             | Dragon              | Kang (κ Vir)            | 9°     |
| 3 | 氐      | Dī     | **Root**         | Raccoon-dog         | Zubenelgenubi (α Lib)   | 15°    |
| 4 | 房      | Fáng   | Room             | Rabbit              | Dschubba (δ Sco)        | 5°     |
| 5 | 心      | Xīn    | Heart            | Fox                 | Antares (α Sco)         | 5°     |
| 6 | 尾      | Wěi    | Tail             | Tiger               | Shaula (λ Sco)          | 18°    |
| 7 | 箕      | Jī     | Winnowing Basket | Leopard             | Polis (γ Sgr)           | 11°    |

**Mansion 3 — Dī 氐, "The Root" — deserves the long entry.** Dī is
where the dragon's body truly begins to unfold. The two preceding
mansions (Horn and Neck) are the dragon's head; from Root, the spine
extends. The Chinese character 氐 means **root, foundation, the
underlying ground of earth-currents, the source of life-force**. In
classical Chinese astronomy Dī is the dragon's chest cavity — the
seat of the breath, the hollow that resonates.

Dī is also the lunar mansion of the **Saga Dawa** Buddhist month —
the fourth month of the Tibetan lunisolar calendar, when the Buddha's
birth, enlightenment, and *parinirvāṇa* are all commemorated. The
Tibetan tradition reads this mansion as the place where merit
accumulated multiplies tenfold (some sources say a hundred thousand),
and the entire month carries that quality because the Full Moon of
Saga Dawa falls in or near Dī. **The dragon root awakens.** Earth
currents begin to move before the dragon itself rises — this is the
felt quality of the mansion, both in Chinese geomantic reading and
in the Tibetan Buddhist usage that overlays it.

[SOURCE: Chinese classical astronomy for the mansion definition;
SOURCE: Tibetan Buddhism for the Saga Dawa correspondence. The
synthesis — the dragon-root reading as a single integrated symbol
spanning both traditions — is [ANALYTICAL CONTRIBUTION] from the
*Falco Council on Saga Dawa* source PDF that motivated the
addition of the Stellar Layer.]

The remaining six mansions of the Azure Dragon trace the dragon's
**body**: Room (chamber, the dragon's dwelling) — Heart (Antares, the
fire-star, one of the most ancient reference points in human
astronomy, called the "Anti-Mars" because its rust-red color rivals
Mars) — Tail (the dragon's tail, wide at 18°) — Winnowing Basket
(separator of essence from chaff, traditionally associated with the
wind). When the Azure Dragon rises in spring, the agricultural year
begins.

### Black Tortoise Palace (North, Winter, Water)

| #  | Chinese | Pinyin | English      | Animal            | Reference Star            | Width  |
|----|---------|--------|--------------|-------------------|---------------------------|--------|
| 8  | 斗      | Dǒu    | Dipper       | Xiezhi (unicorn)  | Kaus Borealis (λ Sgr)     | 26°    |
| 9  | 牛      | Niú    | Ox           | Ox                | Dabih (β Cap)             | 8°     |
| 10 | 女      | Nǚ     | Maiden       | Bat               | Sadalsuud (β Aqr)         | 12°    |
| 11 | 虛      | Xū     | Emptiness    | Rat               | β Aqr area                | 10°    |
| 12 | 危      | Wēi    | Rooftop      | Swallow           | Sadalmelik (α Aqr)        | 17°    |
| 13 | 室      | Shì    | Encampment   | Boar              | Markab (α Peg)            | 17°    |
| 14 | 壁      | Bì     | Wall         | Porcupine         | Algenib (γ Peg)           | 14°    |

Note: **Dǒu** (mansion 8) is the *Southern* Dipper (in Sagittarius), not
the Big Dipper (北斗 Běi Dǒu, the Northern Dipper / Ursa Major). The
Big Dipper is a circumpolar asterism and not part of the
twenty-eight-mansion system, which is ecliptic-bound. Confusing the
two is a classical error in beginner mistranslations.

The Ox (Niú) and the Maiden (Nǚ) are linked by the **Qīxī Festival**
myth — the Cowherd and the Weaver Girl, lovers separated across the
Milky Way and reunited once a year on the seventh night of the
seventh month. Vega (the Weaver Girl) sits near the boundary; the
Ox is associated with Altair across the river.

**Wall** (Bì, mansion 14) is the last mansion of the Black Tortoise
and crosses the 0°/360° ecliptic boundary in the engine's sidereal
lookup. The mansion boundary spans 343° → 14°, wrapping the vernal
point. The lookup code in `stellar.py` handles this wrap explicitly.

### White Tiger Palace (West, Autumn, Metal)

| #  | Chinese | Pinyin | English      | Animal     | Reference Star               | Width  |
|----|---------|--------|--------------|------------|------------------------------|--------|
| 15 | 奎      | Kuí    | Legs         | Wolf       | Mirach (β And)               | 16°    |
| 16 | 婁      | Lóu    | Bond         | Dog        | Sheratan (β Ari)             | 12°    |
| 17 | 胃      | Wèi    | Stomach      | Pheasant   | Mirfak area (α Per)          | 14°    |
| 18 | 昴      | Mǎo    | Hairy Head   | Cock       | **Alcyone (η Tau, Pleiades)**| 11°    |
| 19 | 畢      | Bì     | Net          | Crow       | **Aldebaran (α Tau)**        | 17°    |
| 20 | 觜      | Zī     | Turtle Beak  | Monkey     | Meissa (λ Ori)               | 3°     |
| 21 | 參      | Shēn   | Three Stars  | Ape        | **Alnilam (ε Ori, Belt)**    | 12°    |

The White Tiger contains the densest cluster of bright reference stars
in the entire mansion system. Three of the most luminous and ancient
sky markers — **the Pleiades, Aldebaran, and Orion's Belt** — are all
in adjacent mansions here. This is why the autumn-into-winter sky
felt to ancient observers like the most stable, most navigationally
useful part of the celestial sphere.

**Zī 觜 (Turtle Beak)** is the narrowest mansion in the system, at
about 3°. It is the head of Orion. The mansion's narrowness is one of
the reasons mansion-based timing is sensitive to ayanamsa calibration
— a few minutes of arc error in the sidereal correction can shift the
Moon out of Zī entirely, while in wider mansions like the Well (27°)
the same error makes no difference.

### Vermillion Bird Palace (South, Summer, Fire)

| #  | Chinese | Pinyin | English        | Animal    | Reference Star                | Width  |
|----|---------|--------|----------------|-----------|-------------------------------|--------|
| 22 | 井      | Jǐng   | Well           | Tapir     | Tejat (μ Gem area)            | 27°    |
| 23 | 鬼      | Guǐ    | Ghost          | Sheep     | Asellus Borealis (γ Cnc)      | 5°     |
| 24 | 柳      | Liǔ    | Willow         | Muntjac   | Alterf (λ Hya area)           | 15°    |
| 25 | 星      | Xīng   | Star           | Horse     | Alphard (α Hya)               | 8°     |
| 26 | 張      | Zhāng  | Extended Net   | Deer      | ν Hya                         | 18°    |
| 27 | 翼      | Yì     | Wings          | Snake     | α Crt                         | 18°    |
| 28 | 軫      | Zhěn   | Chariot        | Worm      | Gienah Corvi (γ Crv)          | 5°     |

The Vermillion Bird is the bird-figure laid across the summer sky.
The Well is widest (27°), the Ghost (the Beehive Cluster / Praesepe
region) is narrow and traditionally inauspicious — its name 鬼 means
"ghost" or "demon" and the cluster of faint stars was anciently read
as a chariot of spirits. The Chariot (Zhěn) closes the cycle, and the
next mansion in the ecliptic wrap is Jiǎo (Horn) — the dragon
reappears.

## Sidereal vs. Tropical — the Lahiri Correction

This is the single most important technical point about the Stellar
Layer.

The twenty-eight mansion boundaries are **sidereal**. They are
anchored to actual reference stars and stay locked to those stars
(modulo the very slow proper motions of the stars themselves, which
are negligible on the timescales the Astrolabium handles). The mansions
do not move with the precession of the equinoxes.

The modern Western tropical zodiac (the one used in popular astrology
and in standard ephemeris output from packages like `ephem`) is
**tropical**. It is anchored to the **vernal equinox** — the point
where the Sun crosses the celestial equator northward at the start of
northern spring. Because the Earth's rotational axis precesses with a
period of ~26,000 years, the vernal equinox drifts backward through
the constellations at about 50.29 arcseconds per Julian year. Two
thousand years ago the vernal equinox was in Aries; today it is in
Pisces, drifting toward Aquarius.

The angular offset between the tropical and sidereal zero points is
called the **ayanamsa** (from Sanskrit अयनांश, "portion of the
solstice"). There are several conventional definitions; the one used
by the Astrolabium engine is the **Lahiri (Chitrapaksha) ayanamsa**,
the standard of the Indian National Calendar Reform Committee since
1955. At J2000.0 the Lahiri ayanamsa is 23.8519°; it increases by
~50.29″/year due to general precession.

[MATHEMATICAL FACT — astronomical constant. The Lahiri value is
defined to make the sidereal longitude of Spica exactly 180° (the
star anchors mansion 1, Jiǎo, in the Chinese system and the boundary
of Chitra nakshatra in the Indian one). The linear approximation in
`stellar.py` is valid to less than one arcminute over centuries.]

In `astrolabium/src/engine/stellar.py`, the function
`_lahiri_ayanamsa(year)` returns the offset in degrees, and
`_ecliptic_longitude_of_body(body, dt, sidereal=True)` applies it by
default to every body position before mansion lookup:

```python
lon_deg = (tropical_longitude_from_ephem - ayanamsa) % 360.0
```

The `sidereal=False` flag exists for debugging and for users who
explicitly want tropical longitudes. **All mansion lookups must use
sidereal longitudes.** Using tropical longitudes against the mansion
table will misplace every body by ~24° (about two mansions) in the
current epoch, and the error grows with time.

## How the engine positions bodies in mansions

The Stellar Layer reports the mansion currently occupied by:

- **the Sun** — `get_solar_mansion(dt)` — moves through one mansion in
  about thirteen days
- **the Moon** — `get_lunar_mansion(dt)` — moves through one mansion
  in about a day (27.32 days for the full sidereal month / 28)
- **the five visible planets** — `get_planetary_mansions(dt)` —
  Mercury, Venus, Mars, Jupiter, Saturn (the classical "wandering
  stars"), each independently. Mercury can race through several
  mansions in a month; Saturn lingers in one mansion for over a year.

```python
from astrolabium.engine import stellar

state = stellar.get_stellar_state(dt)
# Returns: sun_mansion, lunar_mansion, planet_mansions, palace_summary
```

The composition follows a strict pattern: get the body's tropical
ecliptic longitude from `ephem`, subtract the Lahiri ayanamsa for the
year, take the result modulo 360°, and look up which mansion's start
≤ longitude < end. The Wall mansion wraps the 0° boundary and is
handled with an explicit special case in `get_mansion_by_longitude`.

The position **does not depend on the observer's latitude or
longitude on Earth**. Mansion occupancy is a geocentric / heliocentric
fact about the solar system, the same for every observer at every
location simultaneously. (This is opposite to the Divine Hours, the
Organ Clock, and LGBF, all of which require `(lat, lon, tz)` because
they are local-solar-position-dependent.)

Outer planets (Uranus, Neptune, Pluto) are deliberately not included
in `get_planetary_mansions`. The classical Chinese system was built
around the five visible planets; adding the outers would be a
modern overlay, not a tradition-faithful reading. They can be added
on request, but the default is the five-planet canon.

## The Saga Dawa connection — Root Mansion as Buddha-month

The Stellar Layer was added in Sprint A of the "Stellar Sprint"
specifically because of the **Saga Dawa** lunar month in the Tibetan
calendar. Saga Dawa is the fourth Tibetan lunar month — typically May
or June in the Gregorian calendar — during which the Buddha's birth,
enlightenment, and parinirvāṇa are all commemorated on the full moon.
The month's name itself comes from the Tibetan rendering of *Vaiśākha*,
the corresponding month in the Indian luni-solar calendar.

The Full Moon of Saga Dawa falls in or very near the **Dī 氐 mansion
— the Root**. In Tibetan Buddhist astrological reading, the merit of
any virtuous act performed during Saga Dawa multiplies (sources say
ten- to ten-thousand-fold; the *Padma Karpo* tradition gives a
hundred-thousand-fold multiplier specifically on the Full Moon of
Saga Dawa). The month carries the quality of accumulated merit
amplified.

Reading the same astronomical fact through the Chinese system: the
Full Moon falls in the dragon's root, the seat of breath, the cavity
where the earth-currents resonate. The dragon awakens. Spring is
giving way to early summer; the agricultural cycle has rooted and is
about to expand upward into the Vermillion Bird's heat.

The two readings are not the same teaching, but they are **the same
astronomical anchor read by two traditions**, and the Astrolabium
exposes both. When the Moon is in Dī, the Stellar Layer returns the
mansion data with its `notes` field intact, and the orchestrator can
elaborate the Saga Dawa overlay for users in a Buddhist practice
context.

[SOURCE: Tibetan Buddhism — Saga Dawa observance documented across
the Kagyu, Nyingma, Gelug, and Sakya lineages. The specific
correspondence to mansion Dī is [ANALYTICAL CONTRIBUTION] from the
source PDF that motivated this layer's addition.]

## Cross-traditions — Indian nakshatras, Tibetan reckoning

Three related lunar-mansion systems exist across Asia. The engine
uses the **Chinese** definitions by default. The other two are noted
here for orientation, not for invocation.

**Indian Nakshatras (नक्षत्र)**. The *Vedāṅga Jyotiṣa* and later
*Sūrya Siddhānta* describe a system of **27 nakshatras**, each 13°20′
wide (360° / 27, equal arcs), anchored to reference stars. A
secondary 28-nakshatra variant inserts **Abhijit** (Vega) between
Uttarāṣāḍhā and Śravaṇa. The reference stars partly overlap with the
Chinese mansions — Spica anchors Citra (the Indian counterpart of
Jiǎo), Aldebaran anchors Rohiṇī (counterpart of Bì 畢), Antares
anchors Jyeṣṭhā (counterpart of Xīn 心) — but **the boundaries are
equal arcs in the Indian system and unequal in the Chinese**, so
mansion identity for a given longitude can differ between the two
systems even when the reference stars match. [SOURCE: classical
Indian astronomy / Jyotiṣa.]

**Tibetan Gyukar (རྒྱུ་སྐར་)**. The Tibetan astronomical tradition
uses the Indian 27-mansion system as inherited through the *Kālacakra
Tantra*, with its own Tibetan names for each mansion (e.g., *Tha-skar*
for Aśvinī, *Bra-nye* for Bharaṇī). The Saga Dawa correspondence
above is given in this tradition's terms when discussed in Tibetan
Buddhist contexts. [SOURCE: Tibetan Kālacakra astronomy.]

**Arabic/Islamic Manāzil al-Qamar (منازل القمر)**. The "lunar
houses" of medieval Islamic astronomy are a 28-mansion system,
ultimately derived from the Indian tradition through Persian
intermediaries, but with significant changes in reference stars and
in talismanic interpretation. Cornelius Agrippa (*De Occulta
Philosophia*, 1531) carries the system into Western Renaissance
magic. The Astrolabium does not invoke this tradition. [SOURCE:
medieval Islamic astronomy; Agrippa for the Western reception.]

When a user asks about "lunar mansions" without specifying which
tradition, **Meridian defaults to the Chinese 28-mansion system that
the engine actually computes**, and notes the existence of the related
traditions only if asked.

## What never to do

- **Never read a tropical zodiac sign as if it were a mansion.** "The
  Moon is in Taurus" is a tropical claim. "The Moon is in Bì (Net)"
  is a sidereal claim about Chinese mansion 19, which currently
  contains Aldebaran. The two are different categories of statement.
  Converting between them requires the Lahiri ayanamsa.

- **Never report a body's mansion from a tropical longitude.** If
  `sidereal=False` is passed to `_ecliptic_longitude_of_body`, the
  returned longitude must not be looked up in the mansion table. The
  function's docstring is explicit; the API surface (the
  `get_*_mansion` functions) defaults to sidereal and should not be
  bypassed without intent.

- **Never claim the system predicts events.** The mansion of the Sun
  or the Moon at a given moment **situates** the moment within a
  celestial reference frame — it tells you where in the stellar
  geography the moment falls. It does not forecast outcomes. Classical
  Chinese mansion-based augury existed (and is documented in the
  Hàn-era *Wǔxíng Zhì* treatises), but the Astrolabium does not
  perform it. The engine reports position; interpretation is the
  practitioner's.

- **Never confuse the Southern Dipper (Dǒu 斗, mansion 8) with the
  Northern Dipper (Běi Dǒu 北斗, the Big Dipper / Ursa Major).** The
  Northern Dipper is circumpolar and not on the ecliptic; it is not
  one of the twenty-eight mansions. The Southern Dipper is in
  Sagittarius and is mansion 8 of the Black Tortoise palace.

- **Never quote mansion widths as if they were exact.** The widths
  given in `lunar_mansions.json` follow the classical Chinese canon
  (Han through Ming sources) and round to whole degrees. Modern
  astronomical sources occasionally give slightly different boundaries
  (the *Kāishùyé* spec, the Qing-era Xīyù system, etc., differ
  by fractions of a degree). The engine uses the classical values as
  the canonical convention; precise modern boundaries are not
  authoritative for this system.

- **Never report a Sun mansion without noting that the Sun moves
  through mansions much faster than perception suggests.** Twelve to
  fourteen days per mansion is fast on a human ritual-calendar
  timescale. The Sun's mansion changes within a single lunar month;
  the Moon's mansion changes within a single day. Both are normal.

## Cross-references

- `.claude/rules/temporal-bodies.md` — where the Stellar Layer sits
  relative to the Soul, Astral, and Gross bodies (it is a separate
  layer, not part of the four-body schema; it complements them)
- `.claude/rules/trigram-laws.md` — the 6+2 lunar architecture
  governing the Soul layer; the lunar mansions are an independent
  parameterization of the same lunar motion read through stellar
  rather than phase-trigram coordinates
- `.claude/rules/ling-gui-ba-fa.md` — the Astral layer; LGBF and the
  Stellar Layer operate on completely independent computational
  substrates and may be cross-read for compound timing
- `.claude/rules/divine-hours.md` — local solar time; mansion lookup
  is geocentric and does not require location, unlike Divine Hours
- `astrolabium/data/lunar_mansions.json` — the canonical table
- `astrolabium/src/engine/stellar.py` — the computation engine,
  including Lahiri ayanamsa, body position lookup, and palace
  decoration
- `docs/specs/operators_manual.md` — Part 1, user-facing Stellar Layer
  presentation
- `docs/specs/guidebook.md` — Part 2, technical reference and worked
  examples for mansion positioning
