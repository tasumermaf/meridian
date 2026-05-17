"""
Build registers.json from the Phase 2 dispatch data.

Source: astrolabium/docs/interpretive/dispatch/dispatch_phase2_data.md
Output: astrolabium/code/data/registers.json

The dispatch file contains all 9 registers in markdown table format.
This script parses those tables into structured JSON.

Run: python data/build_registers.py
"""

import json
import re
from pathlib import Path


def parse_table(lines):
    """Parse a markdown table into list of dicts."""
    if len(lines) < 3:
        return []
    headers = [h.strip() for h in lines[0].split("|") if h.strip()]
    rows = []
    for line in lines[2:]:  # Skip header and separator
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def find_table_after(lines, marker):
    """Find the next markdown table after a line containing marker."""
    start = None
    for i, line in enumerate(lines):
        if marker in line:
            start = i
            break
    if start is None:
        return []

    table_lines = []
    in_table = False
    for line in lines[start:]:
        if "|" in line and line.strip().startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table:
            break
    return table_lines


def build_laws(lines):
    """Build Register A: Law Identity from transposed table."""
    table = find_table_after(lines, "REGISTER A:")
    if not table:
        raise ValueError("Could not find Register A table")

    rows = parse_table(table)
    law_names = [h.strip() for h in table[0].split("|") if h.strip()][1:]

    laws = {}
    field_map = {}
    for row in rows:
        field = row.get("Field", "")
        field_map[field] = {name: row.get(name, "") for name in law_names}

    for name in law_names:
        is_key = name in ("Fall of Events", "Divinity")
        vowel = field_map.get("**Vowel**", {}).get(name, "")
        mudra = field_map.get("**Mudra**", {}).get(name, "")
        laws[name] = {
            "prime": int(field_map["**Prime**"][name]),
            "trigram": field_map["**Trigram**"][name].split()[0],
            "symbol": field_map["**Trigram**"][name].split()[-1] if len(field_map["**Trigram**"][name].split()) > 1 else "",
            "binary": field_map["**Binary**"][name],
            "adonaj_ba": field_map["**Adonaj-Ba**"][name],
            "color": field_map["**Color**"][name],
            "perception_pos": field_map["**Perception (+)**"][name],
            "perception_neg": field_map["**Perception (−)**"][name],
            "quest_short": field_map["**Quest Short**"][name],
            "quest_tarot": field_map["**Quest Tarot**"][name],
            "vowel": vowel if vowel and "[GAP]" not in vowel else None,
            "mudra": mudra if mudra and "[GAP]" not in mudra else None,
            "is_solar_key": is_key,
        }
    return laws


