# Goal G13D Acceptance Report — Placeholder, Fake, Dead-path & Surface Integration Audit

## Status
PASS

## Objective
Find false completion: placeholders, mock-only paths, static responses, unconnected UI, dead adapters, duplicated schemas and code that exists but is not reachable in a real vertical slice.

## Key findings & fixes
1. **Architecture-guard placeholder bug (found + fixed, root cause).** `scripts/architecture_check.py::scan_placeholders` used
   `next((pattern.search(line) for pattern in PLACEHOLDER_PATTERNS), None)` which returns the FIRST pattern's result
   (None for TODO on most lines) and never advanced — the guard effectively only ever checked `TODO` and silently
   missed `FIXME`/`XXX`/`NotImplemented`/`placeholder`/`stub`/`mock-only` in production. Fixed to scan all patterns
   (first non-None match) with a documented `return NotImplemented` rich-comparison exception. Regression test added.
2. **Schema drift (found + fixed).** The TS SDK's stable OpenAPI document listed `/worlds/{id}/projection` (GET) and
   `/worlds/{id}/commands` (POST), neither of which exists on the server (server exposes /worlds, /state, /events,
   /actions, /checkpoint, /replay, /branches, /branches/compare, /healthz). Fixed by making the FastAPI app the single
   source of truth: `scripts/export_openapi.py` exports `packages/sdk_ts/src/openapi-contract.json` (10 paths /
   10 operations); the TS SDK test now parses the real contract; a Python drift test regenerates and compares, and
   detects manual edits. Server 10 ops = SDK 10 ops (aligned).
3. **Dead code:** 0 production modules unreferenced.
4. **Hardcoded-state candidates:** 10 large dict literals reviewed and classified as legitimate code literals
   (serialization field maps, GEDCOM record mappings, component defaults, manifest defaults) — not production world truth.
   `synthetic_microworld.py` remains an explicit deterministic fixture.
5. **Surface integration:** every stateful API route resolves `request.app.state.runtime` (WorldRuntime); no route
   returns canned world state. E2E smoke proves committed state appears in the projected `/state` response.

## Delivered
- `scripts/false_completion_scan.py` — placeholder/dead-code/hardcoded-state scanners, surface-integration map, schema-drift audit.
- `scripts/export_openapi.py` + `packages/sdk_ts/src/openapi-contract.json` — canonical OpenAPI contract from the server.
- `reports/FALSE_COMPLETION_AUDIT.md`, `reports/SURFACE_INTEGRATION_MAP.md`, `reports/SCHEMA_DRIFT_AUDIT.md`,
  `reports/false_completion_audit.json`, `reports/G13D_REPORT.md`.
- `tests/architecture/test_false_completion.py` — 7 tests.
- `packages/sdk_ts` — openapi.test.ts now consumes the real contract (22 TS tests pass); tsconfig resolveJsonModule.

## Evidence
| Check | Result |
|---|---|
| `uv run python scripts/false_completion_scan.py` | placeholders=0 dead=0 hardcoded=10(candidates) drift_aligned=True |
| `uv run python scripts/quality.py` | PASS — ruff, pyright 0, 410 pytest, architecture PASS |
| `npm run typecheck` + `npm test` (sdk_ts) | PASS — 22 tests |
| E2E smoke (server truth) | PASS — committed entity appears in `/state` projection |

## Remaining limitations
- AST-based scans cannot prove runtime behavior; complemented by E2E and the 410-test suite.
- 10 hardcoded literals remain as reviewed code literals (documented in FALSE_COMPLETION_AUDIT.md).

## Final checkpoint
- commit: `g13d: placeholder, fake, dead-path & surface integration audit`
