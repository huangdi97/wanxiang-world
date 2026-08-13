# Package, Schema & Dependency Registry (G04A)

Ownership: `wanxiang_substrate.packages` (portable package definitions).

## Model

- `PackageManifest`: portable domain/world/scenario manifest with a semantic
  version, schema version, dependency constraints, content hash and executable
  trust class. Content hash is sha256 over the canonical serialization.
- `SemanticVersion` / `VersionConstraint`: deterministic ordering and
  constraints (`==`, `>=`, `<=`, `>`, `<`, `^`, `*`).
- `PackageLock`: deterministic resolution result pinning every package version.

## Resolver

`DependencyResolver` walks the graph in sorted order, picks the highest
satisfying version, and raises structured errors for cycles (`DependencyCycle`),
missing packages (`MissingDependency`) and incompatible re-pins
(`DependencyConflict`). Every already-pinned package must satisfy every later
constraint.

## Registry

`InMemoryPackageRegistry` verifies content hashes on registration, lists
versions deterministically (descending), and resolves roots to a `PackageLock`.
A `PackageRegistry` protocol keeps the storage port replaceable; no remote
registry is required.

## Trust

`ExecutableExtensionPolicy` is default-deny: untrusted packages can never
register an executable resolver; trusted packages may execute declared known
extensions (`.py`, `.js`, `.wasm`, ...).

## Migration

`migrate_manifest` upgrades older manifest schema versions through declared
steps (v1 -> v2 adds explicit `executable_trust`). A compatibility matrix
declares known-compatible package pairs; newer-than-target schemas are
rejected.