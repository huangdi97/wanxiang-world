# ADR-0030: Minimal World Host & Authority Boundary Design (G05A)

- Status: accepted
- Date: 2026-08-13

## Context

G05A needs an orchestration boundary for hosted worlds that is clearly NOT a
second Commit Authority, with lifecycle modes that persist independently of
sessions.

## Decision

1. WorldHost holds the authoritative runtime and exposes command/query ports;
   every command is routed to Commit Authority; the host never mutates state.
2. Lifecycle modes (running/paused/stopped) gate command submission only.
3. HostRegistry manages hosts in the single-process modular monolith and
   supports shutdown without touching canonical history.

## Consequences

- Orchestration is clearly separated from authority; lifecycle control does not
  create a mutation path.