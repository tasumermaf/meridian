"""
Compound Timeline Generator — produces a linear chronological list of all
compound windows (2+ simultaneous phenomena) from a start datetime through
the end of the current Divine Year.

Contiguous 15-minute steps with the SAME active set are consolidated into
a single window with start/end times.

Output: Markdown file at data/compound_timeline.md

Usage:
    cd astrolabium/code
    python -m scripts.compound_timeline
"""

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.astrolabium import calculate_complete_state
from src.frequency import COMPOUND_TYPES
from src.resonance import RESONANCE_BOOLEAN_TYPES
from src.engine.calendar import get_divine_year

LAT = 45.4167
LON = 7.8833
TZ = "Europe/Rome"
INTERVAL = 15  # minutes


def _get_active_set(state: dict) -> frozenset:
    """Return frozenset of all active boolean types."""
    active = set()
    compounds = state.get("compounds", {})
    for c in COMPOUND_TYPES:
        if compounds.get(c):
            active.add(c)

    resonances = state.get("resonances", {})
    for cat_name in ("elemental", "qualitative", "rhythmic", "calendrical"):
        cat = resonances.get(cat_name, {})
        if isinstance(cat, dict):
            for rtype, rdata in cat.items():
                if rtype in RESONANCE_BOOLEAN_TYPES:
                    if isinstance(rdata, dict) and rdata.get("active"):
                        active.add(rtype)
    return frozenset(active)


def _get_state_summary(state: dict) -> dict:
    """Extract key state fields for context."""
    cal = state.get("calendar", {})
    return {
        "primeval_law": state["primeval"]["law"],
        "derivative_law": state["derivative"]["law"],
        "organ": state["organ_clock"]["organ"],
        "element": state["organ_clock"]["element"],
        "phase": state["primeval"]["phase"],
        "vessel": state["derivative"]["vessel"],
        "divine_hour": state["divine_hour"]["index"],
        "month_number": cal.get("month_number"),
        "month_name": cal.get("month_name", ""),
        "sephirotic_day": cal.get("sephirotic_day_number"),
        "sephirotic_planet": cal.get("sephirotic_planet", ""),
    }


def _fmt_dt(dt: datetime) -> str:
    """Format datetime as compact ISO-like string."""
    return dt.strftime("%Y-%m-%d %H:%M")


def main():
    # Determine boundaries: NOW through end of Divine Year
    start_dt = datetime(2026, 3, 2, 12, 0)  # Now
    year_info = get_divine_year(start_dt)
    end_dt = year_info["next_year_start"]

    remaining_days = (end_dt - start_dt).total_seconds() / 86400
    expected_steps = int(remaining_days * 24 * 60 / INTERVAL) + 1

    print(f"=== Compound Timeline Generator ===")
    print(f"Divine Year {year_info['year']}")
    print(f"  From:  {start_dt.isoformat()}")
    print(f"  To:    {end_dt.isoformat()}")
    print(f"  Days:  {remaining_days:.1f}")
    print(f"  Steps: ~{expected_steps}")
    print()

    delta = timedelta(minutes=INTERVAL)
    current = start_dt
    total = 0

    # Window tracking
    windows = []
    current_recipe = frozenset()
    window_start = None
    window_end = None
    window_state = None

    t0 = time.time()

    while current < end_dt:
        state = calculate_complete_state(current, LAT, LON, TZ)
        total += 1
        active = _get_active_set(state)

        if len(active) >= 2:
            if active == current_recipe:
                # Extend current window
                window_end = current
            else:
                # Close previous window if any
                if current_recipe and len(current_recipe) >= 2:
                    windows.append({
                        "start": window_start,
                        "end": window_end,
                        "recipe": current_recipe,
                        "state": window_state,
                    })
                # Start new window
                current_recipe = active
                window_start = current
                window_end = current
                window_state = _get_state_summary(state)
        else:
            # No compound active — close any open window
            if current_recipe and len(current_recipe) >= 2:
                windows.append({
                    "start": window_start,
                    "end": window_end,
                    "recipe": current_recipe,
                    "state": window_state,
                })
            current_recipe = frozenset()
            window_start = None
            window_end = None
            window_state = None

        if total % 3000 == 0:
            elapsed = time.time() - t0
            rate = total / elapsed
            remaining = (expected_steps - total) / rate if rate > 0 else 0
            print(
                f"  Step {total}/{expected_steps} "
                f"({total/expected_steps*100:.1f}%) "
                f"— {rate:.0f} steps/s, ~{remaining:.0f}s remaining"
            )

        current += delta

    # Close final window
    if current_recipe and len(current_recipe) >= 2:
        windows.append({
            "start": window_start,
            "end": window_end,
            "recipe": current_recipe,
            "state": window_state,
        })

    elapsed_total = time.time() - t0
    print(f"\nCompleted: {total} steps in {elapsed_total:.1f}s "
          f"({total/elapsed_total:.0f} steps/s)")
    print(f"Total compound windows: {len(windows)}")

    # ── Generate Markdown ──
    output_path = Path(__file__).parent.parent / "data" / "compound_timeline.md"

    # Collect stats
    total_compound_steps = sum(
        1 + int((w["end"] - w["start"]).total_seconds() / (INTERVAL * 60))
        for w in windows
    )
    complexity_counts = {}
    for w in windows:
        n = len(w["recipe"])
        complexity_counts[n] = complexity_counts.get(n, 0) + 1

    # Group windows by month
    month_windows = {}
    for w in windows:
        m = w["state"]["month_number"]
        name = w["state"]["month_name"]
        key = (m, name)
        if key not in month_windows:
            month_windows[key] = []
        month_windows[key].append(w)

    lines = []
    lines.append("# Compound Timeline — Divine Year 77")
    lines.append("")
    lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC")
    lines.append(f"**Period:** {_fmt_dt(start_dt)} → {_fmt_dt(end_dt)}")
    lines.append(f"**Location:** Damanhur ({LAT}°N, {LON}°E)")
    lines.append(f"**Resolution:** {INTERVAL} min")
    lines.append(f"**Total steps scanned:** {total:,}")
    lines.append(f"**Total compound windows:** {len(windows):,}")
    lines.append(f"**Steps with a compound active:** {total_compound_steps:,} "
                 f"({total_compound_steps/total*100:.1f}%)")
    lines.append("")
    lines.append("## Complexity Distribution of Windows")
    lines.append("")
    lines.append("| Components | Windows | Description |")
    lines.append("|:----------:|--------:|:------------|")
    for n in sorted(complexity_counts.keys()):
        lines.append(f"| {n} | {complexity_counts[n]:,} | {n}-component compound |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Chronological Timeline")
    lines.append("")
    lines.append("Each entry is a contiguous window where the **same compound recipe**")
    lines.append("was active. When the recipe changes (even by one component), a new")
    lines.append("window begins.")
    lines.append("")

    # Write by month
    for (m_num, m_name), m_wins in sorted(month_windows.items()):
        lines.append(f"### Month {m_num} — {m_name}")
        lines.append("")
        lines.append(f"*{len(m_wins)} compound windows in this month*")
        lines.append("")

        for i, w in enumerate(m_wins, 1):
            start = w["start"]
            end = w["end"]
            duration_min = int((end - start).total_seconds() / 60) + INTERVAL
            recipe = w["recipe"]
            st = w["state"]
            n = len(recipe)

            # Classify components
            compounds = sorted(c for c in recipe if c in COMPOUND_TYPES)
            resonances = sorted(r for r in recipe if r in RESONANCE_BOOLEAN_TYPES)

            lines.append(f"**{i}. {_fmt_dt(start)} → {_fmt_dt(end)}** "
                         f"({duration_min} min) — **{n} components**")

            # Components on one line if short, else listed
            comp_strs = []
            for c in compounds:
                comp_strs.append(f"`{c}` (C)")
            for r in resonances:
                comp_strs.append(f"`{r}` (R)")

            if len(comp_strs) <= 3:
                lines.append(f"  Components: {', '.join(comp_strs)}")
            else:
                lines.append(f"  Components:")
                for cs in comp_strs:
                    lines.append(f"  - {cs}")

            lines.append(f"  State: {st['primeval_law']} / {st['derivative_law']} | "
                         f"{st['organ']} ({st['element']}) | "
                         f"{st['phase']} | {st['vessel']} | "
                         f"Hour {st['divine_hour']} | "
                         f"Seph. Day {st['sephirotic_day']} ({st['sephirotic_planet']})")
            lines.append("")

    # Summary
    lines.append("---")
    lines.append("")
    lines.append("## Summary Statistics")
    lines.append("")

    # Highest complexity windows
    max_n = max(len(w["recipe"]) for w in windows)
    max_windows = [w for w in windows if len(w["recipe"]) == max_n]
    lines.append(f"**Highest complexity:** {max_n} components "
                 f"({len(max_windows)} windows)")
    for w in max_windows[:5]:
        lines.append(f"  - {_fmt_dt(w['start'])} → {_fmt_dt(w['end'])}: "
                     f"{', '.join(sorted(w['recipe']))}")
    lines.append("")

    # Longest windows
    longest = sorted(windows,
                     key=lambda w: (w["end"] - w["start"]).total_seconds(),
                     reverse=True)[:10]
    lines.append("**Longest continuous windows (same recipe):**")
    for w in longest:
        dur = int((w["end"] - w["start"]).total_seconds() / 60) + INTERVAL
        lines.append(f"  - {_fmt_dt(w['start'])} → {_fmt_dt(w['end'])} "
                     f"({dur} min, {len(w['recipe'])} components): "
                     f"{', '.join(sorted(w['recipe']))}")
    lines.append("")

    content = "\n".join(lines) + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nTimeline written to {output_path}")
    print(f"File size: {len(content):,} characters, {len(lines):,} lines")


if __name__ == "__main__":
    main()
