# G62F Report — Security / Rights

**PASS** — source text is treated as data and malicious instruction markers
fail the job; resolved bytes must match the immutable source hash; archive
security checks run before adapter ingest; and E0/unapproved sources remain
non-compilable. No provider or authoring surface receives Commit Authority.

Evidence: malicious-source, hash-mismatch, E0, and existing ingestion-security
negative tests. Private/copyrighted bytes are not fixtures in Git.
