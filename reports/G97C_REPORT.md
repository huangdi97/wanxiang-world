# G97C — Non-literary Long-run Certification

Date: 2026-08-27  
Status: PASS

## Scope

G97C verifies that a different source domain can use the same long-horizon
runtime substrate. It uses a public, rights-approved, training-disabled
GEDCOM family source with the existing `family` profile. This is a bounded
qualification fixture, not the original 2026-08-25 323,815-character private
book; the original real-book report remains `NOT_ACCEPTED`.

## Shared product path

`tests/integration/test_g97c_non_literary_long_run.py` runs:

`GEDCOM SourceRecord → OneClickAuthoring(profile=family) → WorldPackage →
Preview → PlayableService → Living Instance → SQLite WorldRuntime → Commit
Authority`.

The test constructs its own family-source record and uses the same public
long-horizon contracts as G97B: `BackgroundSimulation`,
`RecurringScheduler`, `HorizonQualification`, `RunCheckpointStore`,
`SimulationLODRuntime`, `CostBudgetLedger`, and `CompactionService`. No
literary profile, literary source adapter, or literary-specific runtime branch
is used.

## Measured evidence

| Measure | Result |
|---|---:|
| Source profile / kind | family / GEDCOM (public) |
| Horizon samples | 24h / 7d / 30d |
| Horizon | 30 simulated days / 3,000 world ticks |
| Selected source actors | 2 of 3 family individuals |
| Main-branch committed events | 160 |
| Runtime/run checkpoints | 30 |
| Actor-local memories | 30 per selected actor / 60 total |
| Serialized state storage | 2,542 → 33,401 bytes |
| World budget calls / charged storage | 150 / 30,859 bytes |
| Observed LOD levels | L0, L3, L4 |
| Reference compaction summaries | 13 |
| Replay vs SQLite restart recovery | equal |
| Branch isolation | parent unchanged after child-only write |

All required horizon samples reached their exact target ticks. The checkpoint
cursor ended at tick 3,000 and matched a newly constructed scheduler after
resume. The injected publication crash left no latest checkpoint. A fresh
SQLite runtime restored the same final semantic hash, and reference-only
compaction preserved replay equality without deleting or rewriting
authoritative events.

## Generality boundary

The public GEDCOM `family` flow produced the living instance and the same
Commit Authority handled clock, status, and actor-local memory effects. The
30-day run therefore supplies cross-domain substrate evidence, not a second
runtime implementation. The child branch accepted a family-only status
proposal while the parent event tuple/hash remained unchanged.

This evidence does not claim scientific validity, universal domain coverage,
or the original private-book acceptance. It only closes the G97C
non-literary long-run scope.

## Quality and architecture evidence

- Focused family/G97B/G92H long-horizon regression: `12 passed, 2 warnings`
  in 33.01s.
- G97C standalone run: `1 passed, 1 warning` in 5.87s.
- Full quality: `1448 passed, 1 skipped, 2 warnings` in 385.59s (6:25).
- The one skip is the documented PostgreSQL `EXTERNAL_BLOCKED` profile because
  `WANXIANG_POSTGRES_TEST_URL` is not configured.
- Ruff check and format check: PASS; full Pyright: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.

G97C is PASS. The shared substrate is qualified for this non-literary family
scope; G97D-G97J and other M94 release gates remain pending, v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED`, and no v5.5 rc1, v5.6 work, model training, or
private-source upload was performed.
