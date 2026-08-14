# M25 Qualification — v5.1 Backward Migration & Final Certification

## Preconditions

All Goals in M25 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M25 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M25.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M25_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- v5.0 persisted worlds/events/snapshots/packages upgrade/replay deterministically.
- Public API/SDK/ABI changes are compatible or explicitly migrated/deprecated.
- Synthetic full reference world passes v5.1 end-to-end.
- Family/Heritage/Campaign/Narrative paths pass generic/source-gated qualification.
- Product surfaces/adapters still consume one server truth.
- Minimal-core final audit has zero stable P0/P1 duplication/dead-path findings.
- Clean-room build/upgrade/restore/replay passes.
- All final reports exist and stable P0/P1 gaps are zero.

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
- generate all final v5.1 certification reports required by `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`;
- create the final local M25/v5.1 checkpoint;
- **stop the program** and report completion to the user. Do not invent or start G29/M26.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.
