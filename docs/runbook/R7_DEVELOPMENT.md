# R7 Developer Quickstart

R7 is an engineering branch, not a new Stable release.

## Read first

1. `docs/architecture/R7_CORDIS_NATIVE_ARCHITECTURE.md`
2. `docs/architecture/R7_PROFILES_RUNTIME_LOCK_MIGRATION.md`
3. `docs/architecture/R7_CAPABILITY_FOUNDRY_GATEWAY_EXECUTION.md`
4. `docs/architecture/R7_EXPERIENCE_APPLICATION_FABRIC.md`
5. `reports/r7/15_R7_FINAL_CLOSURE_REPORT.md`

## Install and qualify

```bash
uv sync --all-groups --all-packages
pnpm install --frozen-lockfile

uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest -q
uv run python scripts/architecture_check.py
uv run python scripts/kernel_guard.py

pnpm -r lint
pnpm -r typecheck
pnpm -r test
pnpm -r build
```

For exact-SHA closure use `scripts/r7_final_qualification.py` or
`.github/workflows/r7-qualification.yml`.

## Change rules

- never add a second canonical-write path;
- never put canonical world state in Cordis Context;
- consumers depend on versioned seams, not provider internals;
- generated/untrusted code uses Execution Fabric;
- agent/capability output is proposal-side;
- RuntimeLock drift fails closed;
- profile major upgrades use shadow replay + migrate/fork/reject;
- update evidence only after the tested SHA is known.
