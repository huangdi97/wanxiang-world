# G56B Report — Structural Parsing (M53)

## Status
**PASS** — Unified structural parsing: chapters/sections/paragraphs for books,
records for JSON/YAML/GEDCOM, rows for CSV.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/parsing/parser.py` (new):
   - `StructureParser` — converts canonical adapter content (IngestResult) into
     a versioned ParsedDocument node tree:
     - text/markdown: `#` chapter headings + `##`-`######` sections + paragraphs;
     - JSON/YAML: top-level keys as record nodes (canonical JSON);
     - CSV: rows as record nodes;
     - GEDCOM: `0 @xref@` records as record nodes.
   - Deterministic node ids + content hashes; parser/segmenter versioned.
2. `tests/unit/substrate/test_parsed_document.py` — book/JSON/CSV/GEDCOM
   structural tests.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_parsed_document.py -q` | 7 passed |
| ruff / pyright | PASS / 0 errors |
