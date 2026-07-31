"""
Astrolabium Caudae Rubrae — Readout Layer.

Correspondence-forward output. Data first, from the registers, in fixed
order. No prose. No interpretation. No narration.

WHY THIS MODULE EXISTS
----------------------
The interpretation layer was instructed to produce "a reading, not a data
report" — 3-6 paragraphs, rotating vocabulary, weaving threads. That
instruction reliably produced unreadable output and, worse, let values
drift: prose restates numbers, and restated numbers corrupt.

XR-001 (`rhombic/results/XR-001-externalization-pilot/RESULTS.md`,
released 2026-07-14) measured exactly this regime with format as the sole
variable: prose re-encoding corrupted 36.4% of numeric facts vs 9.4% for
typed state blocks at matched token budgets (McNemar p = 3.524e-21), with
the loss occurring at WRITE time. The readout is the Astrolabium eating
its own cooking: every correspondence is emitted as a typed line or a
table row, straight from the engine state, never as narrative.

ORDER OF PRESENTATION (fixed; do not reorder)
    1. WHEN / WHERE / SOLAR   — the frame
    2. VESSEL   (Astral)      — which Extraordinary Vessel is open
    3. LUNAR    (Soul)        — phase, trigram, Law
    4. ORGAN    (Gross)       — the organ clock
    5. HOUR                   — the Divine Hour and its protocol
    6. CALENDAR               — divine month, sephirotic day
    7. KEYS                   — Solar Keys, if cusping
    8. COMPOUNDS              — active only, named
    9. RESONANCES             — active only, named

Absent data prints as "—". Nothing is inferred, softened, or filled in.
"""

from typing import Optional

from .presentation import (
    MERIDIAN_NAMES,
    TRIGRAM_NATURE,
    VESSEL_ENGLISH,
    COMPOUND_DISPLAY,
    RESONANCE_DISPLAY,
)

DASH = "—"

# Compounds that are internal/raw duplicates of a presented compound.
# Suppressed from the readout so a single structural fact is reported once.
_COMPOUND_ALIASES = {"two_body_unity_raw"}

# ── precision ─────────────────────────────────────────────────────
#
# The operative unit of this instrument is the DIVINE HOUR, not the clock.
# Divine Hours are unequal — they stretch and contract with the season and
# the latitude — so a minute-exact clock time is a scheduling translation,
# not a temporal fact, and quoting it to the minute implies a precision the
# system does not carry. Coarse is therefore the default: clock times round
# to five minutes and are marked approximate; hour position is reported as
# a phrase rather than a decimal.
#
# Ask for EXACT only when the minute is genuinely load-bearing (pinning a
# boundary, comparing locations, debugging the engine).

COARSE = "coarse"
EXACT = "exact"
_ROUND_TO_MINUTES = 5


# ── helpers ───────────────────────────────────────────────────────


def _v(value) -> str:
    """Render a value, or an em dash when absent. Never invents."""
    if value is None or value == "":
        return DASH
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def _clock(iso: Optional[str], precision: str = EXACT) -> str:
    """
    HH:MM from an ISO timestamp; em dash if absent.

    In COARSE precision the time is rounded to the nearest five minutes and
    marked with '~' — the clock is a translation of solar position, not a
    fact the instrument measures to the minute.
    """
    if not iso:
        return DASH
    text = str(iso)
    hhmm = text.split("T")[1][:5] if "T" in text else text[:5]
    if precision != COARSE:
        return hhmm
    try:
        hh, mm = (int(part) for part in hhmm.split(":"))
    except ValueError:
        return hhmm
    total = round((hh * 60 + mm) / _ROUND_TO_MINUTES) * _ROUND_TO_MINUTES
    total %= 24 * 60
    return f"~{total // 60:02d}:{total % 60:02d}"


