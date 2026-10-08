# G62D Report — Idempotency / Resume

**PASS** — repeated start/preview is idempotent, cancellation preserves the
checkpoint contract, cancelled jobs can resume, and a changed byte stream is
rejected when it reuses an existing job/source fingerprint. A new source
version or job id is required for changed bytes.

Evidence: M58 cancel/resume tests and
`test_mixed_bundle_and_source_version_change_are_distinct`.
