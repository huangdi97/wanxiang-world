# G60D Report — Incremental Rebuild

## Status

**PASS** — Rebuild planning is deterministic and content-hash driven. A draft
  revision change requests a full rebuild; otherwise only changed or removed
  sections are selected.

## Evidence

- `IncrementalRebuilder.plan` sorts section names and compares the union of
  prior/current hashes.
- `IncrementalRebuilder.content_hash` uses canonical JSON and SHA-256.
- Architecture, lint, and type gates pass for the implementation.

