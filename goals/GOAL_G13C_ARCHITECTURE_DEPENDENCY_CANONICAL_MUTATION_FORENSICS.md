# G13C — Architecture, Dependency & Canonical-Mutation Forensics

> Milestone: M10
> Depends on: G13B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Independently prove that the implemented repository still obeys the architecture boundaries after M0-M9 growth, especially the single Commit Authority and dependency direction.

## Scope

- Trace every production write path that can affect world state.
- Audit imports/dependencies between domain/application/runtime/persistence/API/projection/plugin/model-provider packages.
- Detect direct ORM/DB access from forbidden layers, route business logic, mutable global state and hidden side effects.
- Audit package/domain plugin extension points for accidental privileged mutation.

## Non-goals

- Do not rely only on existing architecture tests; inspect source graph and runtime call graph where feasible.
- Do not refactor unrelated style issues in this audit-only Goal.

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
- Never “solve” an architecture test by weakening the test or adding allowlists without ADR evidence.

## Deliverables

- reports/ARCHITECTURE_FORENSICS.md
- reports/DEPENDENCY_GRAPH.md
- reports/CANONICAL_MUTATION_PATHS.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Generate an import/dependency graph and forbidden-edge report.
- Search for direct repository/session usage outside approved adapters/use-cases.
- Instrument or test commit entry points to prove canonical mutations have one authority path.
- Audit projections, simulators, Reality Bridge, Director, LLM/model providers and clients for mutation bypasses.
- Record cycle, ownership and privilege findings.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Architecture tests intentionally introduce representative forbidden imports in test fixtures and must detect them.
- Mutation-bypass tests attempt direct state writes from projection/model/plugin paths and must fail.
- Import-cycle detector runs on production packages.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No unapproved canonical mutation path exists.
- Any architecture violation becomes P0 or P1 gap with owner and fix target.
- The report distinguishes logical kernel boundaries from physical package layout.
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
- After acceptance passes, create a local checkpoint commit such as: `g13c: architecture, dependency & canonical-mutation forensics`.
- Record final commit SHA in `reports/G13C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
