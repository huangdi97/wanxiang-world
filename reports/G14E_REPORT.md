# Goal G14E Acceptance Report — World Host, Multiplayer, Reconnect, Ordering & Backpressure Chaos

## Status
PASS

## Objective
Stress host lifecycle and network command ordering to prove sessions/projections can disconnect and recover without becoming alternative authorities.

## Delivered
- `tests/integration/test_g14e_host_multiplayer.py` — 4 tests.
- `reports/HOST_MULTIPLAYER_CHAOS.md` — scenarios, design notes, evidence.
- `reports/G14E_REPORT.md`.

## Findings
- Reconnect resyncs from authoritative server history; stale client writes are rejected explicitly.
- 30-client burst through the command queue preserves strict per-branch order and idempotency.
- Backpressure is bounded and observable (QueueFull); the world advances independently of slow clients;
  stale queued commands are reported as conflict, never silently applied.
- Embodiment lease ownership is unique per actor; disconnect recovery via expire/re-acquire works.

## Evidence
- `uv run pytest tests/integration/test_g14e_host_multiplayer.py -q` -> 4 passed.

## Remaining limitations
- Real network transport/latency is not simulated; ordering/backpressure semantics are covered deterministically
  at the host/queue layer.

## Final checkpoint
- commit: `g14e: world host, multiplayer, reconnect, ordering & backpressure chaos`
