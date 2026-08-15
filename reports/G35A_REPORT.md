# Goal G35A Acceptance Report — 红楼梦来源策略与合法版本登记

## Status
**EXTERNAL_BLOCKED** (real full-text source) — generic registration mechanism PASS

## Objective
Acquire and register a legally usable, traceable, verifiable《红楼梦》text as
the real WorldPack Source Gate; or record EXTERNAL_BLOCKED precisely and
continue generic tasks.

## Evidence
- Workspace contains no legal full-text edition (only
  `sources/red_chamber/README.md` + `MANIFEST_TEMPLATE.yaml`); environment is
  read-only + network-restricted; prior M15 record already EXTERNAL_BLOCKED.
- `reports/RED_CHAMBER_SOURCE_GATE.md` records the exact missing needs
  (URI/file, checksum, edition, rights grant, review status).
- Mechanism verified with a synthetic, explicitly-labeled fixture (NOT real
  canon): `tests/unit/substrate/test_red_chamber_source_registration.py`
  (3 tests: checksum reproducible; rights/review_status non-empty;
  no model-memory canon fabricated).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_red_chamber_source_registration.py -q` | 3 passed |
| workspace scan for legal text | none present (templates only) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed file) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| User-existing legal text preferred | N/A (none present) |
| Public-domain/legal version obtained | EXTERNAL_BLOCKED (env + no rights-verification capability) |
| Source record: URI/checksum/edition/rights note | EXTERNAL_BLOCKED for real text; mechanism verified with synthetic fixture |
| Model memory NOT used as Canon | PASS (tested; sources dir = templates only) |
| Generic tasks continue | PASS (registration mechanism + tests) |
| Report + ledgers updated | PASS |

## Changed files
- added: tests/unit/substrate/test_red_chamber_source_registration.py,
  reports/RED_CHAMBER_SOURCE_GATE.md, reports/G35A_REPORT.md
- modified: PLAN.md, STATUS.md, DECISIONS.md, BLOCKERS.md, KNOWN_FAILURES.md,
  CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35a: 红楼梦来源策略与合法版本登记`
