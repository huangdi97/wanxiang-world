# G91A — PressureProfile v1

Date: 2026-08-26  
Status: PASS

## Result

`wanxiang_substrate.reality.pressure.PressureProfile` is a frozen,
schema-versioned Scenario/Domain value object. It carries scarcity, goals,
private information, obligation, authority, reward, sanction, reputation,
time, risk, and norm dimensions, each bounded to `[0,1]`, together with
scenario/domain refs and deduplicated source refs. It is a configuration input
only: it does not represent actor goals, canonical state, events, or authority.

The v1 serializer writes a nested dimension map plus schema/version and
provenance. The reader accepts the flat v0 draft shape (including the
`goal_pressure` spelling) and always emits v1. Fingerprints and matched
zero-pressure profiles are deterministic.

## Evidence

- `tests/unit/substrate/test_g91a_pressure.py`: 7 passed.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.
- Architecture/kernel focused regression: 28 passed.
- `uv run ruff check` and `uv run pyright` on the changed files: PASS; 0
  errors and 0 warnings.
- No `PressureProfile` or pressure-specific type was added to
  `packages/domain` or `packages/runtime`.

G91A is complete and committed. M88 Gate 16 remains pending until the
G91H real playable-world qualification; v5.5 remains `IN_PROGRESS /
NOT_ACCEPTED`. No model training or v5.6 work was performed.
