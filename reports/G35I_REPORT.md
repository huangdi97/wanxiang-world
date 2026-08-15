# Goal G35I Acceptance Report — 编译 RedChamber World Definition 与 Scenario

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A). The
assembler compiles a v5.2 WorldPack Definition + Scenario from an
explicitly-labeled synthetic corpus; no canon is fabricated.

## Objective
Compile a RedChamber World Definition and Scenario: PackageAssembler; a
realistic/literary constitution ref; GenesisSpec; evolution policy refs;
signature/hash/dependencies; validate/install/export/import + instantiation
dry-run; no Core hardcode.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/worldpack/assembler.py`:
   - `GenesisSpec` — birth content (source_id, scenario_ref, distilled_refs,
     initial_facts) with stable content hash.
   - `literary_constitution()` — generic realistic/literary constitution
     (no_omniscient_future_leak, character_knowledge_boundary,
     source_gate_before_canon, ...); no Red Chamber proper nouns.
   - `WorldPackSignature` + `sign_world_pack` / `verify_world_pack` — HMAC
     over package_id:content_hash (reuses hmac/hashlib pattern).
   - `WorldPackAssembler.assemble()` — compiles ScenarioPoint from the source
     corpus, builds PackageManifest (kind=world, v5.2 constitution/genesis/
     evolution_policy/lineage refs) with content hash, links WorldDefinition,
     signs the pack. Deterministic; no Commit Authority writes.
2. `tests/unit/substrate/test_worldpack_assembly.py` (8 tests):
   - assemble with refs/hash/signature; validate+install+export+import
     (lock hash round-trip); instantiation dry-run (no events/authority);
     no Core hardcode (core packages free of Red Chamber names); generic
     literary constitution; scenario compiled from source; tampered manifest
     fails verification; deterministic assembly.

## Reuse (no duplicate abstraction)
- G35E `ScenarioPoint` / `scenario_at`, G35B `segment_source`.
- G34B `PackageManifest` v5.2 refs; G04A registry/install; G31A WorldDefinition;
  G30B ConstitutionManifest.
- No new registry/engine; assembly is pure.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_worldpack_assembly.py tests/unit/substrate/test_completion_ledger_review.py tests/unit/substrate/test_character_knowledge.py tests/unit/substrate/test_narrative_domain.py tests/unit/substrate/test_canon_compilation.py tests/unit/substrate/test_entity_distillation.py tests/unit/substrate/test_identity_distillation.py tests/unit/substrate/test_source_locator.py -q` | 56 passed |
| `uv run ruff check` / `ruff format --check` | PASS / PASS |
| `uv run pyright` (changed files) | 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=1028 |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| PackageAssembler | PASS |
| realistic/literary constitution ref | PASS |
| GenesisSpec | PASS |
| Evolution policy refs | PASS |
| Signature / hash / dependencies | PASS (tested) |
| package validate/install/export/import | PASS (tested) |
| instantiation dry-run | PASS (tested) |
| no Core hardcode | PASS (tested) |
| Real《红楼梦》text | EXTERNAL_BLOCKED (G35A) |
| Report + ledgers updated | PASS |

## Risks / not done
- The assembled pack uses synthetic content; real Red Chamber canon requires a
  legal, traceable edition before a real world pack can be compiled.

## Changed files
- added: packages/substrate/src/wanxiang_substrate/worldpack/ (2 files),
  tests/unit/substrate/test_worldpack_assembly.py, reports/G35I_REPORT.md,
  reports/RED_CHAMBER_WORLD_PACK_ACCEPTANCE.md
- modified: reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md, PLAN.md,
  STATUS.md, DECISIONS.md, CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g35i: 编译 RedChamber World Definition 与 Scenario`
