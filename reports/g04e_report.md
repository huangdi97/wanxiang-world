# Goal G04E Acceptance Report

## Status
PASS

## Pre-goal state
- branch: master
- commit: 1b4e17b (G04D checkpoint)
- working-tree notes: clean before G04E work

## Objective
Implement install validation + transactional registry update, portable export,
exact version pinning at world instantiation, explicit upgrade/migration
compatibility and trusted/untrusted extension enforcement.

## Delivered
- `wanxiang_substrate.packages.install`: PackageInstaller (resolve -> verify
  hashes -> trust -> compatibility -> InstallRecord), InstallRecord with exact
  pins/lock hash/schema+domain pins/rights/evidence/asset refs,
  export_install (portable JSON + stable hash), explicit upgrade with
  fork-required incompatibility detection.
- M4 vertical: author -> Source Gate -> compiler -> ledger canon -> registry ->
  install (pinned) -> instantiate (pins in instance metadata) -> export/re-
  import -> publish v2 without mutating the v1 instance (replay-stable).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run python scripts/quality.py` (full gate) | 309 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- `tests/integration/test_package_install.py` (6): install/export roundtrip;
  tampered hash rejected; untrusted executable denied; incompatible dependency
  rejected; publishing v2 does not mutate v1-pinned record; explicit upgrade
  records fork requirement on incompatible major.
- `tests/integration/test_m4_qualification.py` (1): author->review->install->
  instantiate vertical; v1 instance replay-stable after v2 publish.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | guard + review |
| Goal + regression tests PASS | PASS | 309 tests incl. M1-M3/G04A-D |
| Lint/type/architecture PASS | PASS | full quality gate |
| Install/export roundtrip | PASS | roundtrip test |
| Tampered hash / incompatible dep rejected | PASS | negative tests |
| v2 does not mutate v1-pinned instance | PASS | vertical + record tests |
| Upgrade records fork requirement | PASS | incompatible-upgrade test |
| Trusted/untrusted extension rules | PASS | trust test |
| No new forbidden dependency | PASS | architecture guard |

## Key decisions
- Transactional install; explicit upgrade with fork requirement; instance pins
  recorded in metadata (ADR-0029).

## Known limitations
- Compatibility matrix covers synthetic pairs; real-world pairs grow with data.

## External blockers
None.

## Final checkpoint
- commit: `goal g04e: package install, export & migration compatibility`