# G13B — Design-to-Implementation Traceability Matrix

> Milestone: M10
> Depends on: G13A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Build a clause-level traceability system from the v5.0-R1 mother specification and M0-M9 program contracts to production implementation, tests and runtime evidence.

## Scope

- Extract normative MUST/SHALL/不可/必须/only-authority style requirements from the design and engineering program.
- Map each requirement to owner package/module, public contract, tests, migration/version implications and runtime evidence.
- Classify each as VERIFIED, PARTIAL, GAP, EXTERNAL_BLOCKED or NOT_APPLICABLE with rationale.
- Include the 5 Planes/16 Kernels, hierarchy, one Commit Authority, Source Gate, Rights, Event/Replay/Branch, Host, Projection, CoSim and worldness criteria.

## Non-goals

- Do not mark a requirement VERIFIED solely because a class/interface exists.
- Do not use model knowledge to fill missing product requirements.
- Do not collapse multiple independent requirements into a vague single row.

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
- Traceability is an audit artifact, not a substitute for tests.

## Deliverables

- reports/DESIGN_IMPLEMENTATION_TRACEABILITY.md
- reports/design_implementation_traceability.json
- reports/KERNEL_COVERAGE_SUMMARY.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create a stable requirement ID scheme (e.g. WX-SPEC-...).
- Generate reports/DESIGN_IMPLEMENTATION_TRACEABILITY.md plus machine-readable JSON/CSV-like representation.
- Link requirements to exact test names and implementation symbols/paths.
- Flag orphan production features that have no design owner and design requirements with no implementation owner.
- Create a coverage summary by Kernel, cross-cutting concern and product surface.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Traceability parser/validator checks unique IDs and valid statuses.
- Every G00A-G12H claimed deliverable has at least one trace row or explicit supersession note.
- Every one of the 16 logical kernels has concrete implementation and test ownership or a GAP.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No P0 architecture requirement is left UNMAPPED.
- The matrix can drive deterministic gap extraction in G13H/G13I.
- External-data requirements remain distinctly EXTERNAL_BLOCKED and do not mask generic capability gaps.
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
- After acceptance passes, create a local checkpoint commit such as: `g13b: design-to-implementation traceability matrix`.
- Record final commit SHA in `reports/G13B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
