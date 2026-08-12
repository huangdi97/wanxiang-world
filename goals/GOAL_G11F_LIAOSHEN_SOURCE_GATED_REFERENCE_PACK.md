# G11F — Liaoshen Source-gated Reference Pack

> Phase: P8 — Co-Simulation and Strategy  
> Target milestone: M8  
> Execution mode: continuous; on PASS create checkpoint and continue automatically.  
> Product source of truth: `docs/spec/WANXIANG_v5_MASTER_SPEC.md`

## 1. Objective

Exercise historical campaign packaging only from approved Liaoshen sources and preserve disputes/uncertainty; otherwise stop only this real-data slice at Source Gate.

## 2. Dependencies / Entry Conditions

This Goal may start only when the following are true:

- G11E

Before editing production code, rerun the narrow regression suite for the dependency boundary. If a prior milestone regression is discovered, repair the regression first and record it; do not build new capability on a broken base.

## 3. Required Reading

Read before implementation:

- `docs/spec/WANXIANG_v5_MASTER_SPEC.md`, especially:
  - §5.4 Co-Simulation Fabric
  - §15 Liaoshen reference instance
  - Appendix D §33 Experiment Runtime
  - Appendix E §51 simulation verification/validation
- `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md`
- `02_ENGINEERING_STANDARDS.md`
- `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`
- `05_CODEX_REMAINING_PROGRAM_MASTER_PROMPT.md`
- `06_REMAINING_GOALS_INDEX.md`
- `07_MILESTONE_GATES_M2_M9.md`
- current `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing source, tests, migrations, ADRs and the previous Goal report

Do not infer missing requirements from model memory or old chats.

## 4. Scope

- source manifests
- rights/review
- historical entities/events/places/organizations
- uncertain/conflicting claims
- scenario baseline
- historical versus counterfactual labels

## 5. Non-goals

- No model-memory historical fabrication.
- No hidden conversion of contested claim to fact.
- No requirement that M8 depend on unavailable real sources.

Also out of scope for every Goal unless explicitly named here:
- bypassing Source Gate for real data;
- creating microservices/distributed infrastructure merely for future scale;
- replacing the existing event/commit/replay authority with a new subsystem;
- weakening earlier tests to make the new feature pass.

## 6. Architecture Constraints

1. `Canonical World State` remains authoritative; this Goal may submit commands/observations/proposed deltas but may not create a second mutation path.
2. All new domain semantics live behind cohesive modules and stable ports. External libraries belong in adapters.
3. `domain` remains independent of FastAPI, SQLAlchemy/Alembic, frontend frameworks and model-provider SDKs.
4. Persisted/public types are versioned; migrations and compatibility behavior are explicit.
5. Deterministic core tests do not require network, credentials or an LLM.
6. Projection/session/adapter state never becomes world truth merely because it exists in a client or external system.
7. Rights, provenance, knowledge isolation and audit metadata are enforced at the earliest relevant boundary.
8. Default production source-file target remains approximately <=300 lines. Split by responsibility rather than hiding code in generic `manager.py`, `service.py`, `utils.py` or `helpers.py`.
9. No global mutable singleton, hidden constructor I/O, swallowed exceptions or ORM session leakage.
10. New behavior must be observable with structured identifiers and reproducible from documented fixtures.
11. If a new plugin/extension can execute code, apply the trusted/untrusted package policy; default to no arbitrary executable code from untrusted packages.
12. A new adapter may fail or be unavailable without corrupting or partially mutating canonical state.

## 7. Deliverables

- Production implementation for Liaoshen Source-gated Reference Pack under existing modular-monolith boundaries.
- Typed public/domain/application contracts with explicit version metadata where persisted or externally consumed.
- Deterministic synthetic fixtures and fakes for every external boundary introduced by this Goal.
- Goal-specific automated tests plus regression coverage for all earlier milestone invariants touched by the change.
- `reports/g11f_report.md` with commands, results, acceptance evidence, limitations and changed files.
- Ledger/ADR updates for non-trivial architecture or compatibility decisions.

## 8. Implementation Tasks

Execute all tasks; split implementation internally into cohesive work packages rather than one large file:

1. Inspect configured Liaoshen source area.
2. Compile only approved/allowed materials through Source Gate.
3. Preserve disputed dates/locations/strengths as claims/evidence where sources differ.
4. Label historical record, reconstruction and counterfactual branches distinctly.
5. If sources are absent/disallowed, create gate manifests/tests and mark real pack EXTERNAL_BLOCKED.
6. Run limited replay/branch experiment only when source baseline is legitimate.
7. Document source coverage and validity limits.

Additional mandatory work:
- inspect existing abstractions before adding new ones; reuse only if semantics match;
- add explicit errors for invalid/unsupported/conflict states;
- add schema/version metadata at first persistence/public exposure;
- add audit/trace data for important decisions and mutations;
- update generated API/SDK schemas when relevant;
- run a changed-files cohesion review before declaring PASS.

## 9. Tests

Goal-specific required tests:

- unapproved source cannot compile canonical history
- conflicting claims coexist
- counterfactual branch never overwrites historical baseline
- every historical datum has provenance/truth label
- M8 generic co-sim passes regardless of real-source availability

Global regression tests required when applicable:
- M1 Commit/Event/Replay/Branch/Idempotency/StaleRevision suite;
- architecture dependency guards;
- migration compatibility;
- rights/projection leakage;
- deterministic replay and semantic hash;
- persistence restart;
- negative/error-path assertions.

Tests must prove behavior, not file existence. Mocks may isolate external systems, but acceptance must exercise real internal code paths.

## 10. Acceptance Criteria

- All implementation tasks in G11F are complete; no acceptance-critical TODO/FIXME/placeholder/NotImplemented/mock-only production path remains.
- All Goal-specific tests PASS and all previously passing milestone gates remain green.
- Ruff/lint, type checking, architecture conformance and applicable frontend/build checks PASS.
- Any persisted/public schema change has a migration/compatibility test and does not silently break old replay/package data.
- Any canonical mutation introduced by this Goal still flows through Validate/Resolve/Commit and produces auditable events.
- No new direct dependency from domain/core to FastAPI, SQLAlchemy, UI, model SDK or concrete external adapter is introduced.
- Goal evidence report exists and the final local Git checkpoint is created only after PASS.

Acceptance status for each criterion must be one of `PASS`, `FAIL`, `EXTERNAL_BLOCKED`, `NOT_APPLICABLE`, with evidence.

## 11. Failure / Blocker Handling

- Treat implementation defects, test failures, type errors, design inconsistencies that can be resolved from the master specification, missing internal migrations and architecture violations as **internal work**. Fix them.
- Use `EXTERNAL_BLOCKED` only for genuinely unavailable external data, authorization, credential, service, hardware or engine binary that the Goal explicitly depends on.
- When an external item is blocked, still complete the interface, fake/fixture, validation, error handling, documentation and all internal acceptance possible.
- A real-data reference pack being `EXTERNAL_BLOCKED` must not block a generic platform milestone if the milestone gate explicitly permits that path.
- Never fabricate real historical/literary/family/museum facts to avoid a blocker.
- If a blocker reveals a contradiction in the master spec that changes product semantics, document it in `BLOCKERS.md` and stop only the affected branch of work; continue independent Goals if safe.

## 12. Documentation Updates

Before PASS:
- update `STATUS.md` and `PLAN.md`;
- append important compatibility/architecture choices to `DECISIONS.md` or ADRs;
- update `BLOCKERS.md` and `KNOWN_FAILURES.md`;
- add a concise `CHANGELOG.md` entry;
- update `docs/IMPLEMENTATION_STATUS.md`;
- update API/package/interop/runbook docs touched by this Goal;
- write `reports/g11f_report.md` with reproducible commands and evidence.

## 13. Git / Checkpoint Requirements

After all acceptance criteria PASS or permitted external-only items are explicitly documented:
1. ensure the working tree contains only intended changes;
2. run the full Goal gate one final time;
3. create a local commit:
   `goal g11f: liaoshen source-gated reference pack`
4. record the commit hash in the Goal report and `STATUS.md`;
5. do not push/deploy unless the user separately requests it;
6. continue automatically to the next Goal.

If the Goal is the last Goal before a milestone, do not mark the milestone PASS yet. Run the milestone qualification document first.
