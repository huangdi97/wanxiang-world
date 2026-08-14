# Host & Multiplayer Chaos Qualification (G14E)

## Scenarios
| Scenario | Expected | Result |
|---|---|---|
| Reconnect resync | stale client rejected (StaleRevision); resync from server history; retry with correct revision commits | PASS |
| Many clients via command queue | strict per-branch order (event_seq 1..n); unique command ids; duplicate id rejected | PASS |
| Slow client backpressure | bounded queue (QueueFull, observable); world advances independently; stale queued commands rejected as conflict (never silently applied) | PASS |
| Lease ownership | unique primary controller per actor (LeaseConflict on second acquire); expire -> recover | PASS |

## Design notes
- Clients/projections never become alternative authorities: all writes go through CommitAuthority with
  expected-revision semantics; client caches are discardable.
- Backpressure is explicit (QueueFull) rather than an unbounded queue; the canonical world advances
  independently of slow consumers.
- Embodiment leases enforce one primary controller per actor; disconnect recovery is via expire/re-acquire.

## Evidence
- `uv run pytest tests/integration/test_g14e_host_multiplayer.py -q` -> 4 passed.
