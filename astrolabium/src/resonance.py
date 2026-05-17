"""
Astrolabium Caudae Rubrae — Resonance Scanner.

Detects cross-dimensional resonances beyond the 18 structural compounds.
17 resonance types across 4 categories: elemental, qualitative, rhythmic,
calendrical. All lookup data from data/resonances.json.

Zero breaking changes to existing compound detection.
"""

import json
from pathlib import Path
from typing import Dict, Optional

_RESONANCE_DATA = None
_JSON_PATH = Path(__file__).parent.parent / "data" / "resonances.json"

# Registry import for cross-lookups
from . import registry


def _load_resonances() -> dict:
    global _RESONANCE_DATA
    if _RESONANCE_DATA is None:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            _RESONANCE_DATA = json.load(f)
    return _RESONANCE_DATA


# ── Boolean resonance type names (produce active/inactive) ──

RESONANCE_BOOLEAN_TYPES = [
    "wu_xing_element_match",
    "vessel_organ_element_match",
    "plum_blossom_wu_xing",
    "stem_trigram_polarity",
    "organ_vessel_polarity",
    "paired_organ_vessel_point",
    "color_affinity",
    "emotion_perception",
    "adonaj_ba_proximity",
    "waxing_wing_alignment",
    "sephirotic_quest_match",
    "season_great_rite",
]

# State-value types (produce distribution values, not boolean)
RESONANCE_STATE_TYPES = [
    "yang_count",
    "divine_hour_law_unity",
    "alchemical_stage",
    "month_group",
    "iao_position",
]

ALL_RESONANCE_TYPES = RESONANCE_BOOLEAN_TYPES + RESONANCE_STATE_TYPES


