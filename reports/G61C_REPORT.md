# G61C Report — Reference CLI

**PASS** — `scripts/wxworld.py reference` runs the same `AuthoringService` as
the Studio API through source registration, draft build, package assembly, and
isolated preview. It emits only package/status metadata, not source payloads.

Evidence: CLI smoke output and `test_authoring_service_reference_e2e_and_idempotent_preview`.

