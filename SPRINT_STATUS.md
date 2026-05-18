# Sprint Status — Meridian / Astrolabium

> **Purpose:** Single canonical record of where the multi-sprint work
> stands. Updated at the end of every phase. If a session dies, the
> next session opens this file FIRST to pick up exactly where the
> previous left off.

---

## CURRENT SPRINT

**Sprint:** C — Ecological Layer
**Branch:** `feature/ecological-layer` (branched from `feature/deep-sky`)
**Started:** May 18, 2026
**Status:** IN PROGRESS

### Sprint A: COMPLETE — pushed
- https://github.com/tasumermaf/meridian/tree/feature/stellar-layer

### Sprint B: COMPLETE — pushed
- https://github.com/tasumermaf/meridian/tree/feature/deep-sky

### Sprint C confirmed design decision
- **Offline-first**: derive ecological markers from astronomy + climate norms.
  No network calls, no API keys. Preserves the Astrolabium's design ethos
  (offline-first throughout).
- Live-weather integration (Open-Meteo etc) deferred to a hypothetical
  Sprint D if/when network-dependence is acceptable.

### Sprint C phase tracker

| # | Phase | Status | Commit | Notes |
|---|-------|--------|--------|-------|
| 0 | Create feature branch | ✅ COMPLETE | (no commit) | branched from feature/deep-sky |
| 1 | Photoperiod state engine + tests | ⏳ NEXT | — | — |
| 2 | Climate-norm ecological markers + tests | ⏳ pending | — | — |
| 3 | Orchestrator integration | ⏳ pending | — | — |
| 4 | Rules files via subagents | ⏳ pending | — | — |
| 5 | Visual asset (local seasonal wheel) | ⏳ pending | — | — |
| 6 | README + final test + push | ⏳ pending | — | — |

Tests: starts at 703 baseline, target ~735-755.

### Sprint A: COMPLETE
- Branch: `feature/stellar-layer` (pushed to GitHub, awaiting merge to main)
- GitHub: https://github.com/tasumermaf/meridian/tree/feature/stellar-layer
- PR-ready: https://github.com/tasumermaf/meridian/pull/new/feature/stellar-layer
- 9 commits, 629 tests passing, 5 new rules files, 2 new visual assets
- Stellar Layer (28 mansions + 24 solar terms + festivals + Tibetan calendar) operational

