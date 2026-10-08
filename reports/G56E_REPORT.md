# G56E Report — Incremental Parsing (M53)

## Status
**PASS** — Content/version cache + segment diff for incremental parsing.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/parsing/incremental.py` (new):
   - `ParseCache` — keyed by (source_id, version, content_hash, parser_version,
     segmenter_version); explicit `invalidate_source`.
   - `IncrementalParser` — returns cached parse when unchanged (was_cached flag);
     re-parses on content/version change.
   - `changed_segments()` — node-level content-hash diff (local re-run target).
2. `tests/unit/substrate/test_incremental_parse.py` — cache/invalidate/diff
   tests (shared with G56F).

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_incremental_parse.py -q` | 6 passed |
| ruff / pyright | PASS / 0 errors |
