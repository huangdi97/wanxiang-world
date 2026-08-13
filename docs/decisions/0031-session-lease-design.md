# ADR-0031: Session & Embodiment Lease Design (G05B)

- Status: accepted
- Date: 2026-08-13

## Context

G05B needs sessions bound to world instances and embodiment leases that
guarantee exactly one primary controller per actor.

## Decision

1. Sessions carry a mode (observe/embody/admin) that gates embodiment.
2. LeaseService enforces one active lease per actor; acquire/renew/release/
   expire are explicit and auditable.
3. Sessions do not duplicate actor state; canonical state stays authoritative.

## Consequences

- No two sessions can fight over one actor; session state never becomes world
  truth.