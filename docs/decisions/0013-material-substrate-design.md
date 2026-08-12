# ADR-0013: Material Substrate Design (G02C)

- Status: accepted
- Date: 2026-08-13

## Context

G02C needs material continuity: objects, containers, custody, ownership and
information payloads with explicit conservation and knowledge boundaries.

## Decision

1. Items/containers/custody/ownership/payloads are versioned entity components;
   no new persisted table.
2. Custody (physical possession) is separate from ownership; transfers require
   the current custodian.
3. Containment supports nested containers with cycle prevention and capacity.
4. Information payloads are sealed until an explicit read by the custodian;
   readers are recorded (custody != knowledge).
5. Consumption/damage are explicit irreversible state transitions with
   conservation assertions.

## Consequences

- Deterministic, replayable material history; branch-isolated custody.
- Component fields stay flat primitives (accepts/readers are comma-joined).
