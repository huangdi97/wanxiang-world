# ADR-0015: Institution Substrate Design (G02E)

- Status: accepted
- Date: 2026-08-13

## Context

G02E needs social/institutional constraints determining authority, duties,
permissions, obligations and sanctions, without hard-coding any historical
hierarchy.

## Decision

1. Roles, time-scoped memberships, delegated permissions and duties are
   versioned entity components; no new persisted table.
2. Permission decisions carry rule references and provenance (role or
   delegated grant).
3. Restricted places require `enter.<place>` permission; spatial move consults
   `InstitutionQuery` (substrate-internal coupling, no cycles).
4. Duties reference clock ticks by id; no cross-package cyclic dependency.

## Consequences

- Deterministic, replayable role/permission history; expired roles cannot grant
  authority; unauthorized actions rejected with explicit rule references.
