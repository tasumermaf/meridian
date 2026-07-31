"""
Guidebook §12 worked-example regression tests.

Pins the three worked examples of astrolabium_guidebook_v2.md (v2.3,
2026-07-30) §12 — and the §13.7 resonance example — to the live engine,
so the document and the engine can never silently diverge again
(AUDIT_2026-07-24 A-10: 0 of 3 examples reproduced before the refit).

Every asserted value below is transcribed in the Guidebook; if one of
these tests fails, either the engine changed (update the Guidebook §12
from a fresh run) or the Guidebook was edited without a run (revert it).

Location: Damanhur, Italy — 45.4°N, 7.9°E, Europe/Rome.
"""

import pytest
from datetime import datetime

from src.astrolabium import calculate_complete_state
from src.engine.stem_branch import get_lgbf_remainder

LAT, LON, TZ = 45.4, 7.9, "Europe/Rome"


def test_example_1_yang_day_2000_01_01_1100():
    """Guidebook §12 Example 1 — Yang day, January 1, 2000, 11:00 CET."""
    dt = datetime(2000, 1, 1, 11, 0)
    state = calculate_complete_state(dt, LAT, LON, TZ)
    lgbf = get_lgbf_remainder(dt, LAT, LON, TZ)

    # Step 1–2: daily pillar 戊午 Wù Wǔ, Yang day
    sb = state["stem_branch"]
    assert sb["daily_stem_index"] == 4
    assert sb["daily_branch_index"] == 6
    assert sb["is_yang_day"] is True

    # Step 3–4: hourly pillar 丁巳 (branch 5 Sì, stem 3 Dīng)
    assert sb["hourly_branch_index"] == 5
    assert lgbf["hour_stem_index"] == 3

    # Step 5–7: Sum 26, mod 9 → 8 → Yin Wei Mai → Geometric Essence (67)
    assert lgbf["substitution_sum"] == 26
    der = state["derivative"]
    assert der["divisor"] == 9
    assert der["remainder"] == 8
    assert der["vessel"] == "Yin Wei Mai"
    assert der["law"] == "Geometric Essence"
    assert der["prime"] == 67
    assert der["confluent"] == "PC-6"

    # Step 8: Organ — Spleen (Earth)
    assert state["organ_clock"]["organ"] == "Spleen"
    assert state["organ_clock"]["element"] == "Earth"

    # Step 9: Divine Hour II
    assert state["divine_hour"]["roman"] == "II"

    # Step 10: elongation 302.03° → phase 5 → Arrow of Complexity (17)
    prim = state["primeval"]
    assert prim["elongation_deg"] == pytest.approx(302.03, abs=0.05)
    assert prim["phase_index"] == 5
    assert prim["law"] == "Arrow of Complexity"
    assert prim["prime"] == 17

    # Step 11–12: no Key, no unity; Yang day → no yin-day flag
    assert state["solar_key"]["active"] is False
    comp = state["compounds"]
    assert comp["two_body_unity"] is False
    assert comp["two_body_unity_raw"] is False
    assert comp["yin_day_blocked"] is False

    # Summary calendar lines: Month 4 EOROS, Sephirotic Day 3 (Mars)
    cal = state["calendar"]
    assert cal["month_number"] == 4
    assert cal["month_name"] == "EOROS"
    assert cal["sephirotic_day"] == 3
    assert cal["sephirotic_planet"] == "Mars"


def test_example_2_yin_day_2000_01_04_1400():
    """Guidebook §12 Example 2 — Yin day, January 4, 2000, 14:00 CET."""
    dt = datetime(2000, 1, 4, 14, 0)
    state = calculate_complete_state(dt, LAT, LON, TZ)
    lgbf = get_lgbf_remainder(dt, LAT, LON, TZ)

    # Step 1–2: daily pillar 辛酉 Xīn Yǒu, Yin day
    sb = state["stem_branch"]
    assert sb["daily_stem_index"] == 7
    assert sb["daily_branch_index"] == 9
    assert sb["is_yang_day"] is False

    # Step 3–4: hourly pillar 乙未 (branch 7 Wèi, stem 1 Yǐ)
    assert sb["hourly_branch_index"] == 7
    assert lgbf["hour_stem_index"] == 1

    # Step 5–7: Sum 25, mod 6 → 1 → Yang Qiao Mai → Divinity (31)
    assert lgbf["substitution_sum"] == 25
    der = state["derivative"]
    assert der["divisor"] == 6
    assert der["remainder"] == 1
    assert der["vessel"] == "Yang Qiao Mai"
    assert der["law"] == "Divinity"
    assert der["prime"] == 31
    assert der["confluent"] == "BL-62"

    # Step 8: Organ — Small Intestine (Fire)
    assert state["organ_clock"]["organ"] == "Sm Intestine"
    assert state["organ_clock"]["element"] == "Fire"

    # Step 9: Divine Hour III
    assert state["divine_hour"]["roman"] == "III"

    # Step 10: elongation 335.99° (< 354, no wrap) → phase 5
    prim = state["primeval"]
    assert prim["elongation_deg"] == pytest.approx(335.99, abs=0.05)
    assert prim["phase_index"] == 5
    assert prim["law"] == "Arrow of Complexity"

    # Step 11: no unity; yin-day flag SET (Yang Qiao restricted + Yin day),
    # but the vessel is still open and read (it IS the reported vessel).
    comp = state["compounds"]
    assert comp["two_body_unity"] is False
    assert comp["two_body_unity_raw"] is False
    assert der["yin_day_restricted"] is True
    assert comp["yin_day_blocked"] is True

    # Summary calendar lines: Month 4 EOROS, Sephirotic Day 6 (Venus)
    cal = state["calendar"]
    assert cal["month_number"] == 4
    assert cal["month_name"] == "EOROS"
    assert cal["sephirotic_day"] == 6
    assert cal["sephirotic_planet"] == "Venus"


