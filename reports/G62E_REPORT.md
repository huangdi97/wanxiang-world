# G62E Report — Large Source Performance

**PASS (reference bound)** — `SourceChunker.iter_chunks` yields bounded
chunks, `ParseRecovery` records a deterministic source hash and ordinal, and
`ContentHashCache` is keyed by source/version/content hash. The reference
path remains deterministic and does not introduce a second source store.

Evidence: `test_large_source_chunking_is_bounded_and_restartable` and
`test_source_chunk_cache_is_content_and_version_addressed`. Production
throughput numbers are intentionally not claimed from a synthetic fixture.
