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