def test_example_3_yin_day_flag_2000_01_02_1000():
    """Guidebook §12 Example 3 + §13.7 — January 2, 2000, 10:00 CET.

    Historically presented as a Two-Body Unity event; under the
    canonical remainder map (ruling R2) there is no unity here — the
    example now demonstrates the yin-day flag mechanics (ruling R4).
    """
    dt = datetime(2000, 1, 2, 10, 0)
    state = calculate_complete_state(dt, LAT, LON, TZ)
    lgbf = get_lgbf_remainder(dt, LAT, LON, TZ)

    # Step 1–2: daily pillar 己未 Jǐ Wèi, Yin day
    sb = state["stem_branch"]
    assert sb["daily_stem_index"] == 5
    assert sb["daily_branch_index"] == 7
    assert sb["is_yang_day"] is False

    # Step 3–4: hourly pillar 己巳 (branch 5 Sì, stem 5 Jǐ)
    assert sb["hourly_branch_index"] == 5
    assert lgbf["hour_stem_index"] == 5

    # Step 5–7: Sum 22, mod 6 → 4 → Dai Mai → Time Matrix (29)
    assert lgbf["substitution_sum"] == 22
    der = state["derivative"]
    assert der["divisor"] == 6
    assert der["remainder"] == 4
    assert der["vessel"] == "Dai Mai"
    assert der["law"] == "Time Matrix"
    assert der["prime"] == 29
    assert der["confluent"] == "GB-41"

    # Step 8: Organ — Spleen (Earth)
    assert state["organ_clock"]["organ"] == "Spleen"

    # Step 9: Divine Hour I
    assert state["divine_hour"]["roman"] == "I"

    # Step 10: elongation 312.53° → phase 5 → Arrow of Complexity (17)
    prim = state["primeval"]
    assert prim["elongation_deg"] == pytest.approx(312.53, abs=0.05)
    assert prim["phase_index"] == 5
    assert prim["law"] == "Arrow of Complexity"

    # Step 11–12: NO unity (17 ≠ 29); yin-day flag SET; vessel open.
    comp = state["compounds"]
    assert comp["two_body_unity"] is False
    assert comp["two_body_unity_raw"] is False
    assert der["yin_day_restricted"] is True
    assert comp["yin_day_blocked"] is True

    # Calendar: Month 4 EOROS (Tappetino, Nigredo), Sephirotic Day 4 (Mercury)
    cal = state["calendar"]
    assert cal["month_number"] == 4
    assert cal["month_name"] == "EOROS"
    assert cal["month_group"] == "Tappetino"
    assert cal["alchemical"] == "Nigredo"
    assert cal["sephirotic_day"] == 4
    assert cal["sephirotic_planet"] == "Mercury"

    # §13.7 resonance example — engine: 4 of 12 Boolean active
    res = state["resonances"]
    assert res["active_count"] == 4
    assert res["total_checked"] == 12
    el = res["elemental"]
    assert el["wu_xing_element_match"]["active"] is True      # R_WX_01
    assert el["vessel_organ_element_match"]["active"] is False  # R_WX_02
    assert el["plum_blossom_wu_xing"]["active"] is True       # R_WX_03
    assert el["stem_trigram_polarity"]["active"] is True      # R-14
    assert el["organ_vessel_polarity"]["active"] is False     # R-15
    assert el["paired_organ_vessel_point"]["active"] is False  # R-16
    q = res["qualitative"]
    assert q["color_affinity"]["active"] is False
    assert q["emotion_perception"]["active"] is False
    assert q["adonaj_ba_proximity"]["active"] is False
    rh = res["rhythmic"]
    assert rh["waxing_wing_alignment"]["active"] is False
    assert rh["yang_count"] == 1
    assert rh["divine_hour_law_unity"] is None                # R-17: no unity
    c = res["calendrical"]
    assert c["sephirotic_quest_match"]["active"] is True      # R_SPH_01
    assert c["season_great_rite"]["active"] is False
    assert c["alchemical_stage"] == "Nigredo"
    assert c["month_group"] == "Tappetino"
    assert c["iao_position"] is None
