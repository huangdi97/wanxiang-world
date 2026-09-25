# R7 02 — Cordis Composition Spike (S1–S5)

Status: `PASS` for the five spike scenarios at composition runtime
`cordis@4.0.0-rc.10` (exact version read from the pinned package).

Reproduce:

```powershell
cd packages\cordis_host
pnpm exec tsc --noEmit
pnpm exec eslint .
pnpm exec vitest run            # 4 files, 19 tests
```

The vitest run also writes the resolved graph to
`artifacts/r7/composition/resolved_graph.json`.

## What was built

`packages/cordis_host` is a pnpm workspace member that pins the official Cordis
package; no Cordis-like kernel is written here. The context carries services,
scopes and lifecycle only — it does not hold canonical world state, and every
canonical write goes through one commit path that requires a capability minted by
the authority bootstrap.

## Scenario results

| Scenario | Requirement | Observed |
|---|---|---|
| S1 | ≥100 continuous commits, monotonic revision, no silent overwrite, final state rebuildable from history | 100/100 commits; head revision `100`; `rebuildFromHistory` equals the incremental state hash; a stale `expectedRevision` raises the typed `RevisionConflictError` |
| S2 | Unloading the actor plugin must not move the history head and must clean runtime effects | head revision and state hash unchanged after unload; rule registry empty for the worldline; leaked timers/listeners/rules all `0` |
| S3 | Mounting actor-rule v2 continues the same worldline from its current revision with no second canonical state | same provider instance; revision advanced by exactly `1`; active rules `["actor-rule/actor_alpha/v2"]`; status `COMMITTED` |
| S4 | ≥1000 mount/unmount cycles with no timer, listener, service or fiber leak | 1000 cycles; deltas for timers, listeners, rules and registry size all `0` against the live baseline |
| S5 | Resolved graph with providers, seams, consumers, scope ownership and exact versions | written to `artifacts/r7/composition/resolved_graph.json`; 16 contracts; exact runtime `cordis 4.0.0-rc.10`; runtime Node `v22.15.0` |

The leak check compares against a live baseline rather than assuming an empty
runtime, because the v2 rule mounted by S3 is still legitimately active.

## Defects the spike caught and fixed

1. **State-hash folding was batch-dependent.** The previous implementation fed
   every event into a single hash object, so `append(e1); append(e2)` produced a
   different digest from folding `[e1, e2]` at once. Replay rebuilt from history
   therefore disagreed with the incremental head hash. `foldStateHash` now folds
   one event at a time and the invariant is asserted by S1.
2. **The lifecycle test measured the wrong baseline.** Comparing absolute
   counters reported the still-mounted v2 plugin as a leak; S4 now measures the
   delta across the cycle loop.

## Security properties exercised

* A capability only writes if it was minted by the authority bootstrap
  (module-private WeakSet check before the provider call); a structural copy of a
  capability is rejected, and an unregistered holder cannot be granted one.
* A hard deny is monotonic: an `ALLOW` recorded after a `HARD_DENY` is retained
  for audit but cannot reopen the decision.
* Cross-worldline writes are denied by policy before the history seam is reached,
  so neither worldline's history changes.
* An `unversioned-overwrite` proposal is denied outright.

## Boundaries

* IMPLEMENTED: Cordis host, versioned seam identity, history/authority/policy
  seams with an in-process provider, worldline scopes, graph export, spike.
* VALIDATED: S1–S5 above, plus `tsc`, ESLint, and the repository Python gate
  (`1507 passed, 1 skipped`, architecture PASS) on this tree.
* NOT_PROVEN: the JSON-RPC provider that bridges the history seam to the Python
  authority; execution fabric, DSH bridge, Capability Foundry, and RealityProfile
  shadow-replay migration are not implemented in this slice.
* EXTERNAL_BLOCKED: nothing in this spike; no network or paid resource is used.
