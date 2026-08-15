# RedChamber WorldPack Acceptance (G35I, M32)

## Status
WORLD PACK MECHANISM ACCEPTED — real《红楼梦》canon EXTERNAL_BLOCKED (G35A).

## What was assembled
- WorldPack Assembler compiles a v5.2 `world` manifest with constitution/
  genesis/evolution-policy/lineage refs, content hash, dependency pins and an
  HMAC signature, plus a WorldDefinition and a ScenarioPoint.
- Constitution: generic realistic/literary (`con_literary_historical`) with
  no-omniscient-future-leak, character-knowledge-boundary and
  source-gate-before-canon root constraints; mutable layers ontology/law/
  ritual/etiquette; evolution policy `distillation_review`.
- GenesisSpec: source corpus + scenario + distilled refs + initial facts
  (synthetic, explicitly labeled).

## Acceptance evidence
| Item | Evidence |
|---|---|
| validate/install/export/import | `test_worldpack_assembly.py::test_validate_install_export_import` PASS (lock hash round-trip) |
| instantiation dry-run | `test_instantiation_dry_run` PASS (no events/authority touched) |
| no Core hardcode | `test_no_core_hardcode` PASS (core packages free of Red Chamber names) |
| signature/hash/dependencies | `test_assemble_world_pack_with_refs_hash_and_signature` + `test_tampered_manifest_fails_verification` PASS |
| determinism | `test_assembly_is_deterministic` PASS |

## Honest boundary
- This is a MECHANISM acceptance. The assembled pack content is synthetic; a
  real Red Chamber world pack cannot be compiled until a legal, traceable
  edition is available (BLOCKERS.md G35A). No model memory is used as Canon.
