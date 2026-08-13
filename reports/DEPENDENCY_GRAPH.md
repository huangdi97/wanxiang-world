# Dependency Graph (G13C)

AST-derived `wanxiang_*` import edges between production packages.

| Package | Imports (wanxiang_*) |
|---|---|
| apps/api | packages/application, packages/domain, packages/persistence, packages/runtime |
| packages/application | packages/domain, packages/runtime |
| packages/persistence | packages/domain, packages/runtime |
| packages/runtime | packages/domain |
| packages/substrate | packages/application, packages/domain, packages/runtime |

No import cycles were detected (see ARCHITECTURE_FORENSICS.md cycle check).
