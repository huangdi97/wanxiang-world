# G56A Report — ParsedDocument Model (M53)

## Status
**PASS** — Unified DocumentMetadata / StructuralNode / AssetRef intermediate
representation established between SourceAdapter output and distillation.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/parsing/model.py` (new):
   - `DocumentMetadata` — source_id/kind/version/parser_version/segmenter_version/
     content_hash/detected_format/size/title.
   - `StructuralNode` — stable node_id/kind (document/chapter/section/paragraph/
     dialogue/table/record/asset)/ordinal/parent + versioned content hash.
   - `ParseDiagnostic` (info/warning/error) + `ParsedDocument` (metadata + node
     tree + asset_refs + diagnostics; ok = no errors).
2. `tests/unit/substrate/test_parsed_document.py` — model validation + hash
   stability tests (shared with G56B).

## Reuse
- `AssetRef`/`BlobRef` referenced via `parsing.model` (no new blob system).
- Nothing here is Canon; parsed structure is a Forge intermediate.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_parsed_document.py -q` | 7 passed |
| ruff / pyright | PASS / 0 errors |
