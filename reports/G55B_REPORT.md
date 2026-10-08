# G55B Report — Blob Asset Reference (M52)

## Status
**PASS** — Content-addressed source/blob/asset reference established; business
records never store raw large bytes (they reference blobs by content hash).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/blob.py` (new):
   - `BlobRef` — content-addressed reference (blob_id/content_hash/size/
     content_type/kind/rights) with `blob://` URI scheme.
   - `SourceBlobStore` — deduplicating adapter over the SINGLE G16D
     `ObjectStore` port: same content hash → same blob (no duplicate storage),
     size guard (default 256 MiB), honest load/locate/stat.
   - `is_blob_uri()` — records can be checked for blob-backed content_ref.
2. `tests/unit/substrate/test_source_blob_ref.py` — 6 tests.

## Reuse
- No second storage implementation: `SourceBlobStore` wraps the existing
  `assets.storage.ObjectStore` port (G16D). No raw bytes enter SourceRecord/
  ParsedDocument business records.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_source_blob_ref.py -q` | 6 passed |
| ruff / pyright | PASS / 0 errors |

## Local commit
- `goal g55b: Blob asset reference (M52)`
