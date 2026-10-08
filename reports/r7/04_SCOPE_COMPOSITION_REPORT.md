# R7 04 — World Scope and Composition

Status: `PASS` for worldline isolation over one Cordis root context.

Reproduce: `pnpm exec vitest run src/scope.test.ts` in `packages/cordis_host`
(2 tests) — part of the package's 41 passing tests (7 files).

## What the scope manager guarantees

`WorldScopeManager` opens a worldline as an isolated Cordis context
(`isolate("history", …).isolate("actor", …)`) and owns the plugin fibers loaded
into it. The authority stays at the root: one bootstrap, and a worldline writes
only through a capability it was granted.

Verified behaviour:

* Two worlds run at once, each with its own history instance and rules.
* Committing three events into each world advances each worldline to revision 3
  independently.
* Closing world A leaves world B's head (revision and state hash) unchanged, and
  world B's rules still registered.
* World A's committed history survives its unload: it is retained in the provider
  and still readable (`retainedProvider("wl_a").head(...).revision === 3`).
* Opening two worlds registers no additional root-level service, and exactly one
  capability grant is recorded.

## Defect found by this test

`closeWorldline` originally also disposed `runtime.ctx.fiber`. Cordis
`isolate()` derives a child context that **shares the parent fiber**, so that
dispose tore down the entire runtime — world B's rules disappeared even though
world B was never closed. The worldline now disposes only its own plugin fibers,
and the defect is documented at the call site.

## Boundaries

* IMPLEMENTED: root/tenant/world/worldline layout for the worldline-scoped seams,
  `history` and `actor` isolation, single root authority, retained history for
  closed worldlines.
* VALIDATED: the two scope tests above plus the S1–S5 spike.
* NOT_PROVEN: tenant-level and experience-level scopes, cross-tenant sharing
  policy, and scope-aware capability delegation.
