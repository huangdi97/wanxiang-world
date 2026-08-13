# G13G — Maintainability, Complexity, Test Quality & Upgradeability Audit

> Milestone: M10
> Depends on: G13F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Measure whether the codebase remains readable, modifiable and upgradeable rather than merely functional after broad implementation.

## Scope

- Audit file/function/class size, cyclomatic complexity, duplication, unstable dependency direction, generic utils/managers/services, test brittleness, fixture coupling and generated-code boundaries.
- Audit Python/JS dependency freshness constraints without forcing risky upgrades.
- Review public typing and error model consistency.
- Identify refactoring hotspots before product/reference-world growth.

## Non-goals

- Do not upgrade every dependency simply because a newer version exists.
- Do not split coherent code mechanically just to satisfy line counts.

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
- Prefer explicit small domain concepts to generic abstractions with broad responsibility.

## Deliverables

- reports/MAINTAINABILITY_AUDIT.md
- reports/UPGRADEABILITY_AUDIT.md
- reports/TEST_QUALITY_AUDIT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Produce complexity/size/duplication/import-cycle reports.
- List files over the engineering threshold and classify justified vs refactor-needed.
- Find broad Any/untyped public APIs and exception swallowing.
- Detect tests that only assert implementation details rather than behavior.
- Create upgrade seams report for DB, API, event schema, package SDK and projections.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Quality tooling runs in CI or a documented local gate.
- Representative architecture/behavior tests survive safe refactor of internals.
- No unexplained God Object or giant generic module remains P0/P1.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- P0/P1 maintainability risks are converted to concrete closure tasks.
- Code-quality exceptions have owner, rationale and expiry/review trigger.
- No “rewrite later” hotspot is left untracked.
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
- After acceptance passes, create a local checkpoint commit such as: `g13g: maintainability, complexity, test quality & upgradeability audit`.
- Record final commit SHA in `reports/G13G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
