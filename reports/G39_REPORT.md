# Goals G39A-G39H Acceptance Report — Full Corpus & Canon Graph (M36)

## Status
PASS (mechanism) — synthetic corpus; real《红楼梦》full text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/canon_graph/` (new):
   - G39A/B: reuses M32 SourceGate/locator + G38F corpus pipeline (full
     checksum/locator/incremental resume via FullCorpusPipeline cache).
   - G39C `SceneCandidate` + `detect_scenes` — time/place/participant cues;
     cross-chapter scene policy.
   - G39D `CharacterGraph` — identity/alias/role/life-stage nodes + relation
     edges (valid_time).
   - G39E `SourceGraph` — place connectivity/containment, item custody, org
     membership.
   - G39F `TimelineGraph` — event before/after/uncertain ordering, participants,
     place, evidence.
   - G39G `CanonGraph` — categories, edition views, contradictory claims
     preserved (never dropped).
   - G39H `CoverageReport` — source->claim traceability, resume/retry counts.
2. `tests/unit/substrate/test_canon_graph.py` (8 tests): scenes; character
   graph; source graph; timeline; canon categories/edition views;
   contradictions preserved; coverage+resume; retry count.

## Reuse
- G35B locators, G35C identity, G38F corpus pipeline; no new registry/engine.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_canon_graph.py -q` | 8 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g39: Full Corpus & Canon Graph (M36 mechanism)`
