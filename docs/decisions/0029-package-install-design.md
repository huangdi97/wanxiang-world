# ADR-0029: Package Install, Export & Migration Compatibility Design (G04E)

- Status: accepted
- Date: 2026-08-13

## Context

G04E needs a transactional install validation pipeline, portable export with
manifests/evidence/rights/asset references, exact version pinning at world
instantiation and explicit upgrade/migration compatibility, without ever
mutating a pinned v1 instance when v2 is published.

## Decision

1. Install resolves a deterministic lock, verifies content hashes, enforces
   executable trust and checks known compatibility, then records exact pins
   transactionally (abort on any error, no partial record).
2. Export is portable JSON with a stable hash for round-trip verification.
3. Upgrade creates an explicit new InstallRecord; undeclared incompatible
   major bumps require a fork/branch and raise `IncompatiblePackage`.
4. World instantiation records the install id + lock hash in instance metadata
   so the live instance is pinned to its exact package versions.

## Consequences

- Installs are auditable and deterministic; v1 instances are never silently
  mutated by v2 publication; migrations are explicit or fork-required.