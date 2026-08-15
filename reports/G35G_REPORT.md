# Goal G35G Acceptance Report — Character Relation Knowledge Boundary Distillation

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A). The
mechanism is proven identity-agnostic via an anonymized key-choice fixture.

## Objective
Build a RUNNABLE per-character model (not personality labels): life-stage /
persona evidence, relation claims, a knowledge boundary, private/public fact
scope, and Completion/Interpretive separation.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/sources/character.py`:
   - `CharacterFact` — source-backed fact with character_key, proposition,
     scope (public/private), kind (life_stage/persona/relation/world),
     temporal (past/present/future), evidence locators.
   - `RelationClaim` — source-backed relation between two character keys with
     type, scope and evidence.
   - `KnowledgeBoundary` — knows(observer, fact): public facts and the
     character's own facts are known; private facts of others stay hidden
     unless an explicit grant (observer_key, fact_id) lifts the boundary;
     future facts are never known at runtime.
   - `CharacterCanon` — facts + relations + boundary + completion_notes;
     runtime_facts (never future), visible_to(observer) (boundary-filtered),
     facts_for / facts_of_kind / relations_for.
   - `CharacterDistiller` — deterministic, pure distillation (caller-supplied
     fact/relation rules + private_knowers grants; edition-agnostic); reuses
     G35E ScenarioPoint/temporal classification + G35B locators.
   - Exported via `wanxiang_substrate.sources` (SDK baseline +8 non-breaking).
2. `tests/unit/substrate/test_character_knowledge.py` (8 tests):
   - life_stage/persona/world fact classification with resolvable evidence;
   - private facts hidden from other characters (knowledge leak test);
   - explicit grant lifts the boundary only for the granted fact;
   - future facts never visible at runtime;
   - relation claims distilled and queryable;
   - ANONYMIZED key-choice fixture (c1/c2/c3, no Red Chamber names);
   - Completion/Interpretive separation (persona kind vs factual kinds;
     completion notes are strings, never facts);
   - determinism.

## Reuse (no duplicate abstraction)
- G35B `SourceLocator` / `segment_source` / `source_slice`.
- G35E `ScenarioPoint` + temporal classification (imported, not duplicated).
- No new registry/engine; candidates/facts only; SourceGate guards eligibility.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_character_knowledge.py tests/unit/substrate/test_canon_compilation.py tests/unit/substrate/test_entity_distillation.py tests/unit/substrate/test_identity_distillation.py tests/unit/substrate/test_narrative_domain.py -q` | 35 passed |
| `uv run pytest tests/integration/test_g17a_sdk_contract.py -q` | 3 passed (baseline) |
| `uv run ruff check` / `ruff format --check` | PASS / PASS |
| `uv run pyright` (changed files) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=1012 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| life-stage / persona evidence | PASS (tested) |
| relation claims | PASS (tested) |
| knowledge boundary (leak prevention) | PASS (tested) |
| private/public fact scope | PASS (tested) |
| future facts control-plane only | PASS (tested) |
| Completion/Interpretive separation | PASS (tested) |
| Anonymized key-choice fixture (identity-agnostic) | PASS (tested) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- Real character canon requires a legal, traceable edition; rules are
  caller-supplied so the mechanism is edition-agnostic.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/sources/character.py,
  tests/unit/substrate/test_character_knowledge.py, reports/G35G_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/sources/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md,
  DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35g: Character Relation Knowledge Boundary Distillation`
