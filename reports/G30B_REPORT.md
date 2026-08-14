# Goal G30B Acceptance Report ? World Constitution ?????

## Status
PASS

## Objective
Introduce a versionable Constitution bounding a world family's root rules
(identity / causality / time / evolution), separating immutable root
constraints from mutable law layers, and binding World Definitions via
constitution_ref.

## Delivered
1. `packages/domain/src/wanxiang_domain/constitution.py`:
   - `ConstitutionId` (ids.py, prefix `con`), `ConstitutionVersion` (non-negative int).
   - `ConstitutionManifest` (frozen, immutable): constitution_id, version, name,
     root_constraints (immutable), mutable_law_layers, provenance, rights_ref,
     evolution_policy, world_definition_ref, schema_version, content_hash.
   - `canonical()` (sorted, hash-stable), `compute_hash()`/`with_hash()`,
     `to_primitive()` (order-preserving) / `constitution_from_primitive()`
     (validated round-trip).
   - `ROOT_CONSTITUTION` ? platform Reality Root (mutable_law_layers = (),
     includes `no_self_amendment` + `world_policy_cannot_modify_platform`).
   - `legacy_default_constitution()` ? compat manifest for old v5.0/v5.1
     WorldPacks (minimal platform invariants; law layers remain author-mutable).
   - World Definition binding: `world_definition_ref` records the
     constitution_ref binding at authoring time (direct `constitution_ref`
     field lands with the World Definition type in G31A and WorldPack schema
     v5.2 in G34B).
   - Exported via `wanxiang_domain.__init__` (SDK baseline +7 non-breaking).
2. `tests/unit/domain/test_constitution.py` (5 tests):
   - schema round-trip preserves content hash + all fields;
   - distinct constitutions share no mutable objects (immutable tuples/frozen);
   - legacy WorldPack binds to the default legacy constitution (compat);
   - root constitution immutable + isolated (no mutable law layers);
   - world-definition binding survives serialization.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/domain/test_constitution.py -q` | 5 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=851 (+7 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| ConstitutionId / Version / Manifest | PASS |
| Immutable root constraints vs mutable law layers boundary | PASS |
| World Definition references constitution_ref | PASS (world_definition_ref binding; direct field in G31A/G34B) |
| Provenance / rights / evolution-policy compatibility | PASS (manifest fields) |
| Schema round-trip | PASS (tested) |
| No shared mutable objects between constitutions | PASS (frozen/tuples, tested) |
| Legacy WorldPack compat | PASS (legacy_default_constitution, tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/domain/src/wanxiang_domain/constitution.py,
  tests/unit/domain/test_constitution.py, reports/G30B_REPORT.md
- modified: packages/domain/src/wanxiang_domain/ids.py,
  packages/domain/src/wanxiang_domain/__init__.py, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g30b: World Constitution ?????`
