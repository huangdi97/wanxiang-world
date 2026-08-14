# Concurrency Adversarial Qualification (G14A)

## Concurrency strategy (documented)
- Canonical writes are serialized through the application runtime: each world instance/branch has a
  strictly ordered event stream, and `CommitAuthority.commit` enforces `expected_revision == current
  revision` before append (StaleRevision) plus command-id idempotency (DuplicateCommandConflict).
- Persistence (SQLite) uses a single process-bound runtime; multi-client semantics are expressed as
  concurrent *command streams* with explicit expected revisions, not raw concurrent DB writers.
- The event store enforces strict per-branch `event_seq` ordering at append; duplicates/out-of-order
  appends are rejected at the boundary.

## Adversarial scenarios (tests/integration/test_g14a_concurrency.py)
| Scenario | Expected behavior | Result |
|---|---|---|
| Lost-update attack (two clients, same expected revision) | one commits; other gets explicit StaleRevision; no invalid event | PASS |
| Duplicate command retry across process restart | one semantic effect; duplicate=True returns the same event | PASS |
| Out-of-order delivery | explicit StaleRevision; no partial state; recovery on retry | PASS |
| Independent instances interleaved | per-instance seq 1..n; no cross-contamination; distinct hashes | PASS |
| 20-command burst | valid contiguous seq; unique command ids | PASS |

## Performance tradeoffs
- Expected-revision checks add O(1) per commit and guarantee no lost updates without cross-world locking;
  unrelated worlds/instances are not globally serialized.

## Evidence
- `uv run pytest tests/integration/test_g14a_concurrency.py -q` -> 5 passed.
- Canonical event sequence remains valid under all stress scenarios; race failures produce structured errors
  (StaleRevision) and the accepted path records an audit trace.
