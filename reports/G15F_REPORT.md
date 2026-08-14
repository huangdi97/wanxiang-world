# Goal G15F Acceptance Report — Branch, Time-travel & Counterfactual Worldline Comparison Qualification

## Status
PASS

## Objective
Demonstrate canon/baseline, intervention and no-intervention worldlines from shared history with reproducible branch comparison.

## Delivered
- `tests/integration/test_g15f_worldlines.py` — 3-worldline comparison test.
- `reports/WORLDLINE_COMPARISON_QUALIFICATION.md`, `reports/G15F_REPORT.md`.

## Findings
- Baseline, deliver, and deliver+read worldlines diverge causally from shared history.
- Parent history unchanged; each worldline replays to its own stable hash; diff highlights differences.
- Historical (read-only) reads are consistent with the fork revision.

## Evidence
- 1 test passed; ruff/pyright clean.

## Remaining limitations
- Real counterfactual experiments require external users; deterministic worldline comparison qualified.

## Final checkpoint
- commit: `g15f: branch, time-travel & counterfactual worldline comparison qualification`
