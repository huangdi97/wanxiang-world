# Goal G15A Acceptance Report — Reference World Contract & External Pack Boundary

## Status
PASS

## Objective
Define the black-box contract a serious reference World Pack must satisfy so world content proves platform generality without being hard-coded into Core.

## Delivered
- `docs/REFERENCE_WORLD_CONTRACT.md` — contract + worldness scenarios + version pinning + reproducible build.
- `scripts/reference_world_conformance.py` — conformance harness (validates metadata, catches missing
  rights/evidence/eval, installs via public PackageInstaller).
- `tests/integration/test_g15a_reference_world_contract.py` — 3 tests.
- `reports/REFERENCE_WORLD_CONTRACT_ACCEPTANCE.md`, `reports/G15A_REPORT.md`.

## Findings
- A tiny external synthetic pack builds and installs without modifying Core (black-box).
- The harness catches missing rights/evidence/eval metadata and reports install failures.
- Core remains domain-neutral (no Core import of reference content).

## Evidence
- 3 tests passed; ruff/pyright clean; full gate remains green.

## Remaining limitations
- Real copyrighted/historical data is not required for synthetic qualification (EXTERNAL_BLOCKED for real slices).

## Final checkpoint
- commit: `g15a: reference world contract & external pack boundary`
