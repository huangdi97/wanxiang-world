# R7 Profiles, RuntimeLock and Migration

## Purpose

A persistent world must remain explainable after providers/packages change.
The stable object is not a forever-frozen executable; it is the exact,
auditable description of the semantics and implementation set that produced a
worldline's history.

## RuntimeLock

Production contracts:
- `wanxiang_reality.lock_store.StoredLock`
- `FileLockStore` / `MemoryLockStore`
- `wanxiang_reality.worldline_open.open_worldline`
- TypeScript `FileLockSource` / Cordis-host lock validation.

A stored lock is create-only unless an explicit exact-revision migration write
is requested. Editing it without a matching digest is tampering, not an upgrade.
Opening verifies identity, profile hashes, runtime facts, provider/schema
versions and composition runtime. Drift fails closed.

## RealityProfile / WorldProfile

RealityProfile says which reality seams define the interpretation of a
worldline. WorldProfile says which runtime/provider dimensions compose the
world. A worldline pins concrete versions; it never follows "latest" silently.

## Major upgrade

```text
quiesce
 -> checkpoint
 -> baseline RuntimeLock
 -> candidate profile/lock
 -> shadow replay
 -> compare identity/state/history/branch/lineage/invariants
 -> migrate | fork | reject
 -> explicit approval + sink
 -> migration artifact / lineage
```

Shadow replay has no canonical write authority. A plan does not mutate the
world. Applying migration requires explicit approval plus an explicit sink.

## Replay

Snapshots are optimization, not truth. R7 contains a snapshotless replay
qualification using the original history with a fresh empty snapshot store and
requires state hash/revision equality.

## Version taxonomy

Keep separate: Wanxiang software, Cordis runtime, Service API/schema, Provider,
RealityProfile, WorldProfile, World Definition, RuntimeLock and migration
artifact/lineage versions.

A provider upgrade may be used by a new lock. An existing worldline cannot
inherit it silently.
