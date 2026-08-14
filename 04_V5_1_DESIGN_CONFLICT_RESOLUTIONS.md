# v5.1 Design Conflict Resolutions for Engineering

These resolutions prevent ambiguous parts of the v5.1 mother spec from causing duplicate runtime systems.

## R1 — CapabilityCommit

**Resolution:** World reality has exactly three commit kinds: StateCommit, OntologyCommit, LawCommit. `CapabilityCommit` references in evolutionary-distillation prose are interpreted as **runtime capability activation/promotion**, implemented through `RuntimeControlTransaction`, not World Commit.

## R2 — GenesisPackage

**Resolution:** Do not create a second package registry. Implement `GenesisSpec`/`GenesisManifest` consumed from WorldPack + Scenario + overrides. Existing package/version/dependency/rights infrastructure remains authoritative.

## R3 — Fact Space

**Resolution:** Share one semantic Fact shape/scope model where useful, but authority remains separated. A scope change cannot promote belief/hypothesis/reconstruction to canonical truth. Canonical promotion requires the normal Commit boundary.

## R4 — Ω / Possibility Space

**Resolution:** Ω is primarily candidate/derived possibility state. Do not persist a complete enumerable possibility universe. Persist only explicit proposals/candidates/plans/experiments required for audit/recovery. Recompute other possibility views from current facts/laws/affordances where practical.

## R5 — Σ / Γ replay context

**Resolution:** committed events/snapshots must carry or resolve stable semantic-space/law-set/constitution versions sufficient for deterministic interpretation/replay. Old events are never silently interpreted using only latest laws/schema.

## R6 — Meaning/Reality/Experience Engine

**Resolution:** these are conceptual architecture views/facades. They do not mandate three services or three God objects. Existing definition/core/runtime/agency/experience modules implement them.

## R7 — Capability naming

**Resolution:** distinguish `ActorCapability` (in-world learned/usable ability) from `RuntimeCapability` (installed provider/service). Avoid unqualified `Capability` types when ambiguity exists.

## R8 — Triple ledgers

**Resolution:** three logical streams may share append-only persistence infrastructure, but must keep typed schemas, retention/rights policies and query boundaries. Do not merge them into one untyped audit-event table.

## R9 — DeepSeek Harness/Cordis

**Resolution:** optional AgentHarness provider/reference only. Core/authority/persistence/history must function without it. Do not fork it as Wanxiang's base runtime.

## R10 — True Genesis

**Resolution:** preserve a research-grade contract/adapter seam; do not fake open-ended universe/life emergence. Stable implementation is not required unless the repository contains independently validated research evidence satisfying the Goal.

## R11 — 5 Planes / 16 Kernels

**Resolution:** logical responsibility/test boundaries only. Do not create 16 deployable services or packages solely to mirror the diagram.

## R12 — CurrentWorldState

**Resolution:** keep as derived/materialized state for efficient runtime. The authoritative semantics are committed history + version context. Derived state must be rebuildable.
