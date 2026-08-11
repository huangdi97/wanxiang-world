# Old G0–G12 → Wanxiang Engineering Program Migration Notes

## 1. Purpose

The v5 master specification's G0–G12 roadmap remains valid as a **macro implementation roadmap**. This program does not replace its product intent. It changes the execution granularity and dependency control so Codex does not implement multiple independent kernels shallowly in one oversized Goal.

---

## 2. What remains unchanged

The following are preserved:

- G0→G12 overall progression from deterministic core toward living worlds, domains, co-simulation and release qualification;
- 5 Planes / 16 Kernels;
- Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection;
- Canonical World State / single Commit Authority;
- event sourcing / snapshot / replay / branch;
- source/evidence gate;
- rights/provenance;
- deterministic/no-LLM core;
- modular monolith first;
- synthetic domain/world fixtures before real data packs;
- Red Chamber, family, museum and Liaoshen as reference World/Domain packages, not Core.

---

## 3. Why execution is changed

The old roadmap names large capabilities. Several single Goals contain multiple independently complex kernels and standards. If sent directly as a one-shot coding task, Codex can satisfy the surface area by creating many shallow modules and interface stubs without deeply qualifying authority/replay/migration semantics.

The new program therefore distinguishes:

```text
Macro G-number / product roadmap
        ↓
Engineering Phase
        ↓
Executable Goal
        ↓
Work Packages
        ↓
Acceptance Gate
        ↓
Milestone
```

---

## 4. Mapping table

| Legacy | Original intent | New execution treatment |
|---|---|---|
| G0 | repository & engineering foundation | split into G00A repository/toolchain + G00B architecture guards |
| G1 | authoritative world kernel | split into contracts, commit, event store, replay/branch, persistence/migration, vertical qualification |
| G2 | living world substrate | split by spatial, temporal, material, body, institution, population/scheduler |
| G3 | agency/cognition/skill | split by observation, memory/belief, actor/org, action/affordance, resolver, skill, capability |
| G4 | compiler/packages/evidence | foundational evidence/rights contracts move earlier; full registry/source/compiler/review remains P4 |
| G5 | embodiment + Studio + 2D | host authority boundary comes first; embodiment/projection/UI separated |
| G6 | host/lifecycle/multiplayer | separated into lifecycle, multi-client command semantics, recovery/resource control |
| G7 | reality bridge + challenge + capability | separated into Reality Bridge, fusion, opportunity/challenge, director, experiment; capability moved with agency |
| G8 | literature / Red Chamber | treated as system qualification milestone + source-gated reference pack, not Core feature growth |
| G9 | family | split into interop, semantic family world, privacy/living archive/persona modes |
| G10 | heritage | split into IIIF, Linked Art/CIDOC, semantic twin, scenarios/simulation integration |
| G11 | co-sim/campaign/Liaoshen | split into generic simulation contract/orchestrator, synthetic campaign mechanisms, strategy experiments, source-gated Liaoshen |
| G12 | hardening/SDK/advanced projection | hardening moves throughout every milestone; final phase becomes release qualification + optional adapters |

---

## 5. Critical order corrections

### 5.1 Evidence/Rights/Version foundations move earlier

Why: Claim/Evidence/Rights/version metadata are first-class concepts used by canonical data. Waiting until the compiler phase would force schema breakage after the kernel is already persisted.

What moves early:
- foundational Claim/Evidence references;
- RightsEnvelope/decision seam;
- schema/version identifiers;
- provenance hooks.

What remains later:
- full Source Registry;
- review workflow;
- completion compiler;
- domain-specific rights policies;
- rich Studio review UI.

### 5.2 Minimal Host authority boundary before serious UI

Why: Studio/Player must learn from the beginning that API/UI are not the world authority. UI should use stable command/query/projection boundaries rather than runtime internals.

### 5.3 Co-Simulation port concept is frozen before campaign integration

The full co-simulation orchestrator remains later, but the architectural rule is frozen early: a simulator emits events/proposed deltas and never writes canonical state directly.

### 5.4 Hardening is continuous

Migration, observability, rights, security, replay compatibility and architecture conformance begin at their first relevant schema/runtime, rather than appearing for the first time in G12.

---

## 6. Goals intentionally not executed tonight

Do not implement tonight:

- G02 spatial/time/material/body/social substrate;
- G03 cognition and agent memory;
- G04 world compiler;
- G05 Studio/Phaser;
- G06 multiplayer/background host beyond M1 minimum;
- G07 reality/challenge/director;
- G08 Red Chamber;
- G09 family;
- G10 museum;
- G11 campaign/co-simulation;
- G12 advanced adapters.

This is not because they are less important. It is because all of them depend on correct event/commit/replay/version semantics.

---

## 7. What tonight must achieve instead

The batch should leave the repository in a state where the following statement is literally testable:

> A deterministic synthetic world instance can receive a structured command, validate and resolve it, commit an ordered event and canonical delta exactly once, persist the result, create a snapshot, replay to the same semantic state, fork an isolated child branch, reject stale revisions and duplicate effects, and reproduce this behavior without an LLM key.

Once this is true, later “living world” capabilities have a trustworthy substrate.

---

## 8. Resume rule after tonight

Do not tell Codex “continue G0–G12” immediately after M1.

First inspect:
- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`;
- `reports/ACCEPTANCE_MATRIX.md`;
- architecture guard output;
- file/module size report;
- migration/replay evidence;
- Git checkpoint.

Only if M1 is PASS should the next engineering contract be authored/frozen for `G02A Spatial Topology & Access`.
