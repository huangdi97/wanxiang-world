# Package Install, Export & Migration Compatibility (G04E)

Ownership: `wanxiang_substrate.packages.install` (transactional install of
pinned packages).

## Install

`PackageInstaller.install(registry, root, root_version, ...)`:
1. resolves a deterministic `PackageLock`;
2. re-verifies every pinned manifest content hash (tampering rejected);
3. enforces executable trust (untrusted packages cannot provide executables);
4. checks known compatibility pairs;
5. records an `InstallRecord` with exact package/schema/domain pins and a lock
   hash, plus rights/evidence/asset refs.

Install is transactional: any validation error aborts with no record.

## Export

`export_install` renders a portable JSON structure (install id, package/version,
pins, lock hash, schema/domain pins, rights/evidence/asset refs). The export
hash is stable, so round-trips are verifiable.

## Upgrade

`PackageInstaller.upgrade` creates an explicit new `InstallRecord`
(`created_from` the previous one). A major incompatibility that is not declared
compatible raises `IncompatiblePackage` and records that a fork/branch is
required. Publishing v2 never mutates an existing v1-pinned install or live
instance.

## Trust

Executable extensions follow the default-deny policy: only trusted packages may
provide declared executables; untrusted packages cannot install executables.