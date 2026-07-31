"""
Analyze the full combinatorial space of simultaneous compound/resonance activation.

Answers:
  1. How many unique alchemical compounds (2+ simultaneous phenomena) occurred?
  2. What is the highest-complexity compound this year?
  3. Full histogram of compound complexity.

Output (AUDIT_2026-07-24 B-29, applied 2026-07-30): results are WRITTEN to
data/compound_recipes_v2.json — console output is a summary view only, the
JSON artifact is authoritative. The artifact pins the exact detector type
lists (compound + boolean resonance) because active-set fingerprints are
only comparable under an identical detector set: the §8 figures of
periodic_table v4/v5.0 were generated under a 17-type set and could not be
reproduced once the set grew to 28.

Usage:
    cd astrolabium/code
    python -m scripts.analyze_compounds [--output data/compound_recipes_v2.json]
"""

import sys
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.astrolabium import calculate_complete_state  # noqa: F401 (re-export)
# Shared DST-skip helper: naive civil scans land on nonexistent/ambiguous
# instants twice a year per DST zone; the engine refuses to fabricate a
# state for them (AUDIT_2026-07-24 C-03). Skip and report the count as data.
from src.frequency import COMPOUND_TYPES, _state_skipping_dst
from src.resonance import RESONANCE_BOOLEAN_TYPES
from src.engine.calendar import get_divine_year

LAT = 45.4167
LON = 7.8833
TZ = "Europe/Rome"
INTERVAL = 15  # minutes

ALL_BOOLEAN = COMPOUND_TYPES + RESONANCE_BOOLEAN_TYPES

DEFAULT_OUTPUT = Path(__file__).parent.parent / "data" / "compound_recipes_v2.json"


def _get_active_set(state: dict) -> frozenset:
    """Return frozenset of all active boolean types."""
    active = set()
    compounds = state.get("compounds", {})
    for c in COMPOUND_TYPES:
        if compounds.get(c):
            active.add(c)

    resonances = state.get("resonances", {})
    for cat_name in ("elemental", "qualitative", "rhythmic", "calendrical"):
        cat = resonances.get(cat_name, {})
        if isinstance(cat, dict):
            for rtype, rdata in cat.items():
                if rtype in RESONANCE_BOOLEAN_TYPES:
                    if isinstance(rdata, dict) and rdata.get("active"):
                        active.add(rtype)
    return frozenset(active)


