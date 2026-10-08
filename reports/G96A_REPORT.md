# G96A — PhysicalWorldProvider ABI

Status: **PASS** (2026-08-27)

## Delivered

- Added immutable `PhysicalBody` and `PhysicalSnapshot` read models. A
  snapshot carries only typed spatial values, canonical instance/branch/
  revision refs, event refs, and a state hash; it owns no canonical state.
- Added versioned `PhysicalSimulationRequest` with snapshot pinning, actor and
  target references, bounded step ticks, deterministic seed, normalized
  parameters, and an input hash.
- Added `PhysicalResolution` with explicit `resolved`/`rejected`/
  `unavailable` status, the existing domain `ProposedWorldDelta`, evidence
  refs, diagnostics, and a deterministic replay hash. Non-resolved output
  cannot carry a delta.
- Added `PhysicalProviderHealth` and the `PhysicalWorldProvider` protocol.
  The protocol exposes only health and simulation; it has no append/apply/
  commit/mutate/submit surface.
- Added schema-checked dictionary round trips for all persisted ABI records.

## Evidence

- Unit/contract: `tests/unit/substrate/test_g96a_physical_provider_abi.py` —
  3 tests passed.
- Product-chain integration:
  `tests/integration/test_g96a_physical_provider_product_chain.py` — a fresh
  SQLite `WorldRuntime` produced the read snapshot; a protocol-conforming
  provider returned a proposal-only resolution; canonical state hash and
  event history stayed unchanged. 1 test passed.
- Focused result: **4 passed**.

## Boundary

This Goal qualifies the ABI only. The deterministic reference physics adapter
is G96D; visual projection and the complete M93 bridge are still pending.
No external engine or GPU/model run is claimed. v5.5 remains
**IN_PROGRESS / NOT_ACCEPTED**.
