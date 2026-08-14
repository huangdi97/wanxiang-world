# Upgradeability Audit (G13G)

## Upgrade seams

| Seam | Mechanism | Version guard | Test |
|---|---|---|---|
| DB schema | Alembic migrations 0001 -> 0002 | head pinning; downgrade round-trip | tests/migration/test_migrations.py |
| API vocabulary | openapi-contract.json exported from FastAPI | drift test regenerates+compares | tests/architecture/test_false_completion.py |
| Event schema | CommittedEvent.schema_version / rule_version | ReplayEngine raises IncompatibleVersion | tests/integration/test_g13e_history.py |
| Package SDK | SemanticVersion pins; publishing never mutates pinned install | incompatible upgrade forks | tests/integration/test_package_install.py |
| Projections | server-composed DTOs; projection state discardable | rebuild from events | tests/integration/test_projection_filters.py |

## Dependency freshness

- Python deps are pinned via uv.lock; JS via pnpm-lock.yaml. No forced upgrades;
  freshness changes require a documented reason and full quality re-run.
- LLM/provider SDKs are absent from deterministic core (model_providers empty).
