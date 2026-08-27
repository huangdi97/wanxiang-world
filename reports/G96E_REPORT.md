# G96E — Reference Visual Projection Provider

Status: **PASS** (2026-08-27)

## Delivered

- Added `ReferenceVisualProvider`, a deterministic structured-scene
  adapter over the existing `VisualWorldProvider` and G96C perspective policy.
- Health capabilities explicitly state actor perspective, state/event refs, and
  non-generative operation; no renderer, GPU, model SDK, or network dependency
  is used.
- Returned frames preserve scene snapshot ref/revision, canonical state hash,
  actor identity, actor-scoped event refs, sanitized objects, and projection
  hash/frame ref evidence.

## Evidence

- Unit/contract: `tests/unit/substrate/test_g96e_reference_visual_provider.py`
  — 1 test passed for structured actor frames, provenance, deterministic health,
  and the projection-only surface.
- Real product chain: `tests/integration/test_g96e_reference_visual_product_chain.py`
  — a fresh SQLite `WorldRuntime` supplied the snapshot identity; Alice and
  a public actor received isolated frames with equal state provenance and
  unchanged canonical state/event history. 1 test passed.
- Focused combined result with G96C regression: **5 passed**.

## Boundary

This Goal qualifies the non-generative reference visual adapter only. It does
not claim external rendering, GPU inference, or a generative world model; G96F
audits external engine adapters. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.

