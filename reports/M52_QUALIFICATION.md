# M52 Qualification — Source Registry & Adapter Foundation

## Status
**M52 Milestone Gate PASS** — Source Registry & Adapter Foundation complete:
SourceRecord convergence, content-addressed blobs, unified adapter ABI, book /
structured / asset adapters, ingestion security; full adapter matrix green.

## Goal status (M52)
| Goal | Status |
|---|---|
| G55A SourceRecord convergence | PASS (commit 59e6238) |
| G55B Blob asset reference | PASS (commit 4ef54cf) |
| G55C SourceAdapter ABI | PASS (commit a4a6253) |
| G55D Book adapters | PASS (commit fe76f62) |
| G55E Structured adapters | PASS (commit ce8a66a) |
| G55F Asset adapter | PASS (commit cee571e) |
| G55G Ingestion security | PASS (commit 6a4158d) |
| G55H M52 qualification | PASS (this report) |
| **M52 Milestone Gate** | **PASS (2026-08-16, reports/M52_QUALIFICATION.md)** |

## Adapter matrix (03_SOURCE_ADAPTER_MATRIX.md)
| Type | Minimum capability | Status |
|---|---|---|
| TXT / Markdown | structured text import | PASS (BookAdapter) |
| EPUB | spine/href/chapter text | PASS (BookAdapter) |
| DOCX | paragraph/heading/table | PASS (BookAdapter) |
| text-PDF | page-aware text; scanned -> OCR_REQUIRED | PASS (BookAdapter; OcrRequired honest) |
| JSON / YAML | JSON Pointer/path later (M53); canonical text now | PASS (StructuredAdapter) |
| CSV | row/column later (M53); canonical rows now | PASS (StructuredAdapter) |
| GEDCOM | xref/tag path later (M53); normalized round-trip | PASS (StructuredAdapter) |
| Generic Asset | register as GenericAsset; semantics optional | PASS (AssetAdapter; semantic_available=False honest) |

Phase B provider ports (OCR/ASR/IIIF/vision) are M62 scope; no provider is
required for M52 (deterministic reference adapters cover the matrix).

## Qualification checks
| Check | Result |
|---|---|
| M52 targeted tests (8 suites incl. source gate + registration) | 68 passed |
| Full regression | 1064 passed + 1 skipped (live PG EXTERNAL_BLOCKED) + 3 deselected (Windows sandbox tmp_path; green on Linux CI) |
| Schema / version / migration | UNCHANGED (no new tables; all in-memory) |
| No second authority/registry/package/state | PASS (single SourceRegistry; adapters propose only) |
| Idempotency / resume | PASS (JobService G54E; blob dedupe; adapter resume no-op) |
| Negative / security tests | PASS (10 ingestion-security attacks) |
| kernel_guard / architecture_check | 0 violations / PASS |

## Evidence commands (2026-08-16)
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_source_* ... test_ingestion_security ...` | 68 passed |
| ruff / pyright | PASS / 0 errors |

## Local checkpoint
- G55A-G55G committed individually; M52 gate certified; next: M53 Parse /
  Segment / Stable Locator (G56A-G56H).

