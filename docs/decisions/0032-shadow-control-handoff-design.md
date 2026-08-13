# ADR-0032: Shadow / Human Policy Control Handoff Design (G05C)

- Status: accepted
- Date: 2026-08-13

## Context

G05C needs a handoff where a human takes over an actor, commits actions, and
releases control to the deterministic controller, with ShadowPolicy unable to
compete for authoritative body control.

## Decision

1. ControlHandoff is a per-actor state machine with resume refs.
2. ShadowPolicy is advice-only; commit raises ShadowCannotCommit.
3. Committed human actions are normal world history; on release the
   deterministic controller resumes from current world + memory state.

## Consequences

- Shadow can never choose canonical actions; takeover/resume is auditable and
  memory is never reset.