"""
Registry tests — verifies structural completeness of registers.json
and locks spec-critical assignments.
"""

import pytest
from src import registry


class TestStructuralCompleteness:
    """All registers present and cross-referenced correctly."""

    def test_eight_laws(self):
        laws = registry.all_laws()
        assert len(laws) == 8
        expected = {
            "Synchronicity", "Sole Atom", "Divinity", "Geometric Essence",
            "Time Matrix", "Fall of Events", "Kaos", "Arrow of Complexity",
        }
        assert set(laws.keys()) == expected

    def test_eight_trigrams(self):
        trigrams = registry.all_trigrams()
        assert len(trigrams) == 8

    def test_eight_vessels(self):
        vessels = registry.all_vessels()
        assert len(vessels) == 8
        expected = {
            "Du Mai", "Ren Mai", "Chong Mai", "Dai Mai",
            "Yang Qiao Mai", "Yin Qiao Mai", "Yang Wei Mai", "Yin Wei Mai",
        }
        assert set(vessels.keys()) == expected

    def test_twelve_organs(self):
        organs = registry.all_organs()
        assert len(organs) == 12

    def test_six_lunar_phases(self):
        for i in range(6):
            phase = registry.get_lunar_phase(i)
            assert "law" in phase
            assert "trigram" in phase

    def test_two_solar_keys(self):
        gold = registry.get_solar_key("gold")
        silver = registry.get_solar_key("silver")
        assert gold["event"] == "sunrise"
        assert silver["event"] == "sunset"

    def test_eight_divine_hours(self):
        for i in range(1, 9):
            hour = registry.get_divine_hour(i)
            assert "wing" in hour

    def test_thirteen_divine_months(self):
        for i in range(1, 14):
            month = registry.get_divine_month(i)
            assert "name" in month

    def test_nine_sephirotic_days(self):
        for i in range(1, 10):
            day = registry.get_sephirotic_day(i)
            assert "sephirah" in day


class TestCrossReferences:
    """Every vessel's law exists in laws dict, etc."""

    def test_vessel_laws_exist(self):
        vessels = registry.all_vessels()
        laws = registry.all_laws()
        for name, v in vessels.items():
            assert v["law"] in laws, f"Vessel {name} has unknown law {v['law']}"

    def test_lunar_phase_trigrams_exist(self):
        trigrams = registry.all_trigrams()
        for i in range(6):
            phase = registry.get_lunar_phase(i)
            assert phase["trigram"] in trigrams, (
                f"Phase {i} has unknown trigram {phase['trigram']}"
            )

    def test_vessel_primes_match_law_primes(self):
        vessels = registry.all_vessels()
        laws = registry.all_laws()
        for name, v in vessels.items():
            law = laws[v["law"]]
            assert v["prime"] == law["prime"], (
                f"Vessel {name}: prime {v['prime']} != law prime {law['prime']}"
            )

    def test_organ_branch_indices_complete(self):
        organs = registry.all_organs()
        indices = {o["branch_index"] for o in organs}
        assert indices == set(range(12))