def hour_position(hour: dict, precision: str = COARSE) -> str:
    """
    Where we stand inside the Divine Hour.

    Coarse: a phrase ('opening', 'well inside', 'closing'). Exact: minutes.
    The phrase is the honest register — an unequal hour has no fixed length,
    so 'closing' transfers between seasons and latitudes where '42.9 min'
    does not.
    """
    progress = hour.get("progress_pct")
    if precision == EXACT:
        remaining = hour.get("remaining_minutes")
        duration = hour.get("duration_minutes")
        if remaining is None and duration is None:
            return DASH
        return f"{_v(duration)} min total · {_v(remaining)} min remaining"
    if progress is None:
        return DASH
    if progress < 25:
        return "opening"
    if progress < 60:
        return "well inside"
    if progress < 85:
        return "past the middle"
    return "closing"


def _point(code: Optional[str]) -> str:
    """SI-3 → 'SI-3 (Small Intestine)'."""
    if not code:
        return DASH
    meridian = code.split("-")[0] if "-" in code else code
    name = MERIDIAN_NAMES.get(meridian)
    return f"{code} ({name})" if name else code


def _vessel_name(code: Optional[str]) -> str:
    """Du Mai → 'Du Mai — Governing Vessel'."""
    if not code:
        return DASH
    english = VESSEL_ENGLISH.get(code)
    return f"{code} — {english}" if english and english != code else code


def _trigram(raw: dict) -> str:
    """☰ Qián — Heaven."""
    symbol = raw.get("symbol") or ""
    name = raw.get("trigram") or ""
    nature = TRIGRAM_NATURE.get(name, "")
    parts = [p for p in (symbol, name) if p]
    text = " ".join(parts)
    if nature:
        text = f"{text} — {nature}" if text else nature
    return text or DASH


def active_compounds(state: dict) -> list:
    """Active compounds as (key, display_name), aliases suppressed."""
    raw = state.get("compounds", {}) or {}
    out = []
    for key, value in raw.items():
        if key in _COMPOUND_ALIASES or not isinstance(value, bool) or not value:
            continue
        display = COMPOUND_DISPLAY.get(key, {}).get("name", key)
        out.append((key, display))
    return out


def active_resonances(state: dict) -> list:
    """Active resonances as (key, display_name, grade)."""
    raw = state.get("resonances", {}) or {}
    out = []
    for category in ("elemental", "qualitative", "rhythmic", "calendrical"):
        for key, value in (raw.get(category) or {}).items():
            if not isinstance(value, dict) or not value.get("active"):
                continue
            display = RESONANCE_DISPLAY.get(key, {}).get("name", key)
            out.append((key, display, value.get("grade")))
    return out


# ── the readout ───────────────────────────────────────────────────


