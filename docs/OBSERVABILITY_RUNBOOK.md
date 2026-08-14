# Observability Runbook (G16E)

## Telemetry model
- Spans correlate `trace_id`, `world_id`, `branch_id`, `command_id`, `stage`, `status`, `latency_ms`,
  and an optional `error_code` — never sensitive payloads or private memory.
- Metrics: counters (commands_failed, queue_full, ...) and gauges (queue_depth).
- No-op exporter by default; in-memory exporter for local diagnostics; a local OTel collector can consume
  the same records (no commercial backend required).

## Diagnosing a failing command
1. Submit the command with a `command_id`.
2. Query spans by `trace_id` (or filter by `command_id`): stages `intake -> commit`.
3. A `status=error` span carries `error_code` (e.g., `validation_rejected`, `persistence_error`).
4. Correlate with metrics: `commands_failed` increments; saturation signals like `queue_full` and
   `queue_depth` gauge.

## Example queries (in-memory exporter)
- `obs.trace("trace_fail_1")` -> the full span chain.
- `obs.metrics.counters["commands_failed"]` -> failure count.
- `obs.metrics.gauges["queue_depth"]` -> current saturation.

## SLO-style internal targets (engineering objectives, not marketing claims)
- Command commit latency and error rates are measurable via spans/metrics; targets are set per deployment
  profile after baseline measurement (recorded in reports/OBSERVABILITY_QUALIFICATION.md).

## Redaction policy
- Private memory/source secrets are never logged by default; span fields are ID/status/latency only.
