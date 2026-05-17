"""
Registry: read-only access to registers.json.

Loads data/registers.json at first access. Provides typed lookups.
No computation. No mutation. Pure data access.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

_DATA = None
_JSON_PATH = Path(__file__).parent.parent / "data" / "registers.json"


def _load() -> dict:
    global _DATA
    if _DATA is None:
        with open(_JSON_PATH, "r", encoding="utf-8") as f:
            _DATA = json.load(f)
    return _DATA


def get_law(name: str) -> dict:
    """Get a Law's full record by name."""
    data = _load()
    if name not in data["laws"]:
        raise KeyError(f"Unknown law: {name}")
    return data["laws"][name]


def get_vessel(name: str) -> dict:
    """Get a Vessel's full record by name."""
    data = _load()
    if name not in data["vessels"]:
        raise KeyError(f"Unknown vessel: {name}")
    return data["vessels"][name]


def get_vessel_for_remainder(remainder: int) -> dict:
    """
    Look up vessel by LGBF remainder.

    Returns dict with vessel name and full vessel data.
    """
    data = _load()
    key = str(remainder)
    if key not in data["vessel_remainder_map"]:
        raise KeyError(f"No vessel for remainder {remainder}")
    name = data["vessel_remainder_map"][key]
    vessel = data["vessels"][name]
    return {"name": name, **vessel}


def get_organ_by_branch(branch_index: int) -> dict:
    """Get organ clock entry by Earthly Branch index (0-11)."""
    data = _load()
    for organ in data["organs"]:
        if organ["branch_index"] == branch_index:
            return organ
    raise KeyError(f"No organ for branch index {branch_index}")


def get_organ_by_name(name: str) -> dict:
    """Get organ clock entry by organ name (e.g., 'Liver', 'Lung')."""
    data = _load()
    for organ in data["organs"]:
        if organ["organ"] == name:
            return organ
    raise KeyError(f"No organ with name {name}")


def get_lunar_phase(phase_index: int) -> dict:
    """Get lunar phase entry by index (0-5)."""
    data = _load()
    for phase in data["lunar_phases"]:
        if phase["index"] == phase_index:
            return phase
    raise KeyError(f"No lunar phase for index {phase_index}")


def get_solar_key(which: str) -> dict:
    """Get solar key data. which = 'gold' or 'silver'."""
    data = _load()
    if which not in data["solar_keys"]:
        raise KeyError(f"Unknown solar key: {which}. Use 'gold' or 'silver'.")
    return data["solar_keys"][which]


def get_divine_hour(index: int) -> dict:
    """Get divine hour entry by index (1-8)."""
    data = _load()
    for hour in data["divine_hours"]:
        if hour["index"] == index:
            return hour
    raise KeyError(f"No divine hour for index {index}")


def get_divine_month(number: int) -> dict:
    """Get divine month entry by number (1-13)."""
    data = _load()
    for month in data["divine_months"]:
        if month["number"] == number:
            return month
    raise KeyError(f"No divine month for number {number}")


def get_sephirotic_day(day: int) -> dict:
    """Get sephirotic day entry by day number (1-9)."""
    data = _load()
    for s in data["sephirotic_days"]:
        if s["day"] == day:
            return s
    raise KeyError(f"No sephirotic day for day {day}")


def get_inner_alchemy(element: str) -> dict:
    """Get inner alchemy transmutation data by Wu Xing element."""
    data = _load()
    if element not in data["inner_alchemy"]:
        raise KeyError(f"Unknown element for inner alchemy: {element}")
    return data["inner_alchemy"][element]


def get_inner_alchemy_for_organ(organ_name: str) -> dict:
    """
    Get inner alchemy transmutation data by organ name.

    Handles the San Jiao / Pericardium split correctly:
    Pericardium shares Fire's entry (HAWWWW), while San Jiao
    has its own entry (HEEEEE). Element-based lookup would conflate them.
    """
    data = _load()
    for alchemy_key, alchemy_entry in data["inner_alchemy"].items():
        if organ_name in alchemy_entry["organs"]:
            return {"alchemy_key": alchemy_key, **alchemy_entry}
    raise KeyError(f"No inner alchemy entry for organ: {organ_name}")


def all_laws() -> dict:
    """Return all 8 Laws."""
    return _load()["laws"]


def all_vessels() -> dict:
    """Return all 8 Vessels."""
    return _load()["vessels"]


def all_organs() -> list:
    """Return all 12 organ entries."""
    return _load()["organs"]


def all_trigrams() -> dict:
    """Return all 8 trigrams."""
    return _load()["trigrams"]
