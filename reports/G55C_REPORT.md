# G55C Report — SourceAdapter ABI (M52)

## Status
**PASS** — Unified SourceAdapter ABI (can_handle/inspect/ingest/resume) with
typed failures; deterministic no-API reference text adapter provided.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/adapter.py` (new):
   - `SourceInspection` (detected_format/text_available/ocr_required/size/diagnostics)
   - `IngestResult` (content + optional blob_ref; references, never raw bytes)
   - `SourceAdapter` Protocol (can_handle/inspect/ingest/resume)
   - `ReferenceTextAdapter` — deterministic TXT/MD no-API path
   - `AdapterRegistry` — selects by kind/filename/content_type
   - `require_text()` — pipeline guard: OCR_REQUIRED or no-text fails honestly
2. `packages/substrate/src/wanxiang_substrate/sources/errors.py` (EXTEND):
   `UnsupportedSource`, `OcrRequired`, `MalformedSourceContent`, `IngestError`.
3. `tests/unit/substrate/test_source_adapter_abi.py` — 8 tests.

## Honest failure paths
- No adapter for kind → `UnsupportedSource` (never silent fallback).
- Scanned source without OCR provider → `OcrRequired` (never fake extraction).
- Declared format unparseable → `MalformedSourceContent`.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_source_adapter_abi.py -q` | 8 passed |
| ruff / pyright | PASS / 0 errors |

## Local commit
- `goal g55c: SourceAdapter ABI (M52)`
