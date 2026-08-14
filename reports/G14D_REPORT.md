# Goal G14D Acceptance Report — Event, Snapshot, Branch & History Corruption Adversarial Qualification

## Status
PASS (one snapshot-corruption gap found and fixed)

## Objective
Attack persisted history with gaps, duplicates, wrong branch IDs, hash mismatches, unsupported versions and damaged snapshots to prove corruption is detected rather than normalized away.

## Findings
- All corruption corpus types are detected with precise errors/diagnostics.
- **Fixed (P1)**: `restore_and_replay` silently used a corrupted snapshot baseline, producing a wrong semantic
  hash with no error. Now snapshots are validated against event history; invalid/unreadable snapshots fall back
  to authoritative event replay, observable via `RestoreResult.snapshot_rejected`.

## Delivered
- `scripts/history_diagnostics.py` — read-only corruption diagnostics (identifies affected event + kind).
- `tests/integration/test_g14d_corruption.py` — 7 tests (corpus + snapshot fallback + read-only scan safety).
- Core fix: `packages/application/src/wanxiang_application/world_runtime.py` (snapshot validation + fallback).
- `reports/HISTORY_CORRUPTION_ADVERSARIAL.md`, `reports/G14D_REPORT.md`.

## Evidence
- `uv run pytest tests/integration/test_g14d_corruption.py -q` -> 7 passed.
- Snapshot/replay/restore regression (23 tests) PASS; no silent semantic drift.

## Remaining limitations
- Auto-repair tools are intentionally absent; remediation is documented and auditable.

## Final checkpoint
- commit: `g14d: event, snapshot, branch & history corruption adversarial qualification`
