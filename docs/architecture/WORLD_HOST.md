# Minimal World Host & Authority Boundary (G05A)

Ownership: `wanxiang_substrate.host` (orchestration boundary).

## WorldHost

`WorldHost` holds the authoritative `WorldRuntime` for one world instance and
exposes command/query ports. It never mutates canonical state: every command
is routed to Commit Authority, and lifecycle modes (running/paused/stopped)
only gate whether commands may be submitted.

## HostRegistry

`HostRegistry` maps world instance ids to hosts in the single-process modular
monolith, lists observable `HostStatus` (mode + revision), and supports
shutdown (client disconnect) without touching canonical history.

## Authority boundary

- WorldHost is orchestration, not a second Commit Authority.
- Paused/stopped hosts reject commands (`HostNotRunning`).
- Lifecycle modes persist independently of sessions.