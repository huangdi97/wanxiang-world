# Background Execution & Work Queue Qualification (G16C)

## Work-item contract
- Work items are `CommandEnvelope`s with a **command_id idempotency key**.
- Delivery semantics: at-least-once intake with in-process dedup (DuplicateQueuedCommand) +
  command-id idempotency at the Commit Authority boundary -> exactly-once semantic effects.

## Queue choice (documented)
- In-process `CommandQueue` (bounded capacity, serialized drain, statuses: accepted/conflict/rejected/duplicate).
- No Redis/Celery/Kafka by default: the modular-monolith profile has no measured need; adding one requires
  evidence and a failure-domain/performance justification.

## Qualification results
| Check | Result |
|---|---|
| At-least-once redelivery cannot duplicate semantic effects | PASS |
| Failed job is diagnosable (status + message) and retryable | PASS |
| Queue pressure (QueueFull) cannot corrupt the world (stream valid; world advances) | PASS |
| Replay/verifiability after queued execution | PASS |

## Retry/dead-letter semantics
- Retry uses a new idempotency key for corrected jobs; the original failed job stays diagnosed in queue history.
- Over-capacity intake is rejected explicitly (QueueFull), never silently dropped.

## Evidence
- `uv run pytest tests/integration/test_g16c_background_queue.py -q` -> 3 passed.
