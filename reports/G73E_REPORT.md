# G73E Report — CI matrix, API/SDK contracts, and package release smoke

**PASS (2026-08-25)**

G73E requalified the repository's generated API contract, SDK compatibility
surface, package authoring path, TypeScript SDK, and full Python quality gate.
The Windows test harness was made workspace-local for the affected temporary
database/architecture probes; this changes test isolation only and does not
change product semantics.

| Gate | Result | Evidence |
|---|---|---|
| OpenAPI export | PASS | 38 paths / 39 operations from `scripts/export_openapi.py` |
| SDK baseline | PASS | 39 API routes, 5 TypeScript symbols, 1472 Python public names |
| Contract drift tests | PASS | OpenAPI/SDK contract tests: 4 passed, 1 warning |
| Python quality | PASS | `scripts/quality.py`: 1201 passed, 1 skipped, 2 warnings; Ruff, format, Pyright, architecture all green |
| Kernel freeze guard | PASS | 0 violations |
| TypeScript SDK | PASS | install, lint, typecheck, build; Vitest 6 files / 22 tests |
| `wxpack` CI sequence | PASS | scaffold, validate, build, certify; public SDK-only imports and runtime install |
| Release manifest | PASS | version `0.1.0`, migration head `0004_add_world_metadata`, reproducible build hash |
| Workspace temp portability | PASS | 15 targeted tests passed; `WANXIANG_TEST_TMP` and workspace scratch avoid restricted user-temp ACLs |

The one skipped Python test is the documented live PostgreSQL integration
without a local service; PostgreSQL migration/integration remains a CI service
job rather than an invented local PASS. No source bytes, private family data,
provider credentials, model cache, or training artifact were added.

The generated OpenAPI contract and SDK baseline are committed together with
their drift assertions. Providers remain proposal-only, concrete worlds remain
outside Core, and all canonical mutation remains behind the existing Commit
Authority.