def readout(state: dict, *, width: int = 20, precision: str = COARSE) -> str:
    """
    Render the complete state as a correspondence-forward block.

    Every line is `LABEL  value` drawn directly from the engine state.
    No sentence in the output asserts anything the tables do not.

    precision=COARSE (default) reports clock times to five minutes and the
    hour position as a phrase. The Divine Hour is the operative unit; the
    clock is a translation. Pass precision=EXACT when the minute matters.
    """
    L = []
    pad = lambda label: f"  {label:<{width}}"  # noqa: E731

    solar = state.get("solar", {}) or {}
    loc = state.get("location", {}) or {}
    vessel = state.get("derivative", {}) or {}
    soul = state.get("primeval", {}) or {}
    organ = state.get("organ_clock", {}) or {}
    hour = state.get("divine_hour", {}) or {}
    cal = state.get("calendar", {}) or {}
    key = state.get("solar_key", {}) or {}

    L.append("=== ASTROLABIUM READOUT ===")

    # 1. FRAME
    ts = state.get("timestamp")
    if not ts:
        when = DASH
    elif precision == COARSE:
        when = f"{str(ts)[:10]} {_clock(ts, COARSE)}"
    else:
        when = str(ts).replace("T", " ")[:22]
    where = DASH
    if loc:
        lat, lon = loc.get("lat"), loc.get("lon")
        if lat is not None and lon is not None:
            where = f"{lat:.4f}, {lon:.4f}"
        if loc.get("tz"):
            where = f"{where} · {loc['tz']}"
    L.append(pad("WHEN") + when)
    L.append(pad("WHERE") + where)
    L.append(
        pad("SOLAR")
        + f"sunrise {_clock(solar.get('sunrise'), precision)} · noon {_clock(solar.get('noon'), precision)}"
        f" · sunset {_clock(solar.get('sunset'), precision)}"
    )

    # 2. VESSEL (Astral)
    L.append("")
    L.append("VESSEL (Astral body)")
    L.append(pad("open") + _vessel_name(vessel.get("vessel")))
    L.append(pad("law") + _v(vessel.get("law")))
    L.append(pad("trigram") + _trigram(vessel))
    L.append(pad("confluent point") + _point(vessel.get("confluent")))
    L.append(pad("coupled point") + _point(vessel.get("coupled")))
    L.append(pad("polarity") + _v(vessel.get("polarity")))
    L.append(pad("pair partner") + _vessel_name(vessel.get("pair_partner")))
    L.append(pad("clinical domain") + _v(vessel.get("vessel_clinical_domain")))
    L.append(pad("yin-day gated") + _v(vessel.get("yin_day_blocked")))
    L.append(
        pad("register")
        + f"vowel {_v(vessel.get('vowel'))} · mudra {_v(vessel.get('mudra'))} · "
        f"Adonaj-Ba {_v(vessel.get('adonaj_ba'))} · colour {_v(vessel.get('color'))}"
    )
    L.append(pad("quest") + _v(vessel.get("quest_short")))

    # 3. LUNAR (Soul)
    L.append("")
    L.append("LUNAR (Soul body)")
    illum = soul.get("illumination_pct")
    phase_line = _v(soul.get("phase"))
    if illum is not None:
        phase_line = f"{phase_line} · {illum}% illuminated"
    if soul.get("waxing") is not None:
        phase_line = f"{phase_line} · {'waxing' if soul.get('waxing') else 'waning'}"
    L.append(pad("phase") + phase_line)
    L.append(pad("trigram") + _trigram(soul))
    L.append(pad("law") + _v(soul.get("law")))
    L.append(pad("yang lines") + _v(soul.get("yang_count")))
    L.append(
        pad("register")
        + f"vowel {_v(soul.get('vowel'))} · mudra {_v(soul.get('mudra'))} · "
        f"Adonaj-Ba {_v(soul.get('adonaj_ba'))} · colour {_v(soul.get('color'))}"
    )
    L.append(pad("quest") + _v(soul.get("quest_short")))

    # 4. ORGAN (Gross)
    L.append("")
    L.append("ORGAN CLOCK (Gross body)")
    L.append(
        pad("organ")
        + f"{_v(organ.get('organ'))} ({_v(organ.get('meridian'))}) · "
        f"{_v(organ.get('element'))} · {_v(organ.get('yin_yang'))}"
    )
    L.append(pad("paired organ") + _v(organ.get("paired")))
    L.append(pad("healing sound") + _v(organ.get("healing_sound")))
    L.append(pad("organ spirit") + _v(organ.get("organ_spirit")))
    L.append(pad("healing colour") + _v(organ.get("healing_color")))
    L.append(pad("emotion −") + _v(organ.get("emotion_negative")))
    L.append(pad("emotion +") + _v(organ.get("emotion_positive")))
    L.append(
        pad("season / sense")
        + f"{_v(organ.get('organ_season'))} · {_v(organ.get('sense_organ'))} · {_v(organ.get('body_tissue'))}"
    )

    # 5. HOUR
    L.append("")
    L.append("DIVINE HOUR")
    roman = _v(hour.get("roman"))
    wing = _v(hour.get("wing"))
    L.append(pad("hour") + f"{roman} ({wing} wing)")
    L.append(pad("protocol") + _v(hour.get("protocols")))
    L.append(pad("position") + hour_position(hour, precision))

    # 6. CALENDAR
    L.append("")
    L.append("CALENDAR")
    L.append(
        pad("divine month")
        + f"{_v(cal.get('month_number'))} {_v(cal.get('month_name'))} — "
        f"{_v(cal.get('month_tier_0_character'))}"
    )
    L.append(
        pad("day in month")
        + f"{_v(cal.get('day_in_month'))} / {_v(cal.get('total_days_in_month'))}"
    )
    L.append(
        pad("sephirotic day")
        + f"{_v(cal.get('sephirotic_day'))} {_v(cal.get('sephirah'))} / "
        f"{_v(cal.get('sephirotic_planet'))} {_v(cal.get('sephirotic_symbol'))}"
    )
    L.append(pad("alchemical stage") + _v(cal.get("alchemical")))
    L.append(pad("great rite") + _v(cal.get("great_rite")))
    L.append(pad("divine year") + _v(cal.get("divine_year")))

    # 7. KEYS
    L.append("")
    L.append("SOLAR KEY")
    if key.get("active") and key.get("key"):
        name = "Gold" if key.get("key") == "gold" else "Silver"
        L.append(
            pad("active")
            + f"{name} Key · {_v(key.get('law'))} · {_v(key.get('event'))}"
        )
        L.append(
            pad("window")
            + f"{_clock(key.get('window_start'), precision)} – {_clock(key.get('window_end'), precision)}"
        )
    else:
        L.append(pad("active") + "none (no cusping window)")

    # 8. COMPOUNDS
    compounds = active_compounds(state)
    L.append("")
    L.append(f"COMPOUNDS ACTIVE ({len(compounds)})")
    if compounds:
        for _, name in compounds:
            L.append(f"  · {name}")
    else:
        L.append("  · none")

    # 9. RESONANCES
    resonances = active_resonances(state)
    L.append("")
    L.append(f"RESONANCES ACTIVE ({len(resonances)})")
    if resonances:
        for _, name, grade in resonances:
            L.append(f"  · {name}" + (f" [{grade}]" if grade else ""))
    else:
        L.append("  · none")

    L.append("")
    L.append("=== END READOUT ===")
    return "\n".join(L)


