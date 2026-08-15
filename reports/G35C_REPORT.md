# Goal G35C Acceptance Report — 人物与别名 Identity Distillation

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A);
identity/alias distillation machinery verified on an explicitly-labeled
synthetic corpus (NOT canon).

## Objective
From approved source text, generate character identity CANDIDATES with
evidence-backed alias claims, resolving aliases without merging distinct
identities, and gate entry into Canon behind a human/rule review.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/identity.py`:
   - `AliasClaim` — one alias of an identity with evidence locators (G35B
     SourceLocator); a claim without evidence is rejected at construction.
   - `IdentityCandidate` — distilled identity candidate (id/key/display/
     aliases/provenance/status); never Canon until review approves.
   - `IdentityDistiller` — deterministic, pure distillation over approved
     source text: segments via `segment_source`, extracts mentions with a
     caller-supplied rule function, resolves mentions to identity keys,
     dedupes evidence locators (sorted for stability). No write path.
   - `IdentityReviewGate` — human/rule review: authorized reviewer
     (`human`/`reviewer`) + every alias has >=1 resolvable evidence locator
     before a candidate may become eligible.
   - `identity_to_claim()` — converts an approved candidate into the shared
     G04B `ClaimCandidate`/`EvidenceLink` model so the existing claim pipeline
     (Completion Ledger G04D / Canon compilation G35E) consumes identities
     without a second claim abstraction.
   - Exported via `wanxiang_substrate.sources` (SDK baseline +9 non-breaking).
2. `tests/unit/substrate/test_identity_distillation.py` (7 tests, synthetic
   corpus): alias→identity resolution with evidence back-links; determinism;
   same-name different-identity non-merge; no-evidence / unresolvable-locator
   candidates rejected by the review gate; unauthorized reviewer rejected;
   approved candidate→eligible + claim conversion; composition with the
   existing SourceGate (approved source compiles, non-eligible source rejected).

## Reuse (no duplicate abstraction)
- G35B `SourceLocator` / `segment_source` / `source_slice` (locators + slices).
- G04B `ClaimCandidate` / `EvidenceLink` / `SourceRecord` / `SourceGate`
  (candidate-with-evidence model + source eligibility).
- `EntityId` semantics preserved (identity_key remains a plain stable key; no
  new id type, no second registry/engine).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_identity_distillation.py -q` | 7 passed |
| `uv run pytest tests/unit/substrate/test_source_locator.py tests/unit/substrate/test_red_chamber_source_registration.py -q` | 7 passed (regression) |
| `uv run pytest tests/integration/test_g17a_sdk_contract.py -q` | 3 passed (baseline) |
| `uv run ruff check` / `ruff format --check` (changed files) | PASS / PASS |
| `uv run pyright` (changed files) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=965 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Entity/Identity Distiller | PASS |
| Alias claims with evidence locators | PASS (tested) |
| Same-name/alias resolution without merging distinct identities | PASS (tested) |
| Human/rule review gate | PASS (tested) |
| No-evidence candidate does not enter Canon | PASS (tested) |
| Reuses SourceGate/SourceLocator/Claim model; no second registry/engine | PASS |
| Real《红楼梦》text (identity distillation input) | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- Real character roster cannot be produced until a legal, traceable edition is
  available; rules (extract/resolve) are caller-supplied so the mechanism is
  edition-agnostic.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/sources/identity.py,
  tests/unit/substrate/test_identity_distillation.py, reports/G35C_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/sources/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md, PLAN.md,
  STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35c: 人物与别名 Identity Distillation`
