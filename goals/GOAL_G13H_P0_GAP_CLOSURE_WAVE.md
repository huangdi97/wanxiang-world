# G13H — P0 Gap Closure Wave

> Milestone: M10
> Depends on: G13G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Close every internally actionable P0 gap found by G13A-G13G before any adversarial or reference-world expansion.

## Scope

- Fix canonical mutation bypass, data-loss/replay corruption, branch contamination, security/rights critical bypass, migration data loss, fake production truth, critical crash inconsistency and build/test blockers.
- Add regression tests before/with fixes.
- Update traceability statuses only after evidence exists.

## Non-goals

- Do not defer P0 to later milestones.
- Do not use EXTERNAL_BLOCKED for internal engineering defects.
- Do not perform unrelated feature expansion.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- A failing P0 acceptance blocks the program from M11.

## Deliverables

- reports/P0_GAP_BACKLOG.md
- reports/P0_CLOSURE_REPORT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create reports/P0_GAP_BACKLOG.md with IDs, owners, root cause and closure evidence.
- Fix in small reviewable commits/checkpoints.
- Run affected regression plus full core invariant suite after each cluster.
- Update ADRs when architecture behavior changes.
- Re-run security/replay/migration checks touched by fixes.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Each fixed P0 has a regression test reproducing the original failure when practical.
- Full M1-M9 critical regression remains green after closure.
- No P0 status remains OPEN.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- P0 open count = 0.
- No fix introduces a canonical bypass or compatibility regression.
- Traceability and acceptance matrix point to post-fix evidence.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13h: p0 gap closure wave`.
- Record final commit SHA in `reports/G13H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
