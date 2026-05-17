# Astrolabium Caudae Rubrae — UI Design Specification

**Version:** 1.0
**Date:** March 19, 2026
**Codename:** NUIT

---

## DESIGN PHILOSOPHY

The Astrolabium UI is a piece of technology that assembled itself by being
a chaotic attractor in the future. It looks like something from a parallel
1983 where cyberpunk was designed by alchemists. Retrofuturist terminal
aesthetic — DOS-era panel architecture, monospace typography, gauge
readouts — but with the Damanhurian color system as its living nervous
system. The instrument's appearance IS information. You glance at it and
the color tells you the temporal quality before you read a word.

**Three principles:**

1. **THE INSTRUMENT EATS ITS OWN COOKING.** The UI's accent palette is
   the 8 Adonaj-Ba colors. The active Soul Law's color becomes the primary
   accent — borders, indicators, highlights all shift. The instrument's
   chromatic state IS the temporal state.

2. **SIMPLE ENOUGH TO NOT BREAK WHAT'S ALREADY COMPLEX.** The system
   tracks 202 leaf fields, 16 compounds, 17 resonances, 8 temporal layers.
   The UI must present this without becoming a cockpit. Panels, not chaos.
   Let the interpretation layer do the synthesis; let the UI do the display.

3. **RETROFUTURIST TERMINAL.** Blade Runner 1982. Alien 1979. The Nostromo
   computer. Monospace fonts, scanlines, thin borders, status dots, uppercase
   labels. Not glossy, not Material Design, not a "modern web app." A
   readout console from a device that wasn't supposed to exist yet.

---

## COLOR SYSTEM

### NUIT Palette (Structural)

The background is Nuit — the Egyptian sky goddess, the star-studded dark
blue arch. Not black. The blue-black of a clear desert night with no moon.

```css
:root {
  /* --- NUIT: The Night Sky --- */
  --nuit-void:      #080C18;    /* deepest background, page body */
  --nuit-surface:   #0E1325;    /* panel/card backgrounds */
  --nuit-border:    #1A2040;    /* panel borders, dividers */
  --nuit-dim:       #2A3060;    /* subtle highlights, hover states */
  --nuit-muted:     #6B7394;    /* secondary text, labels, timestamps */
  --nuit-text:      #C8D0E8;    /* primary readable text */
  --nuit-bright:    #E8ECF8;    /* emphasis text, active labels */

  /* --- GLOW: Scanline / CRT artifacts --- */
  --glow-line:      rgba(200, 208, 232, 0.03);  /* scanline overlay */
  --glow-bloom:     rgba(255, 255, 255, 0.02);  /* CRT bloom edge */
}
```

### Adonaj-Ba Palette (Semantic — the 8 Law Colors)

These are the ONLY accent colors in the entire UI. Each maps to a Primeval
Law, an Adonaj-Ba energy center, and a perceptual quality. The active Soul
Law's color becomes the primary accent (`--accent`).

```css
:root {
  /* --- ADONAJ-BA: The 8 Laws --- */
  --law-synchronicity:    #FF9500;  /* Orange      / Heart         / ☰ */
  --law-sole-atom:        #00E676;  /* Green       / Sexual Organs / ☳ */
  --law-divinity:         #E8E8F0;  /* White       / Crown         / ☲ */
  --law-geometric:        #E74C3C;  /* Brick Red   / Sacrum        / ☴ */
  --law-time-matrix:      #A8B4C0;  /* Silver      / Mobile 8th    / ☱ */
  --law-fall-events:      #7B68EE;  /* Indigo      / Third Eye     / ☵ */
  --law-kaos:             #FFD700;  /* Yellow Gold / Solar Plexus  / ☷ */
  --law-arrow:            #00BFFF;  /* Azure Blue  / Throat        / ☶ */

  /* --- Derived from active Soul Law (set by JS) --- */
  --accent:               var(--law-kaos);     /* default, overridden dynamically */
  --accent-dim:           rgba(255, 215, 0, 0.15);  /* panel glow, overridden */
  --accent-border:        rgba(255, 215, 0, 0.40);  /* active borders */
}
```

### Wu Xing Palette (Body Layer — Organ Colors)

