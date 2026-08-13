# Command Queue & Idempotent Multi-client Semantics (G06B)
Ownership: `wanxiang_substrate.queue`.

## Queue
`CommandQueue` is a bounded per-instance/branch intake with dedup by command
id, serialized drain (total order per branch), structured submission statuses
(accepted/conflict/rejected/duplicate) and backpressure (`QueueFull`).

## Idempotency
Retries of the same command id across reconnects are recognized as duplicates
and never produce a second world effect; M1 idempotency is preserved under
concurrent submissions. Conflicting expected revisions surface as `conflict`
without either half-committing.