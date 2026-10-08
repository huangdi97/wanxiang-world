# G55A Report — SourceRecord Convergence (M52)

## Status
**PASS** — SourceRecord unified with version / checksum / rights / access /
reliability / schema; registry dedupe is version-aware (no silent overwrite).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/model.py` (EXTEND):
   - `SourceRecord` convergence fields: `version` (edition/version), `access`
     (public/private/restricted), `reliability` (0..1), `schema_version`.
   - `SourceAccess` literal + validation.
   - `fingerprint()` = kind:content_hash:version (stable source identity).
   - `canonical_json` includes all convergence fields (audit-stable).
2. `packages/substrate/src/wanxiang_substrate/sources/registry.py` (EXTEND):
   - Dedupe by fingerprint (kind+hash+version): same content new version =
     new registration; same fingerprint = DuplicateSource.
   - `transition()` preserves all convergence fields.
3. `tests/unit/substrate/test_source_record_convergence.py` — 9 tests.

## Backward compatibility
- Existing 26 `SourceRecord(` call sites keep working (new fields defaulted).
- `test_duplicate_content_rejected` still passes (same content + same default
  version "1" → DuplicateSource).
- Existing source-gate / registration suites: 11 passed.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_source_record_convergence.py -q` | 9 passed |
| `pytest tests/integration/test_source_gate.py tests/unit/substrate/test_red_chamber_source_registration.py -q` | 11 passed |
| ruff / pyright | PASS / 0 errors |

## Local commit
- `goal g55a: SourceRecord convergence (M52)`
