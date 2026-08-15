# M36 Qualification — Full Corpus & Canon Graph

## Status
**M36 Milestone Gate PASS (mechanism)**

Real《红楼梦》full text remains EXTERNAL_BLOCKED (G35A); the full-corpus/canon
graph MECHANISM is certified on synthetic corpora, honestly labeled.

## Goal status (M36)
| Goal | Status |
|---|---|
| G39A 完整底本 Source Gate | PASS (mechanism; real text EXTERNAL_BLOCKED) |
| G39B 章节/段落稳定定位器 | PASS (reuses G35B + G38F) |
| G39C Scene Boundary 与场景候选 | PASS |
| G39D 全人物 Identity/Alias/Role Graph | PASS |
| G39E 地点/物品/组织 Source Graph | PASS |
| G39F Event/Timeline/Relation Graph | PASS |
| G39G Canon Graph / Edition Conflict | PASS |
| G39H M36 Full Corpus Qualification | PASS (this report) |

## Quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` (pytest) | 946 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED); file-size failures fixed by module split |
| SDK baseline | regenerated (routes=17 ts=5 py=1118); contract 3/3 PASS |
| architecture_check.py | Architecture conformance: PASS (after canon_graph split) |
| ruff / format / pyright | PASS (0 errors) |

## Key invariants verified (M36)
- Full corpus -> scenes/character/source/timeline/canon graphs, deterministic;
  contradictory claims preserved; edition views isolated.
- Coverage report with source->claim traceability + resume/retry.
- No new Commit/Event/Branch/Registry/Engine; all graph builders are pure.

## Honest boundary
- Real-corpus canon graph requires a legal, traceable edition (BLOCKERS.md).

## Local checkpoint
- G39 mechanism committed; M36 gate certified in this report.
