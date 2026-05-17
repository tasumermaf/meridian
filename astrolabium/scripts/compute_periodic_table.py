"""
Periodic Table v3 Generator — computes compound and resonance frequencies
across one Divine Year at configurable resolution.

Output: JSON results file + formatted Markdown periodic table.

Usage:
    cd astrolabium/code
    python -m scripts.compute_periodic_table [--interval 15] [--output results.json]
"""

import sys
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.astrolabium import calculate_complete_state
from src.frequency import COMPOUND_TYPES
from src.resonance import RESONANCE_BOOLEAN_TYPES, RESONANCE_STATE_TYPES
from src.engine.calendar import get_divine_year, next_new_moon

# ── Configuration ──────────────────────────────────────────────────

# Damanhur, Piedmont, Italy — project spiritual home
LAT = 45.4167
LON = 7.8833
TZ = "Europe/Rome"

ALL_BOOLEAN = COMPOUND_TYPES + RESONANCE_BOOLEAN_TYPES


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


def _get_active_booleans(state: dict) -> set:
    """Return the set of all active boolean types (compounds + resonances)."""
    active = set()
    compounds = state.get("compounds", {})
    for c in COMPOUND_TYPES:
        if compounds.get(c):
            active.add(c)
    for r in RESONANCE_BOOLEAN_TYPES:
        if _is_resonance_active(state, r):
            active.add(r)
    return active


