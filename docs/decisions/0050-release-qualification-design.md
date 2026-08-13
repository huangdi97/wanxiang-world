# ADR-0050: Release Qualification Design (G12A-G12H)
- Status: accepted
- Date: 2026-08-13

## Context
G12 needs release qualification: long-run stability, backup/restore/migration,
SDK/OpenAPI/TS generation, research/projection/foundry/gateway adapters, and
security checks for private installation.

## Decision
1. Stability and backup/restore are system-level tests over existing paths.
2. SDK/OpenAPI/TS generation is deterministic and version-policy-documented.
3. Research/3D/foundry/digital-human adapters are non-authoritative contracts
   with synthetic fakes; real integrations are EXTERNAL_BLOCKED.
4. Security tests cover secrets, uploads, access and audit protection.

## Consequences
- The platform is release-qualified locally; external environment checks are
  explicitly labeled.