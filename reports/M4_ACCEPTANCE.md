# M4 Acceptance ? Worlds Can Be Authored, Reviewed, Installed and Instantiated

## Verdict
PASS

## Scope
P4 (G04A?G04E) delivered on top of verified M1/M2/M3. This gate ran the
mandatory end-to-end synthetic scenario and the full regression suite.

## Mandatory scenario (tests/integration/test_m4_qualification.py)
1. Author synthetic Domain/World/Scenario JSON packs; all pass the Source Gate
   (approved rights, canonical-eligible stage).
2. The Structured Compiler emits provenance-bound candidates.
3. Every candidate is reviewed to canon in the Completion Ledger.
4. Manifests are registered and a pinned world install produces an
   InstallRecord with exact pins + lock hash.
5. The pinned world is instantiated; the install id + lock hash are recorded in
   instance metadata.
6. Export/re-import round-trip hashes match.
7. v2 is published and installed; the v1 record and live v1 instance are
   untouched, and replay of the v1 instance reproduces the identical state
   hash.

## Required proofs
| Proof | Status | Evidence |
|---|---|---|
| Package hierarchy + dependency/version resolution deterministic | PASS | G04A resolver tests (stable lock hash) |
| Untrusted executable extensions denied by default | PASS | trust + install negative tests |
| Source Gate blocks unapproved/rights-denied/malicious content | PASS | G04B gate tests |
| Conflicting claims survive as separate evidence-backed candidates | PASS | G04B conflict test |
| Compiler supports only declared formats; PDF/OCR/video explicit | PASS | G04C unsupported-format test |
| Canon/completion/model/reconstruction/user-fiction labels preserved | PASS | G04D taxonomy + audit tests |
| Install/export round-trip; hashes/version pins checked | PASS | G04E roundtrip + vertical |
| Package/schema migration compatibility tested | PASS | G04A migration + G04E upgrade tests |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1 commit/event/replay/branch/idempotency/stale-revision | PASS | test_m1_acceptance.py in full suite |
| M2 72h living-world | PASS | test_m2_qualification.py in full suite |
| M3 bounded-agent vertical | PASS | test_m3_qualification.py in full suite |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | persistence + migration tests green |
| Rights/projection leakage | PASS | observation/epistemic/source tests green |
| No-LLM deterministic profile | PASS | full suite has no LLM dependency |
| Lint/typecheck | PASS | ruff + pyright clean |
| TODO/placeholder scan + secret scan | PASS | architecture guard |

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed.
- 309 tests passed, 0 errors, architecture PASS.
- Checkpoint commit: `goal g04e: package install, export & migration compatibility`
- Milestone tag: `m4-worlds-authored-installed`