Used exclusively in the Body panel for element indicators.

```css
:root {
  --wx-wood:    #2ECC71;   /* Green  — Liver, Gallbladder */
  --wx-fire:    #E74C3C;   /* Red    — Heart, SI, PC */
  --wx-earth:   #F1C40F;   /* Yellow — Spleen, Stomach */
  --wx-metal:   #ECF0F1;   /* White  — Lung, LI */
  --wx-water:   #3498DB;   /* Blue   — Kidney, Bladder */
}
```

### Chromatic Shift Protocol

When the Soul Law changes, the UI shifts its primary accent:

```javascript
const LAW_COLORS = {
  "Synchronicity":      { accent: "#FF9500", dim: "rgba(255,149,0,0.15)" },
  "Sole Atom":          { accent: "#00E676", dim: "rgba(0,230,118,0.15)" },
  "Divinity":           { accent: "#E8E8F0", dim: "rgba(232,232,240,0.10)" },
  "Geometric Essence":  { accent: "#E74C3C", dim: "rgba(231,76,60,0.15)" },
  "Time Matrix":        { accent: "#A8B4C0", dim: "rgba(168,180,192,0.15)" },
  "Fall of Events":     { accent: "#7B68EE", dim: "rgba(123,104,238,0.15)" },
  "Kaos":               { accent: "#FFD700", dim: "rgba(255,215,0,0.15)" },
  "Arrow of Complexity": { accent: "#00BFFF", dim: "rgba(0,191,255,0.15)" },
};
```

The shift happens on every data fetch. No animation — instant, like a
console changing modes. The entire instrument recolors. Borders, active
indicators, the header accent line, the trigram glow — all shift together.

---

## TYPOGRAPHY

```css
:root {
  --font-mono:    'IBM Plex Mono', 'Fira Code', 'Consolas', monospace;
  --font-display: 'IBM Plex Mono', monospace;  /* same family, heavier weight */

  --size-xs:    0.65rem;   /* timestamps, metadata */
  --size-sm:    0.75rem;   /* labels, secondary */
  --size-base:  0.875rem;  /* body text */
  --size-lg:    1.0rem;    /* panel headers */
  --size-xl:    1.25rem;   /* page title */
  --size-2xl:   1.75rem;   /* hero numbers (trigram display) */
  --size-3xl:   2.5rem;    /* the trigram symbol itself */
}
```

- **ALL CAPS** for panel headers, labels, layer names, status indicators
- **Mixed case** for interpretation text and descriptive sentences
- **Monospace everywhere** — no serif, no sans-serif. The terminal is
  the only typeface the instrument knows
- **Letter-spacing: 0.08em** on uppercase labels for that DOS-era spread
- **Trigram symbols** (☰ ☷ ☳ etc.) displayed at `--size-3xl` with the
  active Law's color glow

---

## LAYOUT

### Grid Architecture