def build_registers(dispatch_path):
    """Parse the dispatch markdown and build the full registers dict."""
    text = Path(dispatch_path).read_text(encoding="utf-8")
    lines = text.splitlines()

    # Register B: Trigrams
    trig_table = find_table_after(lines, "REGISTER B:")
    trig_rows = parse_table(trig_table)
    trigrams = {}
    for r in trig_rows:
        name = r["Trigram"]
        trigrams[name] = {
            "symbol": r["Symbol"],
            "wu_xing": r["Wu Xing"],
            "plum_blossom": r["Plum Blossom"],
            "image": r["Image"],
            "action": r["Action"],
            "law": r["Law"],
            "vessel": r["Vessel"],
        }

    # Register C: Vessels
    ves_table = find_table_after(lines, "REGISTER C:")
    ves_rows = parse_table(ves_table)
    vessels = {}
    for r in ves_rows:
        name = r["Vessel"]
        yin_day = r.get("Yin Day", "")
        vessels[name] = {
            "law": r["Law"],
            "prime": int(r["Prime"]),
            "confluent": r["Confluent"],
            "conf_meridian": r["Conf. Meridian"],
            "conf_branch": int(r["Conf. Branch"]),
            "coupled": r["Coupled"],
            "coup_meridian": r["Coup. Meridian"],
            "coup_branch": int(r["Coup. Branch"]),
            "pair_partner": r["Pair Partner"],
            "polarity": r["Polarity"],
            "yin_day_restricted": "No" not in yin_day,
        }

    # Register D: Organs
    org_table = find_table_after(lines, "REGISTER D:")
    org_rows = parse_table(org_table)
    organs = []
    for r in org_rows:
        conf = r.get("Conf. Vessel", "NONE")
        coup = r.get("Coup. Vessel", "NONE")
        organs.append({
            "branch_index": int(r["Index"]),
            "branch_name": r["Branch"].split()[-1] if " " in r["Branch"] else r["Branch"],
            "branch_chinese": r["Branch"].split()[0] if " " in r["Branch"] else "",
            "organ": r["Organ"],
            "abbr": r["Abbr"],
            "element": r["Element"],
            "yin_yang": r["Yin/Yang"],
            "paired": r["Paired"],
            "wing": r["Wing"],
            "conf_vessel": conf if conf != "NONE" else None,
            "coup_vessel": coup if coup != "NONE" else None,
        })

    # Register E: Lunar Phases
    lun_table = find_table_after(lines, "REGISTER E:")
    lun_rows = parse_table(lun_table)
    lunar_phases = []
    for r in lun_rows:
        elong = r.get("Elongation", "0°–60°")
        parts = elong.replace("°", "").split("–")
        trig_parts = r["Trigram"].split()
        lunar_phases.append({
            "index": int(r["Phase"].split()[0]),
            "name": " ".join(r["Phase"].split()[1:]),
            "elong_start": int(parts[0]),
            "elong_end": int(parts[1]) if len(parts) > 1 else 360,
            "trigram": trig_parts[0],
            "symbol": trig_parts[1] if len(trig_parts) > 1 else "",
            "yang_count": int(r["Yang Count"]),
            "law": r["Law"],
            "prime": int(r["Prime"]),
            "waxing": r.get("Waxing/Waning", "Waxing") == "Waxing",
        })

    # Register F: Solar Keys
    key_table = find_table_after(lines, "REGISTER F:")
    key_rows = parse_table(key_table)
    solar_keys = {}
    for r in key_rows:
        k = r["Key"].lower()
        trig_parts = r["Trigram"].split()
        solar_keys[k] = {
            "law": r["Law"],
            "prime": int(r["Prime"]),
            "trigram": trig_parts[0],
            "symbol": trig_parts[1] if len(trig_parts) > 1 else "",
            "event": r["Solar Event"].lower(),
        }

    # Register G: Divine Hours
    hr_table = find_table_after(lines, "REGISTER G:")
    hr_rows = parse_table(hr_table)
    divine_hours = []
    for r in hr_rows:
        proto = r.get("BTR Protocols", "")
        divine_hours.append({
            "index": int(r["Hour"]),
            "roman": r["Hour"],  # Will be overwritten
            "wing": r["Wing"],
            "position": int(r["Position"].split("/")[0]),
            "protocols": proto if proto and "[GAP" not in proto else None,
        })
    # Fix roman numerals
    romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
    for i, h in enumerate(divine_hours):
        h["index"] = i + 1
        h["roman"] = romans[i]

    # Register H: Divine Months
    mo_table = find_table_after(lines, "REGISTER H:")
    mo_rows = parse_table(mo_table)
    divine_months = []
    for r in mo_rows:
        element = r.get("Element", "")
        rite = r.get("Great Rite", "")
        iao = r.get("IAO", "")
        divine_months.append({
            "number": int(r["#"]),
            "name": r["Month"],
            "group": r["Group"],
            "element": element if element and element != "—" else None,
            "great_rite": rite if rite and rite != "—" else None,
            "iao": iao if iao and iao != "—" else None,
            "alchemical": r.get("Alchemical", ""),
        })

    # Register I: Sephirotic Days
    seph_table = find_table_after(lines, "REGISTER I:")
    seph_rows = parse_table(seph_table)
    sephirotic_days = []
    for r in seph_rows:
        planet_parts = r["Planet"].split()
        sephirotic_days.append({
            "day": int(r["Day"]),
            "sephirah": r["Sephirah"],
            "planet": planet_parts[0],
            "symbol": planet_parts[1] if len(planet_parts) > 1 else "",
            "pillar": r["Pillar"].rstrip("*"),
            "frequency": r["Frequency"],
        })

    # Vessel remainder map (TCM canonical — not from dispatch, hardcoded per LGBF)
    vessel_remainder_map = {
        "1": "Yang Qiao Mai",
        "2": "Yin Qiao Mai",
        "3": "Yang Wei Mai",
        "4": "Dai Mai",
        "5": "Yin Qiao Mai",
        "6": "Chong Mai",
        "7": "Du Mai",
        "8": "Yin Wei Mai",
        "9": "Ren Mai",
    }

    return {
        "meta": {
            "version": "1.0.0",
            "source": "astrolabium/docs/interpretive/dispatch/dispatch_phase2_data.md",
            "spec": "6+2 Trigram-Law Architecture (locked March 1, 2026)",
            "generated": "2026-03-01",
        },
        "laws": build_laws(lines),
        "trigrams": trigrams,
        "vessels": vessels,
        "organs": organs,
        "chia": {
            "Wood": {"organs": ["Liver", "Gallbladder"], "neg": "Anger, frustration", "pos": "Kindness, generosity", "sound": "SHHHHH", "color": "Green", "spirit": "Hun (Green Dragon)", "season": "Spring"},
            "Fire": {"organs": ["Heart", "Sm Intestine", "Pericardium"], "neg": "Hatred, arrogance", "pos": "Love, joy, honor", "sound": "HAWWWW", "color": "Red", "spirit": "Shen (Red Bird)", "season": "Summer"},
            "Earth": {"organs": ["Spleen", "Stomach"], "neg": "Worry, anxiety", "pos": "Fairness, trust", "sound": "WHOOOO", "color": "Yellow", "spirit": "Yi (Phoenix)", "season": "Late Summer"},
            "Metal": {"organs": ["Lung", "Lg Intestine"], "neg": "Sadness, grief", "pos": "Courage, righteousness", "sound": "SSSSSSS", "color": "White", "spirit": "Po (White Tiger)", "season": "Autumn"},
            "Water": {"organs": ["Kidney", "Bladder"], "neg": "Fear, paranoia", "pos": "Gentleness, wisdom", "sound": "WOOOOO", "color": "Blue/Black", "spirit": "Zhi (Blue Turtle)", "season": "Winter"},
            "San Jiao": {"organs": ["San Jiao"], "neg": "Panic, imbalance", "pos": "Peace, harmony", "sound": "HEEEEE", "color": None, "spirit": None, "season": None},
        },
        "lunar_phases": lunar_phases,
        "solar_keys": solar_keys,
        "divine_hours": divine_hours,
        "divine_months": divine_months,
        "sephirotic_days": sephirotic_days,
        "vessel_remainder_map": vessel_remainder_map,
    }


if __name__ == "__main__":
    here = Path(__file__).parent
    project_root = here.parent.parent  # astrolabium/
    dispatch = project_root / "docs" / "interpretive" / "dispatch" / "dispatch_phase2_data.md"

    if not dispatch.exists():
        print(f"ERROR: Dispatch file not found at {dispatch}")
        raise SystemExit(1)

    data = build_registers(dispatch)
    out = here / "registers.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"registers.json written to {out}")
    print(f"  Laws: {len(data['laws'])}")
    print(f"  Trigrams: {len(data['trigrams'])}")
    print(f"  Vessels: {len(data['vessels'])}")
    print(f"  Organs: {len(data['organs'])}")
    print(f"  Lunar phases: {len(data['lunar_phases'])}")
    print(f"  Solar keys: {len(data['solar_keys'])}")
    print(f"  Divine hours: {len(data['divine_hours'])}")
    print(f"  Divine months: {len(data['divine_months'])}")
    print(f"  Sephirotic days: {len(data['sephirotic_days'])}")
