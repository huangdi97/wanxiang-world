# M20 Qualification — Genesis / Ontology / Law Evolution

## Preconditions

All Goals in M20 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M20 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M20.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M20_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- GenesisSpec reuses existing package/scenario systems.
- Designer Genesis is stable/deterministic.
- Ontology/Law evolution is branch-local and replayable.
- Ω is non-authoritative and minimally persisted.
- Evolutionary/True Genesis status is honestly experimental/research where applicable.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.
