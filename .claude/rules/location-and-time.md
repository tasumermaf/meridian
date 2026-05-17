# Location and Time — The Non-Negotiable Constraint

> **This is the most important rule in the entire instrument.** If you
> get this wrong, every other answer the Astrolabium produces is
> meaningless. If you get this right, the rest works.

---

## The Rule

**Every hourly function requires location.** Latitude, longitude, and
timezone. There is **no civil clock** anywhere in this system.

The Divine Hours, the Organ Clock, the LGBF hourly branch, the Solar
Key cusping windows — every one of them derives from solar position at
the practitioner's actual horizon. A practitioner in Damanhur (Italy,
45°N) and a practitioner in Los Angeles (USA, 34°N) at the same
Gregorian instant receive different Astrolabium readings, because their
solar horizons differ. This is correct and load-bearing.

## Why this matters

The Earthly Branch "hour" 卯 (Mao, Large Intestine) is **not**
05:00–07:00 on a wall clock. It is *the second of four divisions of the
day wing, where the day wing is sunrise-to-sunset at the practitioner's
location*. On the equinox at Damanhur, that interval is approximately
177–182 minutes wide (we computed it). On the winter solstice in
Reykjavík, the entire day wing is about 4 hours wide, so each of the
four day "hours" is only an hour long. On the summer solstice in
Reykjavík, the same hour is over five hours wide. Both are correct,
because both are 1/4 of *that location's actual day*.

This is what "unequal hours" means. The hour adjusts to the local
relationship between earth and sun. The mechanical clock, by contrast,
imposed a constant on a non-constant phenomenon. The Astrolabium does
not impose. It reads.

The Gregorian/civil time hour answers the question: *what does
Greenwich say it is here?* It is a globally coordinated abstraction.
The Astrolabium hour answers the question: *what does the sun say it
is here, for this person, today?* These are different questions with
different answers.

## How to handle a user request

### Step 1 — try to auto-detect

If you are running inside the **web frontend** (`astrolabium/frontend/`),
the browser can prompt the user for geolocation. This gives latitude
and longitude. Timezone can be inferred from the browser via
`Intl.DateTimeFormat().resolvedOptions().timeZone`. **Use this.**

If you are running in a **Claude Code CLI** harness (the common case
for this repo), you cannot reliably auto-detect. The user's `tz` from
the shell environment may or may not reflect their actual location
(a traveler's laptop still reports the home timezone). **Do not guess
from system info alone.**

### Step 2 — ask explicitly

If you do not have a confirmed `(lat, lon, tz)` triple, ask. The
phrasing matters:

> "The Astrolabium needs your actual horizon to compute a reading.
> Could you tell me your latitude, longitude, and timezone? A common
> way to get these: search your location on a map and copy the
> coordinates. Timezones look like `Europe/Rome`, `America/Los_Angeles`,
> `Asia/Tokyo`."

If they give you a city name, you can look up the coordinates yourself
(or ask them to confirm). If they give you only a country, this is
usually not specific enough — Italy, for instance, spans about three
degrees of latitude, which moves sunrise by 15+ minutes depending on
season. Push for the city or the specific location.

### Step 3 — be clear about why

A user who has never thought about unequal hours may not understand
why a global timezone isn't enough. Take a moment to explain:

> "The Astrolabium reads from your actual sunrise and sunset, which
> depend on where you are on the planet, not just what timezone you're
> in. Two practitioners in the same timezone but at different latitudes
> get different readings, and the difference matters at the scale this
> instrument operates on — minutes of solar position, not hours of
> clock time."

Once. Do not repeat it after they've already heard you.

### Step 4 — store and reuse

Once a user has given you their location, hold it for the session.
Do not re-ask. If they say "give me my reading at sunrise tomorrow,"
compute against the location they already provided.

If they explicitly travel ("I'm in Tokyo now"), update the location.
A natural prompt is: "Are you still in Damanhur, or do you want me to
recompute for a different location?"

## What the engine accepts

```python
from astrolabium import calculate_complete_state
from datetime import datetime
import pytz

# A complete request:
state = calculate_complete_state(
    dt=datetime.now(pytz.timezone("Europe/Rome")),
    lat=45.4167,           # decimal degrees, north positive
    lon=7.7833,            # decimal degrees, east positive
    tz="Europe/Rome",      # IANA timezone name
)
```

**All four arguments are required.** The function will raise if any are
missing. This is not a bug — it is the system refusing to fake a
sacred-time answer from civil-time inputs.

## Common locations the user might give

| User says               | lat       | lon       | tz                  |
|-------------------------|-----------|-----------|---------------------|
| Damanhur (Vidracco, IT) | 45.4167   | 7.7833    | Europe/Rome         |
| Los Angeles, CA         | 34.0522   | -118.2437 | America/Los_Angeles |
| New York City           | 40.7128   | -74.0060  | America/New_York    |
| London                  | 51.5074   | -0.1278   | Europe/London       |
| Tokyo                   | 35.6762   | 139.6503  | Asia/Tokyo          |
| Sydney                  | -33.8688  | 151.2093  | Australia/Sydney    |
| Beijing                 | 39.9042   | 116.4074  | Asia/Shanghai       |
| Reykjavík               | 64.1466   | -21.9426  | Atlantic/Reykjavik  |

If they give a city not on this list, look it up. Coordinates to four
decimal places are more than enough precision for solar computations
(four decimal places = ~10m of resolution; sunrise moves on the scale
of seconds-per-kilometer of latitude shift).

## Polar edge cases

At latitudes above the Arctic Circle (~66.5°N) or below the Antarctic
Circle (~66.5°S), there are days each year with no sunrise or no
sunset. The solar engine raises specific errors for these. When this
happens:

- The Organ Clock and Divine Hours cannot be computed in the standard
  way (there is no "day wing" if the sun never sets).
- The Soul Layer (lunar phase) still works — the moon does not care
  about polar day or polar night.
- Tell the user this honestly. The instrument has well-defined behavior
  in temperate latitudes; the polar conditions are an edge that the
  Damanhurian source material does not address, and projecting answers
  there would be invention rather than reading.

## Time-of-day defaults

If a user asks for a reading and gives location but not time, default
to **right now** in their timezone. Make this explicit:

> "I'll read the current moment for Damanhur (2026-05-16, 22:47
> Europe/Rome). If you wanted a different instant, just say."

If they want a future or past moment, parse what they give and confirm
back:

> "Reading for tomorrow's sunrise at Damanhur — that's 2026-05-17,
> 05:42 Europe/Rome (sunrise computed for your location)."

## What never to do

- Never compute a "global" or "server time" reading. There is no such
  thing in this system.
- Never substitute a similar timezone for the user's actual one
  (Asia/Tokyo ≠ Asia/Shanghai, both are UTC+9 but one has DST history
  and they sit at different longitudes).
- Never round coordinates to whole degrees. Quarter-degree precision
  (≈27km) is the floor for reasonable solar work.
- Never ignore timezone. The astronomical engine works in UTC
  internally but accepts timezone-aware datetimes; if the user gives
  you 6 PM in their local time, the engine needs to know it's their
  6 PM, not yours.

## Privacy note

Location data is sensitive. Do not log it, do not persist it beyond
the current session, do not include it in any downstream call to
external services unless the user explicitly approves. If a user asks
about privacy, give them a straight answer: their coordinates exist
only in the Python process for the duration of their query, and the
Astrolabium does not phone home.
