# G56C Report — Segment Model (M53)

## Status
**PASS** — Segment model with stable id / content hash / parent / ordinal /
parser+segmenter version established.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/parsing/segment.py` (new):
   - `Segment` — segment_id, locator, text, kind, ordinal, parent_id,
     parser_version, segmenter_version, content hash (stable).
   - `build_segments(parsed, fmt)` — deterministic segmentation of a
     ParsedDocument into locator-bearing segments.
2. `tests/unit/substrate/test_segment_locator.py` — 7 tests (shared with G56D).

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_segment_locator.py -q` | 7 passed |
| ruff / pyright | PASS / 0 errors |
