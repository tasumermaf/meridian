# Sprint Status — Meridian / Astrolabium

> **Purpose:** Single canonical record of where the multi-sprint work
> stands. Updated at the end of every phase. If a session dies, the
> next session opens this file FIRST to pick up exactly where the
> previous left off.

---

## CURRENT SPRINT

**Sprint:** A — Stellar Layer
**Branch:** `feature/stellar-layer`
**Started:** May 18, 2026
**Status:** IN PROGRESS

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
| 1 | 28 Lunar Mansions engine + data + tests | ⏳ NEXT | — | — |
| 2 | 24 Solar Terms engine + data + tests | ⏳ pending | — | — |
| 3 | Cross-Tradition Sacred Festivals registry | ⏳ pending | — | — |
| 4 | Tibetan Buddhist calendar layer | ⏳ pending | — | — |
| 5 | Orchestrator integration | ⏳ pending | — | — |
| 6 | Rules files (5 new + 3 updates) | ⏳ pending | — | delegate to subagents |
| 7 | New visual assets (2 wheels) | ⏳ pending | — | — |
| 8 | README updates | ⏳ pending | — | — |
| 9 | Test suite + push to GitHub | ⏳ pending | — | — |

### Tests

- Baseline (main): **567 passing**
- Current (feature/stellar-layer): 567 passing (no changes yet)
- Target at Sprint A end: ~620-650 passing

### Decisions log

- (none yet — will record as they emerge)

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
