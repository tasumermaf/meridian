"""
Astrolabium API — FastAPI wrapper for the temporal state calculator.

Endpoints:
  GET /state          — Complete state for a moment in time (raw)
  GET /display        — THE OUTPUT LAW surface: readout + typed state + story gate
  GET /projection     — Time series of states (raw)
  GET /frequency      — Compound frequency analysis over a range
  GET /windows        — Contiguous windows for a compound type
  GET /next-compound  — Next occurrence of any compound type
  GET /next-unity     — Next Two-Body Unity window (convenience)
  GET /resonance-coverage — Resonance type diagnostic
  GET /health         — Service health check

All interpretive data from registers.json. No hardcoded mappings.
"""

import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pytz

from ..astrolabium import calculate_complete_state
from ..frequency import (
    scan_compounds, find_windows, next_compound,
    COMPOUND_TYPES, ALL_SEARCHABLE_TYPES,
)
from ..resonance import RESONANCE_BOOLEAN_TYPES, RESONANCE_STATE_TYPES, ALL_RESONANCE_TYPES
from ..presentation import present_state
from ..readout import COARSE, EXACT, readout, story_gate, typed_state
from .. import registry

VERSION = "3.3.0"  # 3.3.0 (2026-07-30): /display serves the Output Law shape (AUDIT B-05)

MAX_PROJECTION_STEPS = 10_000
MAX_SEARCH_HOURS = 8760  # one year

app = FastAPI(
    title="Astrolabium Caudae Rubrae",
    version=VERSION,
    description="Temporal navigation system — 6+2 Trigram-Law Architecture + Resonance Scanner",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Input validation helpers ──────────────────────────────────────────


def _parse_datetime(value: str, param_name: str = "dt") -> datetime:
    """Parse ISO datetime string with structured error on failure."""
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid datetime for '{param_name}': {value!r}. Expected ISO 8601 format (e.g., 2026-03-19T12:00:00).",
        )


def _parse_timezone(tz: str) -> pytz.BaseTzInfo:
    """Validate timezone string and return pytz timezone object."""
    try:
        return pytz.timezone(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown timezone: {tz!r}. Use IANA timezone names (e.g., America/Los_Angeles, Europe/Rome, Asia/Shanghai).",
        )


def _validate_compound(compound: str) -> None:
    """Validate compound/resonance type string."""
    if compound not in ALL_SEARCHABLE_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown compound/resonance: {compound!r}. Valid types: {sorted(ALL_SEARCHABLE_TYPES)}",
        )


def _resolve_datetime(dt: Optional[str], tz: str) -> datetime:
    """Parse dt if provided, otherwise return current time in tz."""
    if dt:
        return _parse_datetime(dt)
    timezone = _parse_timezone(tz)
    return datetime.now(timezone)


