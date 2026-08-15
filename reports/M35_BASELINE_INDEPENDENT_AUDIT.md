# M35 Baseline Independent Audit

## Status
PASS (mechanism) — independent baseline audit of the v5.2/M35 frozen surface.

## Scope
Independent re-verification (G38A + M35) of the frozen baselines:
- Kernel v1 ABI golden: `reports/kernel_v1_abi_golden.json` (golden_hash
  `1ec5768b1785852039bccffc3ffd3cf65bdbd5c179807f5f88b9bd7cb882cae5`, 20 entries).
- v5.2 golden compatibility samples: baseline `f27b77249f14c6ef...`, replay
  `7d17aba7b9b76f04...`, migration head `0004_add_world_metadata`.
- SDK/package/API baseline: routes=17, ts=5, py=1176 (additive-only policy).

## Re-run evidence
`uv run pytest tests/architecture/test_v52_baseline_fixtures.py
tests/architecture/test_v52_responsibility_boundaries.py tests/unit/domain/test_worldline.py
tests/unit/substrate/test_rc001_{instantiate,seven_day,worldlines,promotion,chaos}.py
test_worldpack_assembly.py test_promotion_{ladder,pipeline,control}.py test_lineage_graph.py
test_cross_world.py tests/integration/test_autonomous_scheduler.py -q`
-> **68 passed** (commit/replay/branch/lineage/promotion/7-day re-run, goldens reproducible).

## Kernel freeze check
`uv run python scripts/kernel_guard.py` -> 0 violations (domain names / direct
mutation / ABI drift). Kernel v1 frozen after M35 (tag `m35-kernel-v1-freeze`).

## Limitations
- Baseline hashes are frozen for the platform surface; real RedChamber corpus
  baselines remain EXTERNAL_BLOCKED (no legal edition).
