# V5.1 Package Dependency Graph (G21D)

> Deterministic AST edge scan (package -> imported package).

| package | target responsibility | imports |
|---|---|---|
| apps/api | infrastructure (API composition root) | packages/application, packages/domain, packages/persistence, packages/runtime, packages/substrate |
| packages/application | application (orchestration facade) | packages/domain, packages/runtime |
| packages/cordis_host | EXPERIMENTAL (R7 Cordis composition host, TS) | (none) |
| packages/domain | core | (none) |
| packages/execution | EXPERIMENTAL (R7 isolated execution fabric) | (none) |
| packages/observability | infrastructure (telemetry) | (none) |
| packages/persistence | infrastructure (persistence) | packages/domain, packages/runtime |
| packages/reality | EXPERIMENTAL (R7 versioned reality semantics) | (none) |
| packages/research | EXPERIMENTAL (research namespace) | packages/domain |
| packages/runtime | core | packages/domain |
| packages/sdk_ts | infrastructure (TS SDK, generated contract) | (none) |
| packages/substrate | definition+runtime+agency+experience (modular monolith substrate) | packages/domain, packages/runtime |
