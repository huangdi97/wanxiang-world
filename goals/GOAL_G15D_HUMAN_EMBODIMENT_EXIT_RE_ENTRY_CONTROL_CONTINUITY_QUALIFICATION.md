# G15D — Human Embodiment, Exit, Re-entry & Control Continuity Qualification

> Milestone: M12
> Depends on: G15C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove a human can take over a character/body, leave, and later return while the world and shadow/autonomous policy continue coherently.

## Scope

- EmbodimentLease acquisition/release/expiry, first-person perception, human command validation, shadow policy resumption and session reconnection.
- Test conflicting takeover attempts.

## Non-goals

- Do not let user control bypass actor capabilities, physical constraints or Commit Authority.
- Do not freeze the entire world when one user exits.

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
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Session is ephemeral; world instance/branch persists independently.

## Deliverables

- reports/EMBODIMENT_CONTINUITY_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create scenario: user takes role on day 1, exits day 3, world advances, re-enters later.
- Verify role continuity, memory/knowledge boundary and body state.
- Test lease race/expiry and reconnect.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- World advances after user exit.
- Re-entry receives authoritative current perspective.
- No duplicate controller according to policy.
- Human actions remain normal committed actions.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Control continuity worldness criterion PASS.
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
- After acceptance passes, create a local checkpoint commit such as: `g15d: human embodiment, exit, re-entry & control continuity qualification`.
- Record final commit SHA in `reports/G15D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
