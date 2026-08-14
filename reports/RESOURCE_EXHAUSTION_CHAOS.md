# Resource Exhaustion & Chaos Qualification (G14I)

## Declared stress profile (measured in this environment; no invented capacity numbers)
- Fuzz: 200 seeded structured commands (valid/invalid actions, hostile payloads) with per-step invariant checks.
- Long stream: 1200 committed events on one branch; replay from clean state must reproduce the same semantic hash.
- Backpressure: queue capacity 2-64; over-capacity enqueue -> QueueFull (predictable rejection, no corruption).
- Resource budget: max_commands=5 -> 6th consume -> BudgetExceeded (predictable).
- Repeated failures: 50 invalid actions -> 50 structured rejections; world untouched; valid command still works.

## Results
| Scenario | Result |
|---|---|
| Fuzzed commands never violate event-seq/revision invariants | PASS (200 iterations, stream valid at every step) |
| Long stream replays stably; growth linear and deterministic | PASS (1200 events -> 1200 entities, stable hash) |
| Over-budget load fails predictably (QueueFull / BudgetExceeded) | PASS |
| Repeated failures surface structured errors; world continues | PASS |
| M11 adversarial suites (G14A-H) | 45 passed |
| Full quality gate | PASS — 473 pytest, ruff, pyright, architecture |

## Envelope
- Canonical event sequence remains valid under the declared profile; over-budget load fails with explicit
  backpressure/rejection, never corruption. Unproven scale claims are excluded from release docs.
