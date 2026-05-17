"""
Format the computed periodic table JSON into the v3 Markdown specification.

Usage:
    cd astrolabium/code
    python -m scripts.format_periodic_table [--input data/periodic_table_v3.json]
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

MONTH_NAMES = {
    1: "ISIS", 2: "SADAM", 3: "LIOTHIL", 4: "EOROS",
    5: "TASUMER", 6: "MENON", 7: "OSIRIS", 8: "AGAFEST",
    9: "SAMMA", 10: "SET", 11: "SADAS", 12: "DESURIORIS",
    13: "VADUSFADAHM",
}

# Human-readable names for compound and resonance types
TYPE_LABELS = {
    # Compounds
    "two_body_unity": "Two-Body Unity (P == D)",
    "confluent_intersection": "Confluent Intersection",
    "coupled_intersection": "Coupled Intersection",
    "full_confluent": "Full Confluent (Unity + CI)",
    "full_coupled": "Full Coupled (Unity + CoI)",
    "key_derivative_unity": "Key-Derivative Unity",
    "conditional_3_4": "Conditional 3/4",
    "conditional_3_5": "Conditional 3/5",
    # Resonances
    "wu_xing_element_match": "Wu Xing Element Match (R_WX_01)",
    "vessel_organ_element_match": "Vessel-Organ Element (R_WX_02)",
    "plum_blossom_wu_xing": "Plum Blossom Wu Xing (R_WX_03)",
    "color_affinity": "Color Affinity (R_CLR_01)",
    "emotion_perception": "Emotion-Perception (R_EPR_01)",
    "adonaj_ba_proximity": "Adonaj-Ba Proximity (R_ABD_01)",
    "waxing_wing_alignment": "Waxing-Wing Alignment (R_LUN_01)",
    "sephirotic_quest_match": "Sephirotic Quest Match (R_SPH_01)",
    "season_great_rite": "Season-Great Rite (R_SEA_01)",
}

TYPE_AB = {
    "two_body_unity": "A", "confluent_intersection": "A",
    "coupled_intersection": "A", "full_confluent": "A",
    "full_coupled": "A", "key_derivative_unity": "A",
    "conditional_3_4": "A", "conditional_3_5": "A",
    "wu_xing_element_match": "A", "vessel_organ_element_match": "A",
    "plum_blossom_wu_xing": "A", "color_affinity": "B",
    "emotion_perception": "B", "adonaj_ba_proximity": "B",
    "waxing_wing_alignment": "A", "sephirotic_quest_match": "A",
    "season_great_rite": "A",
}

CATEGORIES = {
    "two_body_unity": "Structural", "confluent_intersection": "Structural",
    "coupled_intersection": "Structural", "full_confluent": "Structural",
    "full_coupled": "Structural", "key_derivative_unity": "Structural",
    "conditional_3_4": "Structural", "conditional_3_5": "Structural",
    "wu_xing_element_match": "Elemental", "vessel_organ_element_match": "Elemental",
    "plum_blossom_wu_xing": "Elemental", "color_affinity": "Qualitative",
    "emotion_perception": "Qualitative", "adonaj_ba_proximity": "Qualitative",
    "waxing_wing_alignment": "Rhythmic", "sephirotic_quest_match": "Calendrical",
    "season_great_rite": "Calendrical",
}


def format_periodic_table(data: dict) -> str:
    meta = data["meta"]
    freq = data["frequency_table"]
    cooccur = data["cooccurrence"]
    dists = data["distributions"]
    sv_dists = data["state_value_distributions"]
    month_prof = data["month_profiles"]
    yin = data["yin_day_blocked"]

    lines = []

    def w(s=""):
        lines.append(s)

    # ── Header ──
    w("# ASTROLABIUM CAUDAE RUBRAE")
    w("## Periodic Table of Compounds and Resonances v3")
    w(f"### Computed {meta['generated'][:10]} — Divine Year {meta['divine_year']}")
    w()
    w("---")
    w()
    w("## COMPUTATION PARAMETERS")
    w()
    w(f"| Parameter | Value |")
    w(f"|-----------|-------|")
    w(f"| Divine Year | **{meta['divine_year']}** (Gregorian anchor: {meta['anchor_gregorian']}) |")
    w(f"| Start | {meta['start']} |")
    w(f"| End | {meta['end']} |")
    w(f"| Duration | {meta['duration_days']} days |")
    w(f"| Total months | {meta['total_months']} ({'intercalary' if meta['is_intercalary'] else 'standard'}) |")
    w(f"| Location | Damanhur ({meta['location']['lat']}°N, {meta['location']['lon']}°E) |")
    w(f"| Timezone | {meta['location']['tz']} |")
    w(f"| Sampling interval | {meta['interval_minutes']} minutes |")
    w(f"| Total samples | {meta['total_steps']:,} |")
    w(f"| Computation time | {meta['computation_time_seconds']}s |")
    w()
    w("---")
    w()

    # ── Main Frequency Table ──
    w("## FREQUENCY TABLE — All 17 Boolean Phenomena")
    w()
    w("The Astrolabium tracks **8 structural compounds** (mechanical timing alignments)")
    w("and **9 boolean resonances** (cross-dimensional alignments). This table shows")
    w("their computed frequency across one complete Divine Year at Damanhur.")
    w()

    # Sort by frequency (descending)
    sorted_types = sorted(
        freq.keys(),
        key=lambda k: freq[k]["count"],
        reverse=True,
    )

    w("| Rank | Phenomenon | Category | Type | Count | % of Time | Steps Active |")
    w("|------|-----------|----------|------|------:|----------:|---------:|")

    for rank, t in enumerate(sorted_types, 1):
        entry = freq[t]
        label = TYPE_LABELS.get(t, t)
        cat = CATEGORIES.get(t, "?")
        ab = TYPE_AB.get(t, "?")
        w(f"| {rank} | {label} | {cat} | {ab} | {entry['count']:,} | {entry['pct']:.2f}% | {entry['count']:,} |")

    w()

    # Yin-day blocking
    w(f"**Yin-Day Blocking:** {yin['count']:,} steps ({yin['pct']:.2f}%) fell on Yin days. "
      f"Raw Two-Body Unity count (before yin-day filter): {yin['raw_unity']:,}.")
    w()
    w("---")
    w()

    # ── State-Value Distributions ──
    w("## STATE-VALUE DISTRIBUTIONS")
    w()
    w("These resonances produce categorical values rather than boolean states.")
    w()

    # Alchemical
    w("### Alchemical Stage (R_CAL_01)")
    w()
    w("| Stage | Count | % |")
    w("|-------|------:|--:|")
    for stage in ["Nigredo", "Albedo", "Rubedo", "Da'ath"]:
        cnt = sv_dists["alchemical_stage"].get(stage, 0)
        pct = round(cnt / meta["total_steps"] * 100, 2) if meta["total_steps"] > 0 else 0
        w(f"| {stage} | {cnt:,} | {pct:.2f}% |")
    w()

    # Month Group
    w("### Month Group (R_CAL_02)")
    w()
    w("| Group | Count | % |")
    w("|-------|------:|--:|")
    for grp in ["Osirian", "Falcon", "Operative", "Tappetino"]:
        cnt = sv_dists["month_group"].get(grp, 0)
        pct = round(cnt / meta["total_steps"] * 100, 2) if meta["total_steps"] > 0 else 0
        w(f"| {grp} | {cnt:,} | {pct:.2f}% |")
    w()

    # IAO
    w("### IAO Position (R_CAL_03)")
    w()
    w("| Letter | Count | % |")
    w("|--------|------:|--:|")
    for letter in ["I", "O", "A", "null"]:
        cnt = sv_dists["iao_position"].get(letter, 0)
        pct = round(cnt / meta["total_steps"] * 100, 2) if meta["total_steps"] > 0 else 0
        label = letter if letter != "null" else "(none)"
        w(f"| {label} | {cnt:,} | {pct:.2f}% |")
    w()

    # Yang Count
    w("### Yang Count Progression (R_LUN_02)")
    w()
    w("| Yang Lines | Count | % |")
    w("|------------|------:|--:|")
    for yc in sorted(sv_dists["yang_count"].keys(), key=lambda x: int(x)):
        cnt = sv_dists["yang_count"][yc]
        pct = round(cnt / meta["total_steps"] * 100, 2) if meta["total_steps"] > 0 else 0
        w(f"| {yc} | {cnt:,} | {pct:.2f}% |")
    w()
    w("---")
    w()

    # ── Law Distributions ──
    w("## LAW DISTRIBUTIONS")
    w()
    w("### Primeval Law (Soul Body — Lunar Phase)")
    w()
    w("| Law | Count | % |")
    w("|-----|------:|--:|")
    for law, cnt in sorted(dists["primeval_law"].items(), key=lambda x: -x[1]):
        pct = round(cnt / meta["total_steps"] * 100, 2)
        w(f"| {law} | {cnt:,} | {pct:.2f}% |")
    w()

    w("### Derivative Law (Astral Body — LGBF)")
    w()
    w("| Law | Count | % |")
    w("|-----|------:|--:|")
    for law, cnt in sorted(dists["derivative_law"].items(), key=lambda x: -x[1]):
        pct = round(cnt / meta["total_steps"] * 100, 2)
        w(f"| {law} | {cnt:,} | {pct:.2f}% |")
    w()

    # ── Per-Law Compound Breakdown ──
    w("### Per-Law Compound Activity")
    w()
    w("Which Primeval Law was active when each compound/resonance fired:")
    w()

    # Pick the most frequent types (top 10)
    top_types = sorted_types[:10]

    for t in top_types:
        entry = freq[t]
        by_law = entry.get("by_law", {})
        if not by_law:
            continue
        label = TYPE_LABELS.get(t, t)
        w(f"**{label}** ({entry['count']:,} total)")
        w()
        w("| Law | Count | % of type |")
        w("|-----|------:|----------:|")
        for law, cnt in sorted(by_law.items(), key=lambda x: -x[1]):
            pct = round(cnt / entry["count"] * 100, 1) if entry["count"] > 0 else 0
            w(f"| {law} | {cnt:,} | {pct:.1f}% |")
        w()

    w("---")
    w()

    # ── Other Distributions ──
    w("## TEMPORAL DISTRIBUTIONS")
    w()

    w("### Lunar Phase")
    w()
    w("| Phase | Count | % |")
    w("|-------|------:|--:|")
    for phase, cnt in sorted(dists["lunar_phase"].items(), key=lambda x: -x[1]):
        pct = round(cnt / meta["total_steps"] * 100, 2)
        w(f"| {phase} | {cnt:,} | {pct:.2f}% |")
    w()

    w("### Vessel (LGBF)")
    w()
    w("| Vessel | Count | % |")
    w("|--------|------:|--:|")
    for vessel, cnt in sorted(dists["vessel"].items(), key=lambda x: -x[1]):
        pct = round(cnt / meta["total_steps"] * 100, 2)
        w(f"| {vessel} | {cnt:,} | {pct:.2f}% |")
    w()

    w("### Organ Clock")
    w()
    w("| Organ | Count | % |")
    w("|-------|------:|--:|")
    for organ, cnt in sorted(dists["organ"].items(), key=lambda x: -x[1]):
        pct = round(cnt / meta["total_steps"] * 100, 2)
        w(f"| {organ} | {cnt:,} | {pct:.2f}% |")
    w()
    w("---")
    w()

    # ── Per-Month Profiles ──
    w("## PER-MONTH FREQUENCY PROFILES")
    w()
    w("How each compound/resonance distributes across the 12-13 Divine Months.")
    w()

    # Build a compact table with months as columns, types as rows
    month_nums = sorted(int(k) for k in month_prof.keys())

    # Header row
    header = "| Phenomenon |"
    sep = "|-----------|"
    for m in month_nums:
        name = MONTH_NAMES.get(m, f"M{m}")
        header += f" {name} |"
        sep += "---:|"
    w(header)
    w(sep)

    # Select meaningful types for the per-month table
    meaningful_types = [t for t in sorted_types if freq[t]["count"] > 0]

    for t in meaningful_types:
        label = TYPE_LABELS.get(t, t)
        # Truncate label for table readability
        short_label = label.split("(")[0].strip()
        if len(short_label) > 28:
            short_label = short_label[:25] + "..."
        row = f"| {short_label} |"
        for m in month_nums:
            m_data = month_prof.get(str(m), {})
            cnt = m_data.get(t, 0)
            m_total = m_data.get("_total", 1)
            pct = round(cnt / m_total * 100, 1) if m_total > 0 else 0
            row += f" {pct:.1f}% |"
        w(row)
    w()
    w("---")
    w()

    # ── Co-occurrence Matrix ──
    w("## CO-OCCURRENCE MATRIX")
    w()
    w("Which Boolean phenomena tend to fire simultaneously.")
    w("Only pairs with > 0 co-occurrences shown.")
    w()
    w("| Pair | Co-occurrences | % of Total Steps |")
    w("|------|---------------:|-----------------:|")

    sorted_pairs = sorted(cooccur.items(), key=lambda x: -x[1])[:40]  # Top 40

    for pair_key, count in sorted_pairs:
        a, b = pair_key.split("|")
        label_a = TYPE_LABELS.get(a, a).split("(")[0].strip()
        label_b = TYPE_LABELS.get(b, b).split("(")[0].strip()
        pct = round(count / meta["total_steps"] * 100, 3) if meta["total_steps"] > 0 else 0
        w(f"| {label_a} + {label_b} | {count:,} | {pct:.3f}% |")

    w()
    w("---")
    w()

    # ── Summary Statistics ──
    w("## SUMMARY")
    w()

    total_compound_active = sum(freq[c]["count"] for c in freq if freq[c].get("type") == "compound")
    total_resonance_active = sum(freq[r]["count"] for r in freq if freq[r].get("type") == "resonance")

    w(f"- **Total samples:** {meta['total_steps']:,}")
    w(f"- **Boolean phenomena tracked:** {len(freq)} (8 compounds + 9 resonances)")
    w(f"- **State-value phenomena tracked:** 4 (alchemical, month_group, IAO, yang_count)")
    w(f"- **Total compound activations:** {total_compound_active:,}")
    w(f"- **Total resonance activations:** {total_resonance_active:,}")

    most_common = sorted_types[0]
    least_common = [t for t in sorted_types if freq[t]["count"] > 0][-1] if any(
        freq[t]["count"] > 0 for t in sorted_types
    ) else None

    w(f"- **Most frequent:** {TYPE_LABELS.get(most_common, most_common)} ({freq[most_common]['pct']:.2f}%)")
    if least_common:
        w(f"- **Least frequent (nonzero):** {TYPE_LABELS.get(least_common, least_common)} ({freq[least_common]['pct']:.2f}%)")

    never_fired = [t for t in sorted_types if freq[t]["count"] == 0]
    if never_fired:
        w(f"- **Never active:** {', '.join(TYPE_LABELS.get(t, t).split('(')[0].strip() for t in never_fired)}")

    w(f"- **Co-occurrence pairs observed:** {len(cooccur)}")
    w()
    w("---")
    w()
    w("## ATTRIBUTION")
    w()
    w("- **8 structural compounds:** defined in `detect_compounds()` (astrolabium.py)")
    w("- **9 boolean resonances:** defined in `detect_resonances()` (resonance.py)")
    w("- **4 state-value resonances:** tracked as distributions")
    w("- **13 resonance type definitions:** `data/resonances.json`")
    w("- **Field coverage fail-safe:** `src/meta_registry.py` (82 fields, 23 resonance-participating)")
    w("- **Register data:** `data/registers.json` (locked)")
    w()
    w("Computation: `scripts/compute_periodic_table.py`")
    w(f"Generated: {meta['generated']}")
    w()

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Format Periodic Table v3 Markdown")
    parser.add_argument(
        "--input", type=str,
        default=str(Path(__file__).parent.parent / "data" / "periodic_table_v3.json"),
    )
    parser.add_argument(
        "--output", type=str,
        default=str(
            Path(__file__).parent.parent.parent
            / "docs" / "specs" / "astrolabium_periodic_table_v3.md"
        ),
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    md = format_periodic_table(data)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Written to {args.output}")
    print(f"Lines: {len(md.splitlines())}")
