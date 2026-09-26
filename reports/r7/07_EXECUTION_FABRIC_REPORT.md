# R7 07 — Isolated Execution Fabric and Irreversible-Effect Outbox

Status: `IMPLEMENTED` / `VALIDATED` (unit level, real subprocess runs).

## 1. Package

New workspace member `packages/execution` (`wanxiang-execution`, no dependencies
outside the standard library). Production files stay under the 300-line gate.

| Module | Responsibility |
|---|---|
| `errors.py` | typed execution/outbox errors |
| `policy.py` | `ExecutionClass`, `TrustLevel`, access enums and pure `authorize()` |
| `trace.py` | `ExecutionTrace`, `trace_digest`, `environment_hash` |
| `local_process.py` | child environment allowlist, `subprocess` invocation, capture capping |
| `fabric.py` | `ExecutionRequest`/`ExecutionResult`, `LocalProcessProvider` |
| `outbox_records.py` | intent/result/attempt records and the `ExternalEffectHandler` port |
| `outbox.py` | append-only JSONL outbox with a strict record codec |
| `outbox_executor.py` | idempotency, pre-call markers, ambiguity, reconciliation, retry budget |

## 2. Invariants

- Deny by default: an untrusted execution cannot request egress or explicit-grant
  secrets, and `IRREVERSIBLE_EXTERNAL` side effects are rejected outright.
- An execution trace is **not** world history: it can never be appended to
  canonical history, and the module says so in its docstring; the guard test
  checks that no commit/authority module is imported.
- The fabric proposes observations only; it holds no commit path.
- Irreversible external effects go through the outbox: the intent is appended
  before the handler runs, a duplicate idempotency key is suppressed rather than
  re-sent, a crash-leftover marker resolves to a recorded `ambiguous` result, and
  ambiguity is never auto-retried.
- The package is a leaf: the architecture guard confirms it imports no other
  wanxiang package, so untrusted capabilities cannot reach the domain or the
  authority by transitivity.

## 3. Evidence

```text
uv run pytest tests/unit/execution -q                 -> 50 passed
uv run pytest tests/unit -q                           -> 855 passed (at the R7 slice)
uv run ruff check .                                   -> All checks passed
uv run pyright packages/execution tests/unit/execution -> 0 errors
uv run python scripts/architecture_check.py           -> PASS
tests/architecture/test_v51_dependency_topology.py    -> packages/execution: (none)
```

## 4. Not claimed

- Isolation is a local subprocess with a scrubbed environment, not a container,
  VM or seccomp sandbox; the trace reports this honestly (`isolation` map).
- `snapshot_ref`/`resume_ref` are always `None`: snapshot/resume of an execution
  is not implemented.
- No external effect handler is wired to a real third-party service yet; tests
  use local handlers.
