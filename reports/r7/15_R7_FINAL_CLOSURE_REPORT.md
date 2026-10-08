# R7 15 — Final Closure Report

## Final Decision

`WAITING_HUMAN`

R7 is **implementation-complete for every locally executable design slice in the
canonical R7 master/Goal, including the extended post-closure sweep**. The
remaining blockers are genuine human/external qualification; they are not
converted into more architecture work.

Implementation code anchor:
`8ebbc4f04a265ab4d9c380fc8da7bbabfe86ce8f`.

At that code anchor:
- CI run `37722944558`: all six jobs green;
- exact-SHA R7 run `37722944544`: 19/19 required steps PASS, 0 failed,
  0 skipped;
- Python: `1802 passed, 1 skipped`; live PostgreSQL: `4 passed`;
- Pyright: 0 errors/warnings; architecture PASS; kernel guard 0 violations;
- SDK TypeScript: 22/22; Cordis host: 77/77.

This file is part of a later documentation synchronization commit. Therefore the
**final closure predicate** is intentionally defined without pretending a future
SHA was already tested: the current branch HEAD must itself have both `ci` and
`r7-qualification` green. If either is absent/red, final exact-SHA closure is
`NOT_PROVEN` until rerun.

No `v5.5.0` Stable tag and no `v5.6` release/branch is created by R7.

## 1. Cordis composition and upgrade boundary

**PASS.** Wanxiang directly uses exactly pinned `cordis@4.0.0-rc.10` as its
first-generation Composition Runtime; there is no second home-grown Cordis-like
kernel. S1-S5 cover 100 commits, unload continuity, provider replacement,
1000-cycle lifecycle, world-scope isolation and resolved graph export.

Current upstream DeepSeek Harness has continued evolving its vendored Cordis.
R7 does not auto-upgrade merely because upstream moved: a host-runtime major or
semantically significant upgrade is Class D and requires clean-room replay,
plugin compatibility, profile resolution, lifecycle leak and rollback
qualification.

## 2. Profile / Bundle / RealityProfile / RuntimeLock / Artifact

**PASS.** Profile/Bundle/Lock/Artifact is first-class. Bundle composition fails
closed on RealityProfile mismatch, unapproved dimension conflict, artifact
identity conflict or missing seam/provider pin. The resolved bundle-stack digest
is bound into immutable RuntimeLock lineage.

RuntimeLock remains persisted per worldline and Python/Cordis world opening
fails closed on missing/tampered/drifted locks or incompatible major
RealityProfile changes.

## 3. World Bootstrap and bounded WorldHandle

**PASS.** Cordis World Bootstrap verifies exact lock, required seams,
resolved-graph binding and history head before exposing a world. The public
WorldHandle exposes bounded observe/history/propose/branch/capability/skill
operations and deliberately withholds raw Context, persistence and Commit
Authority.

## 4. Service seams, history, replay, branch and lineage

**PASS.** Versioned service definitions are independent from providers. History
uses expected-revision semantics; committed history survives plugin unload;
snapshotless reconstruction reproduces the canonical state from complete
history; Branch/Lineage remain distinct from execution snapshots.

## 5. Authority, invariants and three ledgers

**PASS.** Canonical writes remain capability/lease protected with write-surface
guards and monotonic hard deny. Kernel/Domain/World invariant layers converge at
the same authority path.

World history, actor trajectory evidence and runtime-control evidence are
separate ledgers linked by references/hashes rather than collapsed into one
store. No new commit path was introduced.

## 6. Execution Fabric

**PASS for the required/reference R7 scope.** Policy-bound execution is routed
through a provider-neutral ExecutionRouter. Local process and a real Docker
reference provider are qualified. The Docker slice uses a locally constructed
no-pull image and verifies read-only root, no external network, no host mounts
and dropped capabilities.

Content-addressed execution checkpoints can fast-forward identical successful,
side-effect-free work after restart. Secret-bearing/external-effect work is
excluded and remains governed by durable outbox/idempotency/reconciliation.

R7 intentionally does not build a microVM/VM/distributed sandbox fleet without a
real workload requiring it.

## 7. Agent / official DSH boundary

**PASS for Wanxiang's integration contract; live official model-backed DSH E2E
remains `EXTERNAL_BLOCKED`.**

The reference subprocess bridge covers observation, proposal/abstention and
committed/rejected consequence. The optional official DeepSeek Harness SDK
adapter is implemented without importing authority/persistence writers. No fake
live-model evidence is used.

## 8. Capability Foundry and Verified Capability Marketplace

