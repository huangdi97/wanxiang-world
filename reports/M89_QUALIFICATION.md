# M89 — Long-Horizon Runtime + SimulationLOD Qualification

Date: 2026-08-26  
Status: PASS

## Goal closure

| Goal | Result | Evidence |
|---|---|---|
| G92A | PASS | Deterministic recurring scheduler, availability and catch-up over SQLite temporal commits |
| G92B | PASS | RuntimeProfile-bound detached/background modes and session cursor continuity |
| G92C | PASS | Atomic cursor checkpoint, crash injection, resume and duplicate-safe runtime retry |
| G92D | PASS | Reference-only compaction with archive/memory refs and golden replay equality |
| G92E | PASS | L0-L4 scoring/transition, cohort projection and state/memory-ref continuity |
| G92F | PASS | World/actor/provider budget admission, alerts, backpressure and no partial charge |
| G92G | PASS | Real SQLite accelerated 24h and 7d multi-actor qualification |
| G92H | PASS | Same source-created literary package, real SQLite accelerated 30d qualification |

## Long-horizon qualification

`G92H` is the milestone's strongest product-chain evidence. A private,
rights-approved source was passed through `OneClickAuthoring`, registered as a
`PlayableWorldProfile`, entered through `PlayableService`, and then run on the
existing SQLite `WorldRuntime`. The detached scheduler emitted 60 actor
occurrences across 30 exact synthetic days. All canonical clock, actor status,
and actor-local observation effects were committed by the existing Commit
Authority path.

The 30d evidence contains 155 committed events, 30 successful runtime/run
checkpoints, two source actors, 30 actor-local memories per actor, 12
reference-only memory-summary refs, and serialized state storage growth from
1,832 to 31,968 bytes. The 24h, 7d, and 30d samples all reached their exact
target ticks and had equal full replay and restart-recovery semantic hashes.
The injected publication crash left no checkpoint, and a fresh SQLite runtime
restored the final hash. LOD evidence observed L0/L3/L4; world budget usage
recorded 150 calls and 30,136 charged storage bytes.

The source payload remains a local test fixture and is not present in the
repository or public evidence. Scheduler, background policy, LOD, budget, and
compaction components remain proposal/reference boundaries; none owns a second
canonical state, event store, branch system, or Commit Authority.

## Milestone gates

| Gate | Result | Evidence |
|---|---|---|
| 21 24h smoke | ACCEPTED | G92G real SQLite run |
| 22 7d runtime | ACCEPTED | G92G real SQLite multi-actor run |
| 23 30d literary run | ACCEPTED | G92H source-created literary run |
| 24 90d selected-world run | PENDING | M90/M94 scope; not claimed by M89 |
| 25 checkpoint/resume/crash recovery | ACCEPTED | G92H 30 checkpoints, cursor restore, restart hash, atomic crash probe |
| 26 compaction replay equality | ACCEPTED | G92H 155-event reference compaction and equal golden hash |
| 27 LOD transition continuity | ACCEPTED | G92H state/memory refs across L0/L3/L4 |
| 28 cost/storage/memory quantification | ACCEPTED | G92H measured state bytes, memory counts and budget ledger |

## Required quality and architecture evidence

- Full Python regression: `1322 passed, 1 skipped, 2 warnings` in 326.08s;
  the only skip is the documented PostgreSQL profile with no
  `WANXIANG_POSTGRES_TEST_URL`.
- G92A-G92H focused regression: 26 passed, 1 existing Hypothesis warning.
- Ruff check and format check: PASS.
- Full Pyright: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `scripts/duplicate_abstraction_scan.py`: PASS; `unallowed=[]`.
- Architecture forensics: forbidden imports 0, persistence leakage 0, direct
  persistence appends 0, import cycles 0; the existing single Commit Authority
  path remains the only canonical mutation boundary.
- Minimality snapshot: 502 production files / 53,287 LOC, 16 registries,
  25 services, 5 engines, 41 ports, 29 stores, 30 state/schema models,
  0 managers, 0 oversized modules, 0 import cycles, 1 commit path.
- SDK compatibility snapshot regenerated after the additive v5.5 long-horizon
  public surface; the SDK contract tests pass.

M89 is PASS. Gate 24 and all M90-M94/final release gates remain pending, so
v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No model training, private source
upload, v5.4 stable-tag mutation, or v5.6 work was performed.
