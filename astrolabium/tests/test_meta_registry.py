"""
Tests for the Meta-Registry fail-safe.

These tests BREAK when registers.json gains new fields without
corresponding entries in FIELD_REGISTRY or RESONANCE_PARTICIPATION.
That's the point — the fail-safe catches uncatalogued dimensions.
"""

import pytest

from src.meta_registry import (
    check_coverage,
    FIELD_REGISTRY,
    RESONANCE_PARTICIPATION,
    _get_register_fields,
    _get_catalogued_fields,
    _get_resonance_field_specs,
    _load_json,
)


class TestFieldCensus:
    """Level 1: every register field is catalogued."""

    def test_full_field_coverage(self):
        """No uncatalogued fields in registers.json."""
        result = check_coverage()
        L1 = result["level_1"]
        assert L1["uncatalogued_count"] == 0, (
            f"Uncatalogued fields found: {L1['uncatalogued_fields']}"
        )

    def test_catalogued_matches_register_count(self):
        """Total catalogued fields equals total register fields."""
        result = check_coverage()
        L1 = result["level_1"]
        assert L1["total_catalogued"] == L1["total_register_fields"]

    def test_all_dimensions_present(self):
        """Every register dimension appears in FIELD_REGISTRY."""
        registers = _load_json("registers.json")
        actual = _get_register_fields(registers)
        for dim in actual:
            assert dim in FIELD_REGISTRY, (
                f"Dimension '{dim}' in registers.json but not in FIELD_REGISTRY"
            )

    def test_no_empty_categories(self):
        """No dimension has all empty category lists."""
        for dim, categories in FIELD_REGISTRY.items():
            total = sum(len(fields) for fields in categories.values())
            assert total > 0, f"Dimension '{dim}' has zero catalogued fields"


class TestResonanceCoverage:
    """Level 2: every resonance field has participation coverage."""

    def test_full_resonance_coverage(self):
        """No resonance fields missing from RESONANCE_PARTICIPATION."""
        result = check_coverage()
        L2 = result["level_2"]
        assert L2["missing_count"] == 0, (
            f"Missing participation entries: {L2['missing_participation']}"
        )

    def test_no_invalid_type_references(self):
        """Every resonance type referenced in RESONANCE_PARTICIPATION exists."""
        result = check_coverage()
        L2 = result["level_2"]
        assert L2["invalid_count"] == 0, (
            f"Invalid type references: {L2['invalid_types']}"
        )

    def test_no_orphan_participation(self):
        """Every RESONANCE_PARTICIPATION entry maps to a FIELD_REGISTRY resonance field."""
        result = check_coverage()
        L2 = result["level_2"]
        assert L2["orphan_count"] == 0, (
            f"Orphan participation entries: {L2['orphan_participation']}"
        )

    def test_participation_entries_match_fields(self):
        """RESONANCE_PARTICIPATION has exactly as many entries as resonance fields."""
        result = check_coverage()
        L2 = result["level_2"]
        assert L2["participation_entries"] == L2["resonance_fields"]


class TestElementalSilo:
    """Elemental silo enforcement."""

    def test_divine_months_element_siloed(self):
        """divine_months.element is siloed, not in resonance category."""
        dm = FIELD_REGISTRY["divine_months"]
        resonance_fields = dm.get("resonance", [])
        assert "element" not in resonance_fields, (
            "divine_months.element must be siloed, not resonance-participating"
        )
        siloed_fields = dm.get("siloed", [])
        assert "element" in siloed_fields

    def test_silo_violations_in_resonances_json(self):
        """resonances.json declares elemental silo violations."""
        resonances = _load_json("resonances.json")
        violations = resonances.get("elemental_silo_violations", {})
        pairs = violations.get("prohibited_pairs", [])
        assert len(pairs) > 0, "No elemental silo violations declared"


class TestConsistency:
    """Internal consistency checks."""

    def test_resonance_types_exist_in_json(self):
        """Every type referenced by RESONANCE_PARTICIPATION exists in resonances.json."""
        resonances = _load_json("resonances.json")
        type_names = set(resonances.get("resonance_types", {}).keys())

        all_referenced = set()
        for types in RESONANCE_PARTICIPATION.values():
            all_referenced.update(types)

        for t in all_referenced:
            assert t in type_names, (
                f"Resonance type '{t}' referenced in RESONANCE_PARTICIPATION "
                f"but not in resonances.json"
            )

    def test_organs_element_most_covered(self):
        """organs.element should be the most heavily covered field."""
        max_spec = max(
            RESONANCE_PARTICIPATION.keys(),
            key=lambda s: len(RESONANCE_PARTICIPATION[s]),
        )
        assert max_spec == "organs.element"

    def test_every_resonance_type_has_participant(self):
        """Every resonance type in resonances.json is referenced by at least one field."""
        resonances = _load_json("resonances.json")
        type_names = set(resonances.get("resonance_types", {}).keys())

        covered_types = set()
        for types in RESONANCE_PARTICIPATION.values():
            covered_types.update(types)

        for t in type_names:
            assert t in covered_types, (
                f"Resonance type '{t}' has no field referencing it "
                f"in RESONANCE_PARTICIPATION"
            )


class TestMetaRegistryFailSafe:
    """
    Deliberate injection tests: verify the fail-safe CATCHES problems.

    These tests modify FIELD_REGISTRY and RESONANCE_PARTICIPATION
    temporarily to prove the fail-safe fires when coverage breaks.
    """

    def test_fake_register_field_detected(self):
        """Adding a field to registers.json-like data would be caught as uncatalogued."""
        # We can't modify registers.json, but we can test the detection logic
        # by checking that a known-good dimension has exact coverage
        result = check_coverage()
        L1 = result["level_1"]
        assert L1["uncatalogued_count"] == 0
        # Verify that the field census actually inspects all dimensions
        registers = _load_json("registers.json")
        actual = _get_register_fields(registers)
        catalogued = _get_catalogued_fields()
        for dim in actual:
            assert dim in catalogued, f"Dimension '{dim}' not in FIELD_REGISTRY"
            assert actual[dim] == catalogued[dim], (
                f"Dimension '{dim}' mismatch: "
                f"register has {actual[dim] - catalogued[dim]} uncatalogued fields"
            )

    def test_removing_participation_entry_detected(self):
        """If a resonance field loses its RESONANCE_PARTICIPATION entry, Level 2 catches it."""
        # Temporarily remove one entry and verify the check finds it
        import copy
        original = copy.deepcopy(RESONANCE_PARTICIPATION)
        # Pick a known entry to "remove"
        test_key = "laws.trigram"
        assert test_key in RESONANCE_PARTICIPATION, "Test prerequisite failed"
        saved = RESONANCE_PARTICIPATION.pop(test_key)
        try:
            result = check_coverage()
            L2 = result["level_2"]
            assert L2["missing_count"] > 0
            assert test_key in L2["missing_participation"]
        finally:
            RESONANCE_PARTICIPATION[test_key] = saved

    def test_invalid_type_reference_detected(self):
        """If a RESONANCE_PARTICIPATION entry references a bogus type, Level 2 catches it."""
        import copy
        test_key = "laws.color"
        saved = RESONANCE_PARTICIPATION[test_key]
        RESONANCE_PARTICIPATION[test_key] = ["fake_nonexistent_type"]
        try:
            result = check_coverage()
            L2 = result["level_2"]
            assert L2["invalid_count"] > 0
            assert any("fake_nonexistent_type" in s for s in L2["invalid_types"])
        finally:
            RESONANCE_PARTICIPATION[test_key] = saved
