# G20E — Final Release Readiness, Version Freeze & Post-v5 Roadmap

> Milestone: M17
> Depends on: G20D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Produce the final certification bundle, freeze the current stable version, distinguish external blockers/experimental tracks, and leave the repository ready for controlled release or the next design cycle.

## Scope

- Final acceptance matrix, architecture conformance, migration/replay compatibility, security/rights, performance/capacity, long-run stability, reference-world status, SDK/ecosystem, product surfaces and research decisions.
- Version/tag proposal and release notes; no automatic remote push/deploy.

## Non-goals

- Do not claim unresolved EXTERNAL_BLOCKED real data as completed.
- Do not auto-push/tag/deploy without user authorization.
- Do not invent G21 work inside this Goal.

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
- reports produced by preceding Goals in M17

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Completion means proven stable scope, not every imaginable future feature.

## Deliverables

- reports/M17_FINAL_CERTIFICATION.md
- reports/FINAL_PROGRAM_COMPLETION_REPORT.md
- docs/RELEASE_READINESS.md
- docs/POST_V5_ROADMAP.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G20E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Run final full suite.
- Generate FINAL_PROGRAM_COMPLETION_REPORT and RELEASE_READINESS.
- List exact tested environments and known limitations.
- List M16 PROMOTE/KEEP/REJECT decisions as v5.1/v6 roadmap.
- Ensure STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG are current.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Stable P0/P1 gap count = 0.
- All final reports internally consistent.
- Release candidate can be reproduced from local Git checkpoint.
- External blockers and experimental items are explicit.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M17 PASS; Post-M9 Program complete.
- Repository stops after local checkpoint and awaits user review.
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
- After acceptance passes, create a local checkpoint commit such as: `g20e: final release readiness, version freeze & post-v5 roadmap`.
- Record final commit SHA in `reports/G20E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
