# ADR-0051: Cordis-native composition with versioned RealityProfile

- Status: Accepted for R7 engineering branch
- Date: 2026-09-24; implemented and qualified incrementally afterward

## Context

Wanxiang needs dynamic composition/scoped providers/reversible runtime effects,
while persistent worlds need identity/history/authority semantics that cannot
silently change when a plugin/model changes.

## Decision

1. Use exact-pinned Cordis directly as first composition runtime.
2. Do not define `Wanxiang = Cordis`; world semantics are versioned service
   contracts plus RealityProfile/WorldProfile/RuntimeLock.
3. Treat DSH as an agent provider over a gateway, not World OS.
4. Keep canonical state outside Cordis Context.
5. Cordis effects are reversible runtime resources; committed history is not.
6. Major pinned semantic changes require shadow replay plus migrate/fork/reject.
7. Untrusted/generated execution stays outside the trusted in-process host.

## Consequences

Benefits: less framework reinvention, explicit lifecycle/scopes, world persistence
semantics stay Wanxiang-owned, DSH/Cordis can evolve behind pinned boundaries,
and Python/Rust/science providers remain possible.

Costs: TypeScript/Python seam conformance is mandatory; RuntimeLock/migration
evidence becomes mandatory; in-process plugin isolation is not a hostile-code
security boundary; Cordis upgrades require qualification.

Rejected: reimplement a Wanxiang composition kernel; make DSH the world host;
treat Cordis effects as world transactions; silently roll RealityProfile.
