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

## M3 ? Bounded Agents Can Live Inside the World (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M3-01 | M3 gate | GOAL_03A | Observation/perspective isolation: derived read-model, sealed payload, private/group visibility | PASS | 7238461 | |
| M3-02 | M3 gate | GOAL_03B | Belief/memory/epistemic graph: corrections, contradictions, forgetting, actor-scoped access | PASS | 00419ef | |
| M3-03 | M3 gate | GOAL_03C | Actor/org runtime: propose-only policies, order lifecycle, typed transitions | PASS | c7790ff | |
| M3-04 | M3 gate | GOAL_03D | Action/affordance/validator: versioned registry, side-effect-free validation | PASS | b126b7d | |
| M3-05 | M3 gate | GOAL_03E | Resolver/adjudication: deterministic policies, seeded RNG, provenance | PASS | edadaf3 | |
| M3-06 | M3 gate | GOAL_03F | Skill runtime: step expansion through authoritative path, permission gate, failure handling | PASS | 6006fd2 | |
| M3-07 | M3 gate | GOAL_03G | Capability & learning: bounded evidence-backed capability change; skill prerequisites | PASS | goal g03g | |
M3 verdict: PASS (2026-08-13, tag m3-bounded-agents; reports/M3_ACCEPTANCE.md).
M4 verdict: PASS (2026-08-13, tag m4-worlds-authored-installed; reports/M4_ACCEPTANCE.md).
M5 verdict: PASS (2026-08-13, tag m5-human-in-world-without-authority; reports/M5_ACCEPTANCE.md).

## M4 ? Worlds Can Be Authored, Reviewed, Installed and Instantiated (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M4-01 | M4 gate | GOAL_04A | Package/schema/dependency registry: deterministic resolution, cycles/conflicts, content hash, trust, migration | PASS | goal g04a | |
| M4-02 | M4 gate | GOAL_04B | Source registry & gate: immutable sources, rights/stage eligibility, injection default-deny, conflicting claims | PASS | goal g04b | |
| M4-03 | M4 gate | GOAL_04C | Structured compiler: safe readers, deterministic candidates with provenance, PDF/OCR/video unsupported | PASS | goal g04c | |
| M4-04 | M4 gate | GOAL_04D | Completion ledger: truth labels, immutable review, canon lock + override, rights gate, diffs | PASS | goal g04d | |
| M4-05 | M4 gate | GOAL_04E | Install/export/migration: transactional install, exact pins, export roundtrip, v2 does not mutate v1 | PASS | goal g04e | |
| M4-06 | M4 gate | GOAL_04A-E | M4 vertical: author->review->install->instantiate synthetic package end-to-end | PASS | goal g04e | test_m4_qualification |

## M5 ? Human Can Enter a Persistent World Without Becoming the Authority (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M5-01 | M5 gate | GOAL_05A | WorldHost orchestration boundary; lifecycle modes; not a commit authority | PASS | goal g05a | |
| M5-02 | M5 gate | GOAL_05B | One primary embodiment controller per actor; lease lifecycle | PASS | goal g05b | |
| M5-03 | M5 gate | GOAL_05C | Shadow cannot commit; handoff resumes deterministic controller | PASS | goal g05c | |
| M5-04 | M5 gate | GOAL_05D | Projection server-side rights/knowledge filters; debug privilege | PASS | goal g05d | |
| M5-05 | M5 gate | GOAL_05E | Studio TS slice consumes projections; bounded commands | PASS | goal g05e | React render EXTERNAL_BLOCKED |
| M5-06 | M5 gate | GOAL_05F | Phaser TS slice map/tokens/movement via projection API | PASS | goal g05f | Phaser render EXTERNAL_BLOCKED |
| M5-07 | M5 gate | GOAL_05A-F | M5 vertical: lease->takeover->commit->release->disconnect->restart->reconnect hash continuity | PASS | m5 commit | test_m5_qualification |
## Architecture gates (02_ENGINEERING_STANDARDS.md ?16)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| ARCH-01 | Standards ?16 | GOAL_00B | domain -> fastapi/sqlalchemy/alembic detected | PASS | 3410300 | negative tests |
| ARCH-02 | Standards ?16 | GOAL_00B | runtime -> apps.api detected | PASS | 3410300 | |
| ARCH-03 | Standards ?16 | GOAL_00B | plugin/model provider -> persistence internals detected | PASS | 3410300 | |
| ARCH-04 | Standards ?16 | GOAL_00B | import cycles detected | PASS | 3410300 | |
| ARCH-05 | Standards ?16 | GOAL_00B | substrate package guard (fastapi/sqlalchemy/persistence) | PASS | 8c0c7cf | |