**PASS for bounded reference scope.** Artifact2Capability covers interface /
environment extraction, GOLDEN/NEGATIVE/BOUNDARY/SECURITY verification,
provenance, C3 admission, lifecycle/revocation and proposal-only invocation.

The Marketplace is discovery over the verified registry, not a second trust
system. It cannot upgrade promotion level or activate revoked/suspended
packages.

Two real tracked reference paths now exist: the original science capability and
a paper+exact-upstream-repository slice with pinned source provenance and license
evidence. Neither auto-commits scientific output to World truth.

## 9. World Capability Gateway / WorldSkill

**PASS.** The Python SDK gateway exposes scoped metadata/schema/entity/relation/
history/worldline/branch-diff/capability queries, proposal-only actions and
governed fork/experiment/simulation/order requests. Raw canonical projections
require an explicit right. AgentSessionIdentity binds principal, role,
world/branch, actor lease, capability/rights/secret scope, expiry and audit id.

No direct-update, raw database update, validator bypass, history rewrite or force
commit surface exists. MCP/OpenAPI/CLI/gRPC remain adapters, not canonical
protocols; R7 already satisfies the master requirement to establish an SDK/MCP
adapter path via the Python SDK.

## 10. Experience / Projection / Distribution

**PASS for contract/shared-reality scope.** First-class ExperienceBlueprint,
InteractionProfile, ProjectionProfile, DistributionAdapter/Build and
WorldExperienceCard remain non-canonical.

An explicit ExperienceRuntime now coordinates entry/continue, interaction
routing, projection refresh and distribution capabilities through the existing
ExperiencePlayerService. It has no canonical state/event store/commit method.
The product path remains zh-CN-first and Player/Studio separated.

## 11. Reference Worlds and research evidence

**PASS as bounded slices.** Original/Fiction, Heritage, Agent and
Science/Capability slices reuse the same production contracts. A sanitized,
hash-verifiable WorldRunArtifact records reference research evidence without
becoming World truth.

## 12. Reliability / exact SHA

**PASS at implementation code anchor.** CI and exact-SHA evidence are detailed
in reports 13/14. Final documentation HEAD must independently satisfy the same
two-workflow predicate; no SHA inheritance is assumed.

## 13. Architecture Gates A-J

| Gate | Status | Basis |
|---|---|---|
| A Composition | **PASS** | Cordis composition, provider replacement, scope isolation, Bundle/Lock binding, lifecycle |
| B Persistence | **PASS** | unload-safe history, expected revision, replay, snapshotless reconstruction |
| C Authority | **PASS** | single protected write path, layered invariants, hard deny, direct-write guards |
| D Migration | **PASS (bounded)** | profile coexistence, shadow replay, drift, migrate/fork/reject |
| E External Execution | **PASS (reference scope)** | process + real Docker reference, trace/history split, checkpoint/outbox governance |
| F DSH | **PASS (integration contract)** | observe/propose/consequence/no direct commit; live official model external |
| G Capability Foundry | **PASS (reference scope)** | verified artifacts, paper/repo slice, marketplace bound to C3 registry |
| H Experience | **PASS (reference scope)** | shared canonical World plus explicit ExperienceRuntime, zh-CN chain |
| I Reliability | **PASS at code anchor** | CI + exact-SHA full qualification; final docs HEAD must rerun |
| J Evidence Integrity | **PASS** | human/external/reference/production claims remain separated |

## 14. Intentionally deferred, not missing R7 closure work

The canonical R7 design deliberately defers these until a real workload demands
them:

- microVM / full-VM / multi-host sandbox fleet;
- distributed scheduler and multi-host image cache;
- mandatory Wasm Component Model ABI / second composition host;
- production SaaS/payment/robot/chain effect providers;
- every hypothetical RealityProfile family;
- every distribution channel as a shipped product.

Implementing these now would violate R7's own no-premature-abstraction rule.

## 15. Remaining blockers

1. v5.5 Gates 62-66: `WAITING_HUMAN`; a genuine tester must complete
   `reports/M95_PLAYER_TEST_PACKET_ZH_CN.md`.
2. Godot/real-engine Gate 78: `EXTERNAL_BLOCKED`.
3. Live model-backed official DeepSeek Harness E2E: `EXTERNAL_BLOCKED` until
   runtime route + credentials exist.

Live PostgreSQL is qualified in CI and is not an R7 blocker.

## 16. Release boundary

R7 engineering completion does not bypass v5.5 human acceptance, does not create
a v5.5 Stable tag, and does not authorize v5.6. Once final documentation HEAD is
green, there is no remaining locally executable R7 design gap that should be
filled by inventing another subsystem.
