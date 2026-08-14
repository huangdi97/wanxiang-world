# Performance, Capacity & Cost Qualification (G16I)

## Profile
- Environment: recorded in `reports/performance_benchmarks.json` (platform, python, machine).
- Profile name: `small_ci` (SQLite durability profile, single process).

## Measured operating envelope (this environment; SQLite fsync-per-commit)
| Operation | Measured |
|---|---|
| Command commit throughput | ~44 events/s (200 commits in ~4.5s; SQLite durability cost) |
| Replay (1200 events) | ~16 ms |
| 90-day autonomous run (9000 ticks) | ~36 s (G15G) |
| Entity growth (90-day) | bounded (24 entities) |

## Bottlenecks before distributed redesign
- Per-commit SQLite fsync dominates commit latency; a batch/group-commit mode or PostgreSQL is the
  evidence-based next step (not speculative).
- Replay is fast (in-memory); snapshot policy is sound.

## Resource budgets
- `ResourceBudget` (max_commands/max_ticks/max_model_calls) is enforced and violations are explicit
  (`BudgetExceeded`); visible in CI/staging.

## Cost hooks
- Model-provider cost hooks are absent by design (no paid APIs in deterministic core);
  `ResourceBudget.max_model_calls=0` in this profile.

## Evidence
- `uv run python scripts/benchmarks.py` -> reports/performance_benchmarks.json.
- `uv run pytest tests/integration/test_g16i_performance.py -q` -> 3 passed.
- No severe regression against the M9/M12 baseline floors; any future regression requires an ADR.
