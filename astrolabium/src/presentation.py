"""
Astrolabium Caudae Rubrae — Presentation Layer.

Transforms the raw computational state into Damanhurian-first,
practitioner-readable output. No Chinese characters, no insider
shorthand, no pinyin branch names. Trigram symbols preserved.
Acupuncture points use medical designation + plain English.
Extraordinary Vessels use English names, framed as containers
for their Law.

The raw state is the mathematical truth. The presentation layer
is the practitioner's interface to that truth.
"""

from typing import Dict, Optional

from . import registry


# ── Vessel English Names ──────────────────────────────────────────

VESSEL_ENGLISH = {
    "Du Mai": "Governing Vessel",
    "Ren Mai": "Conception Vessel",
    "Chong Mai": "Penetrating Vessel",
    "Dai Mai": "Belt Vessel",
    "Yang Qiao Mai": "Yang Heel Vessel",
    "Yin Qiao Mai": "Yin Heel Vessel",
    "Yang Wei Mai": "Yang Linking Vessel",
    "Yin Wei Mai": "Yin Linking Vessel",
}

# ── Trigram Nature Names ──────────────────────────────────────────

TRIGRAM_NATURE = {
    "Qián": "Heaven",
    "Kūn": "Earth",
    "Zhèn": "Thunder",
    "Xùn": "Wind",
    "Kǎn": "Water",
    "Lí": "Fire",
    "Gèn": "Mountain",
    "Duì": "Lake",
}

# ── Solar Key → Vessel Mapping ────────────────────────────────────

KEY_VESSEL = {
    "gold": {"vessel": "Yin Heel Vessel", "vessel_code": "Yin Qiao Mai"},
    "silver": {"vessel": "Yang Heel Vessel", "vessel_code": "Yang Qiao Mai"},
}

# ── Meridian Full Names ───────────────────────────────────────────

MERIDIAN_NAMES = {
    "LU": "Lung",
    "LI": "Large Intestine",
    "ST": "Stomach",
    "SP": "Spleen",
    "HT": "Heart",
    "SI": "Small Intestine",
    "BL": "Bladder",
    "KI": "Kidney",
    "PC": "Pericardium",
    "SJ": "San Jiao",
    "GB": "Gallbladder",
    "LR": "Liver",
}

# ── Acupuncture Point Descriptions ───────────────────────────────

POINT_DESCRIPTIONS = {
    "SI-3": "On the ulnar border of the hand, in the depression proximal to the 5th metacarpal head",
    "BL-62": "In the depression below the lateral malleolus (outer ankle bone)",
    "LU-7": "On the radial side of the forearm, 1.5 cun above the wrist crease",
    "KI-6": "In the depression below the medial malleolus (inner ankle bone)",
    "SP-4": "On the medial side of the foot, in the depression distal to the 1st metatarsal base",
    "PC-6": "On the inner forearm, 2 cun above the wrist crease, between the tendons",
    "GB-41": "On the dorsum of the foot, in the depression distal to the 4th and 5th metatarsal junction",
    "SJ-5": "On the outer forearm, 2 cun above the wrist crease, between radius and ulna",
}

# ── Compound Display Names and Descriptions ──────────────────────

COMPOUND_DISPLAY = {
    "two_body_unity": {
        "name": "Two-Body Law Unity",
        "description": "The Soul and Astral bodies carry the same Law",
    },
    "key_derivative_unity": {
        "name": "Key-Vessel Unity",
        "description": "The active Solar Key carries the same Law as the open Vessel",
    },
    "confluent_intersection": {
        "name": "Confluent Intersection",
        "description": "The open Vessel's confluent point falls on the active meridian",
    },
    "coupled_intersection": {
        "name": "Coupled Intersection",
        "description": "The open Vessel's coupled point falls on the active meridian",
    },
    "full_confluent": {
        "name": "Full Confluent Alignment",
        "description": "Law Unity with the confluent point on the active meridian",
    },
    "full_coupled": {
        "name": "Full Coupled Alignment",
        "description": "Law Unity with the coupled point on the active meridian",
    },
    "conditional_3_4": {
        "name": "Silver Key + Confluent",
        "description": "Silver Key active while confluent point is on the active meridian",
    },
    "conditional_3_5": {
        "name": "Gold Key + Coupled",
        "description": "Gold Key active while coupled point is on the active meridian",
    },
    "yin_day_blocked": {
        "name": "Yin-Day Gate",
        "description": "The open Vessel is restricted on yin days — six of eight vessels are gated",
    },
    "polarity_aligned": {
        "name": "Polarity Alignment",
        "description": "Vessel polarity matches the day polarity",
    },
    "great_rite_active": {
        "name": "Great Rite Active",
        "description": "The current month hosts a Great Rite",
    },
    "vadusfadahm_active": {
        "name": "VADUSFADAHM Active",
        "description": "The intercalary 13th month is active — the activation formula pervades all temporal layers",
    },
    "sephirotic_rare": {
        "name": "Sephirotic Rare Day",
        "description": "A day beyond Saturn — Uranus (Day 8) or Neptune (Day 9) of the Sephirotic Week",
    },
    "key_amplified_unity": {
        "name": "Key-Amplified Law Unity",
        "description": "Law Unity during an active Solar Key cusping window",
    },
    "anatomical_key": {
        "name": "Anatomical + Key",
        "description": "An anatomical intersection during a Solar Key cusping window",
    },
    "full_alignment_key": {
        "name": "Full Alignment + Key",
        "description": "The maximum compound — full anatomical alignment during a Solar Key cusping window",
    },
}

