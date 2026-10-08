# G57B Report — Distiller Protocol (M54)

## Status
**PASS** — Unified multi-pass Distiller DAG + provider boundary.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/distill/protocol.py` (new):
   - `Distiller` Protocol — name/version/distill(segments) -> CandidateEnvelope.
   - `DistillerDAG` — ordered passes with provenance; `DistillerRegistry` —
     register + run full DAG.
   - Deterministic reference passes always available (no API); model providers
     plug in behind the same boundary and never own Commit.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_distillation_passes.py -q` | 9 passed (with G57A/C-G) |
| ruff / pyright | PASS / 0 errors |
