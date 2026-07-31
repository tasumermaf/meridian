"""
Astrolabium Caudae Rubrae — Frequency Analysis Engine.

Phase 3: scans time ranges to compute compound frequencies, Law distributions,
and window timing. Operates on the clean Torch & Rebuild foundation.

All interpretive data from registers.json via calculate_complete_state().
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import List

from .astrolabium import calculate_complete_state
from .resonance import RESONANCE_BOOLEAN_TYPES


def _state_skipping_dst(current, lat, lon, tz):
    """
    calculate_complete_state, returning None for civil instants that do
    not exist (DST spring-forward gap) or are ambiguous (fall-back hour).

    Scan loops march naive civil time in fixed steps and land on these
    instants twice a year per DST zone. The engine refuses to fabricate a
    state for them (AUDIT_2026-07-24 C-03); scanners skip them and — in
    scan_compounds — report the skip count as data.
    """
    try:
        return calculate_complete_state(current, lat, lon, tz)
    except ValueError as e:
        if "does not exist" in str(e) or "ambiguous" in str(e):
            return None
        raise

COMPOUND_TYPES = [
    # Category 1: Law Unity
    "two_body_unity",
    "key_derivative_unity",
    # Category 2: Anatomical Intersection
    "confluent_intersection",
    "coupled_intersection",
    # Category 3: Combined
    "full_confluent",
    "full_coupled",
    "conditional_3_4",
    "conditional_3_5",
    # Category 4: Polarity
    "yin_day_blocked",
    "polarity_aligned",
    # Category 5: Calendar
    "great_rite_active",
    "vadusfadahm_active",
    "sephirotic_rare",
    # Category 6: Multi-Layer
    "key_amplified_unity",
    "anatomical_key",
    "full_alignment_key",
]

# All searchable types: compounds + boolean resonances
ALL_SEARCHABLE_TYPES = COMPOUND_TYPES + RESONANCE_BOOLEAN_TYPES


def _is_resonance_active(state: dict, rtype: str) -> bool:
    """Check if a boolean resonance type is active in the state."""
    resonances = state.get("resonances", {})
    for cat_name in ("elemental", "qualitative", "rhythmic", "calendrical"):
        cat = resonances.get(cat_name, {})
        if isinstance(cat, dict) and rtype in cat:
            val = cat[rtype]
            if isinstance(val, dict) and "active" in val:
                return val["active"]
    return False


def scan_compounds(
    start_dt: datetime,
    end_dt: datetime,
    lat: float,
    lon: float,
    tz: str,
    interval_minutes: int = 30,
) -> dict:
    """
    Scan a time range and compute compound frequency statistics.

    Returns counts, percentages, Law distributions, and per-Law compound
    breakdowns. The workhorse of Phase 3 frequency analysis.
    """
    delta = timedelta(minutes=interval_minutes)
    current = start_dt
    total = 0

    # Compound counters
    compound_counts = {c: 0 for c in COMPOUND_TYPES}
    compound_by_law = {c: defaultdict(int) for c in COMPOUND_TYPES}
    raw_unity_count = 0
    yin_blocked_count = 0

    # Resonance counters
    resonance_counts = {r: 0 for r in RESONANCE_BOOLEAN_TYPES}

    # State-value distributions
    alchemical_dist = defaultdict(int)
    month_group_dist = defaultdict(int)
    iao_dist = defaultdict(int)
    yang_count_dist = defaultdict(int)
    # divine_hour_law_unity (AUDIT_2026-07-24 D-09, added 2026-07-30):
    # hour-index distribution over Two-Body-Unity steps — the R_RHY_02
    # state value finally has a path to frequency figures.
    dh_law_unity_dist = defaultdict(int)

    # Solar Key activity counters (AUDIT_2026-07-24 C-18, added 2026-07-30):
    # artifact-backed gold/silver key-active tallies.
    gold_key_active_count = 0
    silver_key_active_count = 0

    # Distributions
    primeval_dist = defaultdict(int)
    derivative_dist = defaultdict(int)
    phase_dist = defaultdict(int)
    hour_dist = defaultdict(int)
    vessel_dist = defaultdict(int)
    organ_dist = defaultdict(int)

    skipped = 0
    while current <= end_dt:
        state = _state_skipping_dst(current, lat, lon, tz)
        if state is None:
            skipped += 1
            current += delta
            continue
        total += 1

        # Law distributions
        p_law = state["primeval"]["law"]
        d_law = state["derivative"]["law"]
        primeval_dist[p_law] += 1
        derivative_dist[d_law] += 1

        # Phase distribution
        phase_dist[state["primeval"]["phase"]] += 1

        # Divine hour distribution
        hour_dist[state["divine_hour"]["index"]] += 1

        # Vessel distribution
        vessel_dist[state["derivative"]["vessel"]] += 1

        # Organ distribution
        organ_dist[state["organ_clock"]["organ"]] += 1

        # Compound detection
        compounds = state["compounds"]

        if compounds.get("two_body_unity_raw"):
            raw_unity_count += 1

        if compounds.get("yin_day_blocked"):
            yin_blocked_count += 1

        for c in COMPOUND_TYPES:
            if compounds.get(c):
                compound_counts[c] += 1
                # Track which law was active during the compound
                if c in (
                    "two_body_unity", "full_confluent", "full_coupled",
                    "key_amplified_unity", "full_alignment_key",
                    "polarity_aligned",
                ):
                    compound_by_law[c][p_law] += 1
                elif c in (
                    "key_derivative_unity",
                    "conditional_3_4",
                    "conditional_3_5",
                ):
                    key_law = state["solar_key"].get("law")
                    if key_law:
                        compound_by_law[c][key_law] += 1
                elif c in (
                    "confluent_intersection", "coupled_intersection",
                    "anatomical_key",
                ):
                    compound_by_law[c][d_law] += 1

        # Resonance detection
        resonances = state.get("resonances", {})
        for cat_name in ("elemental", "qualitative", "rhythmic", "calendrical"):
            cat = resonances.get(cat_name, {})
            if isinstance(cat, dict):
                for r_type, r_data in cat.items():
                    if isinstance(r_data, dict) and r_data.get("active"):
                        if r_type in resonance_counts:
                            resonance_counts[r_type] += 1

        # State-value distributions
        cal_resonances = resonances.get("calendrical", {})
        alch = cal_resonances.get("alchemical_stage")
        if alch:
            alchemical_dist[alch] += 1

        mg = cal_resonances.get("month_group")
        if mg:
            month_group_dist[mg] += 1

        iao = cal_resonances.get("iao_position")
        if iao is not None:
            iao_dist[str(iao)] += 1
        else:
            iao_dist["null"] += 1

        yc = resonances.get("rhythmic", {}).get("yang_count")
        if yc is not None:
            yang_count_dist[yc] += 1

        # divine_hour_law_unity: non-null exactly when two_body_unity fires
        dhlu = resonances.get("rhythmic", {}).get("divine_hour_law_unity")
        if dhlu is not None:
            dh_law_unity_dist[dhlu.get("hour_index")] += 1

        # Solar Key activity
        solar_key = state.get("solar_key", {})
        if solar_key.get("active"):
            if solar_key.get("key") == "gold":
                gold_key_active_count += 1
            elif solar_key.get("key") == "silver":
                silver_key_active_count += 1

        current += delta

    # Build result
    def _pct(count):
        return round(count / total * 100, 2) if total > 0 else 0

    compound_results = {}
    for c in COMPOUND_TYPES:
        entry = {
            "count": compound_counts[c],
            "pct": _pct(compound_counts[c]),
        }
        if compound_by_law[c]:
            entry["by_law"] = dict(compound_by_law[c])
        compound_results[c] = entry

    # Add raw unity for yin-day comparison
    compound_results["two_body_unity"]["raw_count"] = raw_unity_count

    # Resonance results
    resonance_results = {}
    for r in RESONANCE_BOOLEAN_TYPES:
        resonance_results[r] = {
            "count": resonance_counts[r],
            "pct": _pct(resonance_counts[r]),
        }

    return {
        "total_steps": total,
        "skipped_nonexistent_steps": skipped,
        "interval_minutes": interval_minutes,
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
        "duration_days": round((end_dt - start_dt).total_seconds() / 86400, 2),
        "compounds": compound_results,
        "resonances": resonance_results,
        "resonance_distributions": {
            "alchemical_stage": dict(alchemical_dist),
            "month_group": dict(month_group_dist),
            "iao_position": dict(iao_dist),
            "yang_count": {str(k): v for k, v in sorted(yang_count_dist.items())},
            "divine_hour_law_unity": {
                str(k): v
                for k, v in sorted(
                    dh_law_unity_dist.items(),
                    key=lambda kv: (kv[0] is None, kv[0]),
                )
            },
        },
        "solar_key_activity": {
            "gold_key_active": {
                "count": gold_key_active_count,
                "pct": _pct(gold_key_active_count),
            },
            "silver_key_active": {
                "count": silver_key_active_count,
                "pct": _pct(silver_key_active_count),
            },
        },
        "yin_day_blocked": {
            "count": yin_blocked_count,
            "pct": _pct(yin_blocked_count),
        },
        "law_distribution": {
            "primeval": dict(primeval_dist),
            "derivative": dict(derivative_dist),
        },
        "phase_distribution": dict(phase_dist),
        "divine_hour_distribution": {
            str(k): v for k, v in sorted(hour_dist.items())
        },
        "vessel_distribution": dict(vessel_dist),
        "organ_distribution": dict(organ_dist),
    }


def find_windows(
    start_dt: datetime,
    end_dt: datetime,
    lat: float,
    lon: float,
    tz: str,
    compound: str,
    interval_minutes: int = 15,
) -> List[dict]:
    """
    Find all contiguous windows where a compound or resonance is active.

    A "window" is a run of consecutive sampling points where the compound
    fires. Returns start, end, duration, and the Law active during each window.
    Accepts both compound types and boolean resonance types.
    """
    is_resonance = compound in RESONANCE_BOOLEAN_TYPES
    if compound not in ALL_SEARCHABLE_TYPES:
        raise ValueError(
            f"Unknown compound/resonance: {compound}. Valid: {ALL_SEARCHABLE_TYPES}"
        )

    delta = timedelta(minutes=interval_minutes)
    current = start_dt
    windows = []

    in_window = False
    window_start = None
    window_law = None
    prev_time = None

    while current <= end_dt:
        state = _state_skipping_dst(current, lat, lon, tz)
        if state is None:
            current += delta
            continue

        if is_resonance:
            active = _is_resonance_active(state, compound)
        else:
            active = state["compounds"].get(compound, False)

        if active and not in_window:
            in_window = True
            window_start = current
            if compound in ("two_body_unity", "full_confluent", "full_coupled"):
                window_law = state["primeval"]["law"]
            elif compound in (
                "key_derivative_unity",
                "conditional_3_4",
                "conditional_3_5",
            ):
                window_law = state["solar_key"].get("law")
            elif is_resonance:
                window_law = state["primeval"]["law"]
            else:
                window_law = state["derivative"]["law"]
        elif not active and in_window:
            in_window = False
            windows.append({
                "start": window_start.isoformat(),
                "end": prev_time.isoformat(),
                "duration_minutes": round(
                    (prev_time - window_start).total_seconds() / 60, 1
                ),
                "law": window_law,
            })
            window_start = None
            window_law = None

        prev_time = current
        current += delta

    # Close open window at end of range
    if in_window and prev_time:
        windows.append({
            "start": window_start.isoformat(),
            "end": prev_time.isoformat(),
            "duration_minutes": round(
                (prev_time - window_start).total_seconds() / 60, 1
            ),
            "law": window_law,
        })

    return windows


def next_compound(
    start_dt: datetime,
    lat: float,
    lon: float,
    tz: str,
    compound: str = "two_body_unity",
    max_hours: int = 168,
    interval_minutes: int = 15,
) -> dict:
    """
    Find the next occurrence of a specific compound or resonance type.

    Scans forward from start_dt at the given interval until the compound
    fires or max_hours is exceeded. Accepts both compound and resonance types.
    """
    is_resonance = compound in RESONANCE_BOOLEAN_TYPES
    if compound not in ALL_SEARCHABLE_TYPES:
        raise ValueError(
            f"Unknown compound/resonance: {compound}. Valid: {ALL_SEARCHABLE_TYPES}"
        )

    delta = timedelta(minutes=interval_minutes)
    current = start_dt
    limit = start_dt + timedelta(hours=max_hours)

    while current < limit:
        state = _state_skipping_dst(current, lat, lon, tz)
        if state is None:
            current += delta
            continue

        if is_resonance:
            found = _is_resonance_active(state, compound)
        else:
            found = state["compounds"].get(compound, False)

        if found:
            result = {
                "found": True,
                "compound": compound,
                "is_resonance": is_resonance,
                "timestamp": current.isoformat(),
                "hours_from_start": round(
                    (current - start_dt).total_seconds() / 3600, 2
                ),
            }
            if compound in ("two_body_unity", "full_confluent", "full_coupled"):
                result["law"] = state["primeval"]["law"]
                result["vessel"] = state["derivative"]["vessel"]
                result["phase"] = state["primeval"]["phase"]
            elif compound in (
                "key_derivative_unity",
                "conditional_3_4",
                "conditional_3_5",
            ):
                result["key"] = state["solar_key"].get("key")
                result["law"] = state["solar_key"].get("law")
                result["vessel"] = state["derivative"]["vessel"]
            elif is_resonance:
                result["law"] = state["primeval"]["law"]
                result["organ"] = state["organ_clock"]["organ"]
                result["element"] = state["organ_clock"]["element"]
            else:
                result["law"] = state["derivative"]["law"]
                result["vessel"] = state["derivative"]["vessel"]
                result["organ"] = state["organ_clock"]["organ"]
            return result
        current += delta

    return {
        "found": False,
        "compound": compound,
        "searched_hours": max_hours,
        "message": f"No {compound} found within {max_hours} hours",
    }
