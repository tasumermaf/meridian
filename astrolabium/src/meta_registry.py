"""
Astrolabium Caudae Rubrae — Meta-Registry Fail-Safe.

Two-level coverage check ensuring no register field goes untracked:

  Level 1 (Field Census): Every field in registers.json is catalogued in
           FIELD_REGISTRY as resonance-participating, compound-participating,
           identity, or structural. Uncatalogued fields = test failure.

  Level 2 (Resonance Coverage): Every field marked "resonance" has an entry
           in RESONANCE_PARTICIPATION linking it to specific resonance type(s).
           Unreferenced resonance fields = test failure.

The fail-safe breaks if registers.json gains new fields without
corresponding entries in this registry. That's the point.
"""

import json
from pathlib import Path
from typing import Dict, List, Set

_DATA_DIR = Path(__file__).parent.parent / "data"

# Dimensions that are lookup tables, not register dimensions
_SKIP_KEYS = {"meta", "vessel_remainder_map"}


def _load_json(filename: str) -> dict:
    with open(_DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Field Registry ──────────────────────────────────────────────────
# Every field in every register dimension must appear here.
# Categories:
#   resonance  — participates in cross-dimensional resonance detection
#   compound   — used in structural compound detection (detect_compounds)
#   identity   — names, labels, symbols, indices that identify the entry
#   structural — internal references, lookup keys, not cross-comparable

FIELD_REGISTRY = {
    "laws": {
        "resonance": [
            "trigram", "adonaj_ba", "color",
            "perception_pos", "perception_neg", "quest_tarot",
        ],
        "compound": ["is_solar_key"],
        "identity": ["symbol", "binary", "quest_short", "vowel", "mudra"],
        "structural": ["prime"],
    },
    "trigrams": {
        "resonance": ["wu_xing", "plum_blossom", "law"],
        "identity": ["symbol", "image", "action", "family", "nature", "direction", "season"],
        "structural": ["vessel"],
    },
    "vessels": {
        "resonance": ["polarity", "conf_meridian", "coup_meridian"],
        "compound": ["yin_day_restricted"],
        "identity": ["pair_partner", "confluent", "coupled", "english_name", "clinical_domain"],
        "structural": [
            "law", "prime",
            "conf_branch",
            "coup_branch",
        ],
    },
    "organs": {
        "resonance": ["element", "wing", "yin_yang", "paired"],
        "compound": [],
        "identity": [
            "branch_index", "branch_name", "branch_chinese",
            "organ", "abbr",
        ],
        "structural": ["conf_vessel", "coup_vessel"],
    },
    "inner_alchemy": {
        "resonance": ["color", "season", "neg", "pos"],
        "identity": ["organs", "sound", "spirit", "sense_organ", "body_tissue"],
    },
    "lunar_phases": {
        "resonance": ["trigram", "yang_count", "waxing"],
        "identity": ["index", "name", "elong_start", "elong_end", "symbol"],
        "structural": ["law", "prime"],
    },
    "solar_keys": {
        "compound": ["law", "trigram"],
        "identity": ["symbol", "event"],
        "structural": ["prime"],
    },
    "divine_hours": {
        "resonance": ["wing", "index"],
        "identity": ["roman", "position", "protocols"],
    },
    "divine_months": {
        "resonance": ["group", "great_rite", "iao", "alchemical"],
        "siloed": ["element"],  # Damanhurian element; Wu Xing cross-comparison prohibited
        "identity": ["number", "name", "tier_0_character"],
    },
    "sephirotic_days": {
        "resonance": ["planet"],
        "identity": ["day", "sephirah", "symbol", "pillar", "frequency"],
    },
}


# ── Resonance Participation Map ─────────────────────────────────────
# Every resonance-participating field (from FIELD_REGISTRY) maps to
# the resonance type(s) that cover it. If a field appears in
# FIELD_REGISTRY.resonance but not here, the consistency check fails.

RESONANCE_PARTICIPATION = {
    # Elemental (Wu Xing silo)
    "laws.trigram": [
        "wu_xing_element_match",
        "vessel_organ_element_match",
        "plum_blossom_wu_xing",
    ],
    "trigrams.wu_xing": [
        "wu_xing_element_match",
        "vessel_organ_element_match",
    ],
    "trigrams.plum_blossom": ["plum_blossom_wu_xing"],
    "organs.element": [
        "wu_xing_element_match",
        "vessel_organ_element_match",
        "plum_blossom_wu_xing",
        "color_affinity",
        "emotion_perception",
        "season_great_rite",
    ],

    # Qualitative (interpretive)
    "laws.color": ["color_affinity"],
    "laws.perception_pos": ["emotion_perception"],
    "laws.perception_neg": ["emotion_perception"],
    "laws.adonaj_ba": ["adonaj_ba_proximity"],
    "inner_alchemy.color": ["color_affinity"],
    "inner_alchemy.neg": ["emotion_perception"],
    "inner_alchemy.pos": ["emotion_perception"],

    # Elemental — Polarity
    "organs.yin_yang": ["organ_vessel_polarity"],
    "vessels.polarity": ["organ_vessel_polarity"],

    # Elemental — Stem-Trigram Polarity
    # is_yang_day comes from stem-branch engine (not a register field),
    # so we link via the trigram's law field as the bridge.
    "trigrams.law": ["stem_trigram_polarity"],

    # Elemental — Paired Organ × Vessel Point
    "organs.paired": ["paired_organ_vessel_point"],
    "vessels.conf_meridian": ["paired_organ_vessel_point"],
    "vessels.coup_meridian": ["paired_organ_vessel_point"],

    # Rhythmic
    "lunar_phases.waxing": ["waxing_wing_alignment"],
    "organs.wing": ["waxing_wing_alignment"],
    "divine_hours.wing": ["waxing_wing_alignment", "divine_hour_law_unity"],
    "divine_hours.index": ["divine_hour_law_unity"],
    "lunar_phases.yang_count": ["yang_count"],
    "lunar_phases.trigram": ["wu_xing_element_match"],

    # Calendrical
    "laws.quest_tarot": ["sephirotic_quest_match"],
    "sephirotic_days.planet": ["sephirotic_quest_match"],
    "inner_alchemy.season": ["season_great_rite"],
    "divine_months.great_rite": ["season_great_rite"],
    "divine_months.group": ["month_group"],
    "divine_months.iao": ["iao_position"],
    "divine_months.alchemical": ["alchemical_stage"],
}


def _get_register_fields(registers: dict) -> Dict[str, Set[str]]:
    """Extract {dimension: set_of_fields} from registers.json programmatically."""
    result = {}
    for dim, data in registers.items():
        if dim in _SKIP_KEYS:
            continue
        if isinstance(data, dict):
            for key, entry in data.items():
                if isinstance(entry, dict):
                    result[dim] = set(entry.keys())
                    break
        elif isinstance(data, list) and data:
            result[dim] = set(data[0].keys())
    return result


def _get_catalogued_fields() -> Dict[str, Set[str]]:
    """Flatten FIELD_REGISTRY into {dimension: set_of_all_fields}."""
    result = {}
    for dim, categories in FIELD_REGISTRY.items():
        fields = set()
        for cat_fields in categories.values():
            fields.update(cat_fields)
        result[dim] = fields
    return result


def _get_resonance_field_specs() -> Set[str]:
    """Return all 'dimension.field' specs marked as resonance-participating."""
    specs = set()
    for dim, categories in FIELD_REGISTRY.items():
        for field in categories.get("resonance", []):
            specs.add(f"{dim}.{field}")
    return specs


def check_coverage() -> dict:
    """
    Two-level coverage check.

    Level 1: Every field in registers.json is catalogued in FIELD_REGISTRY.
    Level 2: Every resonance field has entries in RESONANCE_PARTICIPATION,
             and those entries reference valid resonance types.

    Returns a report dict.
    """
    registers = _load_json("registers.json")
    resonances = _load_json("resonances.json")
    resonance_type_names = set(resonances.get("resonance_types", {}).keys())

    # ── Level 1: Field Census ──
    actual_fields = _get_register_fields(registers)
    catalogued_fields = _get_catalogued_fields()

    uncatalogued_fields = []
    for dim in sorted(actual_fields.keys()):
        if dim not in catalogued_fields:
            for f in sorted(actual_fields[dim]):
                uncatalogued_fields.append(f"{dim}.{f}")
        else:
            for f in sorted(actual_fields[dim] - catalogued_fields[dim]):
                uncatalogued_fields.append(f"{dim}.{f}")

    # ── Level 2: Resonance Coverage ──
    resonance_specs = _get_resonance_field_specs()

    # 2a: Every resonance spec must be in RESONANCE_PARTICIPATION
    missing_participation = []
    for spec in sorted(resonance_specs):
        if spec not in RESONANCE_PARTICIPATION:
            missing_participation.append(spec)

    # 2b: Every RESONANCE_PARTICIPATION entry must reference valid types
    invalid_types = []
    for spec, types in sorted(RESONANCE_PARTICIPATION.items()):
        for t in types:
            if t not in resonance_type_names:
                invalid_types.append(f"{spec} → {t}")

    # 2c: Every RESONANCE_PARTICIPATION entry must be in resonance_specs
    orphan_participation = []
    for spec in sorted(RESONANCE_PARTICIPATION.keys()):
        if spec not in resonance_specs:
            orphan_participation.append(spec)

    total_register = sum(len(f) for f in actual_fields.values())
    total_catalogued = sum(len(f) for f in catalogued_fields.values())

    return {
        "level_1": {
            "total_register_fields": total_register,
            "total_catalogued": total_catalogued,
            "uncatalogued_fields": uncatalogued_fields,
            "uncatalogued_count": len(uncatalogued_fields),
        },
        "level_2": {
            "resonance_fields": len(resonance_specs),
            "participation_entries": len(RESONANCE_PARTICIPATION),
            "missing_participation": missing_participation,
            "missing_count": len(missing_participation),
            "invalid_types": invalid_types,
            "invalid_count": len(invalid_types),
            "orphan_participation": orphan_participation,
            "orphan_count": len(orphan_participation),
        },
    }


if __name__ == "__main__":
    result = check_coverage()
    print("Meta-Registry Coverage Report")
    print("=" * 60)

    L1 = result["level_1"]
    print(f"\nLevel 1 — Field Census")
    print(f"  Register fields:   {L1['total_register_fields']}")
    print(f"  Catalogued fields: {L1['total_catalogued']}")
    print(f"  Uncatalogued:      {L1['uncatalogued_count']}")
    if L1["uncatalogued_fields"]:
        for f in L1["uncatalogued_fields"]:
            print(f"    ! {f}")

    L2 = result["level_2"]
    print(f"\nLevel 2 — Resonance Coverage")
    print(f"  Resonance fields:       {L2['resonance_fields']}")
    print(f"  Participation entries:   {L2['participation_entries']}")
    print(f"  Missing participation:   {L2['missing_count']}")
    if L2["missing_participation"]:
        for f in L2["missing_participation"]:
            print(f"    ! {f}")
    print(f"  Invalid type references: {L2['invalid_count']}")
    if L2["invalid_types"]:
        for f in L2["invalid_types"]:
            print(f"    ! {f}")
    print(f"  Orphan entries:          {L2['orphan_count']}")
    if L2["orphan_participation"]:
        for f in L2["orphan_participation"]:
            print(f"    ! {f}")

    total_issues = (
        L1["uncatalogued_count"]
        + L2["missing_count"]
        + L2["invalid_count"]
        + L2["orphan_count"]
    )
    print(f"\n{'=' * 60}")
    if total_issues == 0:
        print("PASS — Full coverage achieved.")
    else:
        print(f"FAIL — {total_issues} issue(s) found.")
