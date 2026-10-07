# R7 01 — Worldline RuntimeLock Pinning

Status: `IMPLEMENTED / VALIDATED`.

## Implemented

- RuntimeLock is persisted per worldline through `wanxiang_reality.lock_store`
  with frozen JSON schema, explicit revision/write time and canonical digest.
- Existing locks are immutable except through an explicit exact-revision
  migration write; provider upgrades never silently rewrite a lock.
- `open_worldline()` fails closed on missing/tampered/identity/profile/provider/
  schema/config drift and returns `MIGRATION_REQUIRED` for a major
  RealityProfile change.
- The Cordis host reads the same Python-written lock through `FileLockSource`,
  re-checks digest/live versions and refuses mismatched worldlines.
- Cross-language tests create a lock via Python CLI and open it in TypeScript.

The lock binds world/definition/instance/worldline identity,
RealityProfile/WorldProfile refs+hashes, composition runtime/version,
contract/provider/schema versions, artifact hashes, migration lineage and
runtime config hash.

Evidence:
- `packages/reality/src/wanxiang_reality/lock_store.py`
- `packages/reality/src/wanxiang_reality/worldline_open.py`
- `packages/cordis_host/src/stored_lock.ts`
- Python/TypeScript lock tests and exact-SHA qualification.

RuntimeLock is the pinned interpretation/runtime descriptor; it is not world
truth itself.
