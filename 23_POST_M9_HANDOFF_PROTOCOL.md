# Post-M9 Handoff & Repository Integration Protocol

## Purpose
This pack must be merged into the **existing** Wanxiang repository after the M0–M9 program. It is not a new repository bootstrap.

## Preserve
Never delete/reinitialize merely to install this pack:

- `.git/` and current branch/history;
- production source and tests;
- migrations and persisted test fixtures;
- `docs/spec/WANXIANG_v5_MASTER_SPEC.md`;
- previous Engineering Program Architecture/standards/acceptance files;
- `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
- existing `reports/` and acceptance evidence.

## First Codex action
The first action remains independent verification, not new feature coding. Read M9 evidence and run critical regressions, then begin G13A baseline capture.

## If M9 is not actually healthy
Do not blindly continue. Record the regression in the post-M9 baseline and repair the smallest root cause needed to restore the claimed stable checkpoint. Do not restart G0–G12 or replace the repository wholesale.

## Naming and versioning
M10–M17 are program milestones, not a silent change to the v5.0-R1 product specification. Stable code/version changes follow the repository's existing release/version policy. M16 experiments remain explicitly experimental unless promoted by ADR and final regression.

## External blockers
Approved source corpora, private family records, real museum data, Liaoshen sources, external digital-human providers, physical sensors or cloud infrastructure may be unavailable. Such absence blocks only the exact real integration slice. Generic platform behavior, synthetic fixtures, interfaces, deterministic adapters, Source Gate and failure tests must still be completed.
