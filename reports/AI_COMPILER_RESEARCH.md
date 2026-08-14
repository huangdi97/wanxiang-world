# AI-assisted World Compiler Research (G19B)

## Prototype
- Extraction schema: entity_id, entity_type, claims, source_span, confidence, provenance.
- `ExtractionProvider` Port + `DeterministicFixtureProvider` (no paid API).
- `SemanticExtractor` binds candidates to source provenance; `review_diff` produces accepted/rejected + uncertainty band.
- Model output is ALWAYS Candidate/Claim; never auto-promoted to canonical truth.

## Results
| Check | Result |
|---|---|
| Model output remains Candidate (no canonical write capability) | PASS |
| Prompt-injection output parsed as data; system behavior unchanged | PASS |
| Core compiler works with AI disabled (flag OFF, stable path) | PASS |
| Evaluation report includes uncertainty and failure modes | PASS |

## Decision
**KEEP_EXPERIMENTAL** — the deterministic prototype demonstrates the candidate/review seam and source-span
binding, but real LLM extraction quality requires a provider + labeled corpus (EXTERNAL_BLOCKED). Promotion
criteria (benchmark parity + clean-room build) are NOT met yet.

## Evidence
- `uv run pytest tests/integration/test_g19b_ai_compiler.py -q` -> 4 passed.