def typed_state(state: dict) -> str:
    """
    The readout's machine core: `KEY = value` lines, one fact per line.

    This is the form that survives a session boundary, a compaction, or a
    hand-off without corrupting (XR-001 §2a). Anything that must be quoted
    downstream should be quoted from here, never re-narrated from prose.
    """
    vessel = state.get("derivative", {}) or {}
    soul = state.get("primeval", {}) or {}
    organ = state.get("organ_clock", {}) or {}
    hour = state.get("divine_hour", {}) or {}
    cal = state.get("calendar", {}) or {}
    key = state.get("solar_key", {}) or {}
    solar = state.get("solar", {}) or {}

    lines = ["=== VERIFIED STATE: ASTROLABIUM ==="]
    add = lines.append
    add(f"when                 = {_v(state.get('timestamp'))}")
    add(f"sunrise              = {_clock(solar.get('sunrise'))}")
    add(f"sunset               = {_clock(solar.get('sunset'))}")
    add(f"vessel.open          = {_v(vessel.get('vessel'))}")
    add(f"vessel.law           = {_v(vessel.get('law'))}")
    add(f"vessel.confluent     = {_v(vessel.get('confluent'))}")
    add(f"vessel.coupled       = {_v(vessel.get('coupled'))}")
    add(f"vessel.polarity      = {_v(vessel.get('polarity'))}")
    add(f"lunar.phase          = {_v(soul.get('phase'))}")
    add(f"lunar.illumination   = {_v(soul.get('illumination_pct'))}")
    add(f"lunar.trigram        = {_v(soul.get('symbol'))} {_v(soul.get('trigram'))}")
    add(f"soul.law             = {_v(soul.get('law'))}")
    add(f"organ.active         = {_v(organ.get('organ'))} ({_v(organ.get('meridian'))})")
    add(f"organ.element        = {_v(organ.get('element'))}")
    add(f"organ.healing_sound  = {_v(organ.get('healing_sound'))}")
    add(f"hour.roman           = {_v(hour.get('roman'))}")
    add(f"hour.protocol        = {_v(hour.get('protocols'))}")
    add(f"hour.remaining_min   = {_v(hour.get('remaining_minutes'))}")
    add(f"month                = {_v(cal.get('month_number'))} {_v(cal.get('month_name'))}")
    add(f"month.day            = {_v(cal.get('day_in_month'))}/{_v(cal.get('total_days_in_month'))}")
    add(f"sephirotic.day       = {_v(cal.get('sephirotic_day'))} {_v(cal.get('sephirah'))}")
    add(f"alchemical.stage     = {_v(cal.get('alchemical'))}")
    add(f"solar_key.active     = {_v(bool(key.get('active')))}")
    add(f"compounds.active     = {', '.join(n for _, n in active_compounds(state)) or 'none'}")
    add(f"resonances.active    = {len(active_resonances(state))}")
    lines.append("=== END VERIFIED STATE ===")
    return "\n".join(lines)


