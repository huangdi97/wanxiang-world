# G03A — Observation & Perspective Isolation

> Phase: P3 — Agency, Cognition and Action Runtime  
> Target milestone: M3  
> Execution mode: continuous; on PASS create checkpoint and continue automatically.  
> Product source of truth: `docs/spec/WANXIANG_v5_MASTER_SPEC.md`

## 1. Objective

Introduce explicit observations and perspective boundaries so actors only receive information they could perceive or be told.

## 2. Dependencies / Entry Conditions

This Goal may start only when the following are true:

- M2 PASS

Before editing production code, rerun the narrow regression suite for the dependency boundary. If a prior milestone regression is discovered, repair the regression first and record it; do not build new capability on a broken base.

## 3. Required Reading

Read before implementation:

- `docs/spec/WANXIANG_v5_MASTER_SPEC.md`, especially:
  - §6 Agency & Capability Plane
  - Appendix D §§9–12 Character/Memory/Organization
  - Appendix D §§30–31 Action Validator/Resolver
  - §50 Character/Society Tests
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

- Observation schema
- observer/source/time/place/confidence
- visual/acoustic/material information propagation
- public/group/private visibility
- perspective-filtered context assembly

## 5. Non-goals

- Do not implement vector memory.
- Do not let canonical truth be copied wholesale into actor context.
- Do not call an LLM in core tests.

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

- Production implementation for Observation & Perspective Isolation under existing modular-monolith boundaries.
- Typed public/domain/application contracts with explicit version metadata where persisted or externally consumed.
- Deterministic synthetic fixtures and fakes for every external boundary introduced by this Goal.
- Goal-specific automated tests plus regression coverage for all earlier milestone invariants touched by the change.
- `reports/g03a_report.md` with commands, results, acceptance evidence, limitations and changed files.
- Ledger/ADR updates for non-trivial architecture or compatibility decisions.

## 8. Implementation Tasks

Execute all tasks; split implementation internally into cohesive work packages rather than one large file:

1. Define observation contracts and provenance.
2. Derive observations from committed events plus spatial/acoustic/rights conditions.
3. Implement deterministic perspective query service.
4. Separate observed fact from interpretation/belief.
5. Add confidential and overheard-message fixtures.
6. Audit which rule allowed each observation.

Additional mandatory work:
- inspect existing abstractions before adding new ones; reuse only if semantics match;
- add explicit errors for invalid/unsupported/conflict states;
- add schema/version metadata at first persistence/public exposure;
- add audit/trace data for important decisions and mutations;
- update generated API/SDK schemas when relevant;
- run a changed-files cohesion review before declaring PASS.

## 9. Tests

Goal-specific required tests:

- unit: visibility, acoustic propagation, private/group visibility
- negative: actor outside zone cannot observe event
- information isolation: sealed payload/secret stays hidden
- branch: perspective results differ only when branch events justify it
- architecture: projection and cognition consume ports, never bypass rights

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

- All implementation tasks in G03A are complete; no acceptance-critical TODO/FIXME/placeholder/NotImplemented/mock-only production path remains.
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
- write `reports/g03a_report.md` with reproducible commands and evidence.

## 13. Git / Checkpoint Requirements

After all acceptance criteria PASS or permitted external-only items are explicitly documented:
1. ensure the working tree contains only intended changes;
2. run the full Goal gate one final time;
3. create a local commit:
   `goal g03a: observation & perspective isolation`
4. record the commit hash in the Goal report and `STATUS.md`;
5. do not push/deploy unless the user separately requests it;
6. continue automatically to the next Goal.

If the Goal is the last Goal before a milestone, do not mark the milestone PASS yet. Run the milestone qualification document first.
