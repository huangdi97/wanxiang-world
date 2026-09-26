# R7 15 — Final Closure Report

## Final Decision

`NOT_COMPLETE`

Phase A (v5.5 Stable closure, as far as evidence allows) is closed. Phase B (R7
implementation) has produced a working first slice — the Cordis composition
runtime with versioned seams, scope isolation and a certified spike — but the
majority of the R7 Definition of Done is not implemented. No R7 claim below is
made without a reproducible command or artifact.

## 1. Branch / HEAD / worktree

```text
branch   feature/r7-cordis-native
base     4825546 feat(r7): cordis composition host and versioned reality package
worktree clean at the time of this report's commit
```

The v5.5 Stable work stays on `release/v5.5-stable-certification` (remote, CI
green); this branch is cut from it and has not been pushed yet.

## 2. v5.5 Stable status

Gate 79 `PASS` at candidate `a9be096` (and CI verified again at the evidence
commit `48b3402`). Gates 62–66 `USER_INPUT_REQUIRED` / `WAITING_HUMAN` — no
human rating was fabricated. Gate 78 `EXTERNAL_BLOCKED` (no Godot). Gate 80
`LOCKED`; no `v5.5.0` tag or release exists.

## 3. Cordis runtime exact version

`cordis@4.0.0-rc.10`, pinned in `packages/cordis_host/package.json` and reported
verbatim in `artifacts/r7/composition/resolved_graph.json`
(`compositionRuntime.version`, `exact: true`). Node `v22.15.0`.

## 4. WorldProfile / RealityProfile / RuntimeLock

`PARTIAL`. `wanxiang_reality` implements `RealityProfile`, `WorldProfile`,
`RuntimeLock` (including all fields required by master §8.3), canonical-JSON
digests and typed validation, with 30 unit tests. The TS host does not yet
consume a lock: a worldline is not pinned to a `RuntimeLock` at open time, and
the seam versions are not yet asserted against a pinned lock.

## 5. Service seams and providers

`PARTIAL` — see `reports/r7/03_SERVICE_SEAMS_REPORT.md`. 16 versioned contracts,
seam digest recorded, history seam with a provider port, architecture guards on
both sides. The JSON-RPC provider that would let the Python authority serve the
history seam is not implemented, so the Python↔Cordis bridge required by the
contract is missing.

## 6. History / Replay / Branch / Lineage

`PARTIAL`. The composition spike certifies 100 continuous commits, monotonic
revision, typed `expectedRevision` conflict, and rebuild-from-history equality.
Branching, lineage and the full replay contract tests are not implemented in this
slice; the repository's existing Python event store/branch/replay remain the
production path and were not modified.

## 7. Authority / Security

`PARTIAL`, and the implemented part is certified: the capability is minted only
by the authority bootstrap, checked before any provider call, un-forgeable by
shape, and reachable only from `authority.ts` (architecture test). Hard deny is
monotonic; cross-worldline and unversioned-overwrite writes are denied before the
history seam. Not implemented: direct-DB bypass guard for the new seams,
monotonic-guard coverage for rights/privacy/evidence, and a
CommitCapability audit surface exposed to operators.

## 8. Execution Fabric

`NOT_IMPLEMENTED`. No isolated execution class, no `ExecutionPolicy`, no
`ExecutionTrace` separation from world history.

## 9. DSH Bridge

`NOT_IMPLEMENTED`. No JSON-RPC provider, no agent harness bridge, no reject-path
E2E.

## 10. Capability Foundry

`NOT_IMPLEMENTED`. No artifact→capability reference slice, no verified capability
package, no golden verification.

## 11. RealityProfile Migration

`NOT_IMPLEMENTED`. The profile/lock models and `is_major_upgrade_from` exist; the
checkpoint → shadow replay → drift compare → migrate/fork/reject path does not.

## 12. Experience / Application

`UNCHANGED from Phase A`. The M95-R zh-CN player path is committed and passes the
full regression, but no R7 experience work was done in this slice.

## 13. Reference Worlds

`NOT_IMPLEMENTED for R7`. The Phase A reference evidence (source, prompt,
GEDCOM, heritage) is unchanged; the four R7 reference slices were not built.

## 14. Tests / Build / Lint / Typecheck

* `uv run python scripts/quality.py` → `1507 passed, 1 skipped`, architecture PASS
  (the skip is the documented PostgreSQL `EXTERNAL_BLOCKED` profile).
* `packages/cordis_host`: `tsc --noEmit` 0 errors, `eslint .` clean,
  `vitest run` → 5 files / 21 tests passed.
* `packages/reality`: `pytest tests/unit/reality` → 30 passed; pyright 0 errors.

## 15. Clean clone

`NOT_RUN for this branch`. The Phase A exact-SHA clean clone is recorded for
`a9be096`; no R7 clean-clone run exists yet.

## 16. Remote CI / push status

Phase A: runs `36194471592` and `36196736517` succeeded with all six required
jobs green. Phase B: branch not pushed, so no CI run covers this branch yet.

## 17. Remaining BLOCKED / NOT_PROVEN

* Human Gates 62–66 — `WAITING_HUMAN`, needs a real tester.
* Godot/real-engine E2E — `EXTERNAL_BLOCKED` on this host.
* Live PostgreSQL profile — `EXTERNAL_BLOCKED` (no instance).
* Everything listed as `NOT_IMPLEMENTED` in sections 8–13, plus the JSON-RPC
  bridge and worldline RuntimeLock pinning in sections 4–5.

## 18. Architecture Gates A–J

| Gate | Status | Basis |
|---|---|---|
| A Composition | `PARTIAL` | provider replaceable within the history port; consumer/provider separation guarded; A/B world scope isolation certified; resolved graph exported |
| B Persistence | `PARTIAL` | plugin unload does not remove committed history; ≥100 revisions replay-equal; `expectedRevision` defends lost updates; snapshot-deletion rebuild not yet exercised here |
| C Authority | `PARTIAL` | no capability for ordinary plugins; hard deny monotonic; cross-worldline denied. Direct-DB bypass guard for the new seams pending |
| D Migration | `FAIL` | RealityProfile v1/v2 coexistence and shadow replay not implemented |
| E External Execution | `FAIL` | no execution fabric |
| F DSH | `FAIL` | no bridge |
| G Capability Foundry | `FAIL` | no reference slice |
| H Experience | `PARTIAL` | zh-CN player path exists from Phase A; two experiences sharing one canonical reality not demonstrated |
| I Reliability | `PARTIAL` | repository gate + TS gates green; no R7 clean clone; lifecycle leak test green (S4) |
| J Evidence Integrity | `PASS` | every claim above cites a command or artifact; nothing human/external is inferred; Phase A gates are unchanged and no gate was re-scored |

## 19. What a next agent should do first

1. Implement the JSON-RPC history provider and the Python side that serves it, so
   the Cordis host writes canonical history through the real authority.
2. Pin each worldline to a `RuntimeLock` (from `wanxiang_reality`) at open time and
   assert seam versions against it.
3. Build the Execution Fabric and the outbox/idempotency boundary.
4. Then DSH bridge, Capability Foundry, and the RealityProfile shadow-replay
   migration.