def compute_periodic_table(interval_minutes: int = 15) -> dict:
    """
    Full Divine Year computation.

    Returns a dict with all frequency data, co-occurrence matrix,
    per-month profiles, and distribution data.
    """
    # ── Determine Divine Year boundaries ──
    now = datetime(2026, 3, 2, 12, 0)
    year_info = get_divine_year(now)

    start_dt = year_info["year_start"]
    end_dt = year_info["next_year_start"]

    duration_days = (end_dt - start_dt).total_seconds() / 86400
    expected_steps = int(duration_days * 24 * 60 / interval_minutes) + 1

    print(f"=== Periodic Table v3 Computation ===")
    print(f"Divine Year {year_info['year']}")
    print(f"  Gregorian anchor: {year_info['anchor_gregorian']}")
    print(f"  Start:  {start_dt.isoformat()}")
    print(f"  End:    {end_dt.isoformat()}")
    print(f"  Months: {year_info['total_months']}")
    print(f"  Intercalary: {year_info['is_intercalary_year']}")
    print(f"  Duration: {duration_days:.1f} days")
    print(f"  Interval: {interval_minutes} min")
    print(f"  Expected steps: ~{expected_steps}")
    print(f"  Location: Damanhur ({LAT}, {LON})")
    print()

    delta = timedelta(minutes=interval_minutes)
    current = start_dt
    total = 0

    # ── Global counters ──
    compound_counts = {c: 0 for c in COMPOUND_TYPES}
    resonance_counts = {r: 0 for r in RESONANCE_BOOLEAN_TYPES}
    raw_unity_count = 0
    yin_blocked_count = 0

    # ── Co-occurrence matrix (all boolean types) ──
    cooccur = defaultdict(int)

    # ── Distributions ──
    primeval_dist = defaultdict(int)
    derivative_dist = defaultdict(int)
    phase_dist = defaultdict(int)
    hour_dist = defaultdict(int)
    vessel_dist = defaultdict(int)
    organ_dist = defaultdict(int)

    # ── Resonance state-value distributions ──
    alchemical_dist = defaultdict(int)
    month_group_dist = defaultdict(int)
    iao_dist = defaultdict(int)
    yang_count_dist = defaultdict(int)

    # ── Per-month profiles ──
    # month_number -> {type_name -> count, "_total" -> step_count}
    month_profiles = defaultdict(lambda: defaultdict(int))

    # ── Per-compound Law breakdowns ──
    compound_by_law = {c: defaultdict(int) for c in COMPOUND_TYPES}
    resonance_by_law = {r: defaultdict(int) for r in RESONANCE_BOOLEAN_TYPES}

    # ── Timing ──
    t0 = time.time()
    report_every = 2000

    while current < end_dt:
        state = calculate_complete_state(current, LAT, LON, TZ)
        total += 1

        # Distributions
        p_law = state["primeval"]["law"]
        d_law = state["derivative"]["law"]
        primeval_dist[p_law] += 1
        derivative_dist[d_law] += 1
        phase_dist[state["primeval"]["phase"]] += 1
        hour_dist[state["divine_hour"]["index"]] += 1
        vessel_dist[state["derivative"]["vessel"]] += 1
        organ_dist[state["organ_clock"]["organ"]] += 1

        # Month tracking
        month_num = state.get("calendar", {}).get("month_number", 0)
        month_profiles[month_num]["_total"] += 1

        # Compound detection
        compounds = state["compounds"]
        if compounds.get("two_body_unity_raw"):
            raw_unity_count += 1
        if compounds.get("yin_day_blocked"):
            yin_blocked_count += 1

        active_set = _get_active_booleans(state)

        for c in COMPOUND_TYPES:
            if c in active_set:
                compound_counts[c] += 1
                compound_by_law[c][p_law] += 1
                month_profiles[month_num][c] += 1

        for r in RESONANCE_BOOLEAN_TYPES:
            if r in active_set:
                resonance_counts[r] += 1
                resonance_by_law[r][p_law] += 1
                month_profiles[month_num][r] += 1

        # Co-occurrence: for each pair of active booleans, increment
        active_list = sorted(active_set)
        for i in range(len(active_list)):
            for j in range(i + 1, len(active_list)):
                key = f"{active_list[i]}|{active_list[j]}"
                cooccur[key] += 1

        # State-value distributions
        resonances = state.get("resonances", {})
        cal_res = resonances.get("calendrical", {})

        alch = cal_res.get("alchemical_stage")
        if alch:
            alchemical_dist[alch] += 1

        mg = cal_res.get("month_group")
        if mg:
            month_group_dist[mg] += 1

        iao = cal_res.get("iao_position")
        iao_dist[str(iao) if iao is not None else "null"] += 1

        yc = resonances.get("rhythmic", {}).get("yang_count")
        if yc is not None:
            yang_count_dist[int(yc)] += 1

        # Progress
        if total % report_every == 0:
            elapsed = time.time() - t0
            rate = total / elapsed
            remaining = (expected_steps - total) / rate if rate > 0 else 0
            print(
                f"  Step {total}/{expected_steps} "
                f"({total/expected_steps*100:.1f}%) "
                f"— {rate:.0f} steps/s, ~{remaining:.0f}s remaining"
            )

        current += delta

    elapsed_total = time.time() - t0
    print(f"\nCompleted: {total} steps in {elapsed_total:.1f}s "
          f"({total/elapsed_total:.0f} steps/s)")

    # ── Build results ──
    def _pct(count):
        return round(count / total * 100, 3) if total > 0 else 0

    # Main frequency table
    freq_table = {}
    for c in COMPOUND_TYPES:
        entry = {
            "type": "compound",
            "count": compound_counts[c],
            "pct": _pct(compound_counts[c]),
            "by_law": dict(compound_by_law[c]),
        }
        if c == "two_body_unity":
            entry["raw_count"] = raw_unity_count
        freq_table[c] = entry

    for r in RESONANCE_BOOLEAN_TYPES:
        freq_table[r] = {
            "type": "resonance",
            "count": resonance_counts[r],
            "pct": _pct(resonance_counts[r]),
            "by_law": dict(resonance_by_law[r]),
        }

    # Month profiles: convert inner defaultdicts
    month_profiles_clean = {}
    for m_num, data in sorted(month_profiles.items()):
        month_profiles_clean[m_num] = dict(data)

    return {
        "meta": {
            "version": "3.0.0",
            "generated": datetime.utcnow().isoformat() + "Z",
            "divine_year": year_info["year"],
            "anchor_gregorian": year_info["anchor_gregorian"],
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "total_months": year_info["total_months"],
            "is_intercalary": year_info["is_intercalary_year"],
            "duration_days": round(duration_days, 2),
            "interval_minutes": interval_minutes,
            "total_steps": total,
            "location": {"name": "Damanhur", "lat": LAT, "lon": LON, "tz": TZ},
            "computation_time_seconds": round(elapsed_total, 1),
        },
        "frequency_table": freq_table,
        "cooccurrence": dict(cooccur),
        "yin_day_blocked": {
            "count": yin_blocked_count,
            "pct": _pct(yin_blocked_count),
            "raw_unity": raw_unity_count,
        },
        "distributions": {
            "primeval_law": dict(primeval_dist),
            "derivative_law": dict(derivative_dist),
            "lunar_phase": dict(phase_dist),
            "divine_hour": {str(k): v for k, v in sorted(hour_dist.items())},
            "vessel": dict(vessel_dist),
            "organ": dict(organ_dist),
        },
        "state_value_distributions": {
            "alchemical_stage": dict(alchemical_dist),
            "month_group": dict(month_group_dist),
            "iao_position": dict(iao_dist),
            "yang_count": {str(k): v for k, v in sorted(yang_count_dist.items())},
        },
        "month_profiles": month_profiles_clean,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute Periodic Table v3")
    parser.add_argument(
        "--interval", type=int, default=15,
        help="Sampling interval in minutes (default: 15)",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output JSON path (default: data/periodic_table_v3.json)",
    )
    args = parser.parse_args()

    output_path = args.output or str(
        Path(__file__).parent.parent / "data" / "periodic_table_v3.json"
    )

    results = compute_periodic_table(interval_minutes=args.interval)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults written to {output_path}")
    print(f"Total phenomena tracked: {len(results['frequency_table'])}")
    print(f"Co-occurrence pairs: {len(results['cooccurrence'])}")
