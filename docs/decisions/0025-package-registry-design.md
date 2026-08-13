# ADR-0025: Package, Schema & Dependency Registry Design (G04A)

- Status: accepted
- Date: 2026-08-13

## Context

G04A needs portable Domain/World/Scenario package manifests, semantic version
constraints, deterministic dependency resolution and a trusted/untrusted
executable policy, without requiring a remote registry.

## Decision

1. Package manifests are frozen value objects with semantic versions, schema
   versions, dependency constraints, content hashes and an executable trust
   class; hashing is over the canonical serialization.
2. Resolution is deterministic: sorted traversal, highest satisfying version,
   structured cycle/missing/conflict errors; every pinned package must satisfy
   every later constraint.
3. The registry is a replaceable port with an in-memory adapter that verifies
   content hashes; no remote registry is required.
4. Executable extensions are default-deny for untrusted packages; trusted
   packages may run declared known extensions.
5. Manifest schema migration is explicit (v1 -> v2) with a compatibility
   matrix; newer-than-target schemas are rejected.

## Consequences

- Deterministic, auditable package locks; untrusted executable code is denied
  by default; older manifests upgrade through a declared path.