# ── the story gate ────────────────────────────────────────────────

# Interpretation is licensed ONLY by a structural fact the engine detected.
# These are the compounds that earn commentary; everything else is read
# from the tables and left alone.
#
# C-06 (2026-07-30): anatomical_key, conditional_3_4, and conditional_3_5
# added — each is an anatomical intersection amplified by (or conditioned
# on) a Solar Key, i.e. Key amplification of a licensed intersection class,
# so a licensed story may lawfully name the Key aspect.
#
# DECISION (2026-07-30): key_derivative_unity stays EXCLUDED. The
# astrolabium/CLAUDE.md contract licenses five classes only — Two-Body
# Unity, anatomical intersection, Key amplification, Great Rite,
# VADUSFADAHM. Key-Vessel Unity (the Key's Law matching the open Vessel's
# Law) is none of these: it is a Key-layer coincidence, not a
# body-alignment, and does not earn commentary on its own.
STORY_LICENSING_COMPOUNDS = {
    "two_body_unity",
    "key_amplified_unity",
    "full_confluent",
    "full_coupled",
    "full_alignment_key",
    "confluent_intersection",
    "coupled_intersection",
    "anatomical_key",
    "conditional_3_4",
    "conditional_3_5",
    "great_rite_active",
    "vadusfadahm_active",
}

MAX_STORY_SENTENCES = 3


def story_gate(state: dict) -> dict:
    """
    Decide whether interpretation is licensed for this moment, and about what.

    The readout always stands alone. A story is permitted only when the
    engine has detected a structural alignment worth naming — and then only
    about that alignment, in at most MAX_STORY_SENTENCES sentences, with no
    numbers (numbers live in the readout, and restating them corrupts them).

    Returns:
        licensed (bool)    — may an interpretive paragraph be written at all
        subjects (list)    — the specific compound display names it may address
        max_sentences (int)
        rule (str)         — the constraint, carried with the verdict
    """
    licensed_subjects = [
        name for key, name in active_compounds(state)
        if key in STORY_LICENSING_COMPOUNDS
    ]
    return {
        "licensed": bool(licensed_subjects),
        "subjects": licensed_subjects,
        "max_sentences": MAX_STORY_SENTENCES,
        "rule": (
            "Address only the listed subjects. No numbers, times, or values in "
            "prose — those are read from the readout. No vocabulary rotation, "
            "no weaving, no second entry point. If nothing is licensed, the "
            "readout is the complete answer."
        ),
    }
