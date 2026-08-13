# G13A — Post-M9 Baseline Freeze & Independent Evidence Capture

> Milestone: M10
> Depends on: M9 qualified checkpoint
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Establish an independent, reproducible post-M9 audit baseline before any new fixes, so later claims can be compared against immutable repository and runtime evidence.

## Scope

- Capture Git branch/HEAD/worktree, dependency lock state, schema/migration heads, generated OpenAPI/SDK state, test inventory and deployment manifests.
- Run all currently advertised M9 qualification commands without editing production code first.
- Inventory every report that claims PASS and map it to concrete tests, commands and artifacts.
- Create machine-readable audit baseline with hashes for key specs, schemas, migrations and generated contracts.

## Non-goals

- Do not fix defects during the first evidence pass except if a command cannot run because the audit harness itself is missing.
- Do not reinterpret missing evidence as PASS.
- Do not delete or rewrite prior M0-M9 reports.

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
- This Goal is read-mostly: preserve the baseline so later closure work can be compared against it.

## Deliverables

- reports/POST_M9_BASELINE.md
- reports/post_m9_baseline.json
- reports/POST_M9_COMMAND_MATRIX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create reports/POST_M9_BASELINE.md and reports/post_m9_baseline.json.
- Record exact command lines, exit codes and summarized outputs.
- Record test collection counts and skipped/xfail tests with reasons.
- Record all TODO/FIXME/NotImplemented/pass/placeholder/static-fake signals without yet classifying severity.
- Record current DB migration head and perform a disposable clean bootstrap.
- Record current API schema hash and SDK generation hash if applicable.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Baseline command rerun must be reproducible from a clean shell.
- A clean checkout/bootstrap smoke test must either PASS or produce a concrete blocker.
- No prior PASS may be accepted without an evidence pointer.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- POST_M9_BASELINE has repository SHA, environment assumptions, command matrix and evidence locations.
- All missing/ambiguous evidence is marked GAP_CANDIDATE rather than silently accepted.
- Baseline is committed before gap fixes begin.
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
- After acceptance passes, create a local checkpoint commit such as: `g13a: post-m9 baseline freeze & independent evidence capture`.
- Record final commit SHA in `reports/G13A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