# ── Resonance Display Names and Descriptions ─────────────────────

RESONANCE_DISPLAY = {
    "wu_xing_element_match": {
        "name": "Elemental Resonance (Trigram-Organ)",
        "description": "The Primeval trigram's element matches the active organ's element",
    },
    "vessel_organ_element_match": {
        "name": "Elemental Resonance (Vessel-Organ)",
        "description": "The Astral vessel's trigram element matches the active organ's element",
    },
    "plum_blossom_wu_xing": {
        "name": "Plum Blossom Resonance",
        "description": "The Primeval trigram's Plum Blossom element matches the active organ",
    },
    "stem_trigram_polarity": {
        "name": "Day-Trigram Polarity Match",
        "description": "The day's stem polarity matches the Primeval trigram's polarity",
    },
    "organ_vessel_polarity": {
        "name": "Organ-Vessel Polarity Match",
        "description": "The active organ's yin/yang matches the open vessel's polarity",
    },
    "paired_organ_vessel_point": {
        "name": "Paired Organ Point",
        "description": "The open Vessel's acupuncture point falls on the paired organ's meridian",
    },
    "color_affinity": {
        "name": "Color Affinity",
        "description": "The Law's color resonates with the organ's healing color",
    },
    "emotion_perception": {
        "name": "Emotion-Perception Resonance",
        "description": "The Law's perceptual quality aligns with the organ's emotional territory",
    },
    "adonaj_ba_proximity": {
        "name": "Energy Center Proximity",
        "description": "The Law's energy center (Adonaj-Ba) is anatomically near the active organ",
    },
    "waxing_wing_alignment": {
        "name": "Lunar-Solar Rhythm",
        "description": "Waxing moon aligns with Day wing, or waning moon with Night wing",
    },
    "sephirotic_quest_match": {
        "name": "Sephirotic-Quest Match",
        "description": "The Sephirotic day's planet matches the Law's Quest Tarot attribution",
    },
    "season_great_rite": {
        "name": "Season-Great Rite Alignment",
        "description": "The organ's elemental season matches the current Great Rite",
    },
    "yang_count": {
        "name": "Yang Line Count",
        "description": "Number of yang (solid) lines in the current trigram",
    },
    "divine_hour_law_unity": {
        "name": "Divine Hour during Law Unity",
        "description": "Law Unity is active — the specific Divine Hour amplifies or colors it",
    },
    "alchemical_stage": {
        "name": "Alchemical Stage",
        "description": "The month's position in the three-movement alchemical cycle",
    },
    "month_group": {
        "name": "Month Group",
        "description": "The divine month's mythological grouping",
    },
    "iao_position": {
        "name": "IAO Position",
        "description": "The month's position in the IAO vowel cycle",
    },
}


# ── Main Presentation Function ────────────────────────────────────


def _present_point(point_code: str) -> dict:
    """Present an acupuncture point with medical designation and plain English."""
    meridian_code = point_code.split("-")[0] if "-" in point_code else point_code
    return {
        "code": point_code,
        "meridian": MERIDIAN_NAMES.get(meridian_code, meridian_code),
        "description": POINT_DESCRIPTIONS.get(point_code, ""),
    }