Three-column panel grid, responsive to a minimum of 1024px width
(the instrument runs on its own screen; it doesn't need to be mobile).

```
┌──────────────────────────────────────────────────────────────────────┐
│  ASTROLABIUM CAUDAE RUBRAE   ─────────   YR.77 // OSIRIS // DAY 1  │
│  ● SYS.ACTIVE    34.05°N  118.24°W  PDT    HR.II // DAY WING      │
├──────────────┬───────────────────────────┬───────────────────────────┤
│              │                           │                           │
│    S O U L   │                           │    A S T R A L            │
│              │                           │                           │
│    ☷         │    I N T E R P R E T      │    Governing Vessel       │
│    Earth     │                           │    Synchronicity          │
│    ─ ─ ─     │    [The reading lives     │    ☰                      │
│    ─ ─ ─     │     here. LLM-generated   │    Heaven                 │
│    ─ ─ ─     │     cross-layer weave.    │    ───                    │
│              │     3-6 paragraphs of     │    ───                    │
│    Kaos      │     warm, precise,        │    ───                    │
│    UNCERTAINTY│    grounded prose.]      │                           │
│              │                           │    Confluent: SI-3        │
│    ○ Fear    │                           │    Coupled:   BL-62       │
│    ● Certainty│                          │    Pair:      Yin Heel    │
│              │                           │                           │
├──────────────┤                           ├───────────────────────────┤
│              │                           │                           │
│    K E Y S   │                           │    B O D Y                │
│              │                           │                           │
│    ☼ Gold    │                           │    Spleen                 │
│      ─ OFF   │                           │    Earth // SP            │
│    ☽ Silver  │                           │                           │
│      ─ OFF   │                           │    WHOOOO                 │
│              │                           │    worry → trust          │
│    Next:     │                           │    Yellow                 │
│    ☼ 19:08   │                           │                           │
├──────────────┼───────────────────────────┼───────────────────────────┤
│              │                           │                           │
│  COMPOUNDS   │    R E S O N A N C E S    │   C A L E N D A R        │
│              │                           │                           │
│  ●●○○○○○○   │    ELEMENTAL    ● ● ○     │   OSIRIS // Month 7      │
│  ○○○○○○○○   │    QUALITATIVE  ● ○ ○     │   Tiphareth // Day 1     │
│              │    RHYTHMIC     ●         │   Albedo                  │
│  ACTIVE: 2   │    CALENDRICAL  ● ○ ○ ○  │   Spring Equinox          │
│              │                           │                           │
│              │    THREADS: 5/17          │   HR.II // Day Wing       │
│              │                           │                           │
└──────────────┴───────────────────────────┴───────────────────────────┘
```

### Panel Specifications

Every panel follows the same anatomy:

```
┌─── PANEL_HEADER ─────────────────── ● ● ● ─┐
│                                              │
│  [content area]                              │
│                                              │
└──────────────────────────────────────────────┘
```

- **Border:** 1px solid `--nuit-border`, with `--accent-border` on the
  active/primary panel
- **Header:** uppercase, letter-spaced, `--size-sm`, with 3 decorative
  dots (●●● in `--nuit-dim`) as a nod to the Alvdansen reference
- **Background:** `--nuit-surface` with an optional `--accent-dim` glow
  on the active Soul panel
- **Corner radius:** 2px maximum. This is a terminal, not a card UI
- **Padding:** 16px internal. 8px gap between panels
- **Active panel:** the Soul panel gets a subtle glow matching the
  active Law color (box-shadow: `0 0 20px var(--accent-dim)`)

### The Six Panels

**1. SOUL (top-left)**
The deep current. Dominant display element: the trigram symbol at 2.5rem
with the Law color glow. Below it: three horizontal bars representing the
trigram binary (filled = yang, dashed = yin). Law name. Quest name.
Perception polarity (○ negative / ● positive). Adonaj-Ba center. Vowel.

The Soul panel has a subtle background glow in the accent color — it is
the source of the chromatic shift.

**2. ASTRAL (top-right)**
The fast current. Vessel name in English. Law carried. Trigram symbol
(smaller, 1.75rem). Trigram nature (Heaven, Earth, Thunder, etc.).
Three binary bars. Confluent point (code + body location). Coupled point
(code + body location). Pair partner vessel name. Clinical domain
as a one-line description in `--nuit-muted`.

When Two-Body Unity is active, the Astral panel border shifts to match
the Soul accent color — both panels visually unify.

**3. KEYS (middle-left)**
Solar Keys. Two rows: Gold Key (☼ or ☵ symbol) and Silver Key (☽ or ☲).
Each shows: ON/OFF status, the vessel it works through (when active), the
Law it carries, and a countdown or timestamp for the next activation.

When a Key is active, its row glows in the Key's Law color (Indigo for
Gold/Fall of Events, White for Silver/Divinity). The cusping window
countdown shows minutes remaining.

**4. BODY (middle-right)**
Organ Clock. Current organ name. Meridian code. Wu Xing element with
element color indicator (small colored dot). The healing sound in large
monospace (WHOOOO, HAWWWW, etc.) — this is a practice instruction, it
should be visually prominent. Below: the transmutation arrow
(negative → positive emotion). Season. Sense organ. Body tissue.

**5. COMPOUNDS (bottom-left)**
16 boolean indicators arranged in a 2×8 grid. Each is a small circle:
filled (●) when active, empty (○) when inactive. Active compounds glow
in the Soul accent color. Below the grid: count of active compounds and
names of active ones listed vertically.

