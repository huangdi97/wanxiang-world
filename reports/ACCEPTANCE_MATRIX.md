# Acceptance Matrix ? Wanxiang Engineering Program

Maintained throughout the program. Status: PASS | FAIL | EXTERNAL_BLOCKED | PENDING.
Columns: Requirement ID | Source section | Owning Goal | Test/evidence | Current status | Last verified commit | Notes.

## M0 ? Reproducible Engineering Base

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M0-01 | EPA ?19 | GOAL_00A | Fresh bootstrap documented in `docs/runbook/DEVELOPMENT.md`; uv/pnpm installs executed | PASS | 9134801 | |
| M0-02 | EPA ?19 | GOAL_00A | Python toolchain reproducible (`uv sync --all-groups --all-packages`) | PASS | 9134801 | |
| M0-03 | EPA ?19 | GOAL_00A | tests/lint/typecheck pipelines work (ruff, pyright, pytest, pnpm suite) | PASS | 9134801 | |
| M0-04 | EPA ?19 | GOAL_00B | Architecture import guards fail on a fixture violation (negative tests) | PASS | 3410300 | |
| M0-05 | EPA ?19 | GOAL_00A | Ledgers/ADRs/evidence format exist | PASS | 9134801 | |

## M1 ? Authoritative World Exists (03_ACCEPTANCE_TESTING_AND_EVIDENCE.md ?4)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| A1 | Acceptance ?4 | GOAL_01F | valid commit changes canonical state exactly once | PASS | c45b64e | test_a1 |
| A2 | Acceptance ?4 | GOAL_01F | invalid command does not mutate state | PASS | c45b64e | test_a2 |
| A3 | Acceptance ?4 | GOAL_01F | duplicate command idempotency | PASS | c45b64e | test_a3 |
| A4 | Acceptance ?4 | GOAL_01F | stale revision structured rejection | PASS | c45b64e | test_a4 |
| A5 | Acceptance ?4 | GOAL_01F | snapshot + remaining replay equal semantic hash | PASS | c45b64e | test_a5 |
| A6 | Acceptance ?4 | GOAL_01F | full replay from initial baseline | PASS | c45b64e | test_a6 |
| A7 | Acceptance ?4 | GOAL_01F | branch isolation (child does not mutate parent) | PASS | c45b64e | test_a7 |
| A8 | Acceptance ?4 | GOAL_01F | deterministic seed/version reproducibility | PASS | c45b64e | test_a8 |
| A9 | Acceptance ?4 | GOAL_01F | corrupt stream fails explicitly | PASS | c45b64e | test_a9 |
| A10 | Acceptance ?4 | GOAL_01F | migration compatibility with prior fixture | PASS | c45b64e | test_a10 + tests/migration |

## M2 ? Deterministic Living World Exists (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M2-01 | M2 gate | GOAL_02A | Spatial topology/access: reachability, capacity, occupancy, zones | PASS | 8c0c7cf | |
| M2-02 | M2 gate | GOAL_02B | Temporal: monotonic clock, schedules, recurrence, deadlines | PASS | 38acada | |
| M2-03 | M2 gate | GOAL_02C | Material: custody != ownership; custody != knowledge; containers | PASS | 250dd0b | |
| M2-04 | M2 gate | GOAL_02D | Body/condition constrains actions | PASS | 84568a4 | |
| M2-05 | M2 gate | GOAL_02E | Institution roles/duties/permissions affect actions | PASS | 3472a69 | |
| M2-06 | M2 gate | GOAL_02F | Autonomous multi-rate scheduler, deterministic, bounded | PASS | aa2f99f | |
| M2-07 | M2 gate | GOAL_02A-F | 72h integrated living-world scenario | PASS | (m2 commit) | test_m2_qualification |

## Architecture gates (02_ENGINEERING_STANDARDS.md ?16)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| ARCH-01 | Standards ?16 | GOAL_00B | domain -> fastapi/sqlalchemy/alembic detected | PASS | 3410300 | negative tests |
| ARCH-02 | Standards ?16 | GOAL_00B | runtime -> apps.api detected | PASS | 3410300 | |
| ARCH-03 | Standards ?16 | GOAL_00B | plugin/model provider -> persistence internals detected | PASS | 3410300 | |
| ARCH-04 | Standards ?16 | GOAL_00B | import cycles detected | PASS | 3410300 | |
| ARCH-05 | Standards ?16 | GOAL_00B | substrate package guard (fastapi/sqlalchemy/persistence) | PASS | 8c0c7cf | |
