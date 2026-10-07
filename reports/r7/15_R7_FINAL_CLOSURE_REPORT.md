# R7 15 — Final Closure Report

## Final Decision

`WAITING_HUMAN`

R7 Phase B is **implementation-complete for every locally executable design
slice in the R7 Goal**. The overall program cannot be called Stable-complete
because v5.5 Gates 62–66 still require a genuine human player. Live official
DeepSeek Harness model-backed qualification and Godot/real-engine qualification
remain external rows; they are not silently promoted to PASS.

Qualification anchor for the finished R7 implementation:
`f7b719df2ccdd906bf2c0f9c3474b1cbe219bbbf`.

Both workflows on that SHA are green:

- CI run `37582984372`;
- exact-SHA R7 clean-clone run `37582984421`.

No `v5.5.0` Stable tag and no `v5.6` release/branch were created by this
closure.

## 1. Composition / Cordis

**PASS.** Cordis `4.0.0-rc.10` is the pinned first-generation composition
runtime. The repository does not reimplement a parallel Cordis-like kernel.
S1–S5 cover 100-commit continuity, plugin unload continuity, provider
replacement on the same worldline, 1000 mount/unmount cycles, scope isolation
and resolved-graph export.

## 2. RealityProfile / WorldProfile / RuntimeLock

**PASS.** RuntimeLock is persisted per worldline with a frozen schema and
tamper-evident digest. Python `open_worldline()` fails closed on missing lock
(unless creating genesis), identity/profile/provider/schema/config drift and
returns `MIGRATION_REQUIRED` for major RealityProfile change. The Cordis host
reads the same persisted lock and revalidates it.

Evidence: `reports/r7/01_WORLDLINE_RUNTIME_LOCK_REPORT.md`.

## 3. Service seams / History / Replay / Branch / Lineage

**PASS.** Versioned service seams are explicit; providers are replaceable behind
contracts. History uses expected revision semantics. Plugin unload cannot remove
committed history. Snapshotless replay is qualified with a fresh empty snapshot
store and reproduces the canonical state hash/revision from history alone.
Branch isolation and lineage semantics remain distinct from sandbox/runtime
snapshots.

Evidence: `reports/r7/03_SERVICE_SEAMS_REPORT.md`,
`reports/r7/06_HISTORY_AUTHORITY_RPC_REPORT.md`,
`tests/integration/test_r7_snapshotless_replay.py`.

## 4. Authority / Security

**PASS.** Canonical write is capability/lease protected, minter and persistence
write surfaces are architecture-golden guarded, ordinary actors/plugins cannot
append directly, forged/cross-worldline credentials fail, and the Cordis policy
layer provides monotonic hard-deny coverage for cross-worldline, rights,
evidence and external-effect violations. An operator-safe authority grant audit
surface exists.

Evidence: `reports/r7/06B_AUTHORITY_SECURITY_REPORT.md`.

## 5. Execution Fabric / irreversible effects

**PASS for R7 reference scope.** Untrusted/generated work is routed through the
Execution Fabric with deny-by-default policy and explicit ExecutionTrace that is
not World History. A real cross-process localhost HTTP effect handler qualifies
durable intent, idempotency, duplicate suppression, timeout/crash ambiguity,
restart, retry and reconciliation.

Not claimed: hostile-code container/microVM isolation or production
payment/robot/chain providers.

Evidence: `reports/r7/07_EXECUTION_FABRIC_REPORT.md`.

## 6. Agent / DSH

**PASS for the Wanxiang integration contract; live official runtime remains
EXTERNAL_BLOCKED.**

The agent-harness seam, JSON-RPC bridge, consequence callback path, payload
validation and proposal-only behavior are covered with a real subprocess
reference harness. An optional official `deepseek-harness-sdk` provider is
implemented and unit-qualified without faking a live model session. It imports
no Commit Authority/persistence writer.

Live model-backed official DSH E2E still needs an actual official runtime route
and credentials and remains `EXTERNAL_BLOCKED`.

Evidence: `reports/r7/08_AGENT_HARNESS_BRIDGE_REPORT.md`.

## 7. Capability Foundry

**PASS for the tracked reference-artifact path.** Artifact2Capability covers
candidate/interface/environment, GOLDEN/NEGATIVE/BOUNDARY/SECURITY execution,
verification report, provenance-bound package, C3 registry admission,
revocation/version coexistence and proposal-only invocation. Package admission
binds the declared interface and exact verification cases.

The science reference slice proves successful capability execution does not
mutate World history; a later ordinary World action must still pass Authority.

Evidence: `reports/r7/09_CAPABILITY_FOUNDRY_REPORT.md`.

## 8. RealityProfile migration

**PASS for deterministic/reference scope.** Version coexistence, checkpoint,
shadow replay, drift comparison, typed migrate/fork/reject plan, explicit
approval and explicit sink are implemented. Major profile change cannot silently
hot-swap a writable worldline.

Evidence: `reports/r7/10_REALITY_MIGRATION_REPORT.md`.

## 9. Experience / Projection / Distribution

