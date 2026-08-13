# G13E — Event, Replay, Branch, Migration & Version Forensics

> Milestone: M10
> Depends on: G13D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Re-verify the semantic-history foundation under all features added after M1 and detect any event/version/migration behavior that could silently corrupt historical worlds.

## Scope

- Audit event schemas and evolution, snapshot schemas, package versions, DB migrations, replay upcasters if any, branch ancestry and deterministic semantic hashes.
- Replay representative M2-M9 world histories from clean state.
- Verify old instance/package version pinning does not silently adopt new semantics.
- Audit correction-event and immutable-history policy.

## Non-goals

- Do not rewrite historical fixtures to make new runtime tests pass without recording an intentional migration/upcast.
- Do not treat current-state database rows as authoritative history.

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
- Historical truth is corrected with new events/branches or explicit migration semantics, never silent mutation.

## Deliverables

- reports/HISTORY_COMPATIBILITY_FORENSICS.md
- reports/REPLAY_GOLDEN_CORPUS.md
- reports/VERSION_COMPATIBILITY_MATRIX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Collect persisted event versions and compare to runtime handlers.
- Build a compatibility matrix: old events/snapshots/packages/DB → current runtime.
- Replay parent/child branches and verify ancestry/isolation.
- Run migration forward, restore backup, and where supported downgrade/rollback policy tests.
- Detect silent defaulting of unknown/new fields that changes semantic meaning.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Golden replay corpus produces stable semantic hashes.
- Unsupported event version fails explicitly.
- Version-pinned instance behavior test protects against package upgrade drift.
- Migration on representative old DB fixtures preserves event/replay invariants.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No unresolved P0 replay or migration corruption risk.
- All supported/unsupported compatibility ranges are documented.
- Every schema change mechanism has an explicit owner and test.
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
- After acceptance passes, create a local checkpoint commit such as: `g13e: event, replay, branch, migration & version forensics`.
- Record final commit SHA in `reports/G13E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