class TestSpecLock:
    """Lock spec-critical values: these MUST match the 6+2 architecture."""

    def test_gold_key_law(self):
        """Gold Key = Fall of Events (prime 11). NOT Sole Atom."""
        gold = registry.get_solar_key("gold")
        assert gold["law"] == "Fall of Events"
        assert gold["prime"] == 11
        assert gold["trigram"] == "Kǎn"

    def test_silver_key_law(self):
        """Silver Key = Divinity (prime 31)."""
        silver = registry.get_solar_key("silver")
        assert silver["law"] == "Divinity"
        assert silver["prime"] == 31
        assert silver["trigram"] == "Lí"

    def test_zhen_is_sole_atom(self):
        """Zhèn ☳ = Sole Atom (prime 19). NOT Fall of Events."""
        law = registry.get_law("Sole Atom")
        assert law["trigram"] == "Zhèn"
        assert law["prime"] == 19

    def test_kan_is_fall_of_events(self):
        """Kǎn ☵ = Fall of Events (prime 11)."""
        law = registry.get_law("Fall of Events")
        assert law["trigram"] == "Kǎn"
        assert law["prime"] == 11

    def test_solar_keys_are_marked(self):
        """Only Divinity and Fall of Events are solar key laws."""
        laws = registry.all_laws()
        key_laws = {n for n, l in laws.items() if l.get("is_solar_key")}
        assert key_laws == {"Fall of Events", "Divinity"}

    def test_vessel_to_law_assignments(self):
        """All 8 vessel→law assignments from Register C."""
        expected = {
            "Du Mai": "Synchronicity",
            "Ren Mai": "Kaos",
            "Chong Mai": "Arrow of Complexity",
            "Dai Mai": "Time Matrix",
            "Yang Qiao Mai": "Divinity",
            "Yin Qiao Mai": "Fall of Events",
            "Yang Wei Mai": "Sole Atom",
            "Yin Wei Mai": "Geometric Essence",
        }
        vessels = registry.all_vessels()
        for name, law in expected.items():
            assert vessels[name]["law"] == law, (
                f"Vessel {name}: expected {law}, got {vessels[name]['law']}"
            )

    def test_lunar_phase_law_sequence(self):
        """6 cyclic phases in Cantong qi order."""
        expected = [
            ("Kaos", 23),
            ("Sole Atom", 19),
            ("Time Matrix", 29),
            ("Synchronicity", 89),
            ("Geometric Essence", 67),
            ("Arrow of Complexity", 17),
        ]
        for i, (law, prime) in enumerate(expected):
            phase = registry.get_lunar_phase(i)
            assert phase["law"] == law, f"Phase {i}: expected {law}, got {phase['law']}"
            assert phase["prime"] == prime

    def test_yin_day_restrictions(self):
        """Ren Mai and Yang Wei Mai are NOT yin-day restricted."""
        vessels = registry.all_vessels()
        assert vessels["Ren Mai"]["yin_day_restricted"] is False
        assert vessels["Yang Wei Mai"]["yin_day_restricted"] is False
        # The other 6 ARE restricted
        for name in ["Du Mai", "Chong Mai", "Dai Mai",
                      "Yang Qiao Mai", "Yin Qiao Mai", "Yin Wei Mai"]:
            assert vessels[name]["yin_day_restricted"] is True, (
                f"{name} should be yin_day_restricted"
            )


class TestErrorHandling:
    """Registry raises clear errors for bad lookups."""

    def test_unknown_law(self):
        with pytest.raises(KeyError, match="Unknown law"):
            registry.get_law("Nonexistent")

    def test_unknown_vessel(self):
        with pytest.raises(KeyError, match="Unknown vessel"):
            registry.get_vessel("Nonexistent")

    def test_bad_remainder(self):
        with pytest.raises(KeyError):
            registry.get_vessel_for_remainder(99)

    def test_bad_branch(self):
        with pytest.raises(KeyError):
            registry.get_organ_by_branch(99)

    def test_bad_phase(self):
        with pytest.raises(KeyError):
            registry.get_lunar_phase(99)

    def test_unknown_organ_name(self):
        with pytest.raises(KeyError, match="No organ with name"):
            registry.get_organ_by_name("Nonexistent")

    def test_unknown_inner_alchemy_organ(self):
        with pytest.raises(KeyError, match="No inner alchemy entry for organ"):
            registry.get_inner_alchemy_for_organ("Nonexistent")

    def test_bad_divine_month(self):
        with pytest.raises(KeyError):
            registry.get_divine_month(99)

    def test_bad_sephirotic_day(self):
        with pytest.raises(KeyError):
            registry.get_sephirotic_day(99)

    def test_unknown_inner_alchemy_element(self):
        with pytest.raises(KeyError, match="Unknown element"):
            registry.get_inner_alchemy("Nonexistent")


