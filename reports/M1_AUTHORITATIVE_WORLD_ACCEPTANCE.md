# M1 ? Authoritative World Acceptance

- Date: 2026-08-12
- Milestone: M1 Authoritative World Exists
- Verdict: **PASS**
- Evidence bundle: deterministic synthetic micro-world over SQLite; no LLM key.

## 1. Executive summary

Wanxiang now has an authoritative, replayable, branchable world kernel. A
synthetic micro-world (two persons holding a transferable resource + gift
relation) can be instantiated, receive validated/resolved commands, commit
ordered events exactly once through a single Commit Authority, persist
durably, snapshot, replay to the same canonical semantic hash, fork isolated
branches, reject duplicate/stale/invalid commands, and reproduce all of this
without an LLM key.

## 2. Acceptance scenarios (A1-A10, from 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md ?4)

| # | Scenario | Result | Evidence |
|---|---|---|---|
| A1 | Valid commit changes state exactly once | PASS | test_a1_valid_commit_changes_state_exactly_once |
| A2 | Invalid command does not mutate | PASS | test_a2_invalid_command_does_not_mutate |
| A3 | Duplicate command idempotency | PASS | test_a3_duplicate_command_is_idempotent |
| A4 | Stale revision rejected | PASS | test_a4_stale_revision_is_rejected |
| A5 | Snapshot + remaining replay == semantic hash | PASS | test_a5_snapshot_plus_remaining_replay |
| A6 | Full replay from initial baseline | PASS | test_a6_full_replay_from_initial_baseline |
| A7 | Branch isolation (child does not mutate parent) | PASS | test_a7_branch_isolation |
| A8 | Deterministic reproduction (same inputs -> same hash) | PASS | test_a8_deterministic_reproduction |
| A9 | Corrupt/incompatible stream fails explicitly | PASS | test_a9_corrupt_stream_fails_explicitly |
| A10 | Migration compatibility + durable replay | PASS | test_a10_durable_replay_matches_golden + tests/migration |

## 3. M1 qualification questions (master prompt ?22)

1. Is there exactly one Commit Authority for Canonical State? **YES** ? only
   `CommitAuthority.commit` mutates; `InMemoryCanonicalState` has no public mutator.
2. Any bypass mutation path? **NO** ? architecture guard + authority tests.
3. Is the Event Store the authoritative history? **YES** ? append-only, ordered,
   integrity-checked; snapshots are baselines only.
4. Can Derived State be discarded and rebuilt? **YES** ? snapshot + events replay.
5. Is Replay deterministic? **YES** ? golden fixture hash
   `7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00` reproducible.
6. Are branches isolated? **YES** ? child commits never touch parent stream/hash.
7. Are duplicate commands idempotent? **YES** ? prior result returned, no
   duplicate event/effect.
8. Are stale revisions rejected? **YES** ? typed `StaleRevision` (409 via API).
9. Does persistence restart recover? **YES** ? durable SQLite reload + replay.
10. Is migration tested? **YES** ? fresh upgrade, pre-head fixture upgrade
    (0001 -> head), downgrade round trip.
11. Is Core fully LLM-free? **YES** ? no model provider in the authoritative path.
12. Any TODO/mock/placeholder affecting M1? **NO** ? placeholder guard passes.
13. Any architecture boundary violation? **NO** ? guard passes.
14. Giant files / obvious tech debt? **NO** ? no production file > 300 lines.
15. **M1 = PASS.**

## 4. Quality suite (final tree)

| Check | Command | Result |
|---|---|---|
| Ruff lint + format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 130 passed |
| Architecture conformance | `uv run python scripts/architecture_check.py` | PASS |
| Full gate | `uv run python scripts/quality.py` | PASS |
| API contract | OpenAPI smoke (tests/api) | PASS |

## 5. Commits

- goal 01F checkpoint (this batch's final implementation commit).
- Milestone tag `m1-authoritative-world` created at PASS.

## 6. Known limitations (honest)

- PostgreSQL not exercised locally (compatible SQL, documented; compose available).
- Starlette deprecation warning re: httpx2 for TestClient (test-only).
- Synthetic micro-world resolvers live in the application layer, clearly marked
  synthetic; real domain packs are future packages.
- Snapshot restore on forked branches falls back to parent-state replay (no
  child-specific snapshot baseline yet).
