#!/usr/bin/env python
"""
Astrolabium readout — command line.

    python scripts/readout_cli.py                          # now, default location
    python scripts/readout_cli.py --when "2026-07-29 16:00"
    python scripts/readout_cli.py --lat 43.0731 --lon -89.4012 --tz America/Chicago
    python scripts/readout_cli.py --typed                   # typed state block only
    python scripts/readout_cli.py --exact                   # minute-exact (default is coarse)
    python scripts/readout_cli.py --card 0 --window "3:05-4:42 PM"   # instantiation sheet
    python scripts/readout_cli.py --scan 13:00 21:00        # transition table for a day

Data first. The readout is the answer; interpretation is not this tool's job.
"""

import argparse
import datetime as dt
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import astrolabium as A  # noqa: E402
from src.card_sheet import instantiation_sheet  # noqa: E402
from src.readout import COARSE, EXACT, active_compounds, readout, typed_state  # noqa: E402

# Los Angeles — Timothy's default station.
DEFAULT_LAT, DEFAULT_LON, DEFAULT_TZ = 34.0522, -118.2437, "America/Los_Angeles"


def parse_when(text: str, tz: str) -> dt.datetime:
    """Accept 'YYYY-MM-DD HH:MM', 'YYYY-MM-DD', or 'HH:MM' (today)."""
    zone = ZoneInfo(tz)
    text = text.strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(text, fmt).replace(tzinfo=zone)
        except ValueError:
            continue
    try:
        today = dt.datetime.now(zone).date()
        clock = dt.datetime.strptime(text, "%H:%M").time()
        return dt.datetime.combine(today, clock, tzinfo=zone)
    except ValueError:
        raise SystemExit(f"unparseable --when: {text!r}")


def scan(start: str, end: str, args) -> str:
    """Transition table: print a row only when something actually changes."""
    zone = ZoneInfo(args.tz)
    base = parse_when(args.when, args.tz).date() if args.when else dt.datetime.now(zone).date()
    s_h, s_m = (int(x) for x in start.split(":"))
    e_h, e_m = (int(x) for x in end.split(":"))

    rows = ["=== TRANSITIONS ===", f"  {'time':<8}{'organ':<15}{'vessel':<15}{'hour':<6}compounds"]
    previous = None
    for minute in range(s_h * 60 + s_m, e_h * 60 + e_m + 1):
        moment = dt.datetime.combine(base, dt.time(minute // 60, minute % 60), tzinfo=zone)
        state = A.calculate_complete_state(moment, args.lat, args.lon, args.tz)
        organ = state.get("organ_clock", {}).get("organ")
        vessel = state.get("derivative", {}).get("vessel")
        hour = state.get("divine_hour", {}).get("roman")
        names = tuple(n for _, n in active_compounds(state))
        signature = (organ, vessel, hour, names)
        if signature != previous:
            rows.append(
                f"  {minute//60:02d}:{minute%60:02d}   {str(organ):<15}{str(vessel):<15}"
                f"{str(hour):<6}{', '.join(names) if names else 'none'}"
            )
            previous = signature
    rows.append("=== END TRANSITIONS ===")
    return "\n".join(rows)


def main() -> None:
    p = argparse.ArgumentParser(description="Astrolabium readout (data first).")
    p.add_argument("--when", help="'YYYY-MM-DD HH:MM', 'YYYY-MM-DD', or 'HH:MM'")
    p.add_argument("--lat", type=float, default=DEFAULT_LAT)
    p.add_argument("--lon", type=float, default=DEFAULT_LON)
    p.add_argument("--tz", default=DEFAULT_TZ)
    p.add_argument("--typed", action="store_true", help="typed state block only")
    p.add_argument("--exact", action="store_true",
                   help="minute-exact times (default is coarse: the Divine Hour is the unit)")
    p.add_argument("--card", type=int, help="render an instantiation sheet for this trump")
    p.add_argument("--window", help="human window string for the sheet")
    p.add_argument("--place", help="human place string for the sheet")
    p.add_argument("--scan", nargs=2, metavar=("START", "END"), help="transition table, e.g. 13:00 21:00")
    args = p.parse_args()

    if args.scan:
        print(scan(args.scan[0], args.scan[1], args))
        return

    moment = parse_when(args.when, args.tz) if args.when else dt.datetime.now(ZoneInfo(args.tz))
    state = A.calculate_complete_state(moment, args.lat, args.lon, args.tz)

    if args.card is not None:
        print(instantiation_sheet(args.card, state, window=args.window, place=args.place))
    elif args.typed:
        print(typed_state(state))
    else:
        print(readout(state, precision=EXACT if args.exact else COARSE))


if __name__ == "__main__":
    main()
