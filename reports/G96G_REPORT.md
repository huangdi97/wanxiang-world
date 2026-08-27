# G96G — Projection/Reality Consistency

Status: **PASS** (2026-08-27)

## Delivered

- Added versioned `RealityConsistencyResult` records for visual projections
  and physical resolutions against immutable canonical read models.
- Visual checks cover scene/snapshot identity, revision, state hash, object
  entity/position/asset provenance, and event/asset reference containment.
- Physical checks cover snapshot identity/revision, resolution status, and
  proposed updates targeting unknown physical entities.
- Added typed `RealityReconciliationProposal` actions. `retain`,
  `refresh_projection`, `recompute_physical`, and `review` are consumer
  instructions only; every reconciliation proposal carries an empty
  `ProposedWorldDelta`.

## Evidence

- Unit/contract: `tests/unit/substrate/test_g96g_projection_reality_consistency.py`
  — 3 tests passed for consistent round-trip evidence, stale-frame handling,
  hallucinated-object rejection, and physical snapshot checks.
- Real product chain: `tests/integration/test_g96g_reality_consistency_product_chain.py`
  — visual and physical outputs crossed a fresh SQLite `WorldRuntime`; the
  canonical state hash and event history stayed unchanged. 1 test passed.
- Focused result: **4 passed**.
- Full quality: **1442 passed, 1 skipped, 2 warnings**; Ruff, format check,
  Pyright, and architecture conformance all passed.
- Divergent or stale provider output is not accepted as world fact and is
  routed to an empty proposal-only reconciliation record.

## Boundary

This Goal detects provenance/version/reference divergence; it does not make a
provider authoritative and does not claim visual realism or scientific
validity. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.
