# G57A Report — CandidateEnvelope Convergence (M54)

## Status
**PASS** — Unified candidate shell (origin/confidence/source/evidence/
distiller version/provider) across all distillation passes.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/candidates/envelope.py` (new):
   - `CandidateEnvelope` — candidate_id/kind/origin_pass/payload/confidence/
     source_refs/evidence_refs/distiller_version/status/provider; canonical
     hash; status transitions (pending/eligible/rejected).
   - Converges the earlier pattern-specific evolution CandidateEnvelope into
     the shared Forge candidate fabric (no second shell).
2. `tests/unit/substrate/test_distillation_passes.py` — envelope validation +
   hash tests.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_distillation_passes.py -q` | 9 passed (with G57B-G57G) |
| ruff / pyright | PASS / 0 errors |
