# Goal G35F Acceptance Report — Narrative Household HistoricalChina Domain 复用与补齐

## Status
PASS (generic mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A).
The narrative/household/historical-China domain is delivered as a generic
Domain Pack installable by ANY synthetic world; it contains no Red Chamber
proper nouns and no RedChamberCore.

## Objective
- FORBID RedChamberCore: domain must stay generic and reusable.
- Missing actions are defined in the Domain Pack, never in Core reference actions.
- Resolvers for 礼制 (ritual), 职责 (duty), 访问权限 (access), 传话 (message
  relay), 探病 (sick visit) and 书信 (letters).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/narrative/` (new generic domain):
   - `actions.py` — `narrative.perform_ritual`, `narrative.visit_sick`,
     `narrative.send_letter`, `narrative.relay_message` ActionDefinitions with
     permissions; installed via `register_narrative_actions` into an
     ActionRegistry. Core `register_reference_actions` is untouched.
   - `components.py` — versioned narrative.ritual/visit/letter/message
     components on the M1 component model.
   - `resolver.py` — resolvers produce ProposedWorldDeltas through the single
     Commit Authority (no direct writes). `_visit_sick` enforces access
     permission (访问权限) via InstitutionQuery; `_send_letter` reuses material
     item + sealed info-payload components; `register_narrative_domain()`
     installs the whole pack (actions + resolvers).
   - `query.py` — `NarrativeQuery` read-only projections: rituals_by (礼制),
     visits_for (探病), letters_for (书信), messages_for (传话),
     access_allowed (访问权限), pending_duties (职责, delegated to institution).
2. `tests/unit/substrate/test_narrative_domain.py` (6 tests):
   - Domain pack installs without touching Core reference actions.
   - Ritual resolves through the authority and is queryable.
   - Sick visit is REJECTED without access permission, allowed with it.
   - Letter creates a sealed info payload + routing; relay message reaches the
     recipient.
   - The narrative package contains NO Red Chamber proper nouns
     (林黛玉/贾宝玉/潇湘馆/怡红院/红楼梦/贾府/太虚幻境/荣国府).

## Reuse (no duplicate abstraction)
- institution permission/duty model + query for access control and duties.
- material item/info_payload components for the sealed letter.
- agency resolver pattern (validation through authority).
- No new registry/engine; existing ActionRegistry/ResolverRegistry reused.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_narrative_domain.py tests/unit/substrate/test_identity_distillation.py tests/unit/substrate/test_entity_distillation.py tests/unit/substrate/test_canon_compilation.py -q` | 27 passed |
| `uv run pytest tests/integration/test_g17a_sdk_contract.py -q` | 3 passed (baseline) |
| `uv run ruff check` / `ruff format --check` | PASS / PASS |
| `uv run pyright` (narrative + test) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=1004 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| No RedChamberCore (generic domain only) | PASS (tested, no proper nouns) |
| Missing actions defined in Domain Pack (not Core) | PASS (tested) |
| 礼制 ritual resolver | PASS (tested) |
| 职责 duty (delegated) | PASS (tested via pending_duties) |
| 访问权限 access resolver | PASS (tested: denied/allowed) |
| 传话 message relay resolver | PASS (tested) |
| 探病 sick-visit resolver | PASS (tested) |
| 书信 letter resolver (sealed payload) | PASS (tested) |
| Installable by synthetic world without Red Chamber names | PASS (tested) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- Real Red Chamber domain content cannot be authored until a legal, traceable
  edition is available; the generic pack is edition-agnostic.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/narrative/ (5 files),
  tests/unit/substrate/test_narrative_domain.py, reports/G35F_REPORT.md
- modified: reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md, PLAN.md,
  STATUS.md, DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35f: Narrative Household HistoricalChina Domain 复用与补齐`
