# G73B Report — Security/corpus/rights publication audit

**PASS (2026-08-25)**

The repository safety boundary was re-run against the current checkout and the
CI safety job was reviewed as the publication contract.

| Gate | Result | Evidence |
|---|---|---|
| Secret-pattern scan | PASS | `security_forensics.py`: 0 findings |
| Source-gate adversarial probes | PASS | 4 probes; malicious/rights-denied sources blocked |
| Threat/rights matrix | PASS | 8 threats, 6 rights decisions recorded |
| Security/source/OCR/reference regressions | PASS | 22 passed, 2 warnings |
| Architecture conformance | PASS | kernel/import/secret/placeholder guards |
| Forbidden tracked files | PASS | no secret/db artifact; only red-chamber README + manifest template |
| Private/copyrighted corpus publication | PASS | no real book/family corpus tracked |

The CI safety rule remains explicit for secret patterns, env/key/database
artifacts, and `sources/red_chamber/*` exceptions. The current repository has
no provider token, model cache, source bytes, family-private record, or rights
grant embedded in Git. Real source availability remains a separate external
rights/provenance boundary; it is not converted into a local PASS.

Machine evidence: `reports/SECURITY_RIGHTS_SOURCE_FORENSICS.md` and
`reports/security_rights_source_forensics.json`.