def _present_vessel(raw: dict) -> dict:
    """Present the Extraordinary Vessel layer (Astral body)."""
    vessel_code = raw.get("vessel", "")
    english = VESSEL_ENGLISH.get(vessel_code, vessel_code)
    law = raw.get("law", "")
    trigram = raw.get("trigram", "")

    return {
        "vessel": english,
        "law": law,
        "description": f"The {english} is open, carrying {law}.",
        "trigram": raw.get("symbol", ""),
        "trigram_nature": TRIGRAM_NATURE.get(trigram, ""),
        "polarity": raw.get("polarity"),
        "pair_partner": VESSEL_ENGLISH.get(raw.get("pair_partner", ""), raw.get("pair_partner", "")),
        "confluent": _present_point(raw.get("confluent", "")),
        "coupled": _present_point(raw.get("coupled", "")),
        "clinical_domain": raw.get("vessel_clinical_domain"),
        "yin_day_blocked": raw.get("yin_day_blocked", False),
        # Practice context
        "vowel": raw.get("vowel"),
        "mudra": raw.get("mudra"),
        "adonaj_ba": raw.get("adonaj_ba"),
        "color": raw.get("color"),
        "perception": {
            "positive": raw.get("perception_pos"),
            "negative": raw.get("perception_neg"),
        },
        "quest": raw.get("quest_short"),
        "binary": raw.get("binary"),
    }


def _present_soul(raw: dict) -> dict:
    """Present the Primeval Law layer (Soul body)."""
    trigram = raw.get("trigram", "")

    return {
        "law": raw.get("law"),
        "phase": raw.get("phase"),
        "trigram": raw.get("symbol", ""),
        "trigram_nature": TRIGRAM_NATURE.get(trigram, ""),
        "illumination_pct": raw.get("illumination_pct"),
        "waxing": raw.get("waxing"),
        "yang_lines": raw.get("yang_count"),
        # Practice context
        "vowel": raw.get("vowel"),
        "mudra": raw.get("mudra"),
        "adonaj_ba": raw.get("adonaj_ba"),
        "color": raw.get("color"),
        "perception": {
            "positive": raw.get("perception_pos"),
            "negative": raw.get("perception_neg"),
        },
        "quest": raw.get("quest_short"),
        "binary": raw.get("binary"),
    }


def _present_keys(raw: dict) -> dict:
    """Present the Solar Keys layer."""
    active = raw.get("active", False)
    key = raw.get("key")

    result = {"active": active, "key": None}

    if active and key:
        key_display = "Gold" if key == "gold" else "Silver"
        law = raw.get("law", "")
        vessel_info = KEY_VESSEL.get(key, {})
        vessel_name = vessel_info.get("vessel", "")
        event = raw.get("event", "sunrise" if key == "gold" else "sunset").capitalize()

        result["key"] = key_display
        result["law"] = law
        result["event"] = event
        result["vessel"] = vessel_name
        result["description"] = (
            f"The {key_display} Key is active — "
            f"{law} through the {vessel_name}."
        )
        result["window_start"] = raw.get("window_start")
        result["window_end"] = raw.get("window_end")
        result["radius_minutes"] = raw.get("radius_minutes")
        # Practice context
        result["vowel"] = raw.get("vowel")
        result["mudra"] = raw.get("mudra")
        result["adonaj_ba"] = raw.get("adonaj_ba")
        result["color"] = raw.get("color")
        result["perception"] = {
            "positive": raw.get("perception_pos"),
            "negative": raw.get("perception_neg"),
        }

    return result


def _present_body(raw: dict) -> dict:
    """Present the Organ Clock layer (Gross body)."""
    return {
        "organ": raw.get("organ"),
        "abbreviation": raw.get("meridian"),
        "element": raw.get("element"),
        "polarity": raw.get("yin_yang"),
        "paired_organ": raw.get("paired"),
        "wing": raw.get("wing"),
        "inner_alchemy": {
            "healing_sound": raw.get("healing_sound"),
            "emotion_positive": raw.get("emotion_positive"),
            "emotion_negative": raw.get("emotion_negative"),
            "color": raw.get("healing_color"),
            "spirit": raw.get("organ_spirit"),
            "season": raw.get("organ_season"),
            "sense_organ": raw.get("sense_organ"),
            "body_tissue": raw.get("body_tissue"),
        },
    }


