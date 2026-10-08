# G96D — Reference Physical Provider

Status: **PASS** (2026-08-27)

## Delivered

- Added `ReferencePhysicalProvider`, a CI-safe deterministic adapter
  implementing the existing `PhysicalWorldProvider` ABI.
- Added navigation and velocity-step integration, swept circle collision
  detection, stale snapshot/revision rejection, and invalid-input rejection.
- Resolutions carry typed `EntityUpdate` proposals only;
  the provider has no apply, commit, or canonical state write surface.

## Evidence

- Unit/contract: `tests/unit/substrate/test_g96d_reference_physical_provider.py`
  — 2 tests passed, including collision rejection, deterministic replay,
  resolution round-trip, stale snapshot rejection, and protocol checks.
- Real product chain: `tests/integration/test_g96d_reference_physical_product_chain.py`
  — a fresh SQLite `WorldRuntime` supplied the revision/hash boundary;
  the reference step produced evidence/replay hashes while canonical state and
  event history stayed unchanged. 1 test passed.
- Focused result: **3 passed**.
- Full quality: **1433 passed, 1 skipped, 2 warnings**; architecture check PASS.

## Boundary

This Goal is a deterministic reference provider only. It does not claim an
external physics engine, GPU, model, or scientific simulation; visual reference
projection remains G96E. v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**.

