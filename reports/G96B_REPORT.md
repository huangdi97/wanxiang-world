# G96B — VisualWorldProvider ABI

Status: **PASS** (2026-08-27)

## Delivered

- Added immutable `VisualSceneObject` and `VisualSceneState` records pinned to
  a canonical snapshot ref/revision, state hash, event refs, and existing
  content-addressed `AssetRef` values.
- Added `ActorPerspective` with actor identity, origin/radius, object
  allow/deny refs, and asset-rights scope.
- Added sanitized `VisualProjectedObject` and `VisualProjectionFrame`
  records. Frame objects intentionally omit source audience/rights policy;
  frame status, snapshot/event refs, state hash, projection-only marker, and
  deterministic projection hash remain explicit.
- Added `VisualProviderHealth` and `VisualWorldProvider`. The visual protocol
  exposes only health and projection; it has no canonical write operation.
- Added schema-checked round trips and tamper-detecting frame hashes.

## Evidence

- Unit/contract: `tests/unit/substrate/test_g96b_visual_provider_abi.py` —
  3 tests passed.
- Product-chain integration:
  `tests/integration/test_g96b_visual_provider_product_chain.py` — a fresh
  SQLite `WorldRuntime` supplied scene provenance; a protocol-conforming
  provider returned a projection-only frame; canonical state hash and event
  history stayed unchanged. 1 test passed.
- Focused result: **4 passed**.

## Boundary

This Goal qualifies the visual ABI only. Multi-perspective privacy filtering
is G96C; deterministic reference projection is G96E; no external renderer,
GPU, or generative model run is claimed. v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**.
