# Goal G35H Acceptance Report — Completion Ledger 与审核

## Status
PASS (mechanism) — synthetic completion records only; real《红楼梦》text
remains EXTERNAL_BLOCKED (G35A).

## Objective
Record content needed to run but not explicit in source, fully labeled with
E0-E5 review stages; completion records carry support refs / confidence /
review status; can_enter_canon defaults to FALSE; provide a batch-review
CLI/Studio use case.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/ledger/completion.py`:
   - `CompletionRecord` — completion_id, description, support_refs, confidence
     (0..1), review_status (pending E0-E2 / approved E3 / rejected E4 /
     superseded E5), reviewer, rationale, review_version, can_enter_canon
     (default FALSE), evidence_refs.
   - `CompletionDecision` — immutable approve/reject decision with reviewer,
     rationale, evidence_refs.
   - `CompletionReviewLedger` — submit (id registered once; conflicting
     claims never merged/overwritten), review (E0-E5 stage semantics:
     E4/E5 terminal, never auto-upgrade to E0; approval requires authorized
     reviewer + evidence refs + confidence >= policy threshold; rejection
     clears can_enter_canon), supersede (E5), history, by_status, conflicts,
     all.
   - `CompletionStudio` — read-only Studio queries: pending_review,
     canon_candidates, conflicts, stage_summary.
   - `apply_batch_review()` — batch review use case (CLI/API).
   - Reuses `AUTHORIZED_REVIEWERS` from sources.evidence (no duplicate).
2. `scripts/completion_review.py` — batch-review CLI: reads a JSON manifest,
   submits records, applies decisions, writes a report JSON with reviewed ids,
   can_enter_canon, conflicts, stage summary.
3. `tests/unit/substrate/test_completion_ledger_review.py` (9 tests):
   - can_enter_canon defaults false; approval requires evidence;
   - E4 rejected never auto-upgrades to E0 (incl. id-reuse refusal);
   - E5 superseded never auto-upgrades to E0;
   - conflicting claims preserved (both kept, conflicts reported);
   - confidence below threshold refuses approval;
   - unauthorized reviewer rejected;
   - batch-review CLI end-to-end (manifest -> report);
   - Studio queries; deterministic batch order.

## Reuse (no duplicate abstraction)
- G04D `CompletionLedger` truth taxonomy extended (not replaced); E0-E5 stage
  semantics reused from G04B source model.
- `AUTHORIZED_REVIEWERS` imported from sources.evidence.
- No new registry/engine; append-only in-memory ledger consistent with G04D.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_completion_ledger_review.py tests/unit/substrate/test_character_knowledge.py tests/unit/substrate/test_narrative_domain.py tests/unit/substrate/test_canon_compilation.py tests/unit/substrate/test_entity_distillation.py tests/unit/substrate/test_identity_distillation.py tests/integration/test_g17a_sdk_contract.py -q` | 46 passed + 3 (baseline) |
| `uv run ruff check` / `ruff format --check` | PASS / PASS |
| `uv run pyright` (changed files) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=1021 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| completion records | PASS |
| support refs / confidence / review status | PASS (tested) |
| can_enter_canon defaults false | PASS (tested) |
| E4/E5 never auto-upgrade to E0 | PASS (tested) |
| conflicting claims preserved | PASS (tested) |
| batch review CLI/Studio use case | PASS (tested end-to-end) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- HTTP API router deferred to the world-pack surface (G35I/M33) to avoid a
  write router before the pack exists; CLI + Studio cover the batch use case.
- Real completion entries require a legal, traceable edition.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/ledger/completion.py,
  scripts/completion_review.py, tests/unit/substrate/test_completion_ledger_review.py,
  reports/G35H_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/ledger/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md,
  DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35h: Completion Ledger 与审核`
