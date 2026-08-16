# G59B Report — Reference Recommender (M56)

## Status
**PASS** — Deterministic, explainable domain recommendation from source/
candidate features (no model required).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/domains/recommender.py` (new):
   `DomainRecommender.recommend` — feature extraction (family/social/temporal/
   spatial/institutional/norms/epistemic) -> scored `Recommendation` with
   concrete reasons.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_domain_draft.py -q` | 7 passed |
| ruff / pyright | PASS / 0 errors |
