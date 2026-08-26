# Schema Drift Audit (G13D)

- Server operation count: 62
- SDK contract operation count: 62
- Aligned: True

## Server operations missing from the SDK contract

None.

## SDK contract operations missing from the server

None.

The canonical contract is generated from the FastAPI app (`scripts/export_openapi.py`) into `packages/sdk_ts/src/openapi-contract.json`; the drift test regenerates and compares, so a manually edited client is detected.