def main(output_path=None, start_dt=None, end_dt=None):
    """
    Scan the Divine Year (or an explicit range), print the summary, and
    write the recipe artifact. start_dt/end_dt overrides exist for smoke
    tests; the default is the full Divine Year containing 2026-03-02.
    """
    now = datetime(2026, 3, 2, 12, 0)
    year_info = get_divine_year(now)
    if start_dt is None:
        start_dt = year_info["year_start"]
    if end_dt is None:
        end_dt = year_info["next_year_start"]
    output_path = Path(output_path) if output_path else DEFAULT_OUTPUT

    delta = timedelta(minutes=INTERVAL)
    current = start_dt
    total = 0

    # Track unique compound fingerprints (2+ simultaneous phenomena)
    compound_registry = defaultdict(int)  # frozenset -> count
    complexity_hist = Counter()           # N -> count (how many steps had N active)
    max_complexity = 0
    max_compound = frozenset()
    max_timestamp = None
    max_state_summary = None

    t0 = time.time()
    skipped = 0

    while current < end_dt:
        state = _state_skipping_dst(current, LAT, LON, TZ)
        if state is None:
            skipped += 1
            current += delta
            continue
        total += 1
        active = _get_active_set(state)
        n = len(active)

        complexity_hist[n] += 1

        if n >= 2:
            compound_registry[active] += 1

        if n > max_complexity:
            max_complexity = n
            max_compound = active
            max_timestamp = current
            max_state_summary = {
                "primeval_law": state["primeval"]["law"],
                "derivative_law": state["derivative"]["law"],
                "organ": state["organ_clock"]["organ"],
                "element": state["organ_clock"]["element"],
                "phase": state["primeval"]["phase"],
                "vessel": state["derivative"]["vessel"],
                "divine_hour": state["divine_hour"]["index"],
                "month": state.get("calendar", {}).get("month_number"),
            }

        if total % 5000 == 0:
            elapsed = time.time() - t0
            print(f"  Step {total} — {total/elapsed:.0f} steps/s", flush=True)

        current += delta

    elapsed = time.time() - t0

    # Analysis
    print(f"\n{'='*70}")
    print(f"COMPOUND ANALYSIS — Divine Year {year_info['year']}")
    print(f"{'='*70}")
    print(f"Total steps: {total:,}")
    print(f"Skipped nonexistent/ambiguous DST instants: {skipped}")
    print(f"Computation time: {elapsed:.1f}s")
    print()

    print(f"COMPLEXITY HISTOGRAM (how many phenomena active simultaneously)")
    print(f"{'Active':>8}  {'Steps':>8}  {'%':>7}  Description")
    print(f"{'-'*50}")
    for n in sorted(complexity_hist.keys()):
        cnt = complexity_hist[n]
        pct = cnt / total * 100
        desc = ""
        if n == 0:
            desc = "Nothing active"
        elif n == 1:
            desc = "Single phenomenon (not a compound)"
        elif n >= 2:
            desc = f"Compound of {n} phenomena"
        print(f"{n:>8}  {cnt:>8,}  {pct:>6.2f}%  {desc}")

    total_compound_steps = sum(cnt for n, cnt in complexity_hist.items() if n >= 2)
    print(f"\nSteps with a compound (2+ active): {total_compound_steps:,} ({total_compound_steps/total*100:.1f}%)")
    print(f"Unique compound recipes: {len(compound_registry):,}")
    print()

    max_count = compound_registry.get(max_compound, 0)

    print(f"HIGHEST COMPLEXITY COMPOUND")
    print(f"  Complexity: {max_complexity} simultaneous phenomena")
    if max_timestamp is not None:
        print(f"  First occurrence: {max_timestamp.isoformat()}")
    print(f"  Components:")
    for t in sorted(max_compound):
        cat = "compound" if t in COMPOUND_TYPES else "resonance"
        print(f"    - {t} ({cat})")
    if max_state_summary:
        print(f"  State at occurrence:")
        for k, v in max_state_summary.items():
            print(f"    {k}: {v}")
    print()
    print(f"  This exact compound occurred: {max_count} times ({max_count * INTERVAL} minutes total)")
    print()

    # Top 15 most frequent compounds
    ranked_recipes = sorted(
        compound_registry.items(), key=lambda x: (-x[1], sorted(x[0]))
    )
    print(f"TOP 15 MOST FREQUENT COMPOUNDS (by occurrence count)")
    print(f"{'Rank':>4}  {'Count':>6}  {'Size':>4}  Components")
    print(f"{'-'*80}")
    for rank, (compound, count) in enumerate(ranked_recipes[:15], 1):
        components = ", ".join(sorted(compound))
        print(f"{rank:>4}  {count:>6,}  {len(compound):>4}  {components}")

    print()

    # Rarest compounds (occurred only once)
    singletons = [(c, cnt) for c, cnt in compound_registry.items() if cnt == 1]
    print(f"Unique compounds that occurred only once: {len(singletons)}")

    # Show the rarest high-complexity ones
    rare_complex = sorted(
        [(c, cnt) for c, cnt in compound_registry.items() if cnt <= 3 and len(c) >= 5],
        key=lambda x: (-len(x[0]), x[1]),
    )
    if rare_complex:
        print(f"\nRAREST HIGH-COMPLEXITY COMPOUNDS (5+ components, <= 3 occurrences)")
        for compound, count in rare_complex[:10]:
            print(f"  [{count}x] ({len(compound)} components): {', '.join(sorted(compound))}")

    # ── Write the artifact (B-29) ──
    results = {
        "meta": {
            "artifact": "compound_recipes_v2",
            "version": "2.0.0",
            "generated": datetime.utcnow().isoformat() + "Z",
            "divine_year": year_info["year"],
            "anchor_gregorian": year_info["anchor_gregorian"],
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "interval_minutes": INTERVAL,
            "total_steps": total,
            "skipped_nonexistent_steps": skipped,
            "location": {"name": "Damanhur", "lat": LAT, "lon": LON, "tz": TZ},
            "computation_time_seconds": round(elapsed, 1),
            # Pinned detector set (B-29): active-set fingerprints are only
            # comparable under an identical detector type list.
            "detector_set": {
                "compound_types": list(COMPOUND_TYPES),
                "resonance_boolean_types": list(RESONANCE_BOOLEAN_TYPES),
                "total_boolean_types": len(ALL_BOOLEAN),
            },
        },
        "complexity_histogram": {
            str(n): complexity_hist[n] for n in sorted(complexity_hist.keys())
        },
        "total_compound_steps": total_compound_steps,
        "unique_recipe_count": len(compound_registry),
        "singleton_recipe_count": len(singletons),
        "max_complexity": {
            "size": max_complexity,
            "components": sorted(max_compound),
            "first_occurrence": (
                max_timestamp.isoformat() if max_timestamp is not None else None
            ),
            "occurrence_count": max_count,
            "state_at_occurrence": max_state_summary,
        },
        # Every unique recipe, ranked by occurrence count.
        "recipes": [
            {"components": sorted(c), "size": len(c), "count": cnt}
            for c, cnt in ranked_recipes
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nArtifact written to {output_path}")
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Compound recipe analysis over one Divine Year",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help=f"Output JSON path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()
    main(output_path=args.output)
