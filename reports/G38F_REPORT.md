# Goal G38F Acceptance Report — 大 Corpus 流水线容量基线

## Status
PASS (mechanism) — synthetic large corpus; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/corpus/pipeline.py` (new):
   - `generate_synthetic_corpus()` — deterministic synthetic large corpus.
   - `CorpusPipeline` — incremental parse (G35B) -> distill (G35C) -> cache ->
     resume (idempotent).
   - `CorpusProfile` — memory/disk profile with a bounded-memory check.
2. `tests/unit/substrate/test_corpus_pipeline.py` (4 tests): 1000-chapter
   corpus parses/distills; incremental cache + resume; profile within memory
   bounds; deterministic corpus.

## Reuse
- G35B segment_source; G35C IdentityDistiller. No new registry/engine.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_corpus_pipeline.py -q` | 4 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g38f: 大 Corpus 流水线容量基线`