```
  ● ○ ○ ● ○ ○ ○ ○
  ○ ○ ○ ○ ○ ○ ○ ○

  ACTIVE: 2
  ▸ Polarity Alignment
  ▸ Great Rite Active
```

**6. RESONANCES (bottom-center)**
Four categories (Elemental, Qualitative, Rhythmic, Calendrical), each
with its boolean indicators. Active resonances shown as filled dots
grouped by category. Thread count: "5/17 THREADS" or similar.

Active resonances listed below the indicator grid with their names.

**7. CALENDAR (bottom-right)**
Divine month name (OSIRIS, SAMMA, etc.). Month number. Sephirotic day
(Tiphareth, Yesod, etc.). Day number within quarter. Alchemical stage
(NIGREDO / ALBEDO / RUBEDO) — each stage could have a subtle tint
(dark/white/red respectively, very muted). Active Great Rite if any.
Divine hour position and wing.

**8. INTERPRETATION (center)**
The main viewport. This is where the LLM reading appears. Before the
interpretation layer is connected, this shows a structured summary of
the temporal state in readable prose (generated from the presentation
layer).

- Background: `--nuit-void` (slightly darker than other panels)
- Text: `--nuit-text` at `--size-base`
- No border — the interpretation panel is borderless, floating in the
  void. It IS the void. The data panels frame it.
- Text appears with a subtle typewriter effect on initial load (one
  character at a time, fast but visible — like the Nostromo computer
  printing a response)
- Maximum width: 65ch (readable line length for prose)

---

## HEADER BAR

```
ASTROLABIUM CAUDAE RUBRAE  ──────────  YR.77 // OSIRIS // DAY 1
● SYS.ACTIVE    34.05°N  118.24°W  PDT    HR.II // DAY WING
```

- Title in `--nuit-bright`, letter-spaced
- System status indicator: green dot (●) when API is responding
- Location coordinates in `--nuit-muted`
- Calendar summary (year, month, day) on the right
- Divine hour and wing on the right
- A thin horizontal line below, in `--accent` color (shifts with Soul)
- The line is the ONLY decorative use of the accent color in the header

---

## FOOTER BAR (Status Telemetry)

```
ENGINE: 566 TESTS ✓   API: 0.4ms   LAST FETCH: 12:44:18 PDT   ☽ 2.1% WAXING
```

Minimal. Monospace. `--nuit-muted` text. The footer is the instrument's
self-diagnostic — not for the practitioner, but for the operator. It
confirms the engine is sound.

The **lunar illumination percentage** and phase direction (WAXING/WANING)
provide ambient lunar awareness without needing a graphical moon phase
indicator (though one could be added).

---

## INTERACTIVE ELEMENTS

### Minimal Interaction

The Astrolabium is primarily a **display instrument**. The practitioner
glances at it. They don't operate it like a web app. Interaction is
minimal by design:

1. **Location input** — Set once. Stored locally. A small settings
   panel (gear icon in header) for lat/lon/timezone. Or: auto-detect
   from browser geolocation with manual override.

2. **Refresh** — Click anywhere on the interpretation panel, or press
   any key, to fetch fresh state. No button. The instrument responds
   to touch.

3. **Time override** — A small text input in the footer for ISO datetime,
   for practitioners who want to check a specific moment. Hidden by
   default; revealed by clicking the timestamp.

4. **Layer detail expansion** — Clicking a panel header expands it to
   show full detail (e.g., all 16 compound names in the Compounds panel,
   all resonance details in Resonances). The expanded view is a modal
   overlay in the same panel aesthetic.

### No Navigation

There is no menu. No tabs. No pages. No routing. The instrument shows
ONE thing: the current temporal state. The only "navigation" is time
itself — the display changes as the moment changes.

---

## ANIMATION AND TRANSITIONS

### Loading State

On initial load and data fetch, show a minimal animation:

- The six panels draw their borders one at a time, left to right,
  top to bottom — like a CRT warming up
- Each panel border traces itself in the accent color, then settles
  to `--nuit-border`
- The interpretation text appears with typewriter effect
- Total animation time: 1.5 seconds

