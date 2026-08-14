# V5.1 Package Dependency Graph (G21D)

> Deterministic AST edge scan (package -> imported package).

| package | target responsibility | imports |
|---|---|---|
| apps/api | infrastructure (API composition root) | packages/application, packages/domain, packages/persistence, packages/runtime, packages/substrate |
| packages/application | application (orchestration facade) | packages/domain, packages/runtime |
| packages/domain | core | (none) |
| packages/observability | infrastructure (telemetry) | (none) |
| packages/persistence | infrastructure (persistence) | packages/domain, packages/runtime |
| packages/research | EXPERIMENTAL (research namespace) | packages/domain |
| packages/runtime | core | packages/domain |
| packages/sdk_ts | infrastructure (TS SDK, generated contract) | (none) |
| packages/substrate | definition+runtime+agency+experience (modular monolith substrate) | packages/domain, packages/runtime |
