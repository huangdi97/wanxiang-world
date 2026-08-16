# G56G Report — Diagnostics API (M53)

## Status
**PASS** — Structure preview / warnings / errors / locator preview API.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/parsing/diagnostics.py` (new):
   - `DiagnosticsReport` — node counts by kind, warnings, errors, locator
     preview, ok flag, summary().
   - `collect(parsed)` — aggregated diagnostics.
   - `structure_preview(parsed, limit)` — human-readable structural preview.
   - `locator_preview(segments, limit)` — locator strings.
   - `build_preview_report(parsed, fmt)` — report with segment locators.
2. `tests/unit/substrate/test_parse_diagnostics.py` — 5 tests.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_parse_diagnostics.py -q` | 5 passed |
| ruff / pyright | PASS / 0 errors |
