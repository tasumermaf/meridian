"""
Tests for the presentation layer.

Verifies that raw computational state is transformed into
Damanhurian-first, practitioner-readable output with correct
vocabulary, no Chinese characters, and proper English vessel names.
"""

import pytest
from datetime import datetime
import pytz

from src.astrolabium import calculate_complete_state
from src.presentation import (
    present_state,
    VESSEL_ENGLISH,
    TRIGRAM_NATURE,
    KEY_VESSEL,
    MERIDIAN_NAMES,
    POINT_DESCRIPTIONS,
    COMPOUND_DISPLAY,
    RESONANCE_DISPLAY,
    _present_point,
    _present_vessel,
    _present_soul,
    _present_keys,
    _present_body,
    _present_compounds,
    _present_resonances,
)


# ── Fixtures ──────────────────────────────────────────────────────

LA_LAT, LA_LON, LA_TZ = 34.0522, -118.2437, "America/Los_Angeles"


def _get_state(year=2026, month=3, day=19, hour=10, minute=30):
    """Helper to produce a raw state for testing."""
    tz = pytz.timezone(LA_TZ)
    dt = tz.localize(datetime(year, month, day, hour, minute))
    return calculate_complete_state(dt, LA_LAT, LA_LON, LA_TZ)


def _get_display(year=2026, month=3, day=19, hour=10, minute=30):
    """Helper to produce a display state for testing."""
    return present_state(_get_state(year, month, day, hour, minute))


# ── Vocabulary Completeness ───────────────────────────────────────


class TestVocabularyCompleteness:
    """All vessels, trigrams, and meridians have English mappings."""

    def test_all_eight_vessels_mapped(self):
        expected = {
            "Du Mai", "Ren Mai", "Chong Mai", "Dai Mai",
            "Yang Qiao Mai", "Yin Qiao Mai", "Yang Wei Mai", "Yin Wei Mai",
        }
        assert set(VESSEL_ENGLISH.keys()) == expected

    def test_all_eight_trigrams_mapped(self):
        expected = {"Qián", "Kūn", "Zhèn", "Xùn", "Kǎn", "Lí", "Gèn", "Duì"}
        assert set(TRIGRAM_NATURE.keys()) == expected

    def test_all_twelve_meridians_mapped(self):
        expected = {"LU", "LI", "ST", "SP", "HT", "SI", "BL", "KI", "PC", "SJ", "GB", "LR"}
        assert set(MERIDIAN_NAMES.keys()) == expected

    def test_all_eight_points_described(self):
        expected = {"SI-3", "BL-62", "LU-7", "KI-6", "SP-4", "PC-6", "GB-41", "SJ-5"}
        assert set(POINT_DESCRIPTIONS.keys()) == expected

    def test_both_solar_keys_have_vessel(self):
        assert "gold" in KEY_VESSEL
        assert "silver" in KEY_VESSEL
        assert KEY_VESSEL["gold"]["vessel"] == "Yin Heel Vessel"
        assert KEY_VESSEL["silver"]["vessel"] == "Yang Heel Vessel"

    def test_all_16_compounds_have_display(self):
        from src.frequency import COMPOUND_TYPES
        for ct in COMPOUND_TYPES:
            assert ct in COMPOUND_DISPLAY, f"Missing display for compound: {ct}"

    def test_all_resonances_have_display(self):
        from src.resonance import ALL_RESONANCE_TYPES
        for rt in ALL_RESONANCE_TYPES:
            assert rt in RESONANCE_DISPLAY, f"Missing display for resonance: {rt}"


# ── Layer Renaming ────────────────────────────────────────────────


class TestLayerRenaming:
    """Raw layer names are replaced with Damanhurian vocabulary."""

    def test_top_level_keys(self):
        display = _get_display()
        assert "soul" in display
        assert "astral" in display
        assert "keys" in display
        assert "body" in display
        assert "hour" in display
        assert "calendar" in display
        assert "compounds" in display
        assert "resonances" in display
        # Raw names should NOT appear
        assert "primeval" not in display
        assert "derivative" not in display
        assert "organ_clock" not in display
        assert "solar_key" not in display
        assert "stem_branch" not in display


# ── No Chinese Characters ────────────────────────────────────────


