"""
Astrolabium integration tests — complete state and compound detection.
"""

import pytest
from datetime import datetime
import pytz

from src.astrolabium import calculate_complete_state, detect_compounds


# ── Test location: Los Angeles ──
LA_LAT, LA_LON, LA_TZ = 34.0522, -118.2437, "America/Los_Angeles"


class TestCompleteState:
    """Complete state calculation returns all required fields."""

    @pytest.fixture
    def state(self):
        dt = datetime(2026, 3, 1, 14, 0, 0)
        return calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)

    def test_has_all_layers(self, state):
        assert "solar" in state
        assert "organ_clock" in state
        assert "derivative" in state
        assert "primeval" in state
        assert "solar_key" in state
        assert "divine_hour" in state
        assert "calendar" in state
        assert "stem_branch" in state
        assert "compounds" in state
        assert "resonances" in state

    def test_resonances_structure(self, state):
        r = state["resonances"]
        assert "elemental" in r
        assert "qualitative" in r
        assert "rhythmic" in r
        assert "calendrical" in r
        assert "active_count" in r
        assert "total_checked" in r
        assert isinstance(r["active_count"], int)
        assert r["active_count"] >= 0
        assert r["active_count"] <= r["total_checked"]

    def test_calendar_fields(self, state):
        cal = state["calendar"]
        assert "divine_year" in cal
        assert "month_number" in cal
        assert "month_name" in cal
        assert "day_in_month" in cal
        assert "sephirotic_day" in cal
        assert "sephirah" in cal
        assert "quarter" in cal
        assert 1 <= cal["month_number"] <= 13
        assert 1 <= cal["sephirotic_day"] <= 9
        assert cal["divine_year"] > 0

    def test_solar_has_times(self, state):
        assert "sunrise" in state["solar"]
        assert "sunset" in state["solar"]
        assert "noon" in state["solar"]

    def test_organ_clock_fields(self, state):
        oc = state["organ_clock"]
        assert "branch_index" in oc
        assert "organ" in oc
        assert "meridian" in oc
        assert "element" in oc
        assert "wing" in oc
        assert 0 <= oc["branch_index"] <= 11

    def test_derivative_fields(self, state):
        d = state["derivative"]
        assert "law" in d
        assert "vessel" in d
        assert "prime" in d
        assert "remainder" in d
        assert "conf_branch" in d
        assert "coup_branch" in d

    def test_primeval_fields(self, state):
        p = state["primeval"]
        assert "law" in p
        assert "phase" in p
        assert "trigram" in p
        assert "elongation_deg" in p
        assert "illumination_pct" in p

    def test_divine_hour_fields(self, state):
        dh = state["divine_hour"]
        assert "index" in dh
        assert 1 <= dh["index"] <= 8
        assert "roman" in dh
        assert "wing" in dh

    def test_stem_branch_fields(self, state):
        sb = state["stem_branch"]
        assert "daily_stem" in sb
        assert "daily_branch" in sb
        assert "is_yang_day" in sb
        assert "sexagenary_index" in sb

    def test_location_preserved(self, state):
        assert state["location"]["lat"] == LA_LAT
        assert state["location"]["lon"] == LA_LON
        assert state["location"]["tz"] == LA_TZ