def detect_resonances(state: dict) -> dict:
    """
    Detect all cross-dimensional resonances from the assembled state.

    Returns nested dict by category: elemental, qualitative, rhythmic,
    calendrical. Parallel to detect_compounds() — additive, not replacing.
    """
    data = _load_resonances()
    lookups = data["lookup_tables"]

    # Extract common state values
    primeval_trigram = state["primeval"]["trigram"]
    primeval_law = state["primeval"]["law"]
    organ_element = state["organ_clock"]["element"]
    organ_name = state["organ_clock"]["organ"]
    wing = state["organ_clock"]["wing"]
    waxing = state["primeval"]["waxing"]

    # Get law data from registry
    law_data = registry.get_law(primeval_law)

    # Get inner alchemy data via organ name (handles San Jiao/Pericardium split)
    alchemy_data = registry.get_inner_alchemy_for_organ(organ_name)

    # Get trigram data
    trigram_data = registry.all_trigrams().get(primeval_trigram, {})

    active_count = 0
    total_boolean = len(RESONANCE_BOOLEAN_TYPES)

    # ── Category: Elemental ──

    # R_WX_01: Trigram Wu Xing × Organ Wu Xing
    trigram_wx = lookups["trigram_wu_xing"].get(primeval_trigram)
    wx_match = trigram_wx == organ_element if trigram_wx else False
    if wx_match:
        active_count += 1

    # R_WX_02: Vessel-Organ Element Match
    # Derivative vessel → its law → that law's trigram → wu xing
    deriv_law = state["derivative"]["law"]
    deriv_law_data = registry.get_law(deriv_law)
    deriv_trigram = deriv_law_data["trigram"]
    deriv_wx = lookups["trigram_wu_xing"].get(deriv_trigram)
    vessel_organ_match = deriv_wx == organ_element if deriv_wx else False
    if vessel_organ_match:
        active_count += 1

    # R_WX_03: Plum Blossom × Organ Wu Xing
    plum_blossom = trigram_data.get("plum_blossom")
    pb_wx = lookups["plum_blossom_wu_xing_map"].get(plum_blossom) if plum_blossom else None
    pb_match = pb_wx == organ_element if pb_wx else False
    if pb_match:
        active_count += 1

    # R_WX_04: Stem Polarity × Trigram Polarity
    is_yang_day = state.get("stem_branch", {}).get("is_yang_day")
    trigram_pol = lookups.get("trigram_polarity", {}).get(primeval_trigram)
    if is_yang_day is not None and trigram_pol is not None:
        stem_trigram_match = (
            (is_yang_day and trigram_pol == "Yang")
            or (not is_yang_day and trigram_pol == "Yin")
        )
    else:
        stem_trigram_match = False
    if stem_trigram_match:
        active_count += 1

    # R_WX_05: Organ Yin/Yang × Vessel Polarity
    organ_yin_yang = state["organ_clock"].get("yin_yang")
    vessel_polarity = state["derivative"].get("polarity")
    if organ_yin_yang and vessel_polarity:
        organ_vessel_match = organ_yin_yang == vessel_polarity
    else:
        organ_vessel_match = False
    if organ_vessel_match:
        active_count += 1

    # R_AN_01: Paired Organ × Vessel Point
    paired_organ_name = state["organ_clock"].get("paired")
    paired_conf = False
    paired_coup = False
    if paired_organ_name:
        try:
            paired_data = registry.get_organ_by_name(paired_organ_name)
            paired_branch = paired_data["branch_index"]
            paired_meridian = paired_data["abbr"]
            conf_branch = state["derivative"].get("conf_branch")
            conf_meridian = state["derivative"].get("conf_meridian")
            coup_branch = state["derivative"].get("coup_branch")
            coup_meridian = state["derivative"].get("coup_meridian")
            paired_conf = (
                conf_branch == paired_branch
                and conf_meridian == paired_meridian
            )
            paired_coup = (
                coup_branch == paired_branch
                and coup_meridian == paired_meridian
            )
        except KeyError:
            pass
    paired_any = paired_conf or paired_coup
    if paired_any:
        active_count += 1

    elemental = {
        "wu_xing_element_match": {
            "active": wx_match,
            "primeval_wx": trigram_wx,
            "organ_wx": organ_element,
        },
        "vessel_organ_element_match": {
            "active": vessel_organ_match,
            "derivative_wx": deriv_wx,
            "organ_wx": organ_element,
        },
        "plum_blossom_wu_xing": {
            "active": pb_match,
            "plum_blossom": plum_blossom,
            "plum_blossom_wx": pb_wx,
            "organ_wx": organ_element,
        },
        "stem_trigram_polarity": {
            "active": stem_trigram_match,
            "is_yang_day": is_yang_day,
            "trigram_polarity": trigram_pol,
        },
        "organ_vessel_polarity": {
            "active": organ_vessel_match,
            "organ_yin_yang": organ_yin_yang,
            "vessel_polarity": vessel_polarity,
        },
        "paired_organ_vessel_point": {
            "active": paired_any,
            "paired_organ": paired_organ_name,
            "paired_confluent": paired_conf,
            "paired_coupled": paired_coup,
        },
    }

    # ── Category: Qualitative ──

    # R_CLR_01: Law-Organ Color Affinity
    law_color = law_data.get("color", "")
    healing_color = alchemy_data.get("color", "")
    color_key = f"{law_color}:{healing_color}" if law_color and healing_color else ""
    color_grade = lookups["color_affinity_map"].get(color_key, "NONE")
    color_active = color_grade != "NONE"
    if color_active:
        active_count += 1

    # R_EPR_01: Emotion-Perception Resonance
    # Check both positive and negative polarities
    ep_grade = "NONE"
    ep_polarity = None
    for pol in ("pos", "neg"):
        ep_key = f"{primeval_law}:{organ_element}:{pol}"
        g = lookups["emotion_perception_map"].get(ep_key)
        if g and (ep_grade == "NONE" or g == "EXACT"):
            ep_grade = g
            ep_polarity = pol
    ep_active = ep_grade != "NONE"
    if ep_active:
        active_count += 1

    # R_ABD_01: Adonaj-Ba Organ Proximity
    adonaj_ba = law_data.get("adonaj_ba", "")
    abd_key = f"{adonaj_ba}:{organ_name}" if adonaj_ba else ""
    abd_grade = lookups["adonaj_ba_organ_map"].get(abd_key, "NONE")
    abd_active = abd_grade != "NONE"
    if abd_active:
        active_count += 1

    qualitative = {
        "color_affinity": {
            "active": color_active,
            "grade": color_grade,
            "law_color": law_color,
            "healing_color": healing_color,
        },
        "emotion_perception": {
            "active": ep_active,
            "grade": ep_grade,
            "polarity": ep_polarity,
            "law": primeval_law,
            "element": organ_element,
        },
        "adonaj_ba_proximity": {
            "active": abd_active,
            "grade": abd_grade,
            "adonaj_ba": adonaj_ba,
            "organ": organ_name,
        },
    }

    # ── Category: Rhythmic ──

    # R_LUN_01: Waxing/Waning-Wing Alignment
    waxing_wing = (waxing and wing == "Day") or (not waxing and wing == "Night")
    if waxing_wing:
        active_count += 1

    # R_LUN_02: Yang Count (state value — not boolean)
    phase_index = state["primeval"]["phase_index"]
    phase_data = registry.get_lunar_phase(phase_index)
    yang_count_val = phase_data["yang_count"]

    # R_RHY_02: Divine Hour × Law Unity (state value)
    compounds = state.get("compounds", {})
    divine_hour = state.get("divine_hour", {})
    dh_law_unity = None
    if compounds.get("two_body_unity"):
        dh_law_unity = {
            "hour_index": divine_hour.get("index"),
            "hour_roman": divine_hour.get("roman"),
            "wing": divine_hour.get("wing"),
        }

    rhythmic = {
        "waxing_wing_alignment": {
            "active": waxing_wing,
            "waxing": waxing,
            "wing": wing,
        },
        "yang_count": yang_count_val,
        "divine_hour_law_unity": dh_law_unity,
    }

    # ── Category: Calendrical ──

    cal = state.get("calendar", {})

    # R_SPH_01: Sephirotic Planet-Quest Attribution Match
    seph_planet = cal.get("sephirotic_planet")
    quest_tarot = law_data.get("quest_tarot")
    # Get the quest card's Continental attribution
    quest_attr = lookups["quest_planet_map"].get(quest_tarot)
    # Map to sephirotic planet name
    quest_seph = lookups["quest_to_sephirotic_planet"].get(quest_attr)
    seph_quest_match = (
        seph_planet is not None
        and quest_seph is not None
        and seph_planet == quest_seph
    )
    if seph_quest_match:
        active_count += 1

    # R_SEA_01: Season-Great Rite Alignment
    organ_season = alchemy_data.get("season")
    great_rite = cal.get("great_rite")
    season_key = f"{organ_season}:{great_rite}" if organ_season and great_rite else ""
    season_match = lookups["season_great_rite_map"].get(season_key, False)
    if season_match:
        active_count += 1

    # State values (non-boolean)
    alchemical = cal.get("alchemical")
    month_group = cal.get("month_group")

    # IAO from divine_months registry
    month_num = cal.get("month_number")
    iao = None
    if month_num:
        month_data = registry.get_divine_month(month_num)
        iao = month_data.get("iao")

    calendrical = {
        "sephirotic_quest_match": {
            "active": seph_quest_match,
            "sephirotic_planet": seph_planet,
            "quest_tarot": quest_tarot,
            "quest_attribution": quest_attr,
        },
        "season_great_rite": {
            "active": season_match,
            "organ_season": organ_season,
            "great_rite": great_rite,
        },
        "alchemical_stage": alchemical,
        "month_group": month_group,
        "iao_position": iao,
    }

    return {
        "elemental": elemental,
        "qualitative": qualitative,
        "rhythmic": rhythmic,
        "calendrical": calendrical,
        "active_count": active_count,
        "total_checked": total_boolean,
    }
