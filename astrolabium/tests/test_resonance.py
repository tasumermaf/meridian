"""
Tests for the resonance scanner — all 13 resonance types.

Uses mock state dicts matching the pattern in test_astrolabium.py.
Each resonance type has at least one positive and one negative test.
"""

import pytest
from datetime import datetime

from src.resonance import (
    detect_resonances,
    RESONANCE_BOOLEAN_TYPES,
    RESONANCE_STATE_TYPES,
    ALL_RESONANCE_TYPES,
)
from src.astrolabium import calculate_complete_state


# ── Test location: Los Angeles ──
LA_LAT, LA_LON, LA_TZ = 34.0522, -118.2437, "America/Los_Angeles"


def _make_resonance_state(
    primeval_law="Synchronicity",
    primeval_trigram="Qián",
    primeval_phase_index=3,
    primeval_waxing=True,
    derivative_law="Kaos",
    derivative_vessel="Ren Mai",
    derivative_polarity="Yin",
    derivative_conf_branch=2,
    derivative_conf_meridian="LU",
    derivative_coup_branch=9,
    derivative_coup_meridian="KI",
    organ="Heart",
    organ_element="Fire",
    organ_meridian="HT",
    organ_branch=6,
    organ_yin_yang="Yin",
    organ_paired="Sm Intestine",
    wing="Day",
    is_yang_day=True,
    two_body_unity=False,
    divine_hour_index=2,
    divine_hour_roman="II",
    divine_hour_wing="Day",
    sephirotic_planet="Sol",
    great_rite=None,
    alchemical="Nigredo",
    month_group="Osirian",
    month_number=1,
):
    """Build a minimal state dict for resonance testing."""
    return {
        "primeval": {
            "law": primeval_law,
            "trigram": primeval_trigram,
            "phase_index": primeval_phase_index,
            "waxing": primeval_waxing,
        },
        "derivative": {
            "law": derivative_law,
            "vessel": derivative_vessel,
            "polarity": derivative_polarity,
            "conf_branch": derivative_conf_branch,
            "conf_meridian": derivative_conf_meridian,
            "coup_branch": derivative_coup_branch,
            "coup_meridian": derivative_coup_meridian,
        },
        "organ_clock": {
            "branch_index": organ_branch,
            "organ": organ,
            "element": organ_element,
            "meridian": organ_meridian,
            "yin_yang": organ_yin_yang,
            "paired": organ_paired,
            "wing": wing,
        },
        "stem_branch": {
            "is_yang_day": is_yang_day,
        },
        "compounds": {
            "two_body_unity": two_body_unity,
        },
        "divine_hour": {
            "index": divine_hour_index,
            "roman": divine_hour_roman,
            "wing": divine_hour_wing,
        },
        "solar_key": {
            "active": False,
            "key": None,
            "law": None,
        },
        "calendar": {
            "sephirotic_planet": sephirotic_planet,
            "great_rite": great_rite,
            "alchemical": alchemical,
            "month_group": month_group,
            "month_number": month_number,
        },
    }


# ══════════════════════════════════════════════════════════════════════
# Category: Elemental (Type A)
# ══════════════════════════════════════════════════════════════════════