class TestCompoundDetection:
    """Compound detection logic."""

    def _make_state(self, primeval_law, derivative_law, branch=7,
                    conf_branch=7, coup_branch=8, conf_meridian="SI",
                    coup_meridian="BL", meridian="SI", vessel="Du Mai",
                    key_active=False, key_name=None, key_law=None,
                    is_yang_day=True, yin_day_restricted=True,
                    polarity="Yang", great_rite=None,
                    month_number=1, sephirotic_day=1):
        """Build a minimal state dict for compound testing."""
        return {
            "primeval": {"law": primeval_law},
            "derivative": {
                "law": derivative_law,
                "vessel": vessel,
                "polarity": polarity,
                "is_yang_day": is_yang_day,
                "conf_branch": conf_branch,
                "conf_meridian": conf_meridian,
                "coup_branch": coup_branch,
                "coup_meridian": coup_meridian,
                "yin_day_blocked": not is_yang_day and yin_day_restricted,
            },
            "organ_clock": {
                "branch_index": branch,
                "meridian": meridian,
            },
            "solar_key": {
                "active": key_active,
                "key": key_name,
                "law": key_law,
            },
            "calendar": {
                "great_rite": great_rite,
                "month_number": month_number,
                "sephirotic_day": sephirotic_day,
            },
        }

    def test_two_body_unity_when_laws_match(self):
        state = self._make_state("Synchronicity", "Synchronicity")
        compounds = detect_compounds(state)
        assert compounds["two_body_unity"] is True

    def test_no_unity_when_laws_differ(self):
        state = self._make_state("Kaos", "Synchronicity")
        compounds = detect_compounds(state)
        assert compounds["two_body_unity"] is False

    def test_confluent_intersection(self):
        """When vessel confluent point is on active meridian."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            branch=7, meridian="SI",
            conf_branch=7, conf_meridian="SI",
        )
        compounds = detect_compounds(state)
        assert compounds["confluent_intersection"] is True

    def test_no_confluent_when_branch_mismatch(self):
        state = self._make_state(
            "Kaos", "Synchronicity",
            branch=5, meridian="SP",
            conf_branch=7, conf_meridian="SI",
        )
        compounds = detect_compounds(state)
        assert compounds["confluent_intersection"] is False

    def test_full_confluent(self):
        """Full Confluent = Law Unity + Confluent Intersection."""
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            branch=7, meridian="SI",
            conf_branch=7, conf_meridian="SI",
        )
        compounds = detect_compounds(state)
        assert compounds["full_confluent"] is True

    def test_full_alignment_requires_anatomical(self):
        """Full Alignment requires Anatomical Intersection, not just Key active."""
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            branch=5, meridian="SP",  # NO anatomical intersection
            conf_branch=7, conf_meridian="SI",
            key_active=True, key_name="gold", key_law="Fall of Events",
        )
        compounds = detect_compounds(state)
        # Law Unity is true, key is active, but no Anatomical Intersection
        assert compounds["two_body_unity"] is True
        assert compounds["full_confluent"] is False
        assert compounds["full_coupled"] is False

    def test_key_derivative_unity(self):
        """Key-Derivative Unity: key active AND derivative law == key law."""
        state = self._make_state(
            "Kaos", "Fall of Events",
            key_active=True, key_name="gold", key_law="Fall of Events",
        )
        compounds = detect_compounds(state)
        assert compounds["key_derivative_unity"] is True

    def test_no_key_derivative_when_laws_differ(self):
        state = self._make_state(
            "Kaos", "Synchronicity",
            key_active=True, key_name="gold", key_law="Fall of Events",
        )
        compounds = detect_compounds(state)
        assert compounds["key_derivative_unity"] is False

    def test_yin_day_blocks_two_body(self):
        """Yin day restriction blocks Two-Body Unity for restricted vessels."""
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            is_yang_day=False, yin_day_restricted=True,
        )
        compounds = detect_compounds(state)
        assert compounds["two_body_unity_raw"] is True
        assert compounds["two_body_unity"] is False
        assert compounds["yin_day_blocked"] is True

    def test_yin_day_allows_unrestricted(self):
        """Ren Mai and Yang Wei Mai are NOT yin-day restricted."""
        state = self._make_state(
            "Kaos", "Kaos",
            vessel="Ren Mai",
            is_yang_day=False, yin_day_restricted=False,
        )
        compounds = detect_compounds(state)
        assert compounds["two_body_unity"] is True
        assert compounds["yin_day_blocked"] is False

    def test_coupled_intersection(self):
        state = self._make_state(
            "Kaos", "Synchronicity",
            branch=8, meridian="BL",
            coup_branch=8, coup_meridian="BL",
        )
        compounds = detect_compounds(state)
        assert compounds["coupled_intersection"] is True

    def test_full_coupled(self):
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            branch=8, meridian="BL",
            coup_branch=8, coup_meridian="BL",
        )
        compounds = detect_compounds(state)
        assert compounds["full_coupled"] is True

    # ── Category 4: Polarity ──

    def test_polarity_aligned_yang(self):
        """Yang day + Yang vessel = polarity aligned."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            is_yang_day=True, polarity="Yang",
        )
        compounds = detect_compounds(state)
        assert compounds["polarity_aligned"] is True

    def test_polarity_aligned_yin(self):
        """Yin day + Yin vessel = polarity aligned."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            is_yang_day=False, yin_day_restricted=False,
            polarity="Yin",
        )
        compounds = detect_compounds(state)
        assert compounds["polarity_aligned"] is True

    def test_polarity_misaligned(self):
        """Yang day + Yin vessel = not aligned."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            is_yang_day=True, polarity="Yin",
        )
        compounds = detect_compounds(state)
        assert compounds["polarity_aligned"] is False

    # ── Category 5: Calendar ──

    def test_great_rite_active(self):
        """Month with a Great Rite is detected."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            great_rite="Autumn Equinox",
        )
        compounds = detect_compounds(state)
        assert compounds["great_rite_active"] is True

    def test_great_rite_inactive(self):
        """Month without a Great Rite."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            great_rite=None,
        )
        compounds = detect_compounds(state)
        assert compounds["great_rite_active"] is False

    def test_vadusfadahm_active(self):
        """Month 13 is VADUSFADAHM."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            month_number=13,
        )
        compounds = detect_compounds(state)
        assert compounds["vadusfadahm_active"] is True

    def test_vadusfadahm_inactive(self):
        """Regular month is not VADUSFADAHM."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            month_number=6,
        )
        compounds = detect_compounds(state)
        assert compounds["vadusfadahm_active"] is False

    def test_sephirotic_rare_day_9(self):
        """Sephirotic day 9 (Kether) is rare."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            sephirotic_day=9,
        )
        compounds = detect_compounds(state)
        assert compounds["sephirotic_rare"] is True

    def test_sephirotic_not_rare(self):
        """Sephirotic day 5 is not rare."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            sephirotic_day=5,
        )
        compounds = detect_compounds(state)
        assert compounds["sephirotic_rare"] is False

    # ── Category 6: Multi-Layer ──

    def test_key_amplified_unity(self):
        """Two-Body Unity + Key active = Key-Amplified."""
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            key_active=True, key_name="gold", key_law="Fall of Events",
        )
        compounds = detect_compounds(state)
        assert compounds["two_body_unity"] is True
        assert compounds["key_amplified_unity"] is True

    def test_key_amplified_requires_unity(self):
        """Key alone without Unity is not Key-Amplified."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            key_active=True, key_name="gold", key_law="Fall of Events",
        )
        compounds = detect_compounds(state)
        assert compounds["two_body_unity"] is False
        assert compounds["key_amplified_unity"] is False

    def test_anatomical_key(self):
        """Anatomical Intersection + Key active."""
        state = self._make_state(
            "Kaos", "Synchronicity",
            branch=7, meridian="SI",
            conf_branch=7, conf_meridian="SI",
            key_active=True, key_name="silver", key_law="Divinity",
        )
        compounds = detect_compounds(state)
        assert compounds["confluent_intersection"] is True
        assert compounds["anatomical_key"] is True

    def test_full_alignment_key(self):
        """Full Confluent Alignment + Key active = maximum compound."""
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            branch=7, meridian="SI",
            conf_branch=7, conf_meridian="SI",
            key_active=True, key_name="gold", key_law="Fall of Events",
        )
        compounds = detect_compounds(state)
        assert compounds["full_confluent"] is True
        assert compounds["key_amplified_unity"] is True
        assert compounds["anatomical_key"] is True
        assert compounds["full_alignment_key"] is True

    def test_full_alignment_key_blocked_by_yin(self):
        """Yin day blocks Full Alignment + Key."""
        state = self._make_state(
            "Synchronicity", "Synchronicity",
            branch=7, meridian="SI",
            conf_branch=7, conf_meridian="SI",
            key_active=True, key_name="gold", key_law="Fall of Events",
            is_yang_day=False, yin_day_restricted=True,
        )
        compounds = detect_compounds(state)
        assert compounds["full_alignment_key"] is False
        assert compounds["key_amplified_unity"] is False


class TestKnownDatetimes:
    """Spot-check complete state for known datetimes."""

    def test_midday_march_1_2026(self):
        """Basic sanity: midday in LA on March 1, 2026."""
        dt = datetime(2026, 3, 1, 12, 0, 0)
        state = calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)

        # Should be daytime
        assert state["divine_hour"]["wing"] == "Day"
        # Should not be in cusping window at noon
        assert state["solar_key"]["active"] is False
        # Primeval law should come from registry (any valid law)
        assert state["primeval"]["law"] in [
            "Synchronicity", "Sole Atom", "Divinity", "Geometric Essence",
            "Time Matrix", "Fall of Events", "Kaos", "Arrow of Complexity",
        ]
        # Derivative law should come from registry
        assert state["derivative"]["law"] in [
            "Synchronicity", "Sole Atom", "Divinity", "Geometric Essence",
            "Time Matrix", "Fall of Events", "Kaos", "Arrow of Complexity",
        ]

    def test_nighttime(self):
        """11 PM should be night wing."""
        dt = datetime(2026, 3, 1, 23, 0, 0)
        state = calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)
        assert state["divine_hour"]["wing"] == "Night"

    def test_aware_datetime(self):
        """Should handle timezone-aware datetimes."""
        tz = pytz.timezone(LA_TZ)
        dt = tz.localize(datetime(2026, 3, 1, 14, 0, 0))
        state = calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)
        assert "timestamp" in state


class TestEnrichedFields:
    """Verify all enriched fields appear in the complete state output."""

    @pytest.fixture
    def state(self):
        dt = datetime(2026, 3, 1, 14, 0, 0)
        return calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)

    # ── Organ Clock enriched fields ──

    def test_organ_clock_sense_organ(self, state):
        """sense_organ field present in organ_clock layer."""
        assert "sense_organ" in state["organ_clock"]

    def test_organ_clock_body_tissue(self, state):
        """body_tissue field present in organ_clock layer."""
        assert "body_tissue" in state["organ_clock"]

    def test_organ_clock_healing_sound(self, state):
        """healing_sound field present and non-empty."""
        assert "healing_sound" in state["organ_clock"]
        assert state["organ_clock"]["healing_sound"] is not None

    def test_organ_clock_healing_color(self, state):
        assert "healing_color" in state["organ_clock"]

    def test_organ_clock_organ_spirit(self, state):
        assert "organ_spirit" in state["organ_clock"]

    def test_organ_clock_organ_season(self, state):
        assert "organ_season" in state["organ_clock"]

    def test_organ_clock_emotions(self, state):
        assert "emotion_negative" in state["organ_clock"]
        assert "emotion_positive" in state["organ_clock"]

    def test_organ_clock_conf_coup_vessels(self, state):
        """Organ clock reports confluent and coupled vessel associations."""
        assert "conf_vessel" in state["organ_clock"]
        assert "coup_vessel" in state["organ_clock"]

    # ── Derivative enriched fields ──

    def test_derivative_vessel_english(self, state):
        """vessel_english field present in derivative layer."""
        assert "vessel_english" in state["derivative"]
        assert state["derivative"]["vessel_english"] is not None

    def test_derivative_vessel_clinical_domain(self, state):
        """vessel_clinical_domain field present in derivative layer."""
        assert "vessel_clinical_domain" in state["derivative"]
        assert state["derivative"]["vessel_clinical_domain"] is not None

    def test_derivative_trigram_family(self, state):
        assert "trigram_family" in state["derivative"]

    def test_derivative_trigram_nature(self, state):
        assert "trigram_nature" in state["derivative"]

    def test_derivative_trigram_direction(self, state):
        assert "trigram_direction" in state["derivative"]

    def test_derivative_trigram_season(self, state):
        assert "trigram_season" in state["derivative"]

    def test_derivative_trigram_image(self, state):
        assert "trigram_image" in state["derivative"]

    def test_derivative_trigram_action(self, state):
        assert "trigram_action" in state["derivative"]

    def test_derivative_practice_context(self, state):
        """Derivative layer has all practice context fields."""
        d = state["derivative"]
        assert "vowel" in d
        assert "mudra" in d
        assert "adonaj_ba" in d
        assert "color" in d
        assert "perception_pos" in d
        assert "perception_neg" in d
        assert "quest_short" in d
        assert "quest_tarot" in d
        assert "binary" in d
        assert "symbol" in d

    # ── Primeval enriched fields ──

    def test_primeval_trigram_family(self, state):
        assert "trigram_family" in state["primeval"]

    def test_primeval_trigram_nature(self, state):
        assert "trigram_nature" in state["primeval"]

    def test_primeval_trigram_direction(self, state):
        assert "trigram_direction" in state["primeval"]

    def test_primeval_trigram_season(self, state):
        assert "trigram_season" in state["primeval"]

    def test_primeval_practice_context(self, state):
        """Primeval layer has all practice context fields."""
        p = state["primeval"]
        assert "vowel" in p
        assert "mudra" in p
        assert "adonaj_ba" in p
        assert "color" in p
        assert "perception_pos" in p
        assert "perception_neg" in p
        assert "quest_short" in p
        assert "quest_tarot" in p
        assert "binary" in p

    # ── Calendar enriched fields ──

    def test_calendar_month_tier_0_character(self, state):
        """month_tier_0_character field present in calendar layer."""
        assert "month_tier_0_character" in state["calendar"]

    def test_calendar_month_element(self, state):
        assert "month_element" in state["calendar"]

    def test_calendar_iao(self, state):
        assert "iao" in state["calendar"]

    def test_calendar_alchemical(self, state):
        assert "alchemical" in state["calendar"]
        assert state["calendar"]["alchemical"] is not None

    def test_calendar_sephirotic_pillar(self, state):
        assert "sephirotic_pillar" in state["calendar"]

    def test_calendar_sephirotic_frequency(self, state):
        assert "sephirotic_frequency" in state["calendar"]

    def test_calendar_sephirotic_symbol(self, state):
        assert "sephirotic_symbol" in state["calendar"]


class TestSolarKeyPracticeFields:
    """Verify Solar Key has all practice fields when active."""

    def test_key_active_has_practice_fields(self):
        """At sunrise, gold key active — all practice fields populated."""
        from src.engine.solar import get_solar_positions

        solar_pos = get_solar_positions(
            datetime(2026, 3, 1, 6, 0, 0), LA_LAT, LA_LON, LA_TZ
        )
        sunrise = solar_pos["sunrise"]
        state = calculate_complete_state(sunrise, LA_LAT, LA_LON, LA_TZ)

        key = state["solar_key"]
        assert key["active"] is True
        assert key["key"] == "gold"
        assert key["law"] == "Fall of Events"
        assert key["prime"] == 11
        assert key["trigram"] == "Kǎn"
        assert key["symbol"] == "☵"
        assert "window_start" in key
        assert "window_end" in key
        assert "radius_minutes" in key
        # Practice fields
        assert "vowel" in key
        assert "mudra" in key
        assert "adonaj_ba" in key
        assert "color" in key
        assert "perception_pos" in key
        assert "perception_neg" in key

    def test_key_inactive_has_null_law(self):
        """At midday, no key active — law and prime are None."""
        dt = datetime(2026, 3, 1, 12, 0, 0)
        state = calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)
        key = state["solar_key"]
        assert key["active"] is False
        assert key["law"] is None
        assert key["prime"] is None


class TestDeadZoneBranches:
    """Verify organs with no vessel confluent/coupled return null gracefully."""

    def test_dead_zone_branch_liver(self):
        """Liver (branch 1) has no confluent or coupled vessel."""
        from src import registry
        organ = registry.get_organ_by_branch(1)
        assert organ["organ"] == "Liver"
        assert organ["conf_vessel"] is None
        assert organ["coup_vessel"] is None

    def test_dead_zone_branch_lg_intestine(self):
        """Lg Intestine (branch 3) has no confluent or coupled vessel."""
        from src import registry
        organ = registry.get_organ_by_branch(3)
        assert organ["organ"] == "Lg Intestine"
        assert organ["conf_vessel"] is None
        assert organ["coup_vessel"] is None

    def test_active_zone_branch_sm_intestine(self):
        """Sm Intestine (branch 7) has Du Mai confluent and Yang Qiao Mai coupled."""
        from src import registry
        organ = registry.get_organ_by_branch(7)
        assert organ["organ"] == "Sm Intestine"
        assert organ["conf_vessel"] == "Du Mai"
        assert organ["coup_vessel"] == "Yang Qiao Mai"

    def test_dead_zone_count(self):
        """Exactly 4 branches have no vessel associations (dead zones)."""
        from src import registry
        dead = 0
        for i in range(12):
            organ = registry.get_organ_by_branch(i)
            if organ["conf_vessel"] is None and organ["coup_vessel"] is None:
                dead += 1
        assert dead == 4  # Liver, Lg Intestine, Stomach, Heart
