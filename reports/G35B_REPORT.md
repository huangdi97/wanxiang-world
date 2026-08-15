# Goal G35B Acceptance Report — 章节分段与可引用 Source Locator

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A)

## Objective
Convert a source into stable, citable chapter/segment locators without
rewriting the original text.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/locator.py`:
   - `SourceLocator` — source_id, chapter, segment_id, start/end offsets, locator.
   - `segment_source(source_id, text)` — read-only chapter-marker segmentation
     (offsets + chapter numbers preserved; original text never modified).
   - `source_slice(text, locator)` — exact source slice for a claim back-link.
   - `locator_stable_hash(locators)` — deterministic stability hash.
   - Exported via `wanxiang_substrate.sources` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_source_locator.py` (4 tests, synthetic corpus):
   - parser produces stable locators (re-run identical; stable hash);
   - a Canon claim's locator back-links to the exact source slice;
   - original text is never rewritten (read-only);
   - offsets and segment ids are consistent.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_source_locator.py -q` | 4 passed |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=956 |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Parse/segment | PASS |
| Preserve source offsets + chapter numbers | PASS |
| Generate reference locators | PASS |
| Original text not auto-rewritten | PASS (tested) |
| Any Canon claim can be back-linked to a locator | PASS (tested) |
| Parser locator stable on re-run | PASS (tested) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A; mechanism tested with synthetic corpus) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/sources/locator.py,
  tests/unit/substrate/test_source_locator.py, reports/G35B_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/sources/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35b: 章节分段与可引用 Source Locator`