class TestNoChinese:
    """Display output contains no Chinese characters or pinyin branch names."""

    def _all_strings(self, obj, path=""):
        """Recursively yield all string values in a nested dict/list."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from self._all_strings(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from self._all_strings(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            yield (path, obj)

    def test_no_chinese_characters(self):
        display = _get_display()
        for path, value in self._all_strings(display):
            for char in value:
                # CJK Unified Ideographs range
                assert not (0x4E00 <= ord(char) <= 0x9FFF), (
                    f"Chinese character found at {path}: {char!r} in {value!r}"
                )

    def test_no_pinyin_branch_names(self):
        """Branch names like Zǐ, Chǒu, Yín should not appear."""
        display = _get_display()
        pinyin_branches = {"Zǐ", "Chǒu", "Yín", "Mǎo", "Chén", "Sì",
                          "Wǔ", "Wèi", "Shēn", "Yǒu", "Xū", "Hài"}
        for path, value in self._all_strings(display):
            assert value not in pinyin_branches, (
                f"Pinyin branch name found at {path}: {value!r}"
            )

    def test_no_pinyin_trigram_names(self):
        """Pinyin trigram names should not appear; only symbols and nature names."""
        display = _get_display()
        pinyin_trigrams = {"Qián", "Kūn", "Zhèn", "Xùn", "Kǎn", "Lí", "Gèn", "Duì"}
        for path, value in self._all_strings(display):
            # Allow these in lookup keys but not in display values
            if "trigram_nature" not in path and "trigram" in path:
                # Trigram fields should contain symbols (☰) not pinyin
                if value in pinyin_trigrams:
                    pytest.fail(f"Pinyin trigram name in display at {path}: {value!r}")


# ── Vessel Presentation ──────────────────────────────────────────


class TestVesselPresentation:
    """Astral body layer uses English vessel names and descriptive sentences."""

    def test_vessel_english_name(self):
        display = _get_display()
        vessel = display["astral"]["vessel"]
        assert vessel in VESSEL_ENGLISH.values(), f"Vessel name not English: {vessel!r}"

    def test_vessel_description_sentence(self):
        display = _get_display()
        desc = display["astral"]["description"]
        assert "is open, carrying" in desc

    def test_vessel_law_present(self):
        display = _get_display()
        assert display["astral"]["law"] is not None

    def test_confluent_has_code_and_description(self):
        display = _get_display()
        conf = display["astral"]["confluent"]
        assert "code" in conf
        assert "-" in conf["code"]  # Medical designation format (e.g., LU-7)
        assert "meridian" in conf
        assert "description" in conf

    def test_coupled_has_code_and_description(self):
        display = _get_display()
        coup = display["astral"]["coupled"]
        assert "code" in coup
        assert "-" in coup["code"]
        assert "meridian" in coup

    def test_pair_partner_is_english(self):
        display = _get_display()
        partner = display["astral"]["pair_partner"]
        assert partner in VESSEL_ENGLISH.values(), f"Pair partner not English: {partner!r}"

    def test_trigram_is_symbol_not_pinyin(self):
        display = _get_display()
        trigram = display["astral"]["trigram"]
        # Should be a symbol like ☰, not a pinyin name
        assert len(trigram) == 1 and ord(trigram) > 0x2600

    def test_trigram_nature_is_english(self):
        display = _get_display()
        nature = display["astral"]["trigram_nature"]
        assert nature in TRIGRAM_NATURE.values()


# ── Soul Presentation ─────────────────────────────────────────────


class TestSoulPresentation:
    """Soul body layer uses trigram symbols and includes practice context."""

    def test_law_present(self):
        display = _get_display()
        assert display["soul"]["law"] is not None

    def test_phase_present(self):
        display = _get_display()
        assert display["soul"]["phase"] is not None

    def test_trigram_is_symbol(self):
        display = _get_display()
        trigram = display["soul"]["trigram"]
        assert len(trigram) == 1 and ord(trigram) > 0x2600

    def test_practice_context_present(self):
        display = _get_display()
        soul = display["soul"]
        assert "vowel" in soul
        assert "mudra" in soul
        assert "adonaj_ba" in soul
        assert "perception" in soul
        assert "positive" in soul["perception"]
        assert "negative" in soul["perception"]


# ── Solar Key Presentation ────────────────────────────────────────


class TestKeyPresentation:
    """Solar Keys include vessel name and descriptive sentence when active."""

    def test_inactive_key(self):
        # Mid-day, keys should be inactive
        display = _get_display(hour=12)
        assert display["keys"]["active"] is False

    def test_active_gold_key(self):
        # Near sunrise
        display = _get_display(hour=7, minute=2)
        keys = display["keys"]
        if keys["active"]:
            assert keys["key"] == "Gold"
            assert keys["vessel"] == "Yin Heel Vessel"
            assert "Fall of Events" in keys["description"]
            assert "Yin Heel Vessel" in keys["description"]

    def test_active_silver_key(self):
        # Near sunset (March in LA ~ 7:10 PM)
        display = _get_display(hour=19, minute=10)
        keys = display["keys"]
        if keys["active"]:
            assert keys["key"] == "Silver"
            assert keys["vessel"] == "Yang Heel Vessel"
            assert "Divinity" in keys["description"]


# ── Body Presentation ─────────────────────────────────────────────


class TestBodyPresentation:
    """Organ Clock layer uses plain English with inner alchemy practice sounds."""

    def test_organ_present(self):
        display = _get_display()
        assert display["body"]["organ"] is not None

    def test_healing_sound_present(self):
        display = _get_display()
        sound = display["body"]["inner_alchemy"]["healing_sound"]
        assert sound is not None
        # Should be uppercase phonetic instruction
        assert sound == sound.upper()

    def test_emotions_present(self):
        display = _get_display()
        alchemy = display["body"]["inner_alchemy"]
        assert alchemy["emotion_positive"] is not None
        assert alchemy["emotion_negative"] is not None

    def test_element_is_english(self):
        display = _get_display()
        element = display["body"]["element"]
        assert element in ("Wood", "Fire", "Earth", "Metal", "Water")

    def test_practice_section_present(self):
        """Top-level practice section exists with expected structure."""
        display = _get_display()
        assert "practice" in display
        practice = display["practice"]
        assert "soul" in practice
        assert "astral" in practice
        assert "body" in practice
        # Soul practice fields
        assert "quest" in practice["soul"]
        assert "vowel" in practice["soul"]
        assert "mudra" in practice["soul"]
        assert "adonaj_ba" in practice["soul"]
        # Body practice fields
        assert "healing_sound" in practice["body"]
        assert "emotion_positive" in practice["body"]
        assert "emotion_negative" in practice["body"]


# ── Compound Presentation ─────────────────────────────────────────


class TestCompoundPresentation:
    """Compounds have human-readable names and descriptions."""

    def test_all_compounds_have_name(self):
        display = _get_display()
        for key, value in display["compounds"].items():
            if key.startswith("_"):
                continue
            assert "name" in value, f"Compound {key} missing 'name'"
            assert "description" in value, f"Compound {key} missing 'description'"
            assert "active" in value, f"Compound {key} missing 'active'"

    def test_active_list(self):
        display = _get_display()
        active = display["compounds"]["_active"]
        count = display["compounds"]["_active_count"]
        assert isinstance(active, list)
        assert count == len(active)

    def test_no_raw_keys_in_names(self):
        """Display names should not contain underscores."""
        for key, info in COMPOUND_DISPLAY.items():
            assert "_" not in info["name"], f"Underscore in display name: {info['name']}"


# ── Resonance Presentation ────────────────────────────────────────


class TestResonancePresentation:
    """Resonances have human-readable names and descriptions."""

    def test_resonance_categories_present(self):
        display = _get_display()
        res = display["resonances"]
        assert "elemental" in res
        assert "qualitative" in res
        assert "rhythmic" in res
        assert "calendrical" in res

    def test_active_list(self):
        display = _get_display()
        active = display["resonances"]["_active"]
        assert isinstance(active, list)

    def test_boolean_resonances_have_display_info(self):
        display = _get_display()
        for category in ("elemental", "qualitative", "rhythmic", "calendrical"):
            cat = display["resonances"].get(category, {})
            for key, value in cat.items():
                if isinstance(value, dict) and "active" in value:
                    assert "name" in value, f"Resonance {key} missing 'name'"
                    assert "description" in value, f"Resonance {key} missing 'description'"


# ── Point Presentation ────────────────────────────────────────────


class TestPointPresentation:
    """Acupuncture points use medical designation + plain English."""

    @pytest.mark.parametrize("point", list(POINT_DESCRIPTIONS.keys()))
    def test_point_has_description(self, point):
        result = _present_point(point)
        assert result["code"] == point
        assert result["description"] != ""
        assert result["meridian"] != ""

    def test_point_meridian_is_english(self):
        result = _present_point("SI-3")
        assert result["meridian"] == "Small Intestine"

    def test_unknown_point_graceful(self):
        result = _present_point("XX-99")
        assert result["code"] == "XX-99"
        assert result["description"] == ""


# ── Full Integration ──────────────────────────────────────────────


class TestFullIntegration:
    """End-to-end: raw state → presentation → all fields present."""

    def test_present_state_returns_all_sections(self):
        display = _get_display()
        required = {"timestamp", "location", "solar", "soul", "astral",
                    "keys", "body", "hour", "calendar", "compounds", "resonances"}
        assert required.issubset(set(display.keys()))

    def test_timestamp_preserved(self):
        raw = _get_state()
        display = present_state(raw)
        assert display["timestamp"] == raw["timestamp"]

    def test_solar_preserved(self):
        raw = _get_state()
        display = present_state(raw)
        assert display["solar"] == raw["solar"]

    def test_calendar_preserved(self):
        raw = _get_state()
        display = present_state(raw)
        assert display["calendar"] == raw["calendar"]

    def test_hour_preserved(self):
        raw = _get_state()
        display = present_state(raw)
        assert display["hour"] == raw["divine_hour"]
