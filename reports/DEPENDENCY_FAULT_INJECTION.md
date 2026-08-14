# Dependency Fault Injection (G14C)

## Fault profiles (test-only adapter)
- `FaultyEventStore` wraps the durable event store and injects:
  - append failure (DB disconnect / disk-full-like) -> `PersistenceError`;
  - load failure (storage unavailability) -> `PersistenceError`.
- Retry policy: bounded by attempt count; each retry is idempotent by command id.

## Behavior under faults
| Fault | Expected | Result |
|---|---|---|
| Append failure | submit surfaces PersistenceError; no event; no success response | PASS (fail-closed) |
| Load failure | read surfaces PersistenceError; recovery without manual DB mutation | PASS |
| Retry storm (5 attempts) | bounded to attempts; one semantic effect after recovery | PASS |
| API write during fault | HTTP 500 with `persistence_error` code (never fake success); healthz still answers | PASS |

## Operator guidance
- Canonical mutation is fail-closed: if the append cannot be proven durable, the command is not reported as committed.
- Recovery is achieved by retrying after the dependency recovers; no manual DB mutation is required.
- Health endpoint remains available during persistence faults so operators can observe liveness; writes fail closed.

## Evidence
- `uv run pytest tests/integration/test_g14c_fault_injection.py -q` -> 4 passed.
