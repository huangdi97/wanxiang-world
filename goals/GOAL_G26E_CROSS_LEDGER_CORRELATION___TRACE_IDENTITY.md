# G26E — Cross-ledger Correlation & Trace Identity

**Milestone:** M23

## Objective

Allow World/Actor/Runtime ledgers to explain one outcome without merging them.

## Scope

- trace_id/run_id/world/branch/command/decision/runtime revision/commit refs

## Non-goals

- No global mutable trace state

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Standardize correlation identifiers.
- Propagate trace context through host→actor→proposal→commit→projection.
- Add join/query helpers at application/read-model layer.
- Preserve privacy filters.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- One scenario can reconstruct world event + actor decision + runtime config references.
- Missing optional actor record does not invalidate world history.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Three-ledger observability is navigable and typed.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26e: cross-ledger correlation & trace identity`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.