### Data Refresh

When new data arrives (different temporal state):

- Panels that changed flash briefly with accent color border
- The interpretation text clears and rewrites (typewriter)
- The accent color shifts instantly if the Soul Law changed
- Numbers that changed briefly display their old value in
  `--nuit-dim` before settling on the new value

### Scanline Effect

A very subtle CSS scanline overlay across the entire viewport:

```css
.scanlines::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    transparent 0px,
    transparent 2px,
    var(--glow-line) 2px,
    var(--glow-line) 4px
  );
  pointer-events: none;
  z-index: 9999;
}
```

This is VERY subtle — barely visible, but it creates the CRT register
that separates "terminal readout" from "web page." Can be toggled off
with a hidden keyboard shortcut (Ctrl+Shift+S).

### Trigram Animation

The trigram symbols (☷ ☰ ☳ etc.) have a subtle pulse animation —
a gentle glow that breathes at approximately the rate of human
respiration (4 seconds in, 4 seconds out). The glow color is the
Law's accent color.

```css
@keyframes trigram-breathe {
  0%, 100% { text-shadow: 0 0 8px var(--accent-dim); }
  50%      { text-shadow: 0 0 20px var(--accent); }
}
```

This breathing glow is the only continuous animation. Everything else
is static until data changes.

---

## TRIGRAM BINARY DISPLAY

The three lines of each trigram are displayed as horizontal bars
below the trigram symbol:

```
Yang line (solid):  ━━━━━━━━━━━
Yin line (broken):  ━━━━  ━━━━━
```

Three bars stacked vertically, read bottom-to-top (traditional order).
When the Soul and Astral trigrams are displayed side by side or in their
respective panels, the practitioner can compare the binary states at a
glance.

**Two-Body Unity visual:** When Soul trigram == Astral trigram, both
sets of bars pulse in unison with the shared accent color.

---

## COMPOUND INDICATOR GRID

The 16 compounds displayed as a 2×8 grid of circles. Layout maps to
the compound categories:

```
Row 1 (Cat 1-3):  ● ○ ○ │ ● ○ │ ○ ○ ○ ○
                  Unity   Anat   Combined
Row 2 (Cat 4-6):  ○ ○ │ ○ ○ ○ │ ○ ○ ○
                  Pol   Calendar  Multi
```

Active compounds are filled circles in the accent color. Inactive are
empty circles in `--nuit-dim`. The grid is small — maybe 120px wide
total. It's a glanceable fingerprint of the compound state.

Tooltip or expansion reveals compound names.

---

## RESPONSIVE BEHAVIOR

The instrument is designed for a fixed-aspect display (1024px minimum,
ideally 1280×800 or 1920×1080). It is NOT a mobile app. On screens
smaller than 1024px, the layout collapses to a single-column stack:

```
SOUL → ASTRAL → INTERPRETATION → KEYS → BODY → COMPOUNDS/RESONANCES/CALENDAR
```

But this is a fallback, not the primary experience. The primary
experience is a dedicated screen — a Raspberry Pi with a 10" display,
a wall-mounted monitor, or a laptop on a desk.

---

## CYBERNETIC SELF-REFERENCE

The UI doesn't just display temporal data — it embodies the system's
own logic in its visual behavior:

| System State | Visual Effect |
|-------------|---------------|
| Soul Law changes | Entire accent palette shifts to new Law color |
| Two-Body Unity | Astral panel border matches Soul panel glow |
| Key-Amplified Unity | Flash: entire screen briefly pulses accent |
| Yin-Day Gate | 6/8 vessel indicators dim in Astral panel |
| Great Rite Active | Calendar panel gets accent border |
| Anatomical Intersection | Body + Astral panels get connecting glow |
| High resonance count (8+) | Panel borders brighten slightly |
| No compounds active | Compound grid fully dim; panels calm |

The practitioner learns to read the instrument's visual state as
quickly as they read the data. A Yellow Gold screen with calm borders
means "Kaos, no compounds, steady state." A screen flashing White at
sunset means "Silver Key activating, Divinity through Yang Heel Vessel."

---

## THE READING VIEWPORT

