# G55E Report — Structured Adapters (M52)

## Status
**PASS** — JSON/YAML/CSV/GEDCOM structured adapters implemented on the unified
SourceAdapter ABI (stdlib-only, deterministic, no API).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/structured.py` (new):
   - `StructuredAdapter` implements the G55C `SourceAdapter` ABI.
   - JSON: canonical round-trip (`sort_keys`, compact).
   - YAML: reuses the existing `compiler.yaml_mini` subset parser.
   - CSV: stdlib `csv` reader -> canonical row lines (row/col structure kept
     for later stable locators).
   - GEDCOM: reuses the G09A `parse_gedcom` + `serialize_gedcom` (normalized
     round-trip; never discards unknown records).
   - Typed failures: `MalformedSourceContent` / `UnsupportedSource`.
2. `tests/unit/substrate/test_structured_adapters.py` — 8 tests.

## Reuse
- No second parser/registry: YAML + GEDCOM reuse existing substrate parsers.
- Structured content is produced as canonical text for the uniform pipeline.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_structured_adapters.py -q` | 8 passed |
| ruff / pyright | PASS / 0 errors |

## Local commit
- `goal g55e: Structured adapters (M52)`
