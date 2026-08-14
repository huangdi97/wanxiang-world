# Asset/Object Storage, Media Rights & Durable Artifact Handling (G16D)

## Design
- `AssetRef` is immutable and content-addressed (sha256), carrying size/content_type/rights.
- `ObjectStore` Port with a `LocalObjectStore` (content-addressed files) dev adapter; object-storage
  compatible production seam uses the same Port contract.
- Semantic truth stays in canonical state/events; blobs are durable content storage referenced by identity.

## Qualification results
| Check | Result |
|---|---|
| Blob corruption detected on read (integrity mismatch -> AssetCorrupt) | PASS |
| Missing blob is explicit AssetNotFound (not silent) | PASS |
| Asset metadata replayable through canonical commands (content-hash item identity) | PASS |
| Denied rights prevent delivery (AssetRightsDenied) | PASS |
| Canonical events refer to immutable identity/version (asset:<hash>), never a mutable path | PASS |

## Retention/backup
- Blobs are content-addressed (idempotent put); deletion is explicit; backup = replicate the blob root
  (same contract as the production object-store seam). Large binaries are never stored in event payloads.

## Evidence
- `uv run pytest tests/integration/test_g16d_asset_storage.py -q` -> 4 passed.
