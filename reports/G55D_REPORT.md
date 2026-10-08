# G55D Report — Book Adapters (M52)

## Status
**PASS** — TXT/MD/EPUB/DOCX/text-PDF book adapters implemented (stdlib-only,
deterministic, no API); scanned PDF honestly returns OCR_REQUIRED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/book.py` (new):
   - `BookAdapter` implements the G55C `SourceAdapter` ABI.
   - EPUB: META-INF/container.xml → OPF manifest/spine → XHTML chapters in
     spine order (zipfile + xml.etree).
   - DOCX: word/document.xml → paragraphs + table rows (w:p/w:t/w:tbl).
   - text-PDF: best-effort content-stream text extraction (zlib); scanned
     PDFs with no text-showing operators → `OcrRequired` (never fabricated).
   - TXT/MD reuse the text path.
   - `Chapter` value object with stable ordinal.
2. `tests/unit/substrate/test_book_adapters.py` — 8 tests with synthetic
   EPUB/DOCX/text-PDF/scanned-PDF fixtures.

## Honest behavior
- Scanned/image PDF → `OcrRequired` (no OCR provider, no fake extraction).
- Invalid EPUB/DOCX zip or missing parts → `MalformedSourceContent`.
- Unknown kind → `UnsupportedSource`.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_book_adapters.py -q` | 8 passed |
| ruff / pyright | PASS / 0 errors |

## Local commit
- `goal g55d: Book adapters (M52)`