**PASS for R7 contract/shared-reality scope.** ExperienceBlueprint,
InteractionProfile, ProjectionProfile, DistributionAdapter, deterministic
DistributionBuild and WorldExperienceCard are first-class contracts.
Projection/distribution contain no canonical writer or canonical storage.

The Original/Fiction reference world runs a Player Experience and read-only
Observer Experience over the same WorldRuntime; a commit is immediately visible
through both, and branch divergence is worldline divergence rather than copied
Experience state. The existing product path remains zh-CN-first and
Player/Studio separated.

Evidence: `reports/r7/11_EXPERIENCE_APPLICATION_REPORT.md`.

## 10. World Capability Gateway

**PASS for Python SDK contract scope.** AgentSessionIdentity binds
principal/role/world/branch/audit id, expiry and capability/rights/secret scopes.
WorldSkill describes the bounded interface. The gateway exposes observation,
history, branch-diff, proposal-only action and governed fork/experiment requests,
and intentionally exposes no commit/force-commit/raw database/rewrite-history
operation.

MCP/OpenAPI/CLI/gRPC may adapt this gateway; none is the canonical World
protocol.

## 11. Reference worlds

**PASS as bounded architecture slices.**

- Original/Fiction: commit, rejection, branch isolation and shared reality.
- Heritage: rights/source gating, reconstruction-vs-source distinction and
  review-before-canon.
- Agent: real cross-process proposal/consequence flow.
- Science/Capability: C3 verified capability, isolated execution, proposal-only
  result and separate World commit.

Evidence: `reports/r7/12_REFERENCE_WORLDS_REPORT.md`.

## 12. Observability / operations

**PASS for R7 contract scope.** R7 operational/readiness projections cover
world/worldline/revision, RuntimeLock/profile/provider graph refs, proposal/
commit/reject counters, replay/history latency, actor/model/execution accounting,
migration/outbox status and explicitly mark themselves non-canonical. Developer,
operator and zh-CN player quickstarts are tracked under `docs/runbooks/`.

## 13. Full regression / exact-SHA clean clone

**PASS.**

At `f7b719df2ccdd906bf2c0f9c3474b1cbe219bbbf`:

- Python CI: `1749 passed, 1 skipped`; Ruff PASS; Pyright 0 errors;
  architecture PASS; kernel guard 0 violations.
- Live PostgreSQL CI profile: `4 passed`.
- TypeScript: SDK 22 tests PASS; Cordis host 74 tests PASS; lint/typecheck/build
  PASS.
- Exact-SHA qualification: 19/19 required steps PASS, 0 failed, 0 skipped,
  including full Python, security, RuntimeLock, migration, reference worlds,
  pnpm/TS and browser E2E.

Evidence: `reports/r7/13_FULL_REGRESSION_REPORT.md` and
`reports/r7/14_CLEAN_CLONE_REPORT.md`.

## 14. Architecture Gates A–J

| Gate | Status | Basis |
|---|---|---|
| A Composition | **PASS** | replaceable providers, consumer/provider separation, world-scope isolation, resolved graph, 1000-cycle lifecycle |
| B Persistence | **PASS** | committed history survives unload, 100+ revision replay, expected-revision conflicts, snapshotless reconstruction |
| C Authority | **PASS** | branded write capability, direct-write surface guard, monotonic hard deny, cross-worldline denial, safe audit view |
| D Migration | **PASS (bounded)** | v1/v2 coexistence, shadow replay, drift detection, migrate/fork/reject + explicit approval |
| E External Execution | **PASS (reference scope)** | isolated process provider, trace/history separation, real cross-process outbox/reconciliation path |
| F DSH | **PASS (integration contract)** | observe/propose/reject/consequence/no-direct-commit; official live model E2E remains external |
| G Capability Foundry | **PASS (reference scope)** | real tracked Artifact→C3 verification→registry→proposal-only invocation |
| H Experience | **PASS (reference scope)** | two Experiences share one canonical world; zh-CN product path retained |
| I Reliability | **PASS** | full CI + exact-SHA full clean clone + lifecycle/security/browser/PostgreSQL |
| J Evidence Integrity | **PASS** | DESIGN/IMPLEMENTED/VALIDATED/EXTERNAL/HUMAN boundaries remain explicit |

## 15. Remaining non-code blockers

These are not hidden implementation gaps:

1. v5.5 Gates 62–66: `WAITING_HUMAN`; a real tester must complete
   `reports/M95_PLAYER_TEST_PACKET_ZH_CN.md`.
2. Gate 78 Godot/real-engine E2E: `EXTERNAL_BLOCKED` until a supported engine
   route is available.
3. Live model-backed official DeepSeek Harness E2E: `EXTERNAL_BLOCKED` until
   the official SDK/runtime route and credentials are available.

The old "live PostgreSQL unavailable" R7 blocker is closed by GitHub Actions:
PostgreSQL 16 is started as a service and the live integration profile passes.

## 16. Release boundary

R7 design implementation evidence does not bypass v5.5 human acceptance and
does not authorize a v5.6 release. The repository may now wait on genuine human
and external qualification without inventing more local architecture work.
