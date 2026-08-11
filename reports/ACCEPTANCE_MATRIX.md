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

## M1 ? Authoritative World Exists (from 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md ?4)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| A1 | Acceptance ?4 | GOAL_01F | valid commit changes canonical state exactly once | PENDING | ? | |
| A2 | Acceptance ?4 | GOAL_01F | invalid command does not mutate state | PENDING | ? | |
| A3 | Acceptance ?4 | GOAL_01F | duplicate command idempotency | PENDING | ? | |
| A4 | Acceptance ?4 | GOAL_01F | stale revision structured rejection | PENDING | ? | |
| A5 | Acceptance ?4 | GOAL_01F | snapshot + remaining replay equal semantic hash | PENDING | ? | |
| A6 | Acceptance ?4 | GOAL_01F | full replay from initial baseline | PENDING | ? | |
| A7 | Acceptance ?4 | GOAL_01F | branch isolation (child does not mutate parent) | PENDING | ? | |
| A8 | Acceptance ?4 | GOAL_01F | deterministic seed/version reproducibility | PENDING | ? | |
| A9 | Acceptance ?4 | GOAL_01F | corrupt stream fails explicitly | PENDING | ? | |
| A10 | Acceptance ?4 | GOAL_01F | migration compatibility with prior fixture | PENDING | ? | |

## Architecture gates (02_ENGINEERING_STANDARDS.md ?16)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| ARCH-01 | Standards ?16 | GOAL_00B | domain -> fastapi/sqlalchemy/alembic detected | PASS | 3410300 | negative tests |
| ARCH-02 | Standards ?16 | GOAL_00B | runtime -> apps.api detected | PASS | 3410300 | |
| ARCH-03 | Standards ?16 | GOAL_00B | plugin/model provider -> persistence internals detected | PASS | 3410300 | |
| ARCH-04 | Standards ?16 | GOAL_00B | import cycles detected | PASS | 3410300 | |
