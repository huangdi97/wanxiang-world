# V5.2 Backward Compatibility Report

## Summary
The v5.2 platform (frozen at M31) preserves old v5.0/v5.1 world history and
client surfaces. Evidence below is from the current worktree (verified, not
from memory).

## 1. Old history replay / snapshot / branch
- `tests/fixtures/v5_2_baseline/` (M26 golden): events.json / snapshot.json /
  branch.json — replayed/restored/forked under v5.2 with identical semantic
  hashes (see `tests/integration/test_g34d_backward_replay.py`, 4 tests).
- Golden replay hash `7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00`
  unchanged (`test_golden_replay.py`).
- Baseline combined hash `f27b77249f14c6ef5b8b1b10689e69659e9405d6ccf6f0c75d3f4be952c47ecf`
  reproducible (`test_v52_baseline_fixtures.py`).

## 2. Migration compatibility
- Migration chain 0001 -> 0002 -> 0003 -> 0004; old DB copy upgraded to head
  keeps event count and replay hash (`test_g34c_db_migration.py`); downgrade
  0004 -> 0003 restores the old schema.
- WorldPack legacy manifests round-trip unchanged (canonical excludes the new
  v5.2 refs when absent; `test_worldpack_migration.py`).

## 3. API / SDK / client surfaces
- Old world/branch endpoints preserved (no breaking removal): /worlds,
  /worlds/{id}/state|events|actions|branches|branches/compare|checkpoint|replay,
  /healthz (verified by `test_constitution_api.py` OpenAPI diff review +
  old-client smoke).
- New v5.2 resources added additively: /lineage/* (G31G/G33F),
  /constitutions/{id} (G34E), /lineage/promotions (admin-gated).
- SDK baseline: routes=17, ts=5, python=952 (regenerated;
  `test_g17a_sdk_contract.py` drift green).

## 4. Determinism / authority
- Single CommitAuthority commit path (forensics commit_paths=1).
- New v5.2 fields (commit kinds, version context) default to legacy for old
  events (G30F/G30H/G34D).
