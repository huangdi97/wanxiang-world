# G91G — Pressure Behavior Benchmark

Date: 2026-08-26  
Status: PASS

## Result

`PressureBehaviorBenchmark` runs matched pressure-enabled and zero-pressure
traces with the same seed, profile identity/fingerprint, and horizon. It emits
deterministic action traces, derived engineering metrics, metric deltas, trace
hashes, and a validity envelope. Repeated runs reproduce the same hashes.

The result is explicitly scoped to a deterministic synthetic engineering
reference benchmark. `scientific_claim` is false; the report does not infer
causality, biological behavior, or general-world validity from one run. No
model training or external provider is involved.

## Evidence

- `tests/unit/substrate/test_g91g_pressure_benchmark.py`: 2 passed.
- Same-seed/profile/horizon matching and repeatability assertions pass.
- `uv run ruff check`, format check, and `uv run pyright` on changed files:
  PASS; 0 errors and 0 warnings.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.

G91G is complete and committed. G91H is next; M88 Gates 16-20 remain pending
until the real playable-world qualification, and v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED`. No model training or v5.6 work was performed.
