# Module Boundaries & Dependency Direction (M0)

Normative source: `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md` ?8.
Enforcement: `scripts/architecture_check.py` (part of the normal quality gate).

## Physical packages

```text
apps/
  api/                 # transport only (introduced in GOAL_01F)
packages/
  domain/              # pure semantic types/value objects/invariants
  application/         # use cases and orchestration ports
  runtime/             # validate/resolve/commit/replay coordination
  persistence/         # repositories/event store/snapshot adapters (ORM confined here)
  evidence/            # source/evidence/rights core contracts
  model_providers/     # optional model provider ports + deterministic fakes
  observability/       # structured logging, settings, secret redaction
  sdk_ts/              # TypeScript SDK baseline (no Python dependency)
```

## Allowed dependency direction

```text
domain
  ?
evidence contracts (never persistence/web)
  ?
application ports/use-cases
  ?
runtime orchestration
  ?
persistence/adapters and transport
```

- `domain` imports nothing outside stdlib and `wanxiang_domain` itself.
- `persistence` may depend on `domain` (and application port interfaces) but never on web.
- `model_providers` never touches canonical persistence internals.
- `apps/api` is thin: maps transport to application/runtime use cases; no ORM, no canonical rules.

## Enforced forbidden imports (current rules)

| Package | Forbidden top-level modules |
|---|---|
| packages/domain | fastapi, sqlalchemy, alembic, wanxiang_api, httpx, requests, openai, pydantic |
| packages/evidence | fastapi, sqlalchemy, alembic, wanxiang_persistence, httpx, requests |
| packages/application | fastapi, sqlalchemy, alembic, wanxiang_api, httpx, requests |
| packages/runtime | fastapi, sqlalchemy, alembic, wanxiang_api, wanxiang_persistence, httpx, requests |
| packages/persistence | fastapi, wanxiang_api |
| packages/model_providers | fastapi, sqlalchemy, alembic, wanxiang_persistence |
| packages/observability | fastapi, sqlalchemy, alembic |
| apps/api | sqlalchemy, alembic, wanxiang_persistence |

## Other guard rules

- Import cycles between packages are rejected (AST-based graph DFS).
- Production source files target <= 300 lines; generated files (header marker)
  are exempt and reported.
- Committed secrets (API keys, private keys, quoted password/secret values) are rejected.
- TODO/FIXME/placeholder/NotImplemented/stub/mock-only markers are rejected in
  production source paths (docs/tests may discuss these words).

## Adding a boundary

To forbid a new dependency, edit `FORBIDDEN_IMPORTS` in
`scripts/architecture_check.py` and add a negative test in
`tests/architecture/test_architecture_guards.py`.
