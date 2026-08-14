# Cognitive LOD & Large-population Scheduling Research (G19D)

## Prototype
- `CognitiveLodScheduler`: active/background/dormant/crowd tiers with event-driven wakeups.
- Transitions preserve identity and obligations; dormant/crowd actors cost zero resource budget;
  aggregate models never invent private knowledge for individuals.

## Results
| Check | Result |
|---|---|
| LOD transition preserves identity/required obligations | PASS |
| Declared scale profile improves resource use (dormant cost 0) without invariant failures | PASS |
| Benchmark is reproducible (deterministic wakeup schedule) | PASS |
| No silent actor deletion/duplication on wake | PASS |

## Decision
**KEEP_EXPERIMENTAL** — the LOD seam shows resource improvement; promotion requires integration with the
stable population scheduler + a benchmark vs the M12 profile (EXTERNAL_BLOCKED until then).

## Evidence
- `uv run pytest tests/integration/test_g19d_cognitive_lod.py -q` -> 3 passed.
