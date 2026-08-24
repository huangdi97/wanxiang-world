# Domain Extension Guide

Concrete world content belongs in a versioned domain or source package, not in
`packages/domain` or another Kernel module. Reuse the single
`DomainRegistry` and declare capabilities, dependencies, schemas, actions, and
rules as data.

## Register a reusable capability

```python
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry

registry = DomainRegistry()
registry.register(
    DomainCapability(
        domain_id="maritime",
        name="Maritime Operations",
        version="1.0.0",
        provides=("vessel", "route", "port"),
        requires=("spatial",),
        schema_refs=("schema://maritime/v1",),
        actions=("depart", "dock"),
        rules=("port_capacity", "crew_duty"),
        compat=("worldpack>=5.2",),
    )
)
```

When composing a source-to-draft pipeline, pass this registry to the existing
`SourceToDraftPipeline(domains=registry)`. The recommender and dependency
resolver choose a deterministic order and add declared requirements. A domain
does not fork runtime state, replace the source registry, or install itself
into the operating system.

## Package boundary

For a distributable extension, scaffold an external domain pack and validate it
before build:

```powershell
uv run python scripts/wxpack.py scaffold ./packs maritime --kind domain
uv run python scripts/wxpack.py validate ./packs maritime
uv run python scripts/wxpack.py build ./packs maritime
```

Keep package tests at the pack boundary. Domain code may propose actions and
interpret observations; the existing resolver and Commit Authority decide
whether a command changes a living instance.

## Design rules

- Do not add world-specific names or laws to Kernel contracts.
- Do not import FastAPI, SQLAlchemy, Alembic, or an LLM SDK into the domain
  layer.
- Do not create a second registry, runtime, event stream, or commit path.
- Keep candidate, completion, evidence, and rights states explicit.
- Add a guard rule and ADR before changing a dependency direction.
