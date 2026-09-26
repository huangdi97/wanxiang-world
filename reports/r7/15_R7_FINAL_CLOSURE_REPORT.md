# R7 15 — Final Closure Report

## Final Decision

`NOT_COMPLETE`

Phase A (v5.5 Stable closure, as far as evidence allows) is closed. Phase B (R7)
now has a working, CI-verified slice: the Cordis composition runtime with
versioned seams and lock pinning, the cross-language history-authority bridge,
the Execution Fabric with its irreversible-effect outbox, versioned RealityProfile
migration, and the agent-harness (DSH seam) bridge with a reference harness.
The Capability Foundry, the official DSH integration, the R7 reference worlds and
the R7 clean-clone run are not implemented, so the R7 Definition of Done is not
met. No R7 claim below is made without a reproducible command or artifact.

## 1. Branch / HEAD / worktree

```text
branch     feature/r7-cordis-native
code head  526b49b goal R7: verify the cross-language history seam in CI
base       48b3402 (release/v5.5-stable-certification)
worktree   clean: every R7 artefact is committed, no untracked or modified file
```

## 2. v5.5 Stable status

Gate 79 `PASS` at candidate `a9be096` (CI verified again at the evidence commit
`48b3402`). Gates 62–66 `USER_INPUT_REQUIRED` / `WAITING_HUMAN` — no human rating
was fabricated. Gate 78 `EXTERNAL_BLOCKED` (no Godot). Gate 80 `LOCKED`; no
`v5.5.0` tag or release exists. Nothing in Phase A was re-scored by this turn.

## 3. Cordis runtime exact version

`cordis@4.0.0-rc.10`, pinned in `packages/cordis_host/package.json` and reported
verbatim in `artifacts/r7/composition/resolved_graph.json`
(`compositionRuntime.version`, `exact: true`). Node `v22.15.0`.

## 4. WorldProfile / RealityProfile / RuntimeLock

`IMPLEMENTED` / `VALIDATED` — see `reports/r7/01_WORLDLINE_RUNTIME_LOCK_REPORT.md`
and `reports/r7/05_VERSIONED_REALITY_PROFILE_MIGRATION_REPORT.md`.
`wanxiang_reality` owns one lock model (`RealityProfile`, `WorldProfile`,
`RuntimeLock`, canonical-JSON digests, typed validation) and a per-worldline
profile registry; the Cordis host requires a validated `RuntimeLockRef` to open a
worldline, asserts live seam digests against the pinned contract versions, and
records `runtimeLocks` in the resolved graph. Remaining: the lock is supplied by
the caller rather than persisted, and the Python runtime path does not yet refuse
to open a worldline without one.

## 5. Service seams and providers

`IMPLEMENTED` — see `reports/r7/03_SERVICE_SEAMS_REPORT.md` and
`reports/r7/06_HISTORY_AUTHORITY_RPC_REPORT.md`. 16 versioned contracts with a
shared seam digest across Python and TypeScript, and the JSON-RPC history
authority that previously was the missing bridge now exists: Python
`wanxiang_reality.rpc` serves the frozen protocol over stdio and the Cordis host
drives it through `RpcHistoryProvider`/`RpcAuthorityBootstrap`, mapping `-32001`
and `-32002` to typed domain errors. The cross-language test runs in CI.

## 6. History / Replay / Branch / Lineage

`PARTIAL`. The composition spike certifies 100 continuous commits, monotonic
revision, typed `expectedRevision` conflict, rebuild-from-history equality and a
1000× mount/unmount leak check. The RPC authority enforces the same revision
discipline over the wire, verifies batch-vs-incremental hash equality and denies
duplicate/unauthorised appends. The repository's existing Python event
store/branch/replay remains the production path and was not modified.

## 7. Authority / Security

`PARTIAL`, and the implemented part is certified: the capability is minted only by
the authority bootstrap, checked before any provider call, un-forgeable by shape,
and reachable only from `authority.ts` (architecture test). Hard deny is
monotonic; cross-worldline and unversioned-overwrite writes are denied before the
history seam; the RPC append path refuses a request without a granted token and
changes nothing on denial. Not implemented: direct-DB bypass guard for the new
seams, monotonic-guard coverage for rights/privacy/evidence, and an operator-facing
CommitCapability audit surface.

## 8. Execution Fabric

`IMPLEMENTED` / `VALIDATED` for the implemented scope — see
`reports/r7/07_EXECUTION_FABRIC_REPORT.md`. New leaf package `packages/execution`:
deny-by-default `ExecutionPolicy`, honest `ExecutionTrace` that is explicitly not
world history, a real local-subprocess provider, and an append-only outbox for
irreversible external effects with idempotency-key suppression, pre-call markers,
ambiguity recording and reconciliation. Not claimed: container/VM/seccomp-level
sandboxing, execution snapshot/resume, and a real third-party effect handler.

## 9. DSH Bridge

`PARTIAL` — see `reports/r7/08_AGENT_HARNESS_BRIDGE_REPORT.md`. The provider port,
the frozen `wanxiang.r7.agent-harness-rpc.v1` protocol, the JSON-RPC bridge with
timeout and typed protocol errors, and a real reference harness process all exist
and are tested (the reference harness reports `officialDsh: false`). The official
DeepSeek Harness was never provided in this environment, so no official-DSH
integration is claimed.

## 10. Capability Foundry

`NOT_IMPLEMENTED`. No artifact→capability reference slice, no verified capability
package, no golden verification.