def _present_practice(raw_state: dict) -> dict:
    """
    Synthesize practitioner-actionable guidance from all temporal bodies.

    Surfaces the quest-vowel-mudra-adonaj_ba connection as the primary
    Damanhurian practice instruction, with the healing sound as the
    body-level transmutation tool. Answers "what do I DO right now?"
    """
    soul_raw = raw_state.get("primeval", {})
    astral_raw = raw_state.get("derivative", {})
    organ_raw = raw_state.get("organ_clock", {})
    key_raw = raw_state.get("solar_key", {})

    practice = {
        "soul": {
            "law": soul_raw.get("law"),
            "quest": soul_raw.get("quest_short"),
            "vowel": soul_raw.get("vowel"),
            "mudra": soul_raw.get("mudra"),
            "adonaj_ba": soul_raw.get("adonaj_ba"),
            "color": soul_raw.get("color"),
            "perception_positive": soul_raw.get("perception_pos"),
            "perception_negative": soul_raw.get("perception_neg"),
        },
        "astral": {
            "law": astral_raw.get("law"),
            "quest": astral_raw.get("quest_short"),
            "vowel": astral_raw.get("vowel"),
            "mudra": astral_raw.get("mudra"),
            "adonaj_ba": astral_raw.get("adonaj_ba"),
            "color": astral_raw.get("color"),
            "perception_positive": astral_raw.get("perception_pos"),
            "perception_negative": astral_raw.get("perception_neg"),
        },
        "key": None,
        "body": {
            "organ": organ_raw.get("organ"),
            "healing_sound": organ_raw.get("healing_sound"),
            "emotion_positive": organ_raw.get("emotion_positive"),
            "emotion_negative": organ_raw.get("emotion_negative"),
        },
    }

    # Populate key if Solar Key is active
    if key_raw.get("active") and key_raw.get("key"):
        key_display = "Gold" if key_raw["key"] == "gold" else "Silver"
        practice["key"] = {
            "name": key_display,
            "law": key_raw.get("law"),
            "vowel": key_raw.get("vowel"),
            "mudra": key_raw.get("mudra"),
            "adonaj_ba": key_raw.get("adonaj_ba"),
            "color": key_raw.get("color"),
        }

    return practice


def _present_compounds(raw: dict) -> dict:
    """Present compounds with human-readable names and descriptions."""
    presented = {}
    active_list = []

    for key, info in COMPOUND_DISPLAY.items():
        value = raw.get(key, False)
        is_active = bool(value)
        presented[key] = {
            "active": is_active,
            "name": info["name"],
            "description": info["description"],
        }
        if is_active:
            active_list.append(info["name"])

    # Include key-derivative detail if present
    if raw.get("key_derivative_detail"):
        detail = raw["key_derivative_detail"]
        key_display = "Gold" if detail.get("key") == "gold" else "Silver"
        presented["key_derivative_unity"]["detail"] = (
            f"{key_display} Key — {detail.get('law', '')}"
        )

    presented["_active"] = active_list
    presented["_active_count"] = len(active_list)
    return presented


def _present_resonances(raw: dict) -> dict:
    """Present resonances with human-readable names and descriptions."""
    presented = {
        "active_count": raw.get("active_count", 0),
        "total_checked": raw.get("total_checked", 0),
    }
    active_list = []

    # Walk the categorized structure
    for category in ("elemental", "qualitative", "rhythmic", "calendrical"):
        cat_data = raw.get(category, {})
        cat_presented = {}

        for key, value in cat_data.items():
            display = RESONANCE_DISPLAY.get(key)
            if not display:
                # State values without display info — pass through
                cat_presented[key] = value
                continue

            if isinstance(value, dict):
                is_active = value.get("active", False)
                cat_presented[key] = {
                    "active": is_active,
                    "name": display["name"],
                    "description": display["description"],
                }
                # Include grade if present
                if "grade" in value:
                    cat_presented[key]["grade"] = value["grade"]
                if is_active:
                    active_list.append(display["name"])
            else:
                # State value (yang_count, alchemical_stage, etc.)
                cat_presented[key] = {
                    "value": value,
                    "name": display["name"],
                    "description": display["description"],
                }

        presented[category] = cat_presented

    presented["_active"] = active_list
    return presented


def present_state(raw_state: dict) -> dict:
    """
    Transform a raw computational state into practitioner-readable output.

    Layer naming:
        primeval  → soul    (the Soul body's Law, from lunar phase)
        derivative → astral  (the Astral body's Vessel and Law, from LGBF)
        organ_clock → body   (the Gross body's organ, meridian, and inner alchemy)
        solar_key → keys    (the Solar Keys at sunrise/sunset cusps)
        practice          → (synthesized practitioner-actionable guidance)

    Drops: Chinese characters, pinyin branch/stem names, insider shorthand.
    Keeps: Trigram symbols, medical point designations, healing sounds.
    """
    return {
        "timestamp": raw_state.get("timestamp"),
        "location": raw_state.get("location"),
        "solar": raw_state.get("solar"),
        "practice": _present_practice(raw_state),
        "soul": _present_soul(raw_state.get("primeval", {})),
        "astral": _present_vessel(raw_state.get("derivative", {})),
        "keys": _present_keys(raw_state.get("solar_key", {})),
        "body": _present_body(raw_state.get("organ_clock", {})),
        "hour": raw_state.get("divine_hour"),
        "calendar": raw_state.get("calendar"),
        "compounds": _present_compounds(raw_state.get("compounds", {})),
        "resonances": _present_resonances(raw_state.get("resonances", {})),
    }
