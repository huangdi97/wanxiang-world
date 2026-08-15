# M31 — Kernel/Runtime/Forge/Experiences 收敛 + 全平台兼容 Milestone Qualification

## Status: PASS

## Preconditions (all PASS)
| Goal | Status |
|---|---|
| G34A Kernel Runtime Forge Experiences 责任收敛 | PASS (commit g34a) |
| G34B WorldPack Definition schema v5.2 迁移 | PASS (commit g34b) |
| G34C 数据库与 Ledger 兼容迁移 | PASS (commit g34c) |
| G34D 旧 Event Snapshot Branch 向后回放 | PASS (commit g34d) |
| G34E API SDK Client 兼容 | PASS (commit g34e) |
| G34F 性能与复杂度回归 | PASS (commit g34f) |
| G34G M31 全平台兼容资格验收 | PASS (this gate) |

## Commit range
- From: `13dd137` (M30 gate PASS)
- To: HEAD at M31 PASS (g34a..g34g commits)
- Working tree: clean

## Regression (full gate)
Command: `uv run python scripts/quality.py`

| Check | Result |
|---|---|
| ruff check . | PASS |
| ruff format --check . | PASS |
| pyright (strict) | 0 errors |
| pytest -q | 819 passed, 1 skipped (EXTERNAL_BLOCKED: live PostgreSQL) |
| architecture_check.py | Architecture conformance: PASS |

## Acceptance matrix (M31)
| Item | Status |
|---|---|
| Final Kernel/Runtime/Forge/Experiences boundaries + import rules | PASS |
| WorldPack schema v5.2 (constitution/genesis/evolution/lineage refs; legacy hashes preserved) | PASS |
| DB/Ledger migration 0004 (metadata + lineage index; backup/restore) | PASS |
| Old Event/Snapshot/Branch backward replay (M26 golden hashes) | PASS |
| API/SDK compatibility (17 routes; old endpoints preserved; TS SDK) | PASS |
| Performance regression (commit/replay/tick/lineage bounds) | PASS |
| No God Engine; single authority; kernel import isolation | PASS |

## Performance/complexity
- replay 1200 ev ~35 ms; lineage 400-node query ~23 ms; commit SQLite-bound.
- API routes 17; SDK baseline py=952; migration head 0004.

## Next Milestone prerequisites
- M32 (G35A..G35I): Red Chamber Source Gate + compilation — start G35A after
  M31 gate PASS. Real full-text source is EXTERNAL_BLOCKED until a legal
  traceable edition is available.
