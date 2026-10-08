# G96C — Multi-perspective Projection

Status: **PASS** (2026-08-27)

## Delivered

- Added a pure, deterministic `PerspectiveVisualProvider` over the G96B
  `VisualWorldProvider` ABI. It creates one projection frame per actor and
  binds the frame ref to provider, scene snapshot, actor perspective, visible
  object refs, and actor-scoped event refs.
- Enforced actor audience allow/deny policy, view-radius perception, asset-rights
  filtering, and deterministic line-of-sight occlusion using the scene object's
  optional non-negative occlusion radius.
- Kept projected objects sanitized: audience refs, private objects, denied assets,
  and hidden-object event refs do not enter another actor's frame.

## Evidence

- Unit/product contract: `tests/unit/substrate/test_g96c_multi_perspective_projection.py`
  — 2 tests passed, including A/B private-knowledge isolation, rights and
  occlusion filters, deterministic frame refs, and provider-only surface.
- Real product chain: `tests/integration/test_g96c_multi_perspective_product_chain.py`
  — a fresh SQLite `WorldRuntime` supplied the snapshot identity; Alice and
  Bob received distinct actor-scoped frames while canonical state hash and
  event history stayed unchanged. 1 test passed.
- Focused result: **3 passed**.

## Boundary

This Goal adds perception/projection policy only. It does not create a second
canonical state, event store, branch, or commit path. Reference physical and
visual adapters remain G96D/G96E; v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.

