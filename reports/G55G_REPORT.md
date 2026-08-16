# G55G Report — Ingestion Security (M52)

## Status
**PASS** — Pre-ingest security gate: zip bomb / path traversal / size /
encoding / encrypted / corrupt / rights checks with typed failures.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/security.py` (new):
   - `IngestSecurityGate.check_blob` — size limit (256 MiB default), text
     encoding validity (utf-8/utf-16/gb18030), archive checks for epub/docx.
   - `check_archive` — zip-bomb uncompressed/compressed ratio (default 200x),
     member path traversal (`..`, absolute, drive-letter), encrypted members
     (flag_bits 0x1), CRC corruption (`testzip`).
   - `IngestSecurityGate.check_archive` — typed raising path for open archives.
   - Typed errors: `IngestSecurityError`, `SourceSizeExceeded`, `ZipBomb`,
     `PathTraversal`, `EncryptedSource`, `CorruptSource`, `UndecodableSource`.
2. `tests/unit/substrate/test_ingestion_security.py` — 10 tests (incl. negative
   attacks: zip bomb, traversal, encrypted, corrupt, oversized, undecodable).

## Reuse
- Rights gate stays in the existing G04B `SourceGate`; this gate is the
  byte/archive safety layer before adapter ingest.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_ingestion_security.py -q` | 10 passed |
| ruff / pyright | PASS / 0 errors |

## Local commit
- `goal g55g: Ingestion security (M52)`