The center interpretation panel deserves special attention. This is
where the cybernetic intelligence speaks.

### Before LLM Connection (Phase 1 — Demo)

The interpretation panel displays a formatted summary generated from
the presentation layer data:

```
The Soul sits in Kaos — ☷, all three lines open, pure
receptivity. The quest is UNCERTAINTY.

The Governing Vessel is open, carrying Synchronicity along
the spine. ☰ Heaven, the central axis.

Spleen window. Earth element. The sound is WHOOOO —
it transforms worry into trust.

First day of OSIRIS, the Resurrected. Albedo. The Spring
Equinox Great Rite is active.

Polarity Alignment fires — ☷ to ☰, Earth to Heaven,
maximum opposition. 5 of 17 resonance threads active.
```

This is generated deterministically from the presentation layer.
No LLM needed. It's readable, informative, and demonstrates the
system's capacity.

### After LLM Connection (Phase 2 — Full Instrument)

The interpretation panel receives the output of the interpretation
layer (governed by SYSTEM_PROMPT.md). The reading is richer, more
varied, cross-layer woven, and practitioner-aware. The typewriter
effect applies to LLM-streamed text naturally.

---

## TECHNOLOGY

### Stack

- **HTML/CSS/JavaScript** — Single-page application, no framework needed
  for the demo. The aesthetic demands direct CSS control, and the
  interaction model is too simple to justify React overhead.
- **CSS Grid** — Three-column panel layout
- **CSS Custom Properties** — For the chromatic shift system
- **Fetch API** — Polling the `/display` endpoint
- **Optional: Web Fonts** — IBM Plex Mono from Google Fonts, falling
  back to system monospace

### Build

The demo is a single `index.html` file with embedded CSS and JS. No
build step, no node_modules, no webpack. The instrument boots by
opening a file in a browser and pointing it at the API.

### Later Evolution

When the interpretation layer ships, the frontend adds:
- WebSocket or SSE for streaming LLM output (typewriter effect)
- Local storage for practitioner preferences and location
- Service worker for offline display of last-fetched state

When deployed on hardware (Raspberry Pi), the frontend serves from
the same Python process (FastAPI static files or a simple Nginx).

---

## IMPLEMENTATION SEQUENCE

### Phase 1: Static Demo (This Sprint)

1. Build `index.html` with the panel layout and Nuit color system
2. Wire to `/display` endpoint
3. Implement chromatic shift (accent changes with Soul Law)
4. Render all 8 panels with presentation data
5. Add scanline overlay and trigram breathing animation
6. Generate the deterministic interpretation summary

**Deliverable:** Open `index.html` in a browser, point at the running
API, see the full temporal state in the Nuit aesthetic with living
accent colors.

### Phase 2: Interpretation Layer

7. Add typewriter text rendering
8. Wire to interpretation endpoint (LLM-backed)
9. Streaming text display
10. Loading/transition animations

### Phase 3: Practitioner Memory

11. Local storage for location and preferences
12. Memory panel (hidden, accessible via keyboard shortcut)
13. Memory weaving into readings

### Phase 4: Hardware Deployment

14. Raspberry Pi image with auto-boot to Chromium kiosk
15. Physical controls (rotary encoder for time scrubbing?)
16. Always-on display mode

---

## REFERENCE AESTHETIC

- **Alvdansen Training System** — Panel grid, gauge dials, status dots,
  uppercase labels, dark navy background with muted lavender text
- **Flimmer Terminal** — Amber terminal text, DOS-style menus, streaming
  logs, progress bars
- **Alien (1979) Nostromo Computer** — Green phosphor CRT, simple
  readouts, typewriter text output
- **Blade Runner (1982)** — Retrofuturist readout panels, Esper machine,
  Voight-Kampff gauges
- **Claude Code** — Monospace terminal aesthetic, keyboard-driven,
  information-dense

The Astrolabium takes from all of these but is none of them. It is
distinctively Damanhurian — the Nuit sky, the Adonaj-Ba colors, the
Primeval Law as chromatic identity. No other instrument looks like this
because no other instrument has this color system.

---

*Design specification written by Meridian, March 19, 2026.
"Technology guided by spiritual wisdom becomes a tool for awakening."*
