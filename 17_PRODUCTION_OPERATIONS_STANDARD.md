# Production & Operations Standard

Productionization means reproducible operation, not merely Docker files.

Required concerns: typed config, secret handling, health/readiness, production DB qualification, background work semantics, durable assets, observability, authz, rate/resource controls, backup/restore, release artifacts, migration preflight, rollback/fallback policy, capacity benchmarks and operator runbooks.

The baseline private/staging profile should stay as simple as evidence permits. Do not introduce microservices, queues or caches without a failure-domain/performance reason. Every additional stateful component creates new migration, backup, security and observability obligations.

Production deployments must never default to deterministic test Fakes. Development/tests must remain runnable without paid external services.
