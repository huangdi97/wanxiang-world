# Package Ecosystem Acceptance

## Status
PASS (mechanism) — package install/export/import/upgrade/migration accepted.

## Evidence
- WorldPack assembly (G35I/G40A): validate/install/export/import with lock-hash
  round-trip; instantiation dry-run; signature/hash/dependencies verified.
- Dependency resolver + PackageInstaller + RegistryLifecycle (G04A/G04E/G17F):
  deterministic lock, trust enforcement, upgrade compatibility, yank preserves
  history.
- WorldPack schema v5.2 migration (G34B/G34C): legacy hash preserved,
  `migrate_to_v52` + `wxpack migrate`; migration head `0004_add_world_metadata`.
- Tests: `test_worldpack_assembly.py`, `test_worldpack_migration.py`,
  `test_g34c_db_migration.py`, `test_g17a_sdk_contract.py` PASS.

## Boundary
Real RedChamber release bundle content EXTERNAL_BLOCKED (G35A); mechanism bundle
built from synthetic content, explicitly labeled.
