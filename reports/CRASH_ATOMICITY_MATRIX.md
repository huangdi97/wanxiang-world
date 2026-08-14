# Crash Atomicity Matrix (G14B)

## Transaction boundaries and crash behavior
| Boundary | Crash injection | Recovery guarantee | Evidence |
|---|---|---|---|
| Before append (validation/precondition) | test-only `fail_append` on InMemoryEventStore | no event appended; no state published; idempotent retry commits exactly once | test_g14b_crash_atomicity::test_crash_before_append_leaves_no_trace |
| Append boundary (duplicate command) | re-append same command with valid next seq | DuplicateCommandConflict; one semantic effect | test_g14b_crash_atomicity (store.append retry) |
| After append (state publication / cache) | simulated restart on same DB | restart reconstructs from authoritative event history; same semantic hash | test_crash_after_append_recovers_from_authoritative_history |
| Checkpoint / snapshot | restore after checkpoint | snapshot is an optimization; restore_and_replay matches warm state | test_checkpoint_does_not_break_recovery |
| Retry classification | fresh runtime | acknowledged -> same event; unknown -> fresh commit | test_retry_classification_after_restart |
| Host lifecycle transition | set_mode PAUSED then restart | mode + tick persist via canonical events | test_lifecycle_transition_survives_restart |

## Recovery policy (documented)
- Event history is the authoritative truth; snapshots/caches are discardable optimizations.
- A crash before append leaves no event and no state change (atomic append).
- A crash after append is recovered by replaying committed events on restart.
- Duplicate command retries are idempotent (exactly-once semantic effects at the append boundary).
- Fault-injection hooks (`fail_append`) are test-only and never enabled by production defaults.

## Evidence
- `uv run pytest tests/integration/test_g14b_crash_atomicity.py -q` -> 5 passed.
