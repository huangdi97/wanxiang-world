# G56D Report — Stable Locator (M53)

## Status
**PASS** — Format-aware stable locators for EPUB/DOCX/PDF/GEDCOM/JSON/CSV with
round-trip resolution.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/parsing/segment.py` (new):
   - `StableLocator` — `fmt://source_id#kind/ref` string, validated, with
     `to_string()`/`from_string()` round-trip.
   - `locator_for_node` — chapter/paragraph/record/row refs per format
     (JSON pointer-ish, CSV row, GEDCOM xref, book chapter/paragraph ordinal).
   - `resolve(parsed, locator)` — locator -> exact source node text.
2. `tests/unit/substrate/test_segment_locator.py` — round-trip + per-format
   locator tests.

## Reuse
- Extends the G35B SourceLocator concept with format awareness; no second
  locator system.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_segment_locator.py -q` | 7 passed |
| ruff / pyright | PASS / 0 errors |
