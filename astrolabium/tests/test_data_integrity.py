"""
Data Integrity Audit — Final Quality Gate Before Frontend UI.

Comprehensive cross-validation of registers.json, resonances.json,
and meta_registry.py. Tests every internal reference, cross-file
consistency, TCM pair reciprocity, organ clock coverage, inner alchemy coverage,
calendar structure, sephirotic ordering, field uniformity, primality
verification, value domain constraints, null inventory, and resonance
lookup table consistency.

Generated: 2026-03-19
Updated: 2026-03-19 (field uniformity, primes, value domains, nulls,
         resonance lookup coverage, meta-registry integration)
Author: Meridian (data layer audit)
"""

import json
import re
from pathlib import Path

import pytest

# ── Data Loading ────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture(scope="module")
def registers():
    with open(DATA_DIR / "registers.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def resonances():
    with open(DATA_DIR / "resonances.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def laws(registers):
    return registers["laws"]


@pytest.fixture(scope="module")
def trigrams(registers):
    return registers["trigrams"]


@pytest.fixture(scope="module")
def vessels(registers):
    return registers["vessels"]


@pytest.fixture(scope="module")
def organs(registers):
    return registers["organs"]


@pytest.fixture(scope="module")
def inner_alchemy(registers):
    return registers["inner_alchemy"]


@pytest.fixture(scope="module")
def lunar_phases(registers):
    return registers["lunar_phases"]


@pytest.fixture(scope="module")
def divine_months(registers):
    return registers["divine_months"]


@pytest.fixture(scope="module")
def sephirotic_days(registers):
    return registers["sephirotic_days"]


@pytest.fixture(scope="module")
def vessel_remainder_map(registers):
    return registers["vessel_remainder_map"]


# Helper lookups
@pytest.fixture(scope="module")
def organ_abbrs(organs):
    return {o["abbr"] for o in organs}


@pytest.fixture(scope="module")
def organ_names(organs):
    return {o["organ"] for o in organs}


@pytest.fixture(scope="module")
def organ_branch_indices(organs):
    return {o["branch_index"] for o in organs}


@pytest.fixture(scope="module")
def organ_by_name(organs):
    return {o["organ"]: o for o in organs}


@pytest.fixture(scope="module")
def law_names(laws):
    return set(laws.keys())


@pytest.fixture(scope="module")
def trigram_names(trigrams):
    return set(trigrams.keys())


@pytest.fixture(scope="module")
def vessel_names(vessels):
    return set(vessels.keys())


# ====================================================================
# 1. INTERNAL CONSISTENCY OF REGISTERS.JSON
# ====================================================================


class TestVesselInternalConsistency:
    """Every vessel's references resolve to valid entities."""

    def test_vessel_law_references_valid_law(self, vessels, law_names):
        for vname, v in vessels.items():
            assert v["law"] in law_names, (
                f"Vessel '{vname}' references law '{v['law']}' "
                f"which is not in laws: {law_names}"
            )

    def test_vessel_conf_meridian_matches_organ_abbr(self, vessels, organ_abbrs):
        for vname, v in vessels.items():
            assert v["conf_meridian"] in organ_abbrs, (
                f"Vessel '{vname}' conf_meridian '{v['conf_meridian']}' "
                f"not in organ abbreviations: {organ_abbrs}"
            )

    def test_vessel_coup_meridian_matches_organ_abbr(self, vessels, organ_abbrs):
        for vname, v in vessels.items():
            assert v["coup_meridian"] in organ_abbrs, (
                f"Vessel '{vname}' coup_meridian '{v['coup_meridian']}' "
                f"not in organ abbreviations: {organ_abbrs}"
            )

    def test_vessel_conf_branch_matches_organ_branch(self, vessels, organ_branch_indices):
        for vname, v in vessels.items():
            assert v["conf_branch"] in organ_branch_indices, (
                f"Vessel '{vname}' conf_branch {v['conf_branch']} "
                f"not in organ branch indices: {organ_branch_indices}"
            )

    def test_vessel_coup_branch_matches_organ_branch(self, vessels, organ_branch_indices):
        for vname, v in vessels.items():
            assert v["coup_branch"] in organ_branch_indices, (
                f"Vessel '{vname}' coup_branch {v['coup_branch']} "
                f"not in organ branch indices: {organ_branch_indices}"
            )

    def test_vessel_conf_meridian_and_branch_consistent(self, vessels, organs):
        """conf_meridian's branch_index must equal conf_branch."""
        abbr_to_branch = {o["abbr"]: o["branch_index"] for o in organs}
        for vname, v in vessels.items():
            expected_branch = abbr_to_branch[v["conf_meridian"]]
            assert v["conf_branch"] == expected_branch, (
                f"Vessel '{vname}': conf_meridian '{v['conf_meridian']}' "
                f"has branch_index {expected_branch} but conf_branch is {v['conf_branch']}"
            )

    def test_vessel_coup_meridian_and_branch_consistent(self, vessels, organs):
        """coup_meridian's branch_index must equal coup_branch."""
        abbr_to_branch = {o["abbr"]: o["branch_index"] for o in organs}
        for vname, v in vessels.items():
            expected_branch = abbr_to_branch[v["coup_meridian"]]
            assert v["coup_branch"] == expected_branch, (
                f"Vessel '{vname}': coup_meridian '{v['coup_meridian']}' "
                f"has branch_index {expected_branch} but coup_branch is {v['coup_branch']}"
            )


class TestOrganInternalConsistency:
    """Every organ's references resolve to valid entities."""

    def test_organ_conf_vessel_references_valid_vessel(self, organs, vessel_names):
        for o in organs:
            if o["conf_vessel"] is not None:
                assert o["conf_vessel"] in vessel_names, (
                    f"Organ '{o['organ']}' conf_vessel '{o['conf_vessel']}' "
                    f"not in vessels: {vessel_names}"
                )

    def test_organ_coup_vessel_references_valid_vessel(self, organs, vessel_names):
        for o in organs:
            if o["coup_vessel"] is not None:
                assert o["coup_vessel"] in vessel_names, (
                    f"Organ '{o['organ']}' coup_vessel '{o['coup_vessel']}' "
                    f"not in vessels: {vessel_names}"
                )

    def test_organ_paired_references_valid_organ(self, organs, organ_names):
        for o in organs:
            assert o["paired"] in organ_names, (
                f"Organ '{o['organ']}' paired field '{o['paired']}' "
                f"not in organ names: {organ_names}"
            )


class TestLunarPhaseConsistency:
    """Lunar phase references resolve correctly."""

    def test_lunar_phase_trigrams_valid(self, lunar_phases, trigram_names):
        for lp in lunar_phases:
            assert lp["trigram"] in trigram_names, (
                f"Lunar phase '{lp['name']}' trigram '{lp['trigram']}' "
                f"not in trigrams: {trigram_names}"
            )

    def test_lunar_phase_laws_valid(self, lunar_phases, law_names):
        for lp in lunar_phases:
            assert lp["law"] in law_names, (
                f"Lunar phase '{lp['name']}' law '{lp['law']}' "
                f"not in laws: {law_names}"
            )

    def test_six_cyclic_phases(self, lunar_phases):
        """6+2 architecture: 6 cyclic phases (Kan and Li excluded as solar keys)."""
        assert len(lunar_phases) == 6

    def test_lunar_phase_indices_sequential(self, lunar_phases):
        indices = [lp["index"] for lp in lunar_phases]
        assert indices == list(range(6))

    def test_no_solar_key_trigrams_in_cycle(self, lunar_phases):
        """Kan and Li must NOT appear in the cyclic lunar phases."""
        solar_key_trigrams = {"Kǎn", "Lí"}
        cycle_trigrams = {lp["trigram"] for lp in lunar_phases}
        overlap = solar_key_trigrams & cycle_trigrams
        assert not overlap, (
            f"Solar key trigrams found in lunar cycle: {overlap}"
        )

    def test_elongation_ranges_cover_full_circle(self, lunar_phases):
        """Phases should cover 0-360 degrees without gaps."""
        sorted_phases = sorted(lunar_phases, key=lambda p: p["elong_start"])
        assert sorted_phases[0]["elong_start"] == 0
        assert sorted_phases[-1]["elong_end"] == 360
        for i in range(len(sorted_phases) - 1):
            assert sorted_phases[i]["elong_end"] == sorted_phases[i + 1]["elong_start"], (
                f"Gap between phase {sorted_phases[i]['name']} "
                f"(ends {sorted_phases[i]['elong_end']}) and "
                f"{sorted_phases[i + 1]['name']} "
                f"(starts {sorted_phases[i + 1]['elong_start']})"
            )


class TestTrigramConsistency:
    """Trigram references resolve correctly."""

    def test_trigram_law_references_valid_law(self, trigrams, law_names):
        for tname, t in trigrams.items():
            assert t["law"] in law_names, (
                f"Trigram '{tname}' law '{t['law']}' not in laws: {law_names}"
            )

    def test_trigram_vessel_references_valid_vessel(self, trigrams, vessel_names):
        for tname, t in trigrams.items():
            assert t["vessel"] in vessel_names, (
                f"Trigram '{tname}' vessel '{t['vessel']}' not in vessels: {vessel_names}"
            )

    def test_eight_trigrams(self, trigrams):
        assert len(trigrams) == 8


class TestVesselRemainderMap:
    """Remainder map covers all expected remainders with valid vessels."""

    def test_remainder_keys_complete(self, vessel_remainder_map):
        expected = {str(i) for i in range(1, 10)}
        actual = set(vessel_remainder_map.keys())
        assert actual == expected, (
            f"Expected remainder keys {expected}, got {actual}"
        )

    def test_remainder_values_are_valid_vessels(self, vessel_remainder_map, vessel_names):
        for remainder, vname in vessel_remainder_map.items():
            assert vname in vessel_names, (
                f"Remainder {remainder} maps to '{vname}' "
                f"which is not a valid vessel"
            )


class TestInnerAlchemyOrganCoverage:
    """Inner alchemy entries reference valid organs."""

    def test_inner_alchemy_organs_exist(self, inner_alchemy, organ_names):
        for element, entry in inner_alchemy.items():
            for org in entry["organs"]:
                assert org in organ_names, (
                    f"Inner alchemy '{element}' references organ '{org}' "
                    f"which is not in organs array"
                )


# ====================================================================
# 2. CROSS-VALIDATION REGISTERS.JSON <-> RESONANCES.JSON
# ====================================================================


class TestResonanceCrossValidation:
    """Resonances.json is consistent with registers.json and meta_registry."""

    def test_trigram_names_in_resonances_valid(self, resonances, trigram_names):
        """Every trigram name in resonances lookup tables exists in registers."""
        # trigram_wu_xing
        wu_xing_table = resonances["lookup_tables"]["trigram_wu_xing"]
        for tname in wu_xing_table:
            if tname.startswith("_"):
                continue
            assert tname in trigram_names, (
                f"trigram_wu_xing references '{tname}' not in registers trigrams"
            )

        # trigram_polarity
        polarity_table = resonances["lookup_tables"]["trigram_polarity"]
        for tname in polarity_table:
            if tname.startswith("_"):
                continue
            assert tname in trigram_names, (
                f"trigram_polarity references '{tname}' not in registers trigrams"
            )

    def test_resonance_types_in_meta_registry(self, resonances):
        """Every resonance type in resonances.json is referenced in meta_registry."""
        from src.meta_registry import RESONANCE_PARTICIPATION

        resonance_type_names = set(resonances["resonance_types"].keys())
        # Collect all resonance types referenced in RESONANCE_PARTICIPATION
        referenced_types = set()
        for types_list in RESONANCE_PARTICIPATION.values():
            referenced_types.update(types_list)

        # Every resonance type should be referenced at least once
        unreferenced = resonance_type_names - referenced_types
        assert not unreferenced, (
            f"Resonance types defined in resonances.json but not referenced "
            f"in meta_registry RESONANCE_PARTICIPATION: {unreferenced}"
        )

    def test_trigram_wu_xing_matches_registers(self, resonances, trigrams):
        """trigram_wu_xing lookup in resonances.json matches registers.json trigrams."""
        wu_xing_table = resonances["lookup_tables"]["trigram_wu_xing"]
        for tname, t in trigrams.items():
            assert tname in wu_xing_table, (
                f"Trigram '{tname}' missing from resonances trigram_wu_xing"
            )
            assert wu_xing_table[tname] == t["wu_xing"], (
                f"Trigram '{tname}': resonances says wu_xing='{wu_xing_table[tname]}' "
                f"but registers says wu_xing='{t['wu_xing']}'"
            )

    def test_trigram_polarity_excludes_solar_keys(self, resonances):
        """Kan and Li excluded from polarity table (they are Solar Keys)."""
        polarity_table = resonances["lookup_tables"]["trigram_polarity"]
        non_note_keys = {k for k in polarity_table if not k.startswith("_")}
        assert "Kǎn" not in non_note_keys, "Kǎn should be excluded from polarity table"
        assert "Lí" not in non_note_keys, "Lí should be excluded from polarity table"

    def test_trigram_polarity_covers_six_cyclic(self, resonances):
        """The 6 cyclic trigrams all have polarity entries."""
        polarity_table = resonances["lookup_tables"]["trigram_polarity"]
        expected = {"Qián", "Kūn", "Zhèn", "Xùn", "Gèn", "Duì"}
        non_note_keys = {k for k in polarity_table if not k.startswith("_")}
        assert non_note_keys == expected, (
            f"Expected polarity entries for {expected}, got {non_note_keys}"
        )

    def test_color_affinity_map_uses_real_colors(self, resonances, laws, inner_alchemy):
        """Colors in color_affinity_map appear in laws and inner alchemy."""
        color_map = resonances["lookup_tables"]["color_affinity_map"]
        law_colors = {l["color"] for l in laws.values()}
        alchemy_colors = {c["color"] for c in inner_alchemy.values() if c["color"] is not None}

        for key in color_map:
            if key.startswith("_"):
                continue
            parts = key.split(":")
            assert len(parts) == 2, f"Malformed color_affinity key: {key}"
            law_color, healing_color = parts
            assert law_color in law_colors, (
                f"color_affinity_map law color '{law_color}' "
                f"not in law colors: {law_colors}"
            )
            assert healing_color in alchemy_colors, (
                f"color_affinity_map healing color '{healing_color}' "
                f"not in inner alchemy colors: {alchemy_colors}"
            )


# ====================================================================
# 3. VESSEL PAIR CONSISTENCY
# ====================================================================


class TestVesselPairs:
    """Vessel pair relationships are reciprocal and correct."""

    EXPECTED_PAIRS = [
        ("Du Mai", "Yang Qiao Mai"),
        ("Ren Mai", "Yin Qiao Mai"),
        ("Chong Mai", "Yin Wei Mai"),
        ("Dai Mai", "Yang Wei Mai"),
    ]

    def test_pair_reciprocity(self, vessels):
        """If A's partner is B, B's partner is A."""
        for vname, v in vessels.items():
            partner_name = v["pair_partner"]
            assert partner_name in vessels, (
                f"Vessel '{vname}' partner '{partner_name}' not found"
            )
            partner = vessels[partner_name]
            assert partner["pair_partner"] == vname, (
                f"Vessel '{vname}' says partner is '{partner_name}', "
                f"but '{partner_name}' says partner is '{partner['pair_partner']}'"
            )

    def test_expected_four_pairs(self, vessels):
        """The 4 canonical pairs are present."""
        actual_pairs = set()
        for vname, v in vessels.items():
            pair = tuple(sorted([vname, v["pair_partner"]]))
            actual_pairs.add(pair)
        expected = {tuple(sorted(p)) for p in self.EXPECTED_PAIRS}
        assert actual_pairs == expected, (
            f"Expected pairs {expected}, got {actual_pairs}"
        )

    def test_paired_vessels_share_confluent_coupled_crossover(self, vessels):
        """In each pair, A's confluent point = B's coupled point and vice versa."""
        for a_name, b_name in self.EXPECTED_PAIRS:
            a = vessels[a_name]
            b = vessels[b_name]
            assert a["confluent"] == b["coupled"], (
                f"Pair ({a_name}, {b_name}): "
                f"{a_name} confluent='{a['confluent']}' != "
                f"{b_name} coupled='{b['coupled']}'"
            )
            assert b["confluent"] == a["coupled"], (
                f"Pair ({a_name}, {b_name}): "
                f"{b_name} confluent='{b['confluent']}' != "
                f"{a_name} coupled='{a['coupled']}'"
            )

    def test_paired_vessels_crossover_meridians(self, vessels):
        """In each pair, A's conf_meridian = B's coup_meridian and vice versa."""
        for a_name, b_name in self.EXPECTED_PAIRS:
            a = vessels[a_name]
            b = vessels[b_name]
            assert a["conf_meridian"] == b["coup_meridian"], (
                f"Pair ({a_name}, {b_name}): "
                f"{a_name} conf_meridian='{a['conf_meridian']}' != "
                f"{b_name} coup_meridian='{b['coup_meridian']}'"
            )
            assert b["conf_meridian"] == a["coup_meridian"], (
                f"Pair ({a_name}, {b_name}): "
                f"{b_name} conf_meridian='{b['conf_meridian']}' != "
                f"{a_name} coup_meridian='{a['coup_meridian']}'"
            )

    def test_paired_vessels_crossover_branches(self, vessels):
        """In each pair, A's conf_branch = B's coup_branch and vice versa."""
        for a_name, b_name in self.EXPECTED_PAIRS:
            a = vessels[a_name]
            b = vessels[b_name]
            assert a["conf_branch"] == b["coup_branch"], (
                f"Pair ({a_name}, {b_name}): "
                f"{a_name} conf_branch={a['conf_branch']} != "
                f"{b_name} coup_branch={b['coup_branch']}"
            )
            assert b["conf_branch"] == a["coup_branch"], (
                f"Pair ({a_name}, {b_name}): "
                f"{b_name} conf_branch={b['conf_branch']} != "
                f"{a_name} coup_branch={a['coup_branch']}"
            )


# ====================================================================
# 4. ORGAN CLOCK CONSISTENCY
# ====================================================================


class TestOrganClock:
    """12 organs, correct branch coverage, element distribution, pairing."""

    def test_twelve_organs(self, organs):
        assert len(organs) == 12

    def test_branch_indices_cover_0_to_11(self, organs):
        indices = sorted(o["branch_index"] for o in organs)
        assert indices == list(range(12))

    def test_element_distribution(self, organs):
        """
        TCM element distribution:
        Wood x2 (Liver, Gallbladder)
        Fire x4 (Heart, Sm Intestine, Pericardium, San Jiao)
        Earth x2 (Spleen, Stomach)
        Metal x2 (Lung, Lg Intestine)
        Water x2 (Kidney, Bladder)
        """
        from collections import Counter
        element_counts = Counter(o["element"] for o in organs)
        expected = {"Wood": 2, "Fire": 4, "Earth": 2, "Metal": 2, "Water": 2}
        assert dict(element_counts) == expected, (
            f"Element distribution mismatch: got {dict(element_counts)}, "
            f"expected {expected}"
        )

    def test_yin_yang_pairing(self, organs, organ_by_name):
        """Each yin organ's paired field names a yang organ and vice versa."""
        for o in organs:
            partner = organ_by_name[o["paired"]]
            if o["yin_yang"] == "Yin":
                assert partner["yin_yang"] == "Yang", (
                    f"Yin organ '{o['organ']}' paired with "
                    f"non-Yang organ '{partner['organ']}' "
                    f"(yin_yang='{partner['yin_yang']}')"
                )
            else:
                assert partner["yin_yang"] == "Yin", (
                    f"Yang organ '{o['organ']}' paired with "
                    f"non-Yin organ '{partner['organ']}' "
                    f"(yin_yang='{partner['yin_yang']}')"
                )

    def test_paired_reciprocity(self, organs, organ_by_name):
        """If A is paired with B, B is paired with A."""
        for o in organs:
            partner = organ_by_name[o["paired"]]
            assert partner["paired"] == o["organ"], (
                f"Organ '{o['organ']}' paired with '{o['paired']}' "
                f"but '{o['paired']}' paired with '{partner['paired']}'"
            )

    def test_paired_organs_share_element(self, organs, organ_by_name):
        """Interior-exterior pairs share the same Wu Xing element."""
        for o in organs:
            partner = organ_by_name[o["paired"]]
            assert o["element"] == partner["element"], (
                f"Organ '{o['organ']}' ({o['element']}) paired with "
                f"'{partner['organ']}' ({partner['element']}): elements differ"
            )

    def test_wing_assignments(self, organs):
        """
        Standard organ clock wing expectations:
        Branch 0 (Zi/GB) = Night (23:00-01:00 civil equivalent)
        Branch 1 (Chou/LR) = Night (01:00-03:00)
        Branch 2 (Yin/LU) = Night (03:00-05:00)
        Branch 3 (Mao/LI) = Night (05:00-07:00 — dawn)
        Branch 4 (Chen/ST) = Day (07:00-09:00)
        Branch 5 (Si/SP) = Day (09:00-11:00)
        Branch 6 (Wu/HT) = Day (11:00-13:00)
        Branch 7 (Wei/SI) = Day (13:00-15:00)
        Branch 8 (Shen/BL) = Day (15:00-17:00)
        Branch 9 (You/KI) = Day (17:00-19:00)
        Branch 10 (Xu/PC) = Night (19:00-21:00 — dusk)
        Branch 11 (Hai/SJ) = Night (21:00-23:00)
        """
        expected_wings = {
            0: "Night", 1: "Night", 2: "Night", 3: "Night",
            4: "Day", 5: "Day", 6: "Day", 7: "Day",
            8: "Day", 9: "Day", 10: "Night", 11: "Night",
        }
        for o in organs:
            expected = expected_wings[o["branch_index"]]
            assert o["wing"] == expected, (
                f"Organ '{o['organ']}' (branch {o['branch_index']}): "
                f"wing='{o['wing']}', expected '{expected}'"
            )

    def test_six_yin_six_yang(self, organs):
        """6 Yin organs and 6 Yang organs."""
        from collections import Counter
        yy = Counter(o["yin_yang"] for o in organs)
        assert yy["Yin"] == 6
        assert yy["Yang"] == 6

    def test_organ_vessel_reverse_lookup(self, organs, vessels):
        """
        If an organ lists a conf_vessel, that vessel's conf_meridian
        and conf_branch must point back to this organ.
        """
        for o in organs:
            if o["conf_vessel"] is not None:
                v = vessels[o["conf_vessel"]]
                assert v["conf_meridian"] == o["abbr"], (
                    f"Organ '{o['organ']}' lists conf_vessel '{o['conf_vessel']}', "
                    f"but that vessel's conf_meridian is '{v['conf_meridian']}' "
                    f"not '{o['abbr']}'"
                )
                assert v["conf_branch"] == o["branch_index"], (
                    f"Organ '{o['organ']}' lists conf_vessel '{o['conf_vessel']}', "
                    f"but that vessel's conf_branch is {v['conf_branch']} "
                    f"not {o['branch_index']}"
                )
            if o["coup_vessel"] is not None:
                v = vessels[o["coup_vessel"]]
                assert v["coup_meridian"] == o["abbr"], (
                    f"Organ '{o['organ']}' lists coup_vessel '{o['coup_vessel']}', "
                    f"but that vessel's coup_meridian is '{v['coup_meridian']}' "
                    f"not '{o['abbr']}'"
                )
                assert v["coup_branch"] == o["branch_index"], (
                    f"Organ '{o['organ']}' lists coup_vessel '{o['coup_vessel']}', "
                    f"but that vessel's coup_branch is {v['coup_branch']} "
                    f"not {o['branch_index']}"
                )


# ====================================================================
# 5. INNER ALCHEMY COVERAGE
# ====================================================================


class TestInnerAlchemyCoverage:
    """Every organ covered by exactly one inner alchemy entry. San Jiao has own entry."""

    def test_every_organ_in_exactly_one_entry(self, inner_alchemy, organ_names):
        """Each organ appears in exactly one inner alchemy entry's organs list."""
        organ_to_entry = {}
        for element, entry in inner_alchemy.items():
            for org in entry["organs"]:
                assert org not in organ_to_entry, (
                    f"Organ '{org}' appears in both '{organ_to_entry[org]}' "
                    f"and '{element}'"
                )
                organ_to_entry[org] = element

        uncovered = organ_names - set(organ_to_entry.keys())
        assert not uncovered, (
            f"Organs not covered by any inner alchemy entry: {uncovered}"
        )

    def test_san_jiao_has_own_entry(self, inner_alchemy):
        """San Jiao has its own inner alchemy entry, separate from Fire."""
        assert "San Jiao" in inner_alchemy, "San Jiao must have its own entry"
        assert "San Jiao" in inner_alchemy["San Jiao"]["organs"]

    def test_pericardium_in_fire_not_san_jiao(self, inner_alchemy):
        """Pericardium is in Fire's entry, not San Jiao's."""
        assert "Pericardium" in inner_alchemy["Fire"]["organs"], (
            "Pericardium should be in Fire entry"
        )
        assert "Pericardium" not in inner_alchemy["San Jiao"]["organs"], (
            "Pericardium should NOT be in San Jiao entry"
        )

    def test_san_jiao_not_in_fire(self, inner_alchemy):
        """San Jiao should NOT appear in Fire's entry."""
        assert "San Jiao" not in inner_alchemy["Fire"]["organs"], (
            "San Jiao should not be in Fire entry"
        )

    def test_five_elements_plus_san_jiao(self, inner_alchemy):
        """Inner alchemy has exactly 6 entries: Wood, Fire, Earth, Metal, Water, San Jiao."""
        expected = {"Wood", "Fire", "Earth", "Metal", "Water", "San Jiao"}
        assert set(inner_alchemy.keys()) == expected


# ====================================================================
# 6. CALENDAR CONSISTENCY
# ====================================================================


class TestCalendarConsistency:
    """Divine months: 13 entries, correct numbering, IAO, Great Rites."""

    def test_thirteen_months(self, divine_months):
        assert len(divine_months) == 13

    def test_month_numbers_1_to_13(self, divine_months):
        numbers = [m["number"] for m in divine_months]
        assert numbers == list(range(1, 14))

    def test_month_13_is_vadusfadahm(self, divine_months):
        month_13 = [m for m in divine_months if m["number"] == 13][0]
        assert month_13["name"] == "VADUSFADAHM"

    def test_alchemical_stages(self, divine_months):
        """
        Nigredo: months 1-4
        Albedo: months 5-8
        Rubedo: months 9-12
        Da'ath: month 13
        """
        expected = {
            1: "Nigredo", 2: "Nigredo", 3: "Nigredo", 4: "Nigredo",
            5: "Albedo", 6: "Albedo", 7: "Albedo", 8: "Albedo",
            9: "Rubedo", 10: "Rubedo", 11: "Rubedo", 12: "Rubedo",
            13: "Da'ath",
        }
        for m in divine_months:
            assert m["alchemical"] == expected[m["number"]], (
                f"Month {m['number']} ({m['name']}): "
                f"alchemical='{m['alchemical']}', expected '{expected[m['number']]}'"
            )

    def test_alchemical_stage_counts(self, divine_months):
        """Exactly 4 Nigredo, 4 Albedo, 4 Rubedo, 1 Da'ath."""
        from collections import Counter
        stages = Counter(m["alchemical"] for m in divine_months)
        assert stages["Nigredo"] == 4
        assert stages["Albedo"] == 4
        assert stages["Rubedo"] == 4
        assert stages["Da'ath"] == 1

    def test_iao_assignments(self, divine_months):
        """I=ISIS(1), O=OSIRIS(7), A=SET(10), rest null."""
        iao_map = {m["name"]: m["iao"] for m in divine_months}
        assert iao_map["ISIS"] == "I"
        assert iao_map["OSIRIS"] == "O"
        assert iao_map["SET"] == "A"
        # All others null
        for m in divine_months:
            if m["name"] not in ("ISIS", "OSIRIS", "SET"):
                assert m["iao"] is None, (
                    f"Month '{m['name']}' should have iao=null, got '{m['iao']}'"
                )

    def test_six_great_rites(self, divine_months):
        """6 Great Rites assigned to correct months."""
        expected_rites = {
            "ISIS": "Autumn Equinox",
            "SADAM": "Day of the Dead",
            "EOROS": "Winter Solstice",
            "OSIRIS": "Spring Equinox",
            "SAMMA": "Divine Marriage",
            "SET": "Summer Solstice",
        }
        rite_map = {m["name"]: m["great_rite"] for m in divine_months}
        for name, rite in expected_rites.items():
            assert rite_map[name] == rite, (
                f"Month '{name}': great_rite='{rite_map[name]}', expected '{rite}'"
            )
        # Months without Great Rites
        for m in divine_months:
            if m["name"] not in expected_rites:
                assert m["great_rite"] is None, (
                    f"Month '{m['name']}' should have no great_rite, "
                    f"got '{m['great_rite']}'"
                )

    def test_no_galafest_month(self, divine_months):
        """GALAFEST was a hallucination — verify it does not appear."""
        names = {m["name"] for m in divine_months}
        assert "GALAFEST" not in names, "GALAFEST is a known hallucination"

    def test_month_names_match_spec(self, divine_months):
        """All 13 canonical month names present."""
        expected = {
            "ISIS", "SADAM", "LIOTHIL", "EOROS", "TASUMER", "MENON",
            "OSIRIS", "AGAFEST", "SAMMA", "SET", "SADAS", "DESURIORIS",
            "VADUSFADAHM",
        }
        actual = {m["name"] for m in divine_months}
        assert actual == expected


# ====================================================================
# 7. SEPHIROTIC DAYS
# ====================================================================


class TestSephiroticDays:
    """9 entries, correct Chaldean skip-3 ordering."""

    def test_nine_entries(self, sephirotic_days):
        assert len(sephirotic_days) == 9

    def test_day_numbers_1_to_9(self, sephirotic_days):
        days = [d["day"] for d in sephirotic_days]
        assert days == list(range(1, 10))

    def test_chaldean_skip_3_ordering(self, sephirotic_days):
        """
        Chaldean skip-3 planetary ordering extended to outer planets:
        Sol, Luna, Mars, Mercury, Jupiter, Venus, Saturn, Uranus, Neptune
        """
        expected_planets = [
            "Sol", "Luna", "Mars", "Mercury", "Jupiter",
            "Venus", "Saturn", "Uranus", "Neptune",
        ]
        actual_planets = [d["planet"] for d in sephirotic_days]
        assert actual_planets == expected_planets, (
            f"Sephirotic day planet ordering:\n"
            f"  Expected: {expected_planets}\n"
            f"  Actual:   {actual_planets}"
        )

    def test_sephiroth_ordering(self, sephirotic_days):
        """Sephiroth follow the Tree from Tiphareth outward."""
        expected = [
            "Tiphareth", "Yesod", "Geburah", "Hod", "Chesed",
            "Netzach", "Binah", "Chokmah", "Kether",
        ]
        actual = [d["sephirah"] for d in sephirotic_days]
        assert actual == expected


# ====================================================================
# 8. SOLAR KEYS CONSISTENCY
# ====================================================================


class TestSolarKeys:
    """Solar keys reference valid laws and trigrams."""

    def test_two_solar_keys(self, registers):
        keys = registers["solar_keys"]
        assert len(keys) == 2
        assert "gold" in keys
        assert "silver" in keys

    def test_gold_key_is_kan_fall_of_events(self, registers, law_names, trigram_names):
        gold = registers["solar_keys"]["gold"]
        assert gold["law"] == "Fall of Events"
        assert gold["trigram"] == "Kǎn"
        assert gold["event"] == "sunrise"
        assert gold["law"] in law_names
        assert gold["trigram"] in trigram_names

    def test_silver_key_is_li_divinity(self, registers, law_names, trigram_names):
        silver = registers["solar_keys"]["silver"]
        assert silver["law"] == "Divinity"
        assert silver["trigram"] == "Lí"
        assert silver["event"] == "sunset"
        assert silver["law"] in law_names
        assert silver["trigram"] in trigram_names

    def test_solar_key_laws_marked_is_solar_key(self, laws, registers):
        """Laws that are solar keys have is_solar_key=true, others false."""
        solar_key_law_names = {
            registers["solar_keys"]["gold"]["law"],
            registers["solar_keys"]["silver"]["law"],
        }
        for lname, l in laws.items():
            if lname in solar_key_law_names:
                assert l["is_solar_key"] is True, (
                    f"Law '{lname}' is a solar key but is_solar_key={l['is_solar_key']}"
                )
            else:
                assert l["is_solar_key"] is False, (
                    f"Law '{lname}' is NOT a solar key but is_solar_key={l['is_solar_key']}"
                )


# ====================================================================
# 9. LAW-TRIGRAM-VESSEL CONSISTENCY
# ====================================================================


class TestLawTrigramVesselChain:
    """The law->trigram->vessel chain is consistent across all three lookups."""

    def test_law_trigram_bidirectional(self, laws, trigrams):
        """If law X names trigram Y, trigram Y names law X."""
        for lname, l in laws.items():
            tname = l["trigram"]
            assert tname in trigrams, (
                f"Law '{lname}' references trigram '{tname}' not in trigrams"
            )
            assert trigrams[tname]["law"] == lname, (
                f"Law '{lname}' references trigram '{tname}', "
                f"but that trigram's law is '{trigrams[tname]['law']}'"
            )

    def test_vessel_law_matches_trigram_chain(self, vessels, laws, trigrams):
        """Vessel's law -> that law's trigram -> that trigram's vessel = this vessel."""
        for vname, v in vessels.items():
            law_name = v["law"]
            law = laws[law_name]
            trigram_name = law["trigram"]
            trigram = trigrams[trigram_name]
            assert trigram["vessel"] == vname, (
                f"Vessel '{vname}' -> law '{law_name}' -> trigram '{trigram_name}' "
                f"-> vessel '{trigram['vessel']}' (expected '{vname}')"
            )

    def test_vessel_prime_matches_law_prime(self, vessels, laws):
        """Each vessel's prime matches the prime of its associated law."""
        for vname, v in vessels.items():
            law = laws[v["law"]]
            assert v["prime"] == law["prime"], (
                f"Vessel '{vname}' prime={v['prime']} but "
                f"law '{v['law']}' prime={law['prime']}"
            )

    def test_lunar_phase_law_matches_trigram_law(self, lunar_phases, trigrams):
        """Each lunar phase's law matches the law of its trigram."""
        for lp in lunar_phases:
            trigram = trigrams[lp["trigram"]]
            assert lp["law"] == trigram["law"], (
                f"Lunar phase '{lp['name']}' law='{lp['law']}' "
                f"but trigram '{lp['trigram']}' law='{trigram['law']}'"
            )

    def test_lunar_phase_prime_matches_law_prime(self, lunar_phases, laws):
        """Each lunar phase's prime matches its law's prime."""
        for lp in lunar_phases:
            law = laws[lp["law"]]
            assert lp["prime"] == law["prime"], (
                f"Lunar phase '{lp['name']}' prime={lp['prime']} "
                f"but law '{lp['law']}' prime={law['prime']}"
            )


# ====================================================================
# 10. DIVINE HOURS
# ====================================================================


class TestDivineHours:
    """8 divine hours, correct wing assignments."""

    def test_eight_hours(self, registers):
        assert len(registers["divine_hours"]) == 8

    def test_hour_indices_1_to_8(self, registers):
        indices = [h["index"] for h in registers["divine_hours"]]
        assert indices == list(range(1, 9))

    def test_four_day_four_night(self, registers):
        from collections import Counter
        wings = Counter(h["wing"] for h in registers["divine_hours"])
        assert wings["Day"] == 4
        assert wings["Night"] == 4

    def test_day_hours_first(self, registers):
        """Hours 1-4 are Day, 5-8 are Night."""
        for h in registers["divine_hours"]:
            if h["index"] <= 4:
                assert h["wing"] == "Day", (
                    f"Hour {h['index']} should be Day, got '{h['wing']}'"
                )
            else:
                assert h["wing"] == "Night", (
                    f"Hour {h['index']} should be Night, got '{h['wing']}'"
                )


# ====================================================================
# 11. FIELD UNIFORMITY — Every entry in a dimension has the same fields
# ====================================================================


class TestFieldUniformity:
    """All entries within each register dimension share identical field sets."""

    def test_laws_uniform_fields(self, laws):
        field_sets = [frozenset(v.keys()) for v in laws.values()]
        assert len(set(field_sets)) == 1, (
            f"Law field sets are not uniform: "
            f"{[(k, set(v.keys())) for k, v in laws.items()]}"
        )

    def test_trigrams_uniform_fields(self, trigrams):
        field_sets = [frozenset(v.keys()) for v in trigrams.values()]
        assert len(set(field_sets)) == 1, (
            f"Trigram field sets are not uniform: "
            f"{[(k, set(v.keys())) for k, v in trigrams.items()]}"
        )

    def test_vessels_uniform_fields(self, vessels):
        field_sets = [frozenset(v.keys()) for v in vessels.values()]
        assert len(set(field_sets)) == 1, (
            f"Vessel field sets are not uniform: "
            f"{[(k, set(v.keys())) for k, v in vessels.items()]}"
        )

    def test_organs_uniform_fields(self, organs):
        field_sets = [frozenset(o.keys()) for o in organs]
        assert len(set(field_sets)) == 1, (
            f"Organ field sets are not uniform: "
            f"{[(o['organ'], set(o.keys())) for o in organs]}"
        )

    def test_inner_alchemy_uniform_fields(self, inner_alchemy):
        field_sets = [frozenset(v.keys()) for v in inner_alchemy.values()]
        assert len(set(field_sets)) == 1, (
            f"Inner alchemy field sets are not uniform: "
            f"{[(k, set(v.keys())) for k, v in inner_alchemy.items()]}"
        )

    def test_lunar_phases_uniform_fields(self, lunar_phases):
        field_sets = [frozenset(lp.keys()) for lp in lunar_phases]
        assert len(set(field_sets)) == 1, (
            f"Lunar phase field sets are not uniform"
        )

    def test_divine_hours_uniform_fields(self, registers):
        field_sets = [frozenset(h.keys()) for h in registers["divine_hours"]]
        assert len(set(field_sets)) == 1, (
            f"Divine hour field sets are not uniform"
        )

    def test_divine_months_uniform_fields(self, divine_months):
        field_sets = [frozenset(m.keys()) for m in divine_months]
        assert len(set(field_sets)) == 1, (
            f"Divine month field sets are not uniform"
        )

    def test_sephirotic_days_uniform_fields(self, sephirotic_days):
        field_sets = [frozenset(d.keys()) for d in sephirotic_days]
        assert len(set(field_sets)) == 1, (
            f"Sephirotic day field sets are not uniform"
        )


# ====================================================================
# 12. PRIMALITY VERIFICATION — All "prime" fields are actually prime
# ====================================================================


def _is_prime(n):
    """Deterministic primality test for small numbers."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


class TestPrimality:
    """Every field named 'prime' must contain an actual prime number."""

    def test_law_primes(self, laws):
        for lname, l in laws.items():
            assert _is_prime(l["prime"]), (
                f"Law '{lname}' prime={l['prime']} is NOT prime"
            )

    def test_vessel_primes(self, vessels):
        for vname, v in vessels.items():
            assert _is_prime(v["prime"]), (
                f"Vessel '{vname}' prime={v['prime']} is NOT prime"
            )

    def test_lunar_phase_primes(self, lunar_phases):
        for lp in lunar_phases:
            assert _is_prime(lp["prime"]), (
                f"Lunar phase '{lp['name']}' prime={lp['prime']} is NOT prime"
            )

    def test_solar_key_primes(self, registers):
        for key, sk in registers["solar_keys"].items():
            assert _is_prime(sk["prime"]), (
                f"Solar key '{key}' prime={sk['prime']} is NOT prime"
            )

    def test_all_eight_distinct_primes(self, laws):
        """The 8 Law primes are all distinct — no duplicates."""
        primes = [l["prime"] for l in laws.values()]
        assert len(primes) == len(set(primes)), (
            f"Duplicate primes in laws: {primes}"
        )


# ====================================================================
# 13. VALUE DOMAIN CONSTRAINTS
# ====================================================================


class TestValueDomains:
    """Enum-like fields contain only their allowed values."""

    WU_XING = {"Wood", "Fire", "Earth", "Metal", "Water"}

    def test_organ_yin_yang_values(self, organs):
        for o in organs:
            assert o["yin_yang"] in ("Yin", "Yang"), (
                f"Organ '{o['organ']}' yin_yang='{o['yin_yang']}' "
                f"not in (Yin, Yang)"
            )

    def test_vessel_polarity_values(self, vessels):
        for vname, v in vessels.items():
            assert v["polarity"] in ("Yin", "Yang"), (
                f"Vessel '{vname}' polarity='{v['polarity']}' "
                f"not in (Yin, Yang)"
            )

    def test_organ_element_wu_xing(self, organs):
        for o in organs:
            assert o["element"] in self.WU_XING, (
                f"Organ '{o['organ']}' element='{o['element']}' "
                f"not in Wu Xing: {self.WU_XING}"
            )

    def test_organ_wing_values(self, organs):
        for o in organs:
            assert o["wing"] in ("Day", "Night"), (
                f"Organ '{o['organ']}' wing='{o['wing']}' not in (Day, Night)"
            )

    def test_divine_hour_wing_values(self, registers):
        for h in registers["divine_hours"]:
            assert h["wing"] in ("Day", "Night"), (
                f"Hour {h['index']} wing='{h['wing']}' not in (Day, Night)"
            )

    def test_trigram_wu_xing_values(self, trigrams):
        for tname, t in trigrams.items():
            assert t["wu_xing"] in self.WU_XING, (
                f"Trigram '{tname}' wu_xing='{t['wu_xing']}' "
                f"not in Wu Xing: {self.WU_XING}"
            )

    def test_divine_month_alchemical_values(self, divine_months):
        valid = {"Nigredo", "Albedo", "Rubedo", "Da'ath"}
        for m in divine_months:
            assert m["alchemical"] in valid, (
                f"Month '{m['name']}' alchemical='{m['alchemical']}' "
                f"not in {valid}"
            )

    def test_lunar_phase_waxing_is_boolean(self, lunar_phases):
        for lp in lunar_phases:
            assert isinstance(lp["waxing"], bool), (
                f"Lunar phase '{lp['name']}' waxing={lp['waxing']} "
                f"is not boolean"
            )

    def test_law_is_solar_key_is_boolean(self, laws):
        for lname, l in laws.items():
            assert isinstance(l["is_solar_key"], bool), (
                f"Law '{lname}' is_solar_key={l['is_solar_key']} "
                f"is not boolean"
            )

    def test_vessel_yin_day_restricted_is_boolean(self, vessels):
        for vname, v in vessels.items():
            assert isinstance(v["yin_day_restricted"], bool), (
                f"Vessel '{vname}' yin_day_restricted={v['yin_day_restricted']} "
                f"is not boolean"
            )

    def test_no_empty_strings_in_registers(self, registers):
        """No field in registers.json should contain an empty string."""
        for dim_name, dim_data in registers.items():
            if dim_name in ("meta", "vessel_remainder_map"):
                continue
            if isinstance(dim_data, dict):
                for entry_name, entry in dim_data.items():
                    if isinstance(entry, dict):
                        for field, value in entry.items():
                            assert value != "", (
                                f"{dim_name}.{entry_name}.{field} "
                                f"is an empty string (should be null or populated)"
                            )
            elif isinstance(dim_data, list):
                for entry in dim_data:
                    ident = (
                        entry.get("organ")
                        or entry.get("name")
                        or str(entry.get("number", ""))
                        or str(entry.get("day", ""))
                    )
                    for field, value in entry.items():
                        assert value != "", (
                            f"{dim_name}[{ident}].{field} "
                            f"is an empty string (should be null or populated)"
                        )


# ====================================================================
# 14. NULL VALUE INVENTORY — Intentional nulls documented
# ====================================================================


class TestNullInventory:
    """
    Document and verify all null values in registers.json.
    Every null must be intentional and accounted for here.
    """

    # ── Intentional nulls with justifications ──
    # laws.Time_Matrix: vowel and mudra are null — documented gap,
    #   sources do not specify these for Time Matrix.
    # organs: 4 organs (Liver, Lg Intestine, Stomach, Heart) have
    #   null conf_vessel and coup_vessel — these organs do not host
    #   any EV confluent or coupled points.
    # inner_alchemy.San_Jiao: color, spirit, season, sense_organ, body_tissue
    #   are null — San Jiao is unique; it has no standard Wu Xing
    #   correspondence for these properties.
    # divine_hours 5-8: protocols are null — Hours V-VIII have no
    #   source-documented protocol assignments.
    # divine_months: element is null for 8 months (only 5 have
    #   Damanhurian element); great_rite is null for 7 months (only
    #   6 have Great Rites); iao is null for 10 months (only 3 carry
    #   IAO letters).

    EXPECTED_NULLS_LAWS = {
        "Time Matrix": {"vowel", "mudra"},
    }

    ORGANS_WITH_NULL_VESSELS = {"Liver", "Lg Intestine", "Stomach", "Heart"}

    SAN_JIAO_NULL_FIELDS = {"color", "spirit", "season", "sense_organ", "body_tissue"}

    def test_law_nulls_only_time_matrix(self, laws):
        """Only Time Matrix has null fields; all others are fully populated."""
        for lname, l in laws.items():
            null_fields = {k for k, v in l.items() if v is None}
            if lname in self.EXPECTED_NULLS_LAWS:
                assert null_fields == self.EXPECTED_NULLS_LAWS[lname], (
                    f"Law '{lname}' unexpected nulls: "
                    f"expected {self.EXPECTED_NULLS_LAWS[lname]}, got {null_fields}"
                )
            else:
                assert not null_fields, (
                    f"Law '{lname}' has unexpected null fields: {null_fields}"
                )

    def test_organ_null_vessels_are_expected(self, organs):
        """Only 4 specific organs have null vessel references."""
        for o in organs:
            has_null_conf = o["conf_vessel"] is None
            has_null_coup = o["coup_vessel"] is None
            if o["organ"] in self.ORGANS_WITH_NULL_VESSELS:
                assert has_null_conf and has_null_coup, (
                    f"Organ '{o['organ']}' expected null vessels but has "
                    f"conf={o['conf_vessel']}, coup={o['coup_vessel']}"
                )
            else:
                assert not has_null_conf and not has_null_coup, (
                    f"Organ '{o['organ']}' has unexpected null vessel: "
                    f"conf={o['conf_vessel']}, coup={o['coup_vessel']}"
                )

    def test_organs_no_other_nulls(self, organs):
        """No organ has null in any field except conf_vessel/coup_vessel."""
        for o in organs:
            for field, value in o.items():
                if field in ("conf_vessel", "coup_vessel"):
                    continue
                assert value is not None, (
                    f"Organ '{o['organ']}' has unexpected null in field '{field}'"
                )

    def test_san_jiao_nulls_expected(self, inner_alchemy):
        """San Jiao's known null fields are exactly as expected."""
        sj = inner_alchemy["San Jiao"]
        null_fields = {k for k, v in sj.items() if v is None}
        assert null_fields == self.SAN_JIAO_NULL_FIELDS, (
            f"San Jiao unexpected null pattern: "
            f"expected {self.SAN_JIAO_NULL_FIELDS}, got {null_fields}"
        )

    def test_non_san_jiao_no_nulls(self, inner_alchemy):
        """All inner alchemy entries except San Jiao are fully populated."""
        for element, entry in inner_alchemy.items():
            if element == "San Jiao":
                continue
            null_fields = {k for k, v in entry.items() if v is None}
            assert not null_fields, (
                f"Inner alchemy '{element}' has unexpected null fields: {null_fields}"
            )

    def test_divine_hour_protocol_nulls(self, registers):
        """Hours V-VIII (night) have null protocols; I-IV have protocols."""
        for h in registers["divine_hours"]:
            if h["index"] <= 4:
                assert h["protocols"] is not None, (
                    f"Hour {h['index']} (Day) should have protocols, got null"
                )
            else:
                assert h["protocols"] is None, (
                    f"Hour {h['index']} (Night) should have null protocols "
                    f"(documented gap)"
                )

    def test_divine_month_element_null_pattern(self, divine_months):
        """Only ISIS, SADAM, EOROS, OSIRIS, SET have Damanhurian elements."""
        months_with_element = {"ISIS", "SADAM", "EOROS", "OSIRIS", "SET"}
        for m in divine_months:
            if m["name"] in months_with_element:
                assert m["element"] is not None, (
                    f"Month '{m['name']}' should have element, got null"
                )
            else:
                assert m["element"] is None, (
                    f"Month '{m['name']}' should have null element, "
                    f"got '{m['element']}'"
                )


# ====================================================================
# 15. RESONANCE LOOKUP TABLE COMPLETENESS
# ====================================================================


class TestResonanceLookupTables:
    """Every lookup table in resonances.json is used, valid, and complete."""

    def test_meta_registry_types_exist_in_resonances(self, resonances):
        """Every resonance type referenced by meta_registry exists in resonances.json."""
        from src.meta_registry import RESONANCE_PARTICIPATION

        res_types = set(resonances["resonance_types"].keys())
        ref_types = set()
        for types_list in RESONANCE_PARTICIPATION.values():
            ref_types.update(types_list)

        missing = ref_types - res_types
        assert not missing, (
            f"Resonance types in meta_registry but not in resonances.json: {missing}"
        )

    @staticmethod
    def _extract_lookup_table_refs():
        """Extract all lookup table references from resonance.py.

        Catches both lookups["name"] and lookups.get("name", ...) patterns.
        """
        code_path = Path(__file__).parent.parent / "src" / "resonance.py"
        code = code_path.read_text(encoding="utf-8")
        bracket_refs = set(re.findall(r'lookups\["([^"]+)"\]', code))
        get_refs = set(re.findall(r'lookups\.get\("([^"]+)"', code))
        return bracket_refs | get_refs

    def test_no_orphan_lookup_tables(self, resonances):
        """Every lookup table in resonances.json is referenced by resonance.py."""
        used_tables = self._extract_lookup_table_refs()
        json_tables = set(resonances["lookup_tables"].keys())

        orphans = json_tables - used_tables
        assert not orphans, (
            f"Lookup tables in resonances.json not used by resonance.py: {orphans}"
        )

    def test_resonance_py_tables_exist_in_json(self, resonances):
        """Every lookup table referenced in resonance.py exists in resonances.json."""
        used_tables = self._extract_lookup_table_refs()
        json_tables = set(resonances["lookup_tables"].keys())

        missing = used_tables - json_tables
        assert not missing, (
            f"Lookup tables referenced in resonance.py but not in resonances.json: "
            f"{missing}"
        )

    def test_emotion_perception_map_keys_valid(self, resonances, laws, inner_alchemy):
        """emotion_perception_map keys reference real laws and elements."""
        ep_map = resonances["lookup_tables"]["emotion_perception_map"]
        law_names = set(laws.keys())
        # Elements that appear in inner alchemy (excluding San Jiao special key)
        alchemy_elements = set(inner_alchemy.keys()) - {"San Jiao"}
        # Also include San Jiao as it could be a valid element key
        all_alchemy_keys = set(inner_alchemy.keys())

        for key in ep_map:
            if key.startswith("_"):
                continue
            parts = key.split(":")
            assert len(parts) == 3, f"Malformed emotion_perception key: {key}"
            law, element, polarity = parts
            assert law in law_names, (
                f"emotion_perception_map law '{law}' not in laws"
            )
            assert element in all_alchemy_keys, (
                f"emotion_perception_map element '{element}' not in inner alchemy"
            )
            assert polarity in ("pos", "neg"), (
                f"emotion_perception_map polarity '{polarity}' not in (pos, neg)"
            )

    def test_adonaj_ba_map_keys_valid(self, resonances, laws, organs):
        """adonaj_ba_organ_map keys reference real Adonaj-Ba values and organ names."""
        abd_map = resonances["lookup_tables"]["adonaj_ba_organ_map"]
        adonaj_ba_values = {l["adonaj_ba"] for l in laws.values()}
        organ_names = {o["organ"] for o in organs}

        for key in abd_map:
            if key.startswith("_"):
                continue
            parts = key.split(":")
            assert len(parts) == 2, f"Malformed adonaj_ba key: {key}"
            adb, organ = parts
            assert adb in adonaj_ba_values, (
                f"adonaj_ba_organ_map center '{adb}' not in law Adonaj-Ba values"
            )
            assert organ in organ_names, (
                f"adonaj_ba_organ_map organ '{organ}' not in organ names"
            )

    def test_quest_planet_map_keys_valid(self, resonances, laws):
        """quest_planet_map keys reference real Quest Tarot card names from laws."""
        qp_map = resonances["lookup_tables"]["quest_planet_map"]
        quest_tarot_values = {l["quest_tarot"] for l in laws.values()}

        for key in qp_map:
            if key.startswith("_"):
                continue
            assert key in quest_tarot_values, (
                f"quest_planet_map key '{key}' not in law quest_tarot values"
            )

    def test_plum_blossom_map_covers_all_trigrams(self, resonances, trigrams):
        """Every plum_blossom value in trigrams has a mapping in plum_blossom_wu_xing_map."""
        pb_map = resonances["lookup_tables"]["plum_blossom_wu_xing_map"]
        for tname, t in trigrams.items():
            pb = t["plum_blossom"]
            assert pb in pb_map, (
                f"Trigram '{tname}' plum_blossom='{pb}' has no entry "
                f"in plum_blossom_wu_xing_map"
            )

    def test_season_great_rite_map_keys_valid(self, resonances, inner_alchemy, divine_months):
        """Season-Great Rite map keys reference real inner alchemy seasons and month great rites."""
        sgr_map = resonances["lookup_tables"]["season_great_rite_map"]
        alchemy_seasons = {c["season"] for c in inner_alchemy.values() if c["season"] is not None}
        great_rites = {m["great_rite"] for m in divine_months if m["great_rite"] is not None}

        for key in sgr_map:
            if key.startswith("_"):
                continue
            parts = key.split(":")
            assert len(parts) == 2, f"Malformed season_great_rite key: {key}"
            season, rite = parts
            assert season in alchemy_seasons, (
                f"season_great_rite_map season '{season}' not in inner alchemy seasons"
            )
            assert rite in great_rites, (
                f"season_great_rite_map rite '{rite}' not in divine month great rites"
            )


# ====================================================================
# 16. META-REGISTRY COVERAGE INTEGRATION
# ====================================================================


class TestMetaRegistryCoverage:
    """The meta-registry check_coverage() function reports zero issues."""

    def test_full_coverage(self):
        """Level 1 + Level 2 coverage check must report zero issues."""
        from src.meta_registry import check_coverage

        report = check_coverage()

        L1 = report["level_1"]
        assert L1["uncatalogued_count"] == 0, (
            f"Uncatalogued register fields: {L1['uncatalogued_fields']}"
        )

        L2 = report["level_2"]
        assert L2["missing_count"] == 0, (
            f"Resonance fields without participation entries: "
            f"{L2['missing_participation']}"
        )
        assert L2["invalid_count"] == 0, (
            f"Invalid resonance type references: {L2['invalid_types']}"
        )
        assert L2["orphan_count"] == 0, (
            f"Orphan participation entries: {L2['orphan_participation']}"
        )
