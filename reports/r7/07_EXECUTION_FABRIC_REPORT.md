# R7 07 — Execution Fabric and Irreversible-Effect Boundary

Status: `IMPLEMENTED / VALIDATED` for R7 reference scope.

`packages/execution` provides deny-by-default policy, a real local subprocess
provider, bounded output capture, environment scrubbing and ExecutionTrace
evidence. Execution output is Observation/Proposal and has no canonical writer.
Process isolation is not claimed as a hostile-code container/microVM sandbox.

The irreversible-effect path is exercised through a real cross-process localhost
HTTP handler, not an in-function fake. Integration covers durable intent,
idempotency/duplicate suppression, crash-before-answer ambiguity, timeout,
bounded retry, restart/journal reconstruction, explicit reconciliation and
identifiers-only external journal/no secret leakage.

Evidence:
- `tests/integration/test_r7_effect_outbox.py`
- `scripts/r7_effect_sink.py`
- execution unit/architecture tests.

This is real reference I/O, not a claim about production payment/SaaS/robot/
chain/device integration.

```text
Execution Success != World Truth
Committed External Intent != External Effect succeeded
```


## Extended R7 execution closure (2026-10-08)

The Execution Fabric now also contains a provider-neutral `ExecutionRouter`.
Callers select an `ExecutionPolicy`; they do not import a Docker/process
implementation directly. Local process and Docker container providers declare
their execution classes behind the same seam.

A real CI container qualification builds a local rootfs image without registry
pulls and verifies read-only root filesystem, no external network, no host
mounts, dropped Linux capabilities, bounded resources and proposal-only output.
This is stronger reference isolation than the original subprocess slice, while
still **not** claiming that Docker alone is a hostile-code security proof.

Execution checkpoint/resume is implemented at a completed boundary: identical,
side-effect-free work can fast-forward from content-addressed trace/output
evidence after restart. Secret-bearing or externally side-effecting executions
are deliberately excluded and continue through the Outbox/reconciliation path.

The design boundary remains:
`ExecutionTrace != World History`,
`container snapshot != World Branch`,
`execution success != World truth`.
