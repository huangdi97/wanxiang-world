# G14G — Authorization, Rights, Privacy & Data-leak Adversarial Qualification

> Milestone: M11
> Depends on: G14F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Attempt privilege escalation and information leakage across branches, sessions, perspectives, living-person privacy classes and export paths.

## Scope

- Cross-user/session access, guessed IDs, branch leakage, hidden knowledge leakage, private memory access, rights-revoked asset export, audit deletion and backup exposure.
- Exercise API and projection layers.

## Non-goals

- Do not accept UI hiding as authorization.
- Do not use production personal data for tests.

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
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Explicitly document historical/audit retention exceptions to revocation where legally/architecturally required.

## Deliverables

- reports/AUTH_RIGHTS_PRIVACY_ADVERSARIAL.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build adversarial identities/roles with synthetic data.
- Test every sensitive API with insufficient privilege.
- Test rights changes invalidate future projection/export access.
- Inspect caches for cross-tenant/branch leakage.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Unauthorized access consistently denied server-side.
- Perspective filters prevent knowledge leakage.
- Revocation is enforced according to documented semantics.
- Normal users cannot alter audit truth.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No high/critical authorization or privacy bypass.
- Security evidence is repeatable in CI/staging.
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
- After acceptance passes, create a local checkpoint commit such as: `g14g: authorization, rights, privacy & data-leak adversarial qualification`.
- Record final commit SHA in `reports/G14G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.