### Sprint B confirmed parameters
- Branch strategy: branch off `feature/stellar-layer` (Sprint B depends on Sprint A's stellar engine)
- Scope: Tier 2 from the original plan — axial precession, heliacal risings, major lunar standstills, Vedic deep-time
- Save strategy: same as Sprint A — per-phase commits, subagent delegation for verbose rules files
- Sprint C (ecological) deferred to its own planning round

### Sprint B phase tracker

| # | Phase | Status | Commit | Notes |
|---|-------|--------|--------|-------|
| 0 | Create feature branch | ✅ COMPLETE | (no commit) | branched from feature/stellar-layer |
| 1 | Axial precession engine + data + tests | ✅ COMPLETE | 61801ca | 18 tests, 647 total. Pisces 80.7%, ~414yr to Aquarius. |
| 2 | Heliacal risings engine + star data + tests | ✅ COMPLETE | ba9857d | 15 tests, 662 total. 22-star catalog. Sirius @ Memphis = Aug 4. |
| 3 | Major lunar standstills engine + tests | ✅ COMPLETE | aaa4359 | 15 tests, 677 total. 18.6yr cycle. Next major 2043, minor 2034. |
| 4 | Vedic yuga/kalpa deep-time engine + tests | ✅ COMPLETE | b063ee3 | 17 tests, 694 total. Kali Yuga 1.187%, Kalpa 45.67%. |
| 5 | Orchestrator integration | ✅ COMPLETE | d730f0b | 9 tests, 703 total. 4 new state keys, full backward compat. |
| 6 | Rules files (4 new + updates) via subagents | ✅ COMPLETE | 7c54d30 | 1,665 lines via 4 parallel subagents + stellar-layer.md + CLAUDE.md updates. |
| 7 | New visual asset (precession wheel) | ✅ COMPLETE | 7c54d30 | precession-wheel.png with all 12 Ages, Pisces highlighted, Aries glyph at vernal equinox. |
| 8 | README updates | ✅ COMPLETE | c2e9825 | Deep Sky section, 7 inline images, 21-rules tree. |
| 9 | Final test pass + push | ✅ COMPLETE | (9 commits) | 703 passing. Pushed to origin/feature/deep-sky. PR-ready. |

Tests: starts at 629 (Sprint A baseline), target ~660-680.

### Confirmed plan parameters

- Branch strategy: feature branches off `tasumermaf/meridian`, three planned (A, B, C)
- Sidereal default: Chinese 28-mansion (canonical)
- Tibetan calendar variant: Phugpa (default); variants noted in rules, not in code
- All three sprints in scope across multiple sessions
- Save strategy: per-phase commits + this file + subagent delegation for verbose work

### Phase tracker

| # | Phase | Status | Commit | Notes |
|---|-------|--------|--------|-------|
| 0 | Create feature branch | ✅ COMPLETE | (no commit yet) | branch created locally |
| 1 | 28 Lunar Mansions engine + data + tests | ✅ COMPLETE | 70d360d | 18 tests, 585 total passing. Sidereal via Lahiri ayanamsa. |
| 2 | 24 Solar Terms engine + data + tests | ✅ COMPLETE | 225b92c | 16 tests, 601 total passing. Tropical. 4 cardinal terms tied to Damanhurian Great Rites. |
| 3 | Cross-Tradition Sacred Festivals registry | ✅ COMPLETE | 23a22e8 | 16 tests, 617 total. 32 festivals across 10 traditions. Saga Dawa active on live query. |
| 4 | Tibetan Buddhist calendar layer | ✅ COMPLETE | 216a1f7 | 4 tests, 621 total. get_tibetan_month(dt). Phugpa default. Live: May 18 = Month 4 Saga Dawa. |
| 5 | Orchestrator integration | ✅ COMPLETE | 5dbeb31 | 8 tests, 629 total. 4 new state keys. Backward-compat verified. Perf-optimized year search. |
| 6 | Rules files (5 new + 3 updates) | ✅ COMPLETE | e0c2b3f | 1,890 lines via 5 parallel subagents + 3 updates. Massive context savings. |
| 7 | New visual assets (2 wheels) | ✅ COMPLETE | e0c2b3f | 28-mansion + 24-solar-term wheels, live data for Damanhur 2026-05-18. |
| 8 | README updates | ✅ COMPLETE | 8fc1179 | Stellar Layer section, 6 inline images, numbers expanded, 17-rules tree. |
| 9 | Test suite + push to GitHub | ✅ COMPLETE | (8 commits) | 629 passing. Pushed to origin/feature/stellar-layer. PR-ready. |

### Tests

- Baseline (main): **567 passing**
- Current (feature/stellar-layer): **629 passing** (567 + 18 stellar + 16 solar terms + 20 festivals/tibetan + 8 orchestrator)
- Target at Sprint A end: ~620-650 passing

### Decisions log

- **Sidereal correction:** apply Lahiri ayanamsa (~24.2° at 2026) to tropical ephem
  longitudes before mansion lookup. Documented in `stellar.py` as `_lahiri_ayanamsa()`.
  This aligns modern astronomical computation with the classical sidereal mansion
  boundaries from the Han-through-Ming canon.

---

## REMAINING SPRINTS (PLANNED, NOT STARTED)

### Sprint B — Deep Sky
**Branch:** `feature/deep-sky` (not created yet; will branch from updated main after Sprint A merges)
**Scope:** Tier 2 — axial precession, heliacal risings, major lunar standstills, Vedic yuga/kalpa deep-time
**Estimated effort:** 8-12 hrs
**Status:** Waiting for Sprint A to merge to main

### Sprint C — Ecological Layer
**Branch:** `feature/ecological-layer` (not created yet)
**Scope:** Tier 3 — external environmental data ingestion (NOAA / NASA MODIS / phenology / migration)
**Estimated effort:** 20-40 hrs (data-source decisions deserve their own planning round first)
**Status:** Awaiting Sprint A + B completion before scoping; needs API/data-source choices

---

## RECOVERY PROTOCOL (if a session dies mid-work)

A new session resuming this work should:

1. Read this file (`SPRINT_STATUS.md`) — see current sprint, current phase, what's done, what's in flight
2. Read the sprint plan (`C:/Projects/meridian-sprint-plan.md`) — see the full proposal
3. `cd C:/Projects/meridian && git log --oneline feature/stellar-layer` — see committed phases
4. `git status` — see anything in flight not yet committed
5. Continue from the "Next on resumption" note in the in-flight phase
6. Update this file at the end of each completed phase

---

*Last updated: May 18, 2026, Phase 0 complete.*