## 11. RealityProfile Migration

`IMPLEMENTED` / `VALIDATED` at unit and property level — see
`reports/r7/05_VERSIONED_REALITY_PROFILE_MIGRATION_REPORT.md`. Per-worldline
version pinning with coexistence (no silent hot swap), checkpoint + shadow replay,
drift comparison and a typed `migrate`/`fork`/`reject` plan; applying a migration
requires an explicit approval and an explicit sink. Remaining: no production-scale
long-history migration and no approval surface in API/CLI.

## 12. Experience / Application

`UNCHANGED from Phase A`. The M95-R zh-CN player path is committed and passes the
full regression, but no R7 experience work was done in this slice.

## 13. Reference Worlds

`NOT_IMPLEMENTED for R7`. The Phase A reference evidence (source, prompt, GEDCOM,
heritage) is unchanged; the four R7 reference slices were not built.

## 14. Tests / Build / Lint / Typecheck

* `uv run python scripts/quality.py` → `1605 passed, 1 skipped`, architecture
  `PASS` (the skip is the documented PostgreSQL `EXTERNAL_BLOCKED` profile).
* R7 Python suites: `tests/unit/reality` 64, `tests/unit/execution` 50,
  `tests/unit/runtime/test_r7_agent_harness.py` 14 → 128 passed.
* `packages/cordis_host`: `tsc --noEmit` 0 errors, `eslint .` clean,
  `vitest run` → 7 files / 41 tests passed, including the real cross-language
  Python authority test.
* Lint/format/typecheck: `ruff check .` clean, `ruff format --check .` clean,
  `pyright` 0 errors.
* Snapshot gates moved with the R7 abstractions and were regenerated, not
  weakened: `registry_classes` 17→18, `ports` 44→48, `state_classes` 39→40; hard
  invariants unchanged (0 import cycles, exactly 1 commit path, 0 manager-named
  classes). The SDK baseline change is purely additive (15 added, 0 removed).

## 15. Clean clone

`NOT_RUN for this branch`. The Phase A exact-SHA clean clone is recorded for
`a9be096`; no R7 clean-clone run exists yet.

## 16. Remote CI / push status

Phase A: runs `36194471592`, `36196736517` green. Phase B: `36204929548`
(`1fe086b`), `36206057016` (`dc06062`) green; `36265050397` (`a7acc21`) exposed a
real gap — the `ts` job had no Python toolchain, so the cross-language test failed
with `spawn uv ENOENT`. The `ts` job now provisions uv and syncs the Python
workspace, and run `36268215094` at `526b49b` is green with all six jobs passing
(`ts`: 41 passed, 0 skipped — the cross-language test genuinely ran).

## 17. Remaining BLOCKED / NOT_PROVEN

* Human Gates 62–66 — `WAITING_HUMAN`, needs a real tester.
* Godot/real-engine E2E — `EXTERNAL_BLOCKED` on this host.
* Live PostgreSQL profile — `EXTERNAL_BLOCKED` (no instance).
* Official DSH integration — `EXTERNAL_BLOCKED`: no official harness binary or
  credentials were provided.
* Capability Foundry, R7 reference worlds, R7 clean-clone run —
  `NOT_IMPLEMENTED` / `NOT_RUN`, no external blocker, simply not built yet.

## 18. Architecture Gates A–J

| Gate | Status | Basis |
|---|---|---|
| A Composition | `PARTIAL` | provider replaceable within the history port; consumer/provider separation guarded; A/B world scope isolation certified; resolved graph incl. `runtimeLocks` exported |
| B Persistence | `PARTIAL` | plugin unload does not remove committed history; ≥100 revisions replay-equal; `expectedRevision` defends lost updates (in-process and over RPC); snapshot-deletion rebuild not yet exercised here |
| C Authority | `PARTIAL` | capability minted only by the bootstrap; hard deny monotonic; cross-worldline denied; RPC append denied without a granted token. Direct-DB bypass guard for the new seams pending |
| D Migration | `PASS` (unit scope) | RealityProfile v1/v2 coexistence, checkpoint + shadow replay, drift compare and typed migrate/fork/reject; no production-scale migration run |
| E External Execution | `PASS` (unit scope) | deny-by-default policy, trace separated from world history, real subprocess provider, outbox idempotency/ambiguity; container-level sandboxing not claimed |
| F DSH | `PARTIAL` | harness port, protocol, bridge and reference harness validated; official DSH `EXTERNAL_BLOCKED` |
| G Capability Foundry | `FAIL` | no reference slice |
| H Experience | `PARTIAL` | zh-CN player path exists from Phase A; two experiences sharing one canonical reality not demonstrated |
| I Reliability | `PARTIAL` | repository gate + TS gates green; no R7 clean clone; lifecycle leak test green (S4) |
| J Evidence Integrity | `PASS` | every claim above cites a command or artifact; nothing human/external is inferred; Phase A gates are unchanged and no gate was re-scored |

## 19. What a next agent should do first

1. Capability Foundry: artifact→capability reference slice running inside the
   Execution Fabric, with a verified capability package and golden verification.
2. Wire the agent-harness bridge into the Cordis host consequence path, and
   integrate the official DSH when a binary/credentials are available.
3. Persist the `RuntimeLock` per worldline and make the Python runtime path refuse
   to open a worldline without one; add the direct-DB bypass guard.
4. Build the four R7 reference slices and run the R7 clean-clone certification.
