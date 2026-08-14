# Goal G17A Acceptance Report — Public SDK Contract, Semantic Versioning & Compatibility Policy

## Status
PASS

## Objective
Freeze the stable extension surface for third-party Domain/World/Experience/Projection packages without exposing internal implementation details.

## Delivered
- `docs/SDK_COMPATIBILITY_POLICY.md` — stable vs experimental namespaces, semver/deprecation policy, extension points, forbidden dependencies.
- `scripts/sdk_baseline.py` + `reports/SDK_API_BASELINE.md` + `reports/sdk_api_baseline.json` — 10 routes, 5 TS symbols, 832 Python public names.
- `tests/integration/test_g17a_sdk_contract.py` — 3 tests.

## Findings
- Third-party operations (pack build/install, instantiate, command, projection) work through the public SDK only.
- Breaking changes are detected by the compatibility snapshot (tamper simulation fails).
- No underscore-prefixed internals leak into the stable surface; experimental APIs are separately documented.
- SDK grants no canonical mutation authority (Commit Authority remains the only writer).

## Evidence
- 3 tests passed; ruff/pyright clean; baseline reproducible.

## Remaining limitations
- Real third-party package publication requires registry infra (M14 later goals); the SDK contract is frozen.

## Final checkpoint
- commit: `g17a: public sdk contract, semantic versioning & compatibility policy`
