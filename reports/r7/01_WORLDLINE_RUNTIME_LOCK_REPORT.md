# R7 01 — Worldline RuntimeLock Pinning

Status: `IMPLEMENTED` / `VALIDATED` (unit + TS integration level).

## 1. What changed

| Artefact | Responsibility |
|---|---|
| `packages/cordis_host/src/lock.ts` | `RuntimeLockRef`/`ProfileRef` types, `validateRuntimeLockRef`, `createRuntimeLockRef`, `assertSeamsMatchLock` |
| `packages/cordis_host/src/host.ts` | `createHost({ lockRef })` — the lock is required, not optional |
| `packages/cordis_host/src/graph.ts` | the resolved graph records `runtimeLocks` (worldline -> lock, reality/world profile, composition runtime version, service contract versions, provider versions) |
| `packages/cordis_host/src/testing.ts` | fixture lock/profile helpers for tests |

The lock data model itself lives in Python (`wanxiang_reality.profiles.RuntimeLock`)
and is consumed as data by TypeScript, so there is exactly one lock model.

## 2. Invariants

- A worldline refuses to open without a validated pinned `RuntimeLockRef`.
- `assertSeamsMatchLock` compares the live seam digests against the contract
  versions recorded in the lock and fails on any mismatch, so a runtime cannot
  silently run with drifted contracts.
- The composition-runtime version is read from `cordis/package.json` and compared
  exactly, including prerelease versions (`4.0.0-rc.10`).
- The resolved graph is evidence: it records what the worldline was actually
  composed from, including `runtimeLocks`.

## 3. Evidence

```text
pnpm -C packages/cordis_host exec tsc --noEmit        -> exit 0
pnpm -C packages/cordis_host exec eslint .            -> exit 0
pnpm -C packages/cordis_host exec vitest run          -> 7 files / 41 tests passed
artifacts/r7/composition/resolved_graph.json          -> runtimeLocks[] present
uv run python scripts/quality.py                      -> architecture PASS
```

## 4. Not claimed

- The lock is not yet persisted per worldline in a store; callers supply it.
- Only the composition host enforces the lock today; the Python runtime path does
  not yet refuse to open a worldline without one.