# ── Global exception handler ─────────────────────────────────────────


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError: polar conditions, bad inputs."""
    detail = str(exc)
    if "Polar conditions" in detail:
        return JSONResponse(
            status_code=422,
            content={
                "error": "polar_conditions",
                "detail": detail,
                "hint": "Solar-position-based calculations require a location where the sun both rises and sets on the given date. Try a latitude closer to the equator, or a different date.",
            },
        )
    return JSONResponse(
        status_code=422,
        content={
            "error": "invalid_input",
            "detail": detail,
            "type": "ValueError",
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all: return structured JSON instead of raw 500."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": str(exc),
            "type": type(exc).__name__,
        },
    )


# ── Request timing middleware ─────────────────────────────────────────


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Response-Time-Ms"] = f"{duration_ms:.1f}"
    return response


# ── Endpoints ─────────────────────────────────────────────────────────


@app.get("/health")
def health():
    """Service health check."""
    laws = registry.all_laws()
    vessels = registry.all_vessels()
    return {
        "status": "healthy",
        "version": VERSION,
        "spec": "6+2 Trigram-Law Architecture + Resonance Scanner",
        "laws_loaded": len(laws),
        "vessels_loaded": len(vessels),
        "compound_types": len(COMPOUND_TYPES),
        "resonance_types": len(ALL_RESONANCE_TYPES),
        "total_trackable": len(ALL_SEARCHABLE_TYPES) + len(RESONANCE_STATE_TYPES),
    }


@app.get("/state")
def get_state(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone (e.g., America/Los_Angeles)"),
    dt: Optional[str] = Query(None, description="ISO datetime (default: now)"),
):
    """
    Complete Astrolabium state for a moment in time.

    Returns all temporal layers: solar, organ clock, derivative
    (Extraordinary Vessel layer), primeval (lunar), solar keys,
    divine hour, stem-branch, compounds, and resonances.

    This is the documented raw endpoint. For practitioner-facing output,
    use /display (the Output Law surface).
    """
    target = _resolve_datetime(dt, tz)
    state = calculate_complete_state(target, lat, lon, tz)
    return state


@app.get("/display")
def get_display(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone (e.g., America/Los_Angeles)"),
    dt: Optional[str] = Query(None, description="ISO datetime (default: now)"),
    precision: str = Query(
        "coarse",
        description="'coarse' (default: clock times to five minutes, hour "
                    "position as a phrase) or 'exact' (minute-exact, opt-in).",
    ),
):
    """
    THE OUTPUT LAW surface (AUDIT B-05, 2026-07-30).

    Returns the practitioner-facing answer in the Output Law shape:

      readout     — the correspondence-forward text block, rendered
                    verbatim by any client (data first, fixed order,
                    one fact per line, absent data as em dash)
      typed_state — the KEY = value machine core; quote values from
                    here, never re-narrate them from prose
      story_gate  — whether interpretation is licensed for this moment,
                    about which subjects, and under what rule
      display     — prose-free structured state in Damanhurian-first
                    vocabulary (per C-05), for structured panels

    `precision` mirrors the CLI: COARSE is the default because the Divine
    Hour, not the clock, is the operative unit. Pass 'exact' only when the
    minute is genuinely load-bearing.
    """
    if precision not in (COARSE, EXACT):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid precision: {precision!r}. Use 'coarse' or 'exact'.",
        )
    target = _resolve_datetime(dt, tz)
    state = calculate_complete_state(target, lat, lon, tz)
    return {
        "readout": readout(state, precision=precision),
        "typed_state": typed_state(state),
        "story_gate": story_gate(state),
        "display": present_state(state),
    }


@app.get("/projection")
def get_projection(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone"),
    start: str = Query(..., description="ISO start datetime"),
    end: str = Query(..., description="ISO end datetime"),
    interval: int = Query(60, gt=0, description="Interval in minutes"),
):
    """
    Time series of complete states.

    Iterates from start to end at the given interval, producing
    a complete state at each step. Capped at 10,000 steps.
    """
    start_dt = _parse_datetime(start, "start")
    end_dt = _parse_datetime(end, "end")

    if end_dt <= start_dt:
        raise HTTPException(status_code=422, detail="'end' must be after 'start'.")

    total_minutes = (end_dt - start_dt).total_seconds() / 60
    step_count = int(total_minutes / interval) + 1
    if step_count > MAX_PROJECTION_STEPS:
        raise HTTPException(
            status_code=422,
            detail=f"Projection would require {step_count} steps (max {MAX_PROJECTION_STEPS}). "
                   f"Increase interval or narrow the time range.",
        )

    delta = timedelta(minutes=interval)
    states = []
    current = start_dt
    while current <= end_dt:
        state = calculate_complete_state(current, lat, lon, tz)
        states.append(state)
        current += delta

    return {
        "count": len(states),
        "interval_minutes": interval,
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
        "states": states,
    }


@app.get("/next-unity")
def get_next_unity(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone"),
    dt: Optional[str] = Query(None, description="ISO datetime (default: now)"),
    max_hours: int = Query(168, gt=0, le=MAX_SEARCH_HOURS, description="Max search window in hours"),
):
    """
    Find the next Two-Body Unity window.

    Scans forward in 30-minute increments until P == D.
    """
    start = _resolve_datetime(dt, tz)

    step = timedelta(minutes=30)
    current = start
    limit = start + timedelta(hours=max_hours)

    while current < limit:
        state = calculate_complete_state(current, lat, lon, tz)
        if state["compounds"]["two_body_unity"]:
            return {
                "found": True,
                "timestamp": current.isoformat(),
                "law": state["primeval"]["law"],
                "vessel": state["derivative"]["vessel"],
                "phase": state["primeval"]["phase"],
                "hours_from_now": round((current - start).total_seconds() / 3600, 2),
            }
        current += step

    return {
        "found": False,
        "searched_hours": max_hours,
        "message": f"No Two-Body Unity found within {max_hours} hours",
    }


@app.get("/frequency")
def get_frequency(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone"),
    start: str = Query(..., description="ISO start datetime"),
    end: str = Query(..., description="ISO end datetime"),
    interval: int = Query(30, gt=0, description="Sampling interval in minutes"),
):
    """
    Compound and resonance frequency analysis over a time range.

    Returns counts, percentages, per-Law breakdowns, and distribution
    statistics for all compound types, resonance types, and temporal layers.
    """
    start_dt = _parse_datetime(start, "start")
    end_dt = _parse_datetime(end, "end")

    if end_dt <= start_dt:
        raise HTTPException(status_code=422, detail="'end' must be after 'start'.")

    total_minutes = (end_dt - start_dt).total_seconds() / 60
    step_count = int(total_minutes / interval) + 1
    if step_count > MAX_PROJECTION_STEPS:
        raise HTTPException(
            status_code=422,
            detail=f"Scan would require {step_count} steps (max {MAX_PROJECTION_STEPS}). "
                   f"Increase interval or narrow the time range.",
        )

    return scan_compounds(start_dt, end_dt, lat, lon, tz, interval)


@app.get("/windows")
def get_windows(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone"),
    start: str = Query(..., description="ISO start datetime"),
    end: str = Query(..., description="ISO end datetime"),
    compound: str = Query("two_body_unity", description="Compound or resonance type"),
    interval: int = Query(15, gt=0, description="Sampling interval in minutes"),
):
    """
    Find all contiguous windows where a compound or resonance is active.

    Returns the start, end, duration, and Law for each window.
    Accepts both structural compound types and boolean resonance types.
    """
    _validate_compound(compound)
    start_dt = _parse_datetime(start, "start")
    end_dt = _parse_datetime(end, "end")

    if end_dt <= start_dt:
        raise HTTPException(status_code=422, detail="'end' must be after 'start'.")

    result = find_windows(start_dt, end_dt, lat, lon, tz, compound, interval)
    return {
        "compound": compound,
        "is_resonance": compound in RESONANCE_BOOLEAN_TYPES,
        "window_count": len(result),
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
        "windows": result,
    }


@app.get("/next-compound")
def get_next_compound(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    tz: str = Query(..., description="Timezone"),
    compound: str = Query("two_body_unity", description="Compound or resonance type"),
    dt: Optional[str] = Query(None, description="ISO datetime (default: now)"),
    max_hours: int = Query(168, gt=0, le=MAX_SEARCH_HOURS, description="Max search window in hours"),
):
    """
    Find the next occurrence of any compound or resonance type.

    Generalized version of /next-unity. Supports all compound and resonance types.
    """
    _validate_compound(compound)
    start = _resolve_datetime(dt, tz)
    return next_compound(start, lat, lon, tz, compound, max_hours)


@app.get("/resonance-coverage")
def get_resonance_coverage():
    """
    Diagnostic endpoint: lists all tracked compound and resonance types.

    Returns the full inventory of what the system can detect and search for.
    """
    return {
        "compound_types": COMPOUND_TYPES,
        "resonance_boolean_types": RESONANCE_BOOLEAN_TYPES,
        "resonance_state_types": RESONANCE_STATE_TYPES,
        "all_searchable": ALL_SEARCHABLE_TYPES,
        "total_compounds": len(COMPOUND_TYPES),
        "total_resonance_boolean": len(RESONANCE_BOOLEAN_TYPES),
        "total_resonance_state": len(RESONANCE_STATE_TYPES),
        "total_trackable": len(COMPOUND_TYPES) + len(ALL_RESONANCE_TYPES),
    }
