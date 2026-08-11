# Goal 01D Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: f8692cb (goal 01C checkpoint)
- working-tree notes: clean

## Objective
Make Wanxiang history operational: snapshots, replay of committed event
streams, isolated branches, semantic state comparison and deterministic
reconstruction.

## Delivered
- `wanxiang_runtime.replay`: ReplayEngine (contiguous seq, fork-aware revision
  check, instance/branch match, schema/rule version checks).
- `wanxiang_runtime.snapshot`: SnapshotStore protocol, create_snapshot_metadata,
  InMemorySnapshotStore (save/load/latest at-or-before revision).
- `wanxiang_runtime.branch`: BranchRepository, fork_branch (explicit ancestry,
  invalid-fork rejection).
- `wanxiang_runtime.diff`: StateDiff + diff_states.
- Commit Authority now fork-aware via `branch_base_revision`.
- Golden replay fixture `tests/fixtures/golden_replay_v1.json` (5 events, pinned
  hash) + generator script.
- `docs/architecture/REPLAY_BRANCHING.md`.

## Key architecture decisions
- Replay uses the same apply path as Commit Authority (no second mutation model).
- Child branch revision = fork_revision + own event count; event_seq is the
  child's own append position; event revision = baseline + seq (fork-aware).
- Snapshot content is the immutable state; content_ref is opaque (durable
  storage in 01E).

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS | |
| Pyright strict | `uv run pyright` | PASS (0 errors) | |
| Pytest | `uv run pytest -q` | 93 passed | tests/unit/runtime, tests/property |
| Architecture | `uv run python scripts/architecture_check.py` | PASS | |
| Full gate | `uv run python scripts/quality.py` | PASS | |

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Derived state can be discarded and rebuilt | PASS | snapshot+remaining replay tests |
| Replay final semantic hash equals original | PASS | golden fixture + property tests |
| Child mutations do not affect parent | PASS | branch isolation test |
| Corrupt history not silently accepted | PASS | gap/corrupt/version tests |
| Golden fixture committed and documented | PASS | golden_replay_v1.json + notes |
| No alternate hidden state-update pathway | PASS | replay uses state.apply |

## Migrations / compatibility
- Golden fixture schema v1; generator script documented.

## Security / rights impact
- None beyond prior goals.

## Known limitations
- In-memory snapshot/branch repositories; durable adapters in GOAL_01E.

## External blockers
None.

## Final checkpoint
- commit: `goal 01D: add replay snapshots and isolated branches`