class TestInnerAlchemyForOrgan:
    """Test get_inner_alchemy_for_organ() — San Jiao / Pericardium split is critical."""

    def test_san_jiao_heeeee(self):
        """San Jiao has its own entry: HEEEEE (NOT HAWWWW from Fire)."""
        result = registry.get_inner_alchemy_for_organ("San Jiao")
        assert result["sound"] == "HEEEEE"
        assert result["alchemy_key"] == "San Jiao"

    def test_pericardium_hawwww(self):
        """Pericardium shares Fire's entry: HAWWWW."""
        result = registry.get_inner_alchemy_for_organ("Pericardium")
        assert result["sound"] == "HAWWWW"
        assert result["alchemy_key"] == "Fire"

    def test_heart_hawwww(self):
        """Heart is Fire element: HAWWWW."""
        result = registry.get_inner_alchemy_for_organ("Heart")
        assert result["sound"] == "HAWWWW"

    def test_sm_intestine_hawwww(self):
        """Sm Intestine is Fire element: HAWWWW."""
        result = registry.get_inner_alchemy_for_organ("Sm Intestine")
        assert result["sound"] == "HAWWWW"

    def test_liver_shhhhh(self):
        """Liver is Wood: SHHHHH."""
        result = registry.get_inner_alchemy_for_organ("Liver")
        assert result["sound"] == "SHHHHH"

    def test_lung_sssssss(self):
        """Lung is Metal: SSSSSSS."""
        result = registry.get_inner_alchemy_for_organ("Lung")
        assert result["sound"] == "SSSSSSS"

    def test_kidney_wooooo(self):
        """Kidney is Water: WOOOOO."""
        result = registry.get_inner_alchemy_for_organ("Kidney")
        assert result["sound"] == "WOOOOO"

    def test_stomach_whoooo(self):
        """Stomach is Earth: WHOOOO."""
        result = registry.get_inner_alchemy_for_organ("Stomach")
        assert result["sound"] == "WHOOOO"

    def test_every_organ_has_inner_alchemy(self):
        """All 12 organ names return an inner alchemy entry without error."""
        organs = registry.all_organs()
        for organ in organs:
            result = registry.get_inner_alchemy_for_organ(organ["organ"])
            assert "sound" in result
            assert "color" in result


class TestDataConsistencyLaws:
    """Verify every Law has all expected enriched fields."""

    def test_all_laws_have_practice_fields(self):
        """All 8 laws have vowel, mudra, adonaj_ba, color."""
        laws = registry.all_laws()
        for name, law in laws.items():
            assert "vowel" in law, f"{name} missing vowel"
            assert "mudra" in law, f"{name} missing mudra"
            assert "adonaj_ba" in law, f"{name} missing adonaj_ba"
            assert "color" in law, f"{name} missing color"

    def test_all_laws_have_perception_fields(self):
        """All 8 laws have perception_pos and perception_neg."""
        laws = registry.all_laws()
        for name, law in laws.items():
            assert "perception_pos" in law, f"{name} missing perception_pos"
            assert "perception_neg" in law, f"{name} missing perception_neg"

    def test_all_laws_have_quest_fields(self):
        """All 8 laws have quest_short and quest_tarot."""
        laws = registry.all_laws()
        for name, law in laws.items():
            assert "quest_short" in law, f"{name} missing quest_short"
            assert "quest_tarot" in law, f"{name} missing quest_tarot"

    def test_all_laws_have_binary_and_symbol(self):
        """All 8 laws have binary and symbol."""
        laws = registry.all_laws()
        for name, law in laws.items():
            assert "binary" in law, f"{name} missing binary"
            assert "symbol" in law, f"{name} missing symbol"


class TestDataConsistencyTrigrams:
    """Verify every trigram has all enriched I Ching fields."""

    def test_all_trigrams_have_family(self):
        trigrams = registry.all_trigrams()
        for name, t in trigrams.items():
            assert "family" in t, f"{name} missing family"
            assert t["family"] is not None, f"{name} family is None"

    def test_all_trigrams_have_nature(self):
        trigrams = registry.all_trigrams()
        for name, t in trigrams.items():
            assert "nature" in t, f"{name} missing nature"
            assert t["nature"] is not None, f"{name} nature is None"

    def test_all_trigrams_have_direction(self):
        trigrams = registry.all_trigrams()
        for name, t in trigrams.items():
            assert "direction" in t, f"{name} missing direction"
            assert t["direction"] is not None, f"{name} direction is None"

    def test_all_trigrams_have_season(self):
        trigrams = registry.all_trigrams()
        for name, t in trigrams.items():
            assert "season" in t, f"{name} missing season"
            assert t["season"] is not None, f"{name} season is None"

    def test_all_trigrams_have_image_and_action(self):
        trigrams = registry.all_trigrams()
        for name, t in trigrams.items():
            assert "image" in t, f"{name} missing image"
            assert "action" in t, f"{name} missing action"

    def test_all_trigrams_have_plum_blossom(self):
        trigrams = registry.all_trigrams()
        for name, t in trigrams.items():
            assert "plum_blossom" in t, f"{name} missing plum_blossom"