class TestWuXingElementMatch:
    """R_WX_01: Trigram Wu Xing × Organ Wu Xing."""

    def test_metal_matches_metal(self):
        """Qián (Metal) during Lung (Metal) hour."""
        state = _make_resonance_state(
            primeval_trigram="Qián",
            organ="Lung", organ_element="Metal",
        )
        r = detect_resonances(state)
        assert r["elemental"]["wu_xing_element_match"]["active"] is True
        assert r["elemental"]["wu_xing_element_match"]["primeval_wx"] == "Metal"
        assert r["elemental"]["wu_xing_element_match"]["organ_wx"] == "Metal"

    def test_metal_does_not_match_fire(self):
        """Qián (Metal) during Heart (Fire) hour."""
        state = _make_resonance_state(
            primeval_trigram="Qián",
            organ="Heart", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["elemental"]["wu_xing_element_match"]["active"] is False

    def test_wood_matches_wood(self):
        """Zhèn (Wood) during Liver (Wood) hour."""
        state = _make_resonance_state(
            primeval_trigram="Zhèn",
            primeval_law="Sole Atom",
            organ="Liver", organ_element="Wood",
        )
        r = detect_resonances(state)
        assert r["elemental"]["wu_xing_element_match"]["active"] is True

    def test_earth_trigrams(self):
        """Kūn (Earth) during Stomach (Earth) hour."""
        state = _make_resonance_state(
            primeval_trigram="Kūn",
            primeval_law="Kaos",
            organ="Stomach", organ_element="Earth",
        )
        r = detect_resonances(state)
        assert r["elemental"]["wu_xing_element_match"]["active"] is True


class TestVesselOrganElementMatch:
    """R_WX_02: Derivative vessel's trigram Wu Xing × Organ Wu Xing."""

    def test_kaos_ren_mai_earth_matches_earth(self):
        """Ren Mai (Kaos → Kūn → Earth) during Stomach (Earth) hour."""
        state = _make_resonance_state(
            derivative_law="Kaos",
            organ="Stomach", organ_element="Earth",
        )
        r = detect_resonances(state)
        assert r["elemental"]["vessel_organ_element_match"]["active"] is True

    def test_no_match_when_different(self):
        """Ren Mai (Earth) during Heart (Fire) hour."""
        state = _make_resonance_state(
            derivative_law="Kaos",
            organ="Heart", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["elemental"]["vessel_organ_element_match"]["active"] is False


class TestPlumBlossomWuXing:
    """R_WX_03: Plum Blossom Wu Xing × Organ Wu Xing."""

    def test_qian_imperial_fire_matches_fire(self):
        """Qián Plum Blossom = Imperial Fire → Fire, during Heart (Fire) hour."""
        state = _make_resonance_state(
            primeval_trigram="Qián",
            organ="Heart", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["elemental"]["plum_blossom_wu_xing"]["active"] is True
        assert r["elemental"]["plum_blossom_wu_xing"]["plum_blossom"] == "Imperial Fire"

    def test_qian_pb_does_not_match_metal(self):
        """Qián standard = Metal, but PB = Imperial Fire. Metal organ should NOT match PB."""
        state = _make_resonance_state(
            primeval_trigram="Qián",
            organ="Lung", organ_element="Metal",
        )
        r = detect_resonances(state)
        # Standard wu_xing matches Metal, but plum_blossom maps to Fire
        assert r["elemental"]["plum_blossom_wu_xing"]["active"] is False

    def test_dui_plum_blossom_wood(self):
        """Duì Plum Blossom = Wood, during Liver (Wood) hour."""
        state = _make_resonance_state(
            primeval_trigram="Duì",
            primeval_law="Time Matrix",
            organ="Liver", organ_element="Wood",
        )
        r = detect_resonances(state)
        assert r["elemental"]["plum_blossom_wu_xing"]["active"] is True


class TestStemTrigramPolarity:
    """R_WX_04: Stem polarity × Trigram polarity."""

    def test_yang_day_yang_trigram_matches(self):
        """Yang day + Qián (Yang) = double-yang."""
        state = _make_resonance_state(
            primeval_trigram="Qián",
            is_yang_day=True,
        )
        r = detect_resonances(state)
        assert r["elemental"]["stem_trigram_polarity"]["active"] is True
        assert r["elemental"]["stem_trigram_polarity"]["is_yang_day"] is True
        assert r["elemental"]["stem_trigram_polarity"]["trigram_polarity"] == "Yang"

    def test_yin_day_yin_trigram_matches(self):
        """Yin day + Kūn (Yin) = double-yin."""
        state = _make_resonance_state(
            primeval_trigram="Kūn",
            primeval_law="Kaos",
            is_yang_day=False,
        )
        r = detect_resonances(state)
        assert r["elemental"]["stem_trigram_polarity"]["active"] is True

    def test_yang_day_yin_trigram_does_not_match(self):
        """Yang day + Kūn (Yin) = mixed, no match."""
        state = _make_resonance_state(
            primeval_trigram="Kūn",
            primeval_law="Kaos",
            is_yang_day=True,
        )
        r = detect_resonances(state)
        assert r["elemental"]["stem_trigram_polarity"]["active"] is False

    def test_yin_day_yang_trigram_does_not_match(self):
        """Yin day + Zhèn (Yang) = mixed, no match."""
        state = _make_resonance_state(
            primeval_trigram="Zhèn",
            primeval_law="Sole Atom",
            is_yang_day=False,
        )
        r = detect_resonances(state)
        assert r["elemental"]["stem_trigram_polarity"]["active"] is False

    def test_solar_key_trigram_returns_false(self):
        """Kǎn (Solar Key) has no polarity in the lookup — returns False."""
        state = _make_resonance_state(
            primeval_trigram="Kǎn",
            primeval_law="Fall of Events",
            is_yang_day=True,
        )
        r = detect_resonances(state)
        assert r["elemental"]["stem_trigram_polarity"]["active"] is False


class TestOrganVesselPolarity:
    """R_WX_05: Organ Yin/Yang × Vessel polarity."""

    def test_yin_organ_yin_vessel_matches(self):
        """Yin organ (Heart) + Yin vessel (Ren Mai) = match."""
        state = _make_resonance_state(
            organ="Heart", organ_yin_yang="Yin",
            derivative_polarity="Yin",
        )
        r = detect_resonances(state)
        assert r["elemental"]["organ_vessel_polarity"]["active"] is True

    def test_yang_organ_yang_vessel_matches(self):
        """Yang organ (Gallbladder) + Yang vessel (Du Mai) = match."""
        state = _make_resonance_state(
            organ="Gallbladder", organ_yin_yang="Yang",
            derivative_polarity="Yang",
        )
        r = detect_resonances(state)
        assert r["elemental"]["organ_vessel_polarity"]["active"] is True

    def test_yin_organ_yang_vessel_no_match(self):
        """Yin organ (Heart) + Yang vessel (Du Mai) = no match."""
        state = _make_resonance_state(
            organ="Heart", organ_yin_yang="Yin",
            derivative_polarity="Yang",
        )
        r = detect_resonances(state)
        assert r["elemental"]["organ_vessel_polarity"]["active"] is False

    def test_yang_organ_yin_vessel_no_match(self):
        """Yang organ (Gallbladder) + Yin vessel (Ren Mai) = no match."""
        state = _make_resonance_state(
            organ="Gallbladder", organ_yin_yang="Yang",
            derivative_polarity="Yin",
        )
        r = detect_resonances(state)
        assert r["elemental"]["organ_vessel_polarity"]["active"] is False


class TestPairedOrganVesselPoint:
    """R_AN_01: Paired organ hosts vessel confluent or coupled point."""

    def test_paired_organ_hosts_confluent(self):
        """Heart paired with Sm Intestine. Du Mai confluent is SI-3 (branch 7, SI).
        Active organ is Heart (branch 6), paired = Sm Intestine (branch 7, SI)."""
        state = _make_resonance_state(
            organ="Heart", organ_branch=6, organ_paired="Sm Intestine",
            derivative_conf_branch=7, derivative_conf_meridian="SI",
            derivative_coup_branch=8, derivative_coup_meridian="BL",
        )
        r = detect_resonances(state)
        assert r["elemental"]["paired_organ_vessel_point"]["active"] is True
        assert r["elemental"]["paired_organ_vessel_point"]["paired_confluent"] is True
        assert r["elemental"]["paired_organ_vessel_point"]["paired_coupled"] is False

    def test_paired_organ_hosts_coupled(self):
        """Kidney paired with Bladder. Yang Qiao Mai coupled is SI-3 (branch 7, SI).
        That doesn't match Bladder (branch 8, BL). Let's use a real case:
        Bladder paired with Kidney. Yin Qiao Mai confluent is KI-6 (branch 9, KI)."""
        state = _make_resonance_state(
            organ="Bladder", organ_branch=8, organ_paired="Kidney",
            derivative_conf_branch=9, derivative_conf_meridian="KI",
            derivative_coup_branch=2, derivative_coup_meridian="LU",
        )
        r = detect_resonances(state)
        assert r["elemental"]["paired_organ_vessel_point"]["active"] is True
        assert r["elemental"]["paired_organ_vessel_point"]["paired_confluent"] is True

    def test_no_match_when_paired_has_no_vessel_point(self):
        """Heart paired with Sm Intestine. Vessel points on Lung and Kidney branches."""
        state = _make_resonance_state(
            organ="Heart", organ_branch=6, organ_paired="Sm Intestine",
            derivative_conf_branch=2, derivative_conf_meridian="LU",
            derivative_coup_branch=9, derivative_coup_meridian="KI",
        )
        r = detect_resonances(state)
        assert r["elemental"]["paired_organ_vessel_point"]["active"] is False

    def test_paired_organ_detail(self):
        """Verify the paired organ name is reported."""
        state = _make_resonance_state(
            organ="Gallbladder", organ_paired="Liver",
        )
        r = detect_resonances(state)
        assert r["elemental"]["paired_organ_vessel_point"]["paired_organ"] == "Liver"


# ══════════════════════════════════════════════════════════════════════
# Category: Qualitative (Type B)
# ══════════════════════════════════════════════════════════════════════


class TestColorAffinity:
    """R_CLR_01: Law color matches organ healing color."""

    def test_exact_green(self):
        """Sole Atom (Green) during Wood organ (Green)."""
        state = _make_resonance_state(
            primeval_law="Sole Atom",
            organ="Liver", organ_element="Wood",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["color_affinity"]["active"] is True
        assert r["qualitative"]["color_affinity"]["grade"] == "EXACT"

    def test_exact_white(self):
        """Divinity (White) during Metal organ (White)."""
        state = _make_resonance_state(
            primeval_law="Divinity",
            organ="Lung", organ_element="Metal",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["color_affinity"]["active"] is True
        assert r["qualitative"]["color_affinity"]["grade"] == "EXACT"

    def test_natural_yellow_gold(self):
        """Kaos (Yellow Gold) during Earth organ (Yellow)."""
        state = _make_resonance_state(
            primeval_law="Kaos",
            organ="Stomach", organ_element="Earth",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["color_affinity"]["active"] is True
        assert r["qualitative"]["color_affinity"]["grade"] == "NATURAL"

    def test_no_affinity(self):
        """Sole Atom (Green) during Fire organ (Red) — no mapping."""
        state = _make_resonance_state(
            primeval_law="Sole Atom",
            organ="Heart", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["color_affinity"]["active"] is False
        assert r["qualitative"]["color_affinity"]["grade"] == "NONE"


class TestEmotionPerception:
    """R_EPR_01: Organ emotion resonates with Law perception."""

    def test_exact_divinity_fire(self):
        """Divinity perception_neg='Hatred', Fire neg='Hatred, arrogance' = EXACT."""
        state = _make_resonance_state(
            primeval_law="Divinity",
            organ="Heart", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["emotion_perception"]["active"] is True
        assert r["qualitative"]["emotion_perception"]["grade"] == "EXACT"

    def test_natural_kaos_earth(self):
        """Kaos perception_neg='Fear, Terror', Earth neg='Worry, anxiety' = NATURAL."""
        state = _make_resonance_state(
            primeval_law="Kaos",
            organ="Stomach", organ_element="Earth",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["emotion_perception"]["active"] is True
        assert r["qualitative"]["emotion_perception"]["grade"] == "NATURAL"

    def test_no_resonance(self):
        """Synchronicity during Metal organ — no mapping entry."""
        state = _make_resonance_state(
            primeval_law="Synchronicity",
            organ="Lung", organ_element="Metal",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["emotion_perception"]["active"] is False


class TestAdonajBaProximity:
    """R_ABD_01: Adonaj-Ba organ proximity."""

    def test_exact_heart(self):
        """Synchronicity (Adonaj-Ba = Heart) during Heart meridian = EXACT."""
        state = _make_resonance_state(
            primeval_law="Synchronicity",
            organ="Heart", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["adonaj_ba_proximity"]["active"] is True
        assert r["qualitative"]["adonaj_ba_proximity"]["grade"] == "EXACT"

    def test_adjacent_sm_intestine(self):
        """Synchronicity (Heart) during Sm Intestine = ADJACENT."""
        state = _make_resonance_state(
            primeval_law="Synchronicity",
            organ="Sm Intestine", organ_element="Fire",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["adonaj_ba_proximity"]["active"] is True
        assert r["qualitative"]["adonaj_ba_proximity"]["grade"] == "ADJACENT"

    def test_exact_solar_plexus_stomach(self):
        """Kaos (Solar Plexus) during Stomach = EXACT."""
        state = _make_resonance_state(
            primeval_law="Kaos",
            organ="Stomach", organ_element="Earth",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["adonaj_ba_proximity"]["active"] is True
        assert r["qualitative"]["adonaj_ba_proximity"]["grade"] == "EXACT"

    def test_no_proximity(self):
        """Sole Atom (Sexual Organs) during Lung — no mapping."""
        state = _make_resonance_state(
            primeval_law="Sole Atom",
            organ="Lung", organ_element="Metal",
        )
        r = detect_resonances(state)
        assert r["qualitative"]["adonaj_ba_proximity"]["active"] is False
        assert r["qualitative"]["adonaj_ba_proximity"]["grade"] == "NONE"


# ══════════════════════════════════════════════════════════════════════
# Category: Rhythmic (Type A)
# ══════════════════════════════════════════════════════════════════════


class TestWaxingWingAlignment:
    """R_LUN_01: Waxing/Waning-Wing Alignment."""

    def test_waxing_day_aligned(self):
        state = _make_resonance_state(primeval_waxing=True, wing="Day")
        r = detect_resonances(state)
        assert r["rhythmic"]["waxing_wing_alignment"]["active"] is True

    def test_waning_night_aligned(self):
        state = _make_resonance_state(primeval_waxing=False, wing="Night")
        r = detect_resonances(state)
        assert r["rhythmic"]["waxing_wing_alignment"]["active"] is True

    def test_waxing_night_not_aligned(self):
        state = _make_resonance_state(primeval_waxing=True, wing="Night")
        r = detect_resonances(state)
        assert r["rhythmic"]["waxing_wing_alignment"]["active"] is False

    def test_waning_day_not_aligned(self):
        state = _make_resonance_state(primeval_waxing=False, wing="Day")
        r = detect_resonances(state)
        assert r["rhythmic"]["waxing_wing_alignment"]["active"] is False


class TestYangCount:
    """R_LUN_02: Yang count is a state value, not boolean."""

    def test_full_moon_yang_3(self):
        """Full Moon (phase_index=3) has yang_count=3."""
        state = _make_resonance_state(primeval_phase_index=3)
        r = detect_resonances(state)
        assert r["rhythmic"]["yang_count"] == 3

    def test_new_moon_yang_0(self):
        """New Moon (phase_index=0) has yang_count=0."""
        state = _make_resonance_state(
            primeval_phase_index=0,
            primeval_law="Kaos",
            primeval_trigram="Kūn",
        )
        r = detect_resonances(state)
        assert r["rhythmic"]["yang_count"] == 0

    def test_first_crescent_yang_1(self):
        """First Crescent (phase_index=1) has yang_count=1."""
        state = _make_resonance_state(
            primeval_phase_index=1,
            primeval_law="Sole Atom",
            primeval_trigram="Zhèn",
        )
        r = detect_resonances(state)
        assert r["rhythmic"]["yang_count"] == 1


class TestDivineHourLawUnity:
    """R_RHY_02: Divine Hour × Law Unity — state value."""

    def test_returns_hour_context_when_unity_active(self):
        """When Two-Body Unity is active, returns hour detail."""
        state = _make_resonance_state(
            two_body_unity=True,
            divine_hour_index=3,
            divine_hour_roman="III",
            divine_hour_wing="Day",
        )
        r = detect_resonances(state)
        dh = r["rhythmic"]["divine_hour_law_unity"]
        assert dh is not None
        assert dh["hour_index"] == 3
        assert dh["hour_roman"] == "III"
        assert dh["wing"] == "Day"

    def test_returns_none_when_no_unity(self):
        """When Two-Body Unity is not active, returns None."""
        state = _make_resonance_state(two_body_unity=False)
        r = detect_resonances(state)
        assert r["rhythmic"]["divine_hour_law_unity"] is None

    def test_night_hour_context(self):
        """Night hour during Law Unity."""
        state = _make_resonance_state(
            two_body_unity=True,
            divine_hour_index=6,
            divine_hour_roman="VI",
            divine_hour_wing="Night",
        )
        r = detect_resonances(state)
        dh = r["rhythmic"]["divine_hour_law_unity"]
        assert dh["hour_index"] == 6
        assert dh["wing"] == "Night"


# ══════════════════════════════════════════════════════════════════════
# Category: Calendrical (Type A)
# ══════════════════════════════════════════════════════════════════════


class TestSephiroticQuestMatch:
    """R_SPH_01: Sephirotic planet matches Quest Tarot attribution."""

    def test_no_match_typically(self):
        """Most combinations don't match."""
        state = _make_resonance_state(
            primeval_law="Synchronicity",
            sephirotic_planet="Mars",
        )
        r = detect_resonances(state)
        assert r["calendrical"]["sephirotic_quest_match"]["active"] is False

    def test_priestess_luna_match(self):
        """Geometric Essence (Quest=Priestess, attr=Moon→Luna) on Yesod/Luna day."""
        state = _make_resonance_state(
            primeval_law="Geometric Essence",
            primeval_trigram="Xùn",
            sephirotic_planet="Luna",
        )
        r = detect_resonances(state)
        assert r["calendrical"]["sephirotic_quest_match"]["active"] is True

    def test_emperor_jupiter_match(self):
        """Time Matrix (Quest=Emperor, attr=Jupiter) on Chesed/Jupiter day."""
        state = _make_resonance_state(
            primeval_law="Time Matrix",
            primeval_trigram="Duì",
            sephirotic_planet="Jupiter",
        )
        r = detect_resonances(state)
        assert r["calendrical"]["sephirotic_quest_match"]["active"] is True


class TestSeasonGreatRite:
    """R_SEA_01: Season-Great Rite Alignment."""

    def test_spring_equinox_wood_organ(self):
        """Wood organ (Spring) during Spring Equinox month."""
        state = _make_resonance_state(
            organ="Liver", organ_element="Wood",
            great_rite="Spring Equinox",
        )
        r = detect_resonances(state)
        assert r["calendrical"]["season_great_rite"]["active"] is True

    def test_no_great_rite(self):
        """No Great Rite active."""
        state = _make_resonance_state(great_rite=None)
        r = detect_resonances(state)
        assert r["calendrical"]["season_great_rite"]["active"] is False

    def test_mismatched_season(self):
        """Fire organ (Summer) during Winter Solstice — no match."""
        state = _make_resonance_state(
            organ="Heart", organ_element="Fire",
            great_rite="Winter Solstice",
        )
        r = detect_resonances(state)
        assert r["calendrical"]["season_great_rite"]["active"] is False


class TestStateValues:
    """R_CAL_01/02/03: State value extraction."""

    def test_alchemical_stage(self):
        state = _make_resonance_state(alchemical="Nigredo")
        r = detect_resonances(state)
        assert r["calendrical"]["alchemical_stage"] == "Nigredo"

    def test_alchemical_rubedo(self):
        state = _make_resonance_state(alchemical="Rubedo", month_number=9)
        r = detect_resonances(state)
        assert r["calendrical"]["alchemical_stage"] == "Rubedo"

    def test_month_group(self):
        state = _make_resonance_state(month_group="Falcon")
        r = detect_resonances(state)
        assert r["calendrical"]["month_group"] == "Falcon"

    def test_iao_position_isis(self):
        """Month 1 (ISIS) has IAO = 'I'."""
        state = _make_resonance_state(month_number=1)
        r = detect_resonances(state)
        assert r["calendrical"]["iao_position"] == "I"

    def test_iao_position_osiris(self):
        """Month 7 (OSIRIS) has IAO = 'O'."""
        state = _make_resonance_state(month_number=7, month_group="Osirian")
        r = detect_resonances(state)
        assert r["calendrical"]["iao_position"] == "O"

    def test_iao_position_null(self):
        """Month 3 (LIOTHIL) has IAO = null."""
        state = _make_resonance_state(month_number=3, month_group="Falcon")
        r = detect_resonances(state)
        assert r["calendrical"]["iao_position"] is None


# ══════════════════════════════════════════════════════════════════════
# Structural / Integration tests
# ══════════════════════════════════════════════════════════════════════


class TestResonanceStructure:
    """Verify output structure and counting."""

    def test_has_all_categories(self):
        state = _make_resonance_state()
        r = detect_resonances(state)
        assert "elemental" in r
        assert "qualitative" in r
        assert "rhythmic" in r
        assert "calendrical" in r
        assert "active_count" in r
        assert "total_checked" in r

    def test_active_count_is_consistent(self):
        """active_count should equal the number of active boolean resonances."""
        state = _make_resonance_state()
        r = detect_resonances(state)

        manual_count = 0
        for cat_name in ("elemental", "qualitative", "rhythmic", "calendrical"):
            cat = r[cat_name]
            if isinstance(cat, dict):
                for key, val in cat.items():
                    if isinstance(val, dict) and "active" in val:
                        if val["active"]:
                            manual_count += 1
        assert r["active_count"] == manual_count

    def test_total_checked_matches_boolean_count(self):
        state = _make_resonance_state()
        r = detect_resonances(state)
        assert r["total_checked"] == len(RESONANCE_BOOLEAN_TYPES)

    def test_with_real_state(self):
        """Resonances produce valid output from a real calculated state."""
        dt = datetime(2026, 3, 1, 14, 0, 0)
        state = calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)
        # Inject resonances (normally done by astrolabium after integration)
        r = detect_resonances(state)

        assert isinstance(r["active_count"], int)
        assert r["active_count"] >= 0
        assert r["active_count"] <= r["total_checked"]

        # All boolean types should have 'active' key
        for rtype in RESONANCE_BOOLEAN_TYPES:
            found = False
            for cat in ("elemental", "qualitative", "rhythmic", "calendrical"):
                if rtype in r[cat] and isinstance(r[cat][rtype], dict):
                    assert "active" in r[cat][rtype]
                    found = True
            assert found, f"Boolean resonance {rtype} not found in output"

    def test_resonance_type_lists_complete(self):
        """ALL_RESONANCE_TYPES = BOOLEAN + STATE types."""
        assert set(ALL_RESONANCE_TYPES) == set(RESONANCE_BOOLEAN_TYPES) | set(RESONANCE_STATE_TYPES)
        assert len(ALL_RESONANCE_TYPES) == 17
