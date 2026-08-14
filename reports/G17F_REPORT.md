# Goal G17F Acceptance Report — Registry Publish, Install, Upgrade, Deprecation & Dependency Resolution

## Status
PASS (one resolver pinning bug found and fixed)

## Objective
Complete lifecycle semantics for sharing versioned packages through a registry without silently changing running worlds.

## Delivered
- `packages/substrate/src/wanxiang_substrate/packages/lifecycle.py` — publish, deprecate, yank, upgrade_candidate, pin install.
- Core fix: `packages/substrate/src/wanxiang_substrate/packages/resolver.py` — explicit root-version pin honored.
- `tests/integration/test_g17f_registry_lifecycle.py` — 4 tests.
- `reports/REGISTRY_LIFECYCLE_QUALIFICATION.md`, `reports/G17F_REPORT.md`.

## Findings
- New publishes never change running instances (pinned); upgrades are explicit.
- Dependency conflicts are actionable; deprecation/yank preserves historical reproducibility.
- Fixed the resolver root-version no-op (P1).

## Evidence
- 4 tests passed; package registry/install regression (20) PASS; ruff/pyright clean.

## Remaining limitations
- A public hosted registry and real distribution are EXTERNAL_BLOCKED; the local/private registry lifecycle is qualified.

## Final checkpoint
- commit: `g17f: registry publish, install, upgrade, deprecation & dependency resolution`
