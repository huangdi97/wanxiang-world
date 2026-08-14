# Persona & Memory Research (G19C)

## Prototype
- `MemoryStore` distinguishes fact memories (with provenance/privacy) from persona-conditioned interpretation.
- Retrieval never leaks private/unknown facts.
- `compact()` preserves provenance and key events (dedupes non-key duplicates).
- `PersonaDrift.drift()` reports anonymous decision-consistency drift (0..1).

## Results
| Check | Result |
|---|---|
| No private/unknown facts leak through memory retrieval | PASS |
| Compaction preserves required provenance and key events | PASS |
| Persona drift metric is reported | PASS |
| Fact memory vs persona interpretation remain distinct | PASS |

## Decision
**KEEP_EXPERIMENTAL** — the deterministic memory/drift seam is sound; real long-horizon persona evaluation
requires an LLM policy adapter + long runs (EXTERNAL_BLOCKED). Promotion criteria (drift < threshold over
90d run) not yet met.

## Evidence
- `uv run pytest tests/integration/test_g19c_persona_memory.py -q` -> 3 passed.
