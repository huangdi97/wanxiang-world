# Goal G35D Acceptance Report — 空间组织物品 Distillation

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A);
place/object/organization + topology distillation verified on an
explicitly-labeled synthetic corpus (NOT canon).

## Objective
Build source-bound candidates for places, paths, objects and organizations
(潇湘馆/怡红院-style gardens, public paths, households, letters/medicine/
gifts), plus runnable topology candidates, routing details that cannot be
directly verified into Completion instead of presenting them as source
evidence.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/evidence.py` (shared):
   - `AUTHORIZED_REVIEWERS` moved here from identity.py (single source of truth).
   - `evidence_ok()` — one rule set (min locators + resolvable source slice)
     used by both identity (G35C) and entity (G35D) review gates so evidence
     rules never drift; MERGE/ADAPT (IdentityReviewGate refactored to use it,
     G35C tests unchanged and green).
2. `packages/substrate/src/wanxiang_substrate/sources/entity_distill.py`:
   - `EntityMention` — source-bound mention (key/kind/display/locators).
   - `EntityConnection` — topology edge (source/target/label/edge kind +
     evidence locators); kinds portal/path/custody/containment/membership.
   - `EntityCandidate` — distilled place/path/object/organization candidate
     with mentions, `completion_notes` (never evidence), provenance, status.
   - `EntityDistiller` — deterministic, pure distillation over approved text
     (caller-supplied entity/connection rules; edition-agnostic); returns
     `DistilledEntities` (candidates + connections + `unresolved_targets`).
   - `EntityReviewGate` — human/rule review: authorized reviewer + every
     mention/connection locator resolves; completion notes never count.
   - Exported via `wanxiang_substrate.sources` (SDK baseline +14 non-breaking).
3. `tests/unit/substrate/test_entity_distillation.py` (8 tests, synthetic):
   place/object/organization candidates with resolvable evidence; topology
   edges source-bound; unresolved connection target -> Completion (not an
   invented candidate); completion note is never evidence; unauthorized
   reviewer rejected; approved -> eligible; determinism; E0-E5 stage
   classification + SourceGate behavior.

## Reuse (no duplicate abstraction)
- G35B `SourceLocator` / `segment_source` / `source_slice`.
- G35C `IdentityReviewGate` rule logic extracted into shared `evidence_ok`
  (identity gate ADAPTED; behavior unchanged).
- G04B `SourceRecord` stages E0-E5 / `SourceGate` eligibility.
- No new registry/engine/store; candidates only.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_entity_distillation.py tests/unit/substrate/test_identity_distillation.py tests/integration/test_g17a_sdk_contract.py -q` | 18 passed |
| `uv run ruff check` / `ruff format --check` (changed files) | PASS / PASS |
| `uv run pyright` (changed files) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=979 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Place/Path/Object/Organization distillers | PASS |
| Topology candidates (portal/path/containment edges) | PASS (tested) |
| Unverifiable details -> Completion (not fake source) | PASS (tested) |
| Completion note is never evidence | PASS (tested) |
| E0-E5 stage classification + SourceGate | PASS (tested) |
| Shared evidence rules (no drift between gates) | PASS (refactor, G35C green) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- Real spatial/organization roster requires a legal, traceable edition; rules
  are caller-supplied so the mechanism is edition-agnostic.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/sources/evidence.py,
  packages/substrate/src/wanxiang_substrate/sources/entity_distill.py,
  tests/unit/substrate/test_entity_distillation.py, reports/G35D_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/sources/identity.py
  (refactor to shared evidence_ok), sources/__init__.py, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35d: 空间组织物品 Distillation`