class TestDataConsistencyVessels:
    """Verify every vessel has enriched fields."""

    def test_all_vessels_have_english_name(self):
        vessels = registry.all_vessels()
        for name, v in vessels.items():
            assert "english_name" in v, f"{name} missing english_name"
            assert v["english_name"] is not None, f"{name} english_name is None"

    def test_all_vessels_have_clinical_domain(self):
        vessels = registry.all_vessels()
        for name, v in vessels.items():
            assert "clinical_domain" in v, f"{name} missing clinical_domain"
            assert v["clinical_domain"] is not None, f"{name} clinical_domain is None"


class TestDataConsistencyMonths:
    """Verify all 13 divine months have tier_0_character."""

    def test_all_months_have_tier_0_character(self):
        for num in range(1, 14):
            month = registry.get_divine_month(num)
            assert "tier_0_character" in month, f"Month {num} missing tier_0_character"
            assert month["tier_0_character"] is not None, (
                f"Month {num} ({month['name']}) tier_0_character is None"
            )

    def test_tier_0_characters_match_spec(self):
        """Verify specific Tier 0 characters from the locked spec."""
        expected = {
            1: "The Gatherer",
            4: "The Director",
            7: "The Resurrected",
            9: "The Container",
            10: "The Destroyer",
            13: "The Activation",
        }
        for num, char in expected.items():
            month = registry.get_divine_month(num)
            assert month["tier_0_character"] == char, (
                f"Month {num}: expected '{char}', got '{month['tier_0_character']}'"
            )


class TestDataConsistencyInnerAlchemy:
    """Verify all 6 inner alchemy entries have sense_organ and body_tissue."""

    def test_five_element_have_sense_organ(self):
        """The 5 Wu Xing entries have sense_organ."""
        for element in ["Wood", "Fire", "Earth", "Metal", "Water"]:
            entry = registry.get_inner_alchemy(element)
            assert "sense_organ" in entry, f"{element} missing sense_organ"
            assert entry["sense_organ"] is not None, f"{element} sense_organ is None"

    def test_five_element_have_body_tissue(self):
        """The 5 Wu Xing entries have body_tissue."""
        for element in ["Wood", "Fire", "Earth", "Metal", "Water"]:
            entry = registry.get_inner_alchemy(element)
            assert "body_tissue" in entry, f"{element} missing body_tissue"
            assert entry["body_tissue"] is not None, f"{element} body_tissue is None"

    def test_san_jiao_has_null_sense_organ(self):
        """San Jiao has null sense_organ and body_tissue (no Wu Xing element)."""
        entry = registry.get_inner_alchemy("San Jiao")
        assert entry["sense_organ"] is None
        assert entry["body_tissue"] is None

    def test_specific_sense_organs(self):
        """Spot-check sense organ values from TCM canon."""
        assert registry.get_inner_alchemy("Wood")["sense_organ"] == "Eyes"
        assert registry.get_inner_alchemy("Fire")["sense_organ"] == "Tongue"
        assert registry.get_inner_alchemy("Earth")["sense_organ"] == "Mouth"
        assert registry.get_inner_alchemy("Metal")["sense_organ"] == "Nose"
        assert registry.get_inner_alchemy("Water")["sense_organ"] == "Ears"

    def test_specific_body_tissues(self):
        """Spot-check body tissue values from TCM canon."""
        assert registry.get_inner_alchemy("Wood")["body_tissue"] == "Tendons/Ligaments"
        assert registry.get_inner_alchemy("Fire")["body_tissue"] == "Blood vessels"
        assert registry.get_inner_alchemy("Water")["body_tissue"] == "Bones/Marrow"
