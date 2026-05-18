"""
Astrolabium Caudae Rubrae — Complete Temporal State Calculator.

Combines engine (pure math) + registry (data) to produce the full
temporal state: what is the alchemical quality of this moment?

All interpretive content comes from registers.json via the registry module.
No hardcoded Law names, vessel-to-Law maps, or trigram assignments in this file.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import pytz

from .engine import solar, lunar, stem_branch, twilight, calendar
from .engine import stellar, solar_terms, festivals
from . import registry
from .resonance import detect_resonances


def calculate_complete_state(
    dt: datetime,
    lat: float,
    lon: float,
    tz: str,
) -> dict:
    """
    Calculate the complete Astrolabium state for a moment in time.

    Assembles all temporal layers with FULL practice context:
    - Solar positions (sunrise/sunset)
    - Organ Clock (Earthly Branch + inner alchemy transmutation practice)
    - LGBF Derivative Law (vessel + Law practice context + trigram qualities)
    - Primeval Law (lunar phase + Law practice context + trigram qualities)
    - Solar Keys (cusping windows + Key Law practice context)
    - Divine Hour (4-fold division + protocols)
    - Calendar (month + sephirotic day + alchemical/IAO context)
    - Compound detection (Unity, Intersection, etc.)
    - Resonance detection (elemental, qualitative, rhythmic, calendrical)

    Every practice-relevant field from registers.json reaches the output.
    The instrument answers both "when" and "what to do."

    Args:
        dt: Datetime for calculation
        lat: Latitude
        lon: Longitude
        tz: Timezone name

    Returns:
        Complete state dict with all layers, practice context, compounds,
        and resonances.
    """
    timezone = pytz.timezone(tz)
    if dt.tzinfo is None:
        dt = timezone.localize(dt)
    else:
        dt = dt.astimezone(timezone)

    # ── 1. Solar positions ──
    solar_pos = solar.get_solar_positions(dt, lat, lon, tz)

    # ── 2. Organ Clock (Earthly Branch from solar position) ──
    branch_index = stem_branch.get_earthly_branch_from_solar(dt, lat, lon, tz)
    organ_data = registry.get_organ_by_branch(branch_index)

    # Determine wing
    is_day = solar_pos["sunrise"] <= dt < solar_pos["sunset"]
    wing = "Day" if is_day else "Night"

    # Inner alchemy transmutation practice for the active organ
    # Looked up by organ name (not element) to handle San Jiao/Pericardium split:
    # Pericardium → Fire (HAWWWW), San Jiao → San Jiao (HEEEEE)
    alchemy_data = registry.get_inner_alchemy_for_organ(organ_data["organ"])

    organ_clock = {
        "branch_index": branch_index,
        "branch_chinese": organ_data["branch_chinese"],
        "branch_name": organ_data["branch_name"],
        "organ": organ_data["organ"],
        "meridian": organ_data["abbr"],
        "element": organ_data["element"],
        "yin_yang": organ_data["yin_yang"],
        "paired": organ_data["paired"],
        "wing": wing,
        "conf_vessel": organ_data["conf_vessel"],
        "coup_vessel": organ_data["coup_vessel"],
        # Inner alchemy transmutation practice [SOURCE: TCM]
        # — what to DO with the active organ window
        "healing_sound": alchemy_data["sound"],
        "emotion_negative": alchemy_data["neg"],
        "emotion_positive": alchemy_data["pos"],
        "healing_color": alchemy_data["color"],
        "organ_spirit": alchemy_data["spirit"],
        "organ_season": alchemy_data["season"],
        "sense_organ": alchemy_data.get("sense_organ"),
        "body_tissue": alchemy_data.get("body_tissue"),
    }

    # ── 3. LGBF (Derivative Law) ──
    lgbf = stem_branch.get_lgbf_remainder(dt, lat, lon, tz)
    vessel_data = registry.get_vessel_for_remainder(lgbf["remainder"])
    derivative_law = vessel_data["law"]
    derivative_law_data = registry.get_law(derivative_law)
    deriv_trigram = derivative_law_data["trigram"]
    deriv_trigram_data = registry.all_trigrams().get(deriv_trigram, {})

    derivative = {
        # Vessel identity
        "law": derivative_law,
        "prime": derivative_law_data["prime"],
        "vessel": vessel_data["name"],
        "vessel_english": vessel_data.get("english_name"),
        "vessel_clinical_domain": vessel_data.get("clinical_domain"),
        "pair_partner": vessel_data["pair_partner"],
        "polarity": vessel_data["polarity"],
        "yin_day_restricted": vessel_data["yin_day_restricted"],
        # Vessel acupuncture points
        "confluent": vessel_data["confluent"],
        "conf_meridian": vessel_data["conf_meridian"],
        "conf_branch": vessel_data["conf_branch"],
        "coupled": vessel_data["coupled"],
        "coup_meridian": vessel_data["coup_meridian"],
        "coup_branch": vessel_data["coup_branch"],
        # LGBF calculation detail
        "remainder": lgbf["remainder"],
        "is_yang_day": lgbf["is_yang_day"],
        "divisor": lgbf["divisor"],
        # Derivative Law practice context [SOURCE: DAM]
        # — the Astral body's operative qualities
        "vowel": derivative_law_data.get("vowel"),
        "mudra": derivative_law_data.get("mudra"),
        "adonaj_ba": derivative_law_data.get("adonaj_ba"),
        "color": derivative_law_data.get("color"),
        "perception_pos": derivative_law_data.get("perception_pos"),
        "perception_neg": derivative_law_data.get("perception_neg"),
        "quest_short": derivative_law_data.get("quest_short"),
        "quest_tarot": derivative_law_data.get("quest_tarot"),
        "binary": derivative_law_data.get("binary"),
        "symbol": derivative_law_data.get("symbol"),
        "is_solar_key": derivative_law_data.get("is_solar_key"),
        # Derivative trigram context [SOURCE: TCM/I Ching]
        "trigram": deriv_trigram,
        "trigram_wu_xing": deriv_trigram_data.get("wu_xing"),
        "trigram_plum_blossom": deriv_trigram_data.get("plum_blossom"),
        "trigram_image": deriv_trigram_data.get("image"),
        "trigram_action": deriv_trigram_data.get("action"),
        "trigram_family": deriv_trigram_data.get("family"),
        "trigram_nature": deriv_trigram_data.get("nature"),
        "trigram_direction": deriv_trigram_data.get("direction"),
        "trigram_season": deriv_trigram_data.get("season"),
    }

    # Yin day restriction check
    yin_day_blocked = (
        not lgbf["is_yang_day"] and vessel_data["yin_day_restricted"]
    )
    derivative["yin_day_blocked"] = yin_day_blocked

    # ── 4. Primeval Law (Lunar Phase) ──
    elong = lunar.get_lunar_elongation(dt)
    phase_index = lunar.get_phase_index(elong)
    illum = lunar.get_illumination(elong)
    phase_data = registry.get_lunar_phase(phase_index)
    primeval_law = phase_data["law"]
    primeval_law_data = registry.get_law(primeval_law)
    primeval_trigram = phase_data["trigram"]
    primeval_trigram_data = registry.all_trigrams().get(primeval_trigram, {})

    primeval = {
        # Lunar phase identity
        "law": primeval_law,
        "prime": primeval_law_data["prime"],
        "phase": phase_data["name"],
        "phase_index": phase_index,
        "trigram": primeval_trigram,
        "symbol": phase_data["symbol"],
        "elongation_deg": round(elong, 2),
        "illumination_pct": round(illum, 1),
        "waxing": phase_data["waxing"],
        "yang_count": phase_data["yang_count"],
        # Primeval Law practice context [SOURCE: DAM]
        # — the Soul body's operative qualities
        "vowel": primeval_law_data.get("vowel"),
        "mudra": primeval_law_data.get("mudra"),
        "adonaj_ba": primeval_law_data.get("adonaj_ba"),
        "color": primeval_law_data.get("color"),
        "perception_pos": primeval_law_data.get("perception_pos"),
        "perception_neg": primeval_law_data.get("perception_neg"),
        "quest_short": primeval_law_data.get("quest_short"),
        "quest_tarot": primeval_law_data.get("quest_tarot"),
        "binary": primeval_law_data.get("binary"),
        "is_solar_key": primeval_law_data.get("is_solar_key"),
        # Primeval trigram context [SOURCE: TCM/I Ching]
        "trigram_wu_xing": primeval_trigram_data.get("wu_xing"),
        "trigram_plum_blossom": primeval_trigram_data.get("plum_blossom"),
        "trigram_image": primeval_trigram_data.get("image"),
        "trigram_action": primeval_trigram_data.get("action"),
        "trigram_family": primeval_trigram_data.get("family"),
        "trigram_nature": primeval_trigram_data.get("nature"),
        "trigram_direction": primeval_trigram_data.get("direction"),
        "trigram_season": primeval_trigram_data.get("season"),
    }

    # ── 5. Solar Keys ──
    cusping = twilight.get_cusping_windows(dt, lat, lon, tz)
    key_state = {"active": cusping["active"], "key": cusping["key"]}
    if cusping["active"] and cusping["key"]:
        key_data = registry.get_solar_key(cusping["key"])
        key_law_data = registry.get_law(key_data["law"])
        key_state["law"] = key_data["law"]
        key_state["prime"] = key_data["prime"]
        key_state["trigram"] = key_data["trigram"]
        key_state["symbol"] = key_data["symbol"]
        key_state["event"] = key_data["event"]
        window = cusping[f"{cusping['key']}_window"]
        key_state["window_start"] = window["start"].isoformat() if hasattr(window["start"], "isoformat") else window["start"]
        key_state["window_end"] = window["end"].isoformat() if hasattr(window["end"], "isoformat") else window["end"]
        key_state["radius_minutes"] = window["radius_minutes"]
        # Key Law practice context [SOURCE: DAM]
        # — what to do during the cusping window
        key_state["vowel"] = key_law_data.get("vowel")
        key_state["mudra"] = key_law_data.get("mudra")
        key_state["adonaj_ba"] = key_law_data.get("adonaj_ba")
        key_state["color"] = key_law_data.get("color")
        key_state["perception_pos"] = key_law_data.get("perception_pos")
        key_state["perception_neg"] = key_law_data.get("perception_neg")
    else:
        key_state["law"] = None
        key_state["prime"] = None

    # ── 6. Divine Hour ──
    divine_hour = _calculate_divine_hour(dt, solar_pos, lat, lon, tz)

    # ── 7. Stem-Branch detail ──
    daily = stem_branch.get_daily_stem_branch(dt)

    # ── 8. Calendar (Divine Month, Sephirotic Day, Divine Year) ──
    month_info = calendar.get_divine_month(dt)
    month_data = registry.get_divine_month(month_info["month_number"])
    seph_info = calendar.get_sephirotic_day(dt)
    seph_data = registry.get_sephirotic_day(seph_info["day"])

    calendar_state = {
        # Month identity
        "divine_year": month_info["divine_year"],
        "month_number": month_info["month_number"],
        "month_name": month_data["name"],
        "month_group": month_data["group"],
        "day_in_month": month_info["day_in_month"],
        "total_days_in_month": month_info["total_days"],
        "is_intercalary": month_info["is_intercalary"],
        "is_intercalary_year": month_info.get("year_is_intercalary", False),
        # Month qualities [SOURCE: DAM]
        "great_rite": month_data["great_rite"],
        "alchemical": month_data["alchemical"],
        "month_element": month_data.get("element"),
        "iao": month_data.get("iao"),
        "month_tier_0_character": month_data.get("tier_0_character"),
        # Sephirotic day [SOURCE: DAM / Western Mystery]
        "sephirotic_day": seph_info["day"],
        "sephirah": seph_data["sephirah"],
        "sephirotic_planet": seph_data["planet"],
        "sephirotic_symbol": seph_data["symbol"],
        "sephirotic_pillar": seph_data["pillar"],
        "sephirotic_frequency": seph_data["frequency"],
        "quarter": seph_info["quarter"],
        "quarter_index": seph_info.get("quarter_index"),
        "quarter_days": seph_info["quarter_days"],
    }

    # ── 9. Assemble state ──
    state = {
        "timestamp": dt.isoformat(),
        "location": {"lat": lat, "lon": lon, "tz": tz},
        "solar": {
            "sunrise": solar_pos["sunrise"].isoformat(),
            "sunset": solar_pos["sunset"].isoformat(),
            "noon": solar_pos["solar_noon"].isoformat(),
            "midnight": solar_pos["solar_midnight"].isoformat(),
        },
        "organ_clock": organ_clock,
        "derivative": derivative,
        "primeval": primeval,
        "solar_key": key_state,
        "divine_hour": divine_hour,
        "calendar": calendar_state,
        "stem_branch": {
            "daily_stem": daily["stem_pinyin"],
            "daily_branch": daily["branch_pinyin"],
            "daily_stem_index": daily["stem_index"],
            "daily_branch_index": daily["branch_index"],
            "sexagenary_index": daily["sexagenary_index"],
            "is_yang_day": daily["is_yang_day"],
            "hourly_branch_index": branch_index,
        },
    }

    # ── 10. Compound detection ──
    state["compounds"] = detect_compounds(state)

    # ── 11. Resonance detection ──
    state["resonances"] = detect_resonances(state)

    # ── 12. Stellar layer (28 Lunar Mansions) ──
    # Where the Sun, Moon, and visible planets sit in the classical
    # Chinese 28-mansion system. Sidereal — see engine/stellar.py.
    state["stellar"] = stellar.get_stellar_state(dt)

    # ── 13. Solar term layer (24 节气) ──
    # Which of the 24 Chinese solar terms is currently active.
    state["solar_term"] = solar_terms.get_solar_term_state(dt)

    # ── 14. Festival proximity (cross-tradition) ──
    # Nearby sacred festivals from the multi-tradition registry,
    # within a 14-day window centered on the moment.
    state["festival_proximity"] = festivals.get_festival_proximity(dt, window_days=14)

    # ── 15. Tibetan lunar month (Phugpa) ──
    # Which Tibetan lunar month contains this moment.
    state["tibetan_month"] = festivals.get_tibetan_month(dt)

    return state


def detect_compounds(state: dict) -> dict:
    """
    Detect all compound configurations from the assembled state.

    Compound definitions per the locked Compound Catalogue v1.0.
    """
    primeval_law = state["primeval"]["law"]
    derivative_law = state["derivative"]["law"]
    active_branch = state["organ_clock"]["branch_index"]
    active_meridian = state["organ_clock"]["meridian"]

    conf_branch = state["derivative"]["conf_branch"]
    coup_branch = state["derivative"]["coup_branch"]
    conf_meridian = state["derivative"]["conf_meridian"]
    coup_meridian = state["derivative"]["coup_meridian"]

    # 1.1 Two-Body Unity: Primeval Law == Derivative Law
    two_body = primeval_law == derivative_law

    # 2.1 Confluent Intersection: vessel confluent on active meridian
    confluent_intersection = (
        conf_branch == active_branch
        and conf_meridian == active_meridian
    )

    # 2.2 Coupled Intersection: vessel coupled on active meridian
    coupled_intersection = (
        coup_branch == active_branch
        and coup_meridian == active_meridian
    )

    # 3.1 Full Confluent Alignment: Law Unity + Confluent Intersection
    full_confluent = two_body and confluent_intersection

    # 3.2 Full Coupled Alignment: Law Unity + Coupled Intersection
    full_coupled = two_body and coupled_intersection

    # 1.2 / 1.3 Key-Derivative Unity
    key_deriv_unity = False
    key_deriv_detail = None
    if state["solar_key"]["active"] and state["solar_key"]["law"]:
        key_law = state["solar_key"]["law"]
        if derivative_law == key_law:
            key_deriv_unity = True
            key_deriv_detail = {
                "key": state["solar_key"]["key"],
                "law": key_law,
            }

    # 3.4 Silver Key-Derivative + Confluent (CONDITIONAL)
    # Silver Key active AND Yang Qiao Mai confluent (BL-62) on active meridian
    cond_3_4 = (
        state["solar_key"]["active"]
        and state["solar_key"]["key"] == "silver"
        and derivative_law == state["solar_key"]["law"]
        and state["derivative"]["vessel"] == "Yang Qiao Mai"
        and conf_meridian == active_meridian
        and conf_branch == active_branch
    )

    # 3.5 Gold Key-Derivative + Coupled (CONDITIONAL)
    # Gold Key active AND Yin Qiao Mai coupled (LU-7) on active meridian
    cond_3_5 = (
        state["solar_key"]["active"]
        and state["solar_key"]["key"] == "gold"
        and derivative_law == state["solar_key"]["law"]
        and state["derivative"]["vessel"] == "Yin Qiao Mai"
        and coup_meridian == active_meridian
        and coup_branch == active_branch
    )

    # Yin day restriction
    yin_day_blocked = state["derivative"].get("yin_day_blocked", False)

    # Effective two-body unity (after yin day gate)
    two_body_effective = two_body and not yin_day_blocked

    # Key activity
    key_active = state["solar_key"]["active"]
    any_anatomical = confluent_intersection or coupled_intersection

    # 6.1 Key-Amplified Unity: Two-Body Unity + any Key active
    key_amplified = two_body_effective and key_active

    # 6.2 Anatomical Intersection + Key: any anatomical during cusping
    anatomical_key = any_anatomical and key_active

    # 6.3 Full Alignment + Key: the absolute maximum compound
    full_alignment = (full_confluent or full_coupled) and not yin_day_blocked
    full_alignment_key = full_alignment and key_active

    # 4.2 Polarity Alignment: vessel polarity matches day polarity
    vessel_polarity = state["derivative"]["polarity"]
    is_yang_day = state["derivative"]["is_yang_day"]
    polarity_aligned = (
        (is_yang_day and vessel_polarity == "Yang")
        or (not is_yang_day and vessel_polarity == "Yin")
    )

    # Calendar-derived compounds
    calendar = state.get("calendar", {})
    great_rite = calendar.get("great_rite")
    great_rite_active = great_rite is not None
    vadusfadahm_active = calendar.get("month_number") == 13
    sephirotic_day = calendar.get("sephirotic_day", 1)
    sephirotic_rare = sephirotic_day >= 8

    return {
        # Category 1: Law Unity
        "two_body_unity": two_body_effective,
        "two_body_unity_raw": two_body,
        "key_derivative_unity": key_deriv_unity,
        "key_derivative_detail": key_deriv_detail,
        # Category 2: Anatomical Intersection
        "confluent_intersection": confluent_intersection,
        "coupled_intersection": coupled_intersection,
        # Category 3: Combined
        "full_confluent": full_confluent and not yin_day_blocked,
        "full_coupled": full_coupled and not yin_day_blocked,
        "conditional_3_4": cond_3_4,
        "conditional_3_5": cond_3_5,
        # Category 4: Polarity
        "yin_day_blocked": yin_day_blocked,
        "polarity_aligned": polarity_aligned,
        # Category 5: Calendar
        "great_rite_active": great_rite_active,
        "vadusfadahm_active": vadusfadahm_active,
        "sephirotic_rare": sephirotic_rare,
        # Category 6: Multi-Layer
        "key_amplified_unity": key_amplified,
        "anatomical_key": anatomical_key,
        "full_alignment_key": full_alignment_key,
    }


def _calculate_divine_hour(
    dt: datetime, solar_pos: dict, lat: float, lon: float, tz: str
) -> dict:
    """Calculate the current Divine Hour (1-8) from solar positions."""
    sunrise = solar_pos["sunrise"]
    sunset = solar_pos["sunset"]

    if sunrise <= dt < sunset:
        # Day period: hours I-IV
        period_start = sunrise
        period_duration = (sunset - sunrise).total_seconds()
        base = 0
    else:
        # Night period: hours V-VIII
        if dt >= sunset:
            period_start = sunset
            next_solar = solar.get_solar_positions(
                dt + timedelta(days=1), lat, lon, tz
            )
            period_end = next_solar["sunrise"]
        else:
            prev_solar = solar.get_solar_positions(
                dt - timedelta(days=1), lat, lon, tz
            )
            period_start = prev_solar["sunset"]
            period_end = sunrise

        period_duration = (period_end - period_start).total_seconds()
        base = 4

    elapsed = (dt - period_start).total_seconds()
    position = elapsed / period_duration if period_duration > 0 else 0
    quarter = min(4, max(1, int(position * 4) + 1))
    hour_index = base + quarter

    hour_data = registry.get_divine_hour(hour_index)

    hour_duration = period_duration / 4
    hour_position = (position * 4) % 1
    remaining_min = hour_duration * (1 - hour_position) / 60

    return {
        "index": hour_index,
        "roman": hour_data["roman"],
        "wing": hour_data["wing"],
        "position": quarter,
        "protocols": hour_data["protocols"],
        "duration_minutes": round(hour_duration / 60, 1),
        "remaining_minutes": round(remaining_min, 1),
        "progress_pct": round(hour_position * 100, 1),
    }
