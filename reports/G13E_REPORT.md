# Goal G13E Acceptance Report — Event, Replay, Branch, Migration & Version Forensics

## Status
PASS (with a P0 replay/branch bug found and fixed in this Goal)

## Objective
Re-verify the semantic-history foundation under all features added after M1 and detect any event/version/migration behavior that could silently corrupt historical worlds.

## Critical finding (P0) — fixed
**Child-branch replay failed on cold restore.** `ReplayEngine._check_event` used a single counter for both
`event_seq` and `revision`. Child branches carry a branch-local `event_seq` (restarts at 1) while `revision`
continues from the fork baseline (fork_revision + n). Cold reads of a forked world (after cache invalidation or
restart) and `restore_and_replay` on a child branch failed with `CorruptEventStream: expected event seq 3, got 1`.

Fix (root cause, no weakening):
- `ReplayEngine.replay` now checks `event_seq` and `revision` as independent counters, with an explicit
  `start_seq` parameter: default `baseline.revision + 1` (snapshot continuation, root branch) vs `start_seq=1`
  (child branch local stream).
- `StateReader.state_at` and `WorldRuntime.restore_and_replay` pass `start_seq=1` for child branches.
- Corruption guard retained: out-of-order/gapped sequences still raise `CorruptEventStream` (regression test added).

## Verification
| Check | Result |
|---|---|
| Golden fixture replay | hash matches fixture expected hash |
| Synthetic micro-world history replay | stable hash across clean replay |
| Unsupported schema/rule version | IncompatibleVersion (explicit, no silent adoption) |
| Version-pinned instance vs rule drift | IncompatibleVersion |
| Child branch cold replay + restore_and_replay | PASS — same semantic hash as warm path |
| Migration 0001 -> head preserves replay hash | PASS |
| `uv run python scripts/quality.py` | PASS — ruff/pyright, 417 pytest, architecture PASS |

## Delivered
- `scripts/history_forensics.py` + `reports/REPLAY_GOLDEN_CORPUS.md`,
  `reports/VERSION_COMPATIBILITY_MATRIX.md`, `reports/HISTORY_COMPATIBILITY_FORENSICS.md`,
  `reports/history_forensics.json`, `reports/G13E_REPORT.md`.
- `tests/integration/test_g13e_history.py` — 7 tests.
- Core fix: `packages/runtime/src/wanxiang_runtime/replay.py`,
  `packages/application/src/wanxiang_application/state_reader.py`,
  `packages/application/src/wanxiang_application/world_runtime.py`.

## Compatibility matrix (summary)
- Supported event schema/rule versions: 1. Unsupported (0,2,99): explicit IncompatibleVersion.
- Migrations: 0001_initial -> 0002_add_event_seq_index (head); downgrade round-trip covered by existing tests.
- Packages: SemanticVersion pins; publishing never mutates a pinned install; incompatible upgrades fork.
- Correction policy: new events/branches or explicit migration semantics; no silent mutation.

## Remaining limitations
- Real external data remains EXTERNAL_BLOCKED as labeled; deterministic history qualification is complete.

## Final checkpoint
- commit: `g13e: event, replay, branch, migration & version forensics`
