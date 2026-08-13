# G13D — Placeholder, Fake, Dead-path & Surface Integration Audit

> Milestone: M10
> Depends on: G13C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Find false completion: placeholders, mock-only paths, static responses, unconnected UI, dead adapters, duplicated schemas and code that exists but is not reachable in a real vertical slice.

## Scope

- Scan production code, routes, frontend data sources, adapters, sample worlds and generated SDKs.
- Differentiate legitimate deterministic Fake adapters in tests from fake production behavior.
- Verify Studio/Phaser/Host/API paths consume real server state and submit real commands where design says they should.
- Identify dead code and duplicate or drifting models.

## Non-goals

- Do not delete test Fakes that implement a formal Port contract.
- Do not demand real external services where the spec allows a Fake for deterministic qualification.

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
- Prefer removal of unused speculative abstractions over preserving dead complexity.

## Deliverables

- reports/FALSE_COMPLETION_AUDIT.md
- reports/SURFACE_INTEGRATION_MAP.md
- reports/SCHEMA_DRIFT_AUDIT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create automated placeholder/dead-code scanning rules with allowlisted documented exceptions.
- Trace UI API calls to server handlers/use cases and back to canonical projections.
- Inspect hardcoded JSON/static world state and ensure it is fixture content, not production truth.
- Compare Python/OpenAPI/TypeScript schemas for drift.
- Classify dead adapters as remove, wire, or explicitly experimental.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- E2E smoke test must fail if frontend is switched to canned data.
- Schema generation drift test must detect manually edited generated clients.
- Production placeholder scanner has zero unexplained high-confidence findings.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No P0/P1 feature is “complete” only through static/mock behavior.
- All disconnected production paths are placed in gap backlog.
- Test fakes are clearly namespaced and never selected by production default configuration.
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
- After acceptance passes, create a local checkpoint commit such as: `g13d: placeholder, fake, dead-path & surface integration audit`.
- Record final commit SHA in `reports/G13D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
