# Wanxiang v5.1 Minimal-Core Consolidation & Migration Program Architecture

## 1. Program intent

v5.1-R1 is an architectural deepening of v5.0, not a greenfield rewrite. The program therefore uses **compatibility-first consolidation**:

`VERIFY → CLASSIFY → DELETE/MERGE → ADAPT → ADD IRREDUCIBLE SEMANTICS → MIGRATE → REQUALIFY`.

The default action for an existing healthy capability is `KEEP` or `ADAPT`, never `REPLACE`.

## 2. Target physical architecture

The logical 5 Planes / 16 Kernels are retained, but the durable physical Python/business-code surface should converge toward five cohesive packages plus infrastructure/adapters:

```text
packages/
  core/            # identity/fact/transition/commit/authority/ledger/replay/branch/invariants
  definition/      # source/evidence/rights/candidates/distillation/genesis/compiler/packages
  runtime/         # host/substrate/scheduler/cosim/reality bridge/orchestration/runtime capabilities
  agency/          # perception/belief/memory/actor/org/skills/harness/trajectory
  experience/      # session/embodiment/projection/director/experiment
  infrastructure/  # persistence/API/providers/simulators/sensors/rendering/assets
```

This is a **target dependency topology**, not a forced rename of every existing module. If the current repository already satisfies the same boundaries with fewer/smaller moves, preserve it and document the mapping.

## 3. Minimal semantic core

The stable core must be able to express:

```text
Distinction  -> stable Identity semantics
Relation     -> typed Relation / scoped Fact semantics
Transition   -> Delta / Event semantics
Commitment   -> one Commit Authority / one World mutation boundary
```

The core must not know Red Chamber, Liaoshen, GEDCOM, museum object classes, specific LLM SDKs, Godot, Babylon, DeepSeek Harness, or concrete simulators.

## 4. One-principle architecture

- **One Reality**: one authoritative committed world history.
- **One Commit Boundary**: every world mutation passes the same authority pipeline.
- **One Event Semantics**: one ordered committed-history model; specialized ledgers may share append-only infrastructure.
- **One Branch Model**: one fork/isolation/replay model.
- **One Candidate Envelope**: generated/distilled/reconstructed proposals share a common candidate contract.
- **One Package System**: Genesis, Heritage, AI or runtime features do not invent parallel package registries.
- **One Runtime Composition Root**: runtime provider composition is centralized and typed, not a global service-locator scattered across business code.
- **One Stable World ABI**: external providers/adapters speak a narrow, versioned contract.
- **One Schema Pipeline**: Python/API/TypeScript schemas have one source/generation path.

## 5. Commit model

World reality supports exactly three semantic commit kinds:

```text
WorldCommit
  STATE      -> facts/state within existing ontology/laws
  ONTOLOGY   -> semantic/ontology-space change
  LAW        -> effective-law/rule-set change
```

These use **one authority pipeline**, not three engines/repositories.

Runtime provider installation/reload/rollback is **not** a World Commit. It uses `RuntimeControlTransaction` and the Runtime Control Ledger.

## 6. Current state

`CurrentWorldState` remains useful as a materialized projection/cache, but authority is the committed history plus the semantic/law version context required to fold it. Derived state must be discardable and reconstructable.

## 7. Fact Space

Use a shared semantic Fact contract with explicit scope/provenance/time, while keeping authority separated by policy/repository/use-case boundaries. Changing a Fact scope must never silently promote belief/hypothesis/reconstruction to canonical reality.

## 8. Genesis

Do not build a second package ecosystem. `GenesisSpec` is an initialization specification consumed from WorldPack + Scenario + overrides. Designer Genesis is stable; Evolutionary Genesis may be experimental; True Genesis remains a research contract unless evidence supports a real implementation.

## 9. Distillation

The existing compiler/source/evidence pipeline should be reused and generalized. `Distiller` produces `CandidateEnvelope`; it does not commit reality. LLM/vision/audio/rule extractors are providers, not separate engines.

## 10. Runtime Capability Fabric

Use typed service contracts, provider descriptors, explicit scopes, dependency DAGs and reversible runtime lifecycle. Business code receives dependencies through explicit construction; it must not call a global registry/service locator.

Distinguish:

- `Actor Capability`: what an in-world actor can do/learn;
- `Runtime Capability`: what provider/service the host has installed.

## 11. Triple ledgers

Keep three logical responsibilities:

- World Ledger — what became real;
- Actor Trajectory Ledger — why an actor chose/proposed something;
- Runtime Control Ledger — what runtime/provider configuration was active.

They may share append-only storage infrastructure but must not become one untyped audit blob.

## 12. Bounded runtime evolution

New runtime capabilities and new world structures enter through candidate/evaluation/promotion paths. Shadow branches, existing invariant tests, chaos tests and experiment runtime must be reused. Ordinary agents can never alter World Constitution, Commit Authority, branch semantics or Evidence/Rights contracts.

## 13. Milestones

- **M18 — Minimal-Core Consolidation Baseline**
- **M19 — Authority Microkernel & Reality Semantics**
- **M20 — Genesis / Ontology / Law Evolution**
- **M21 — Distillation Fabric & Meaning Pipeline**
- **M22 — Runtime Capability Fabric & Stable World ABI**
- **M23 — Triple Ledgers & Reproducibility**
- **M24 — Bounded Runtime Evolution**
- **M25 — Backward Migration, Cross-domain Qualification & v5.1 Certification**

## 14. Definition of minimality

Minimality does not mean compressing unrelated responsibilities into giant files. It means:

- no duplicate authoritative models;
- no duplicate registries for the same lifecycle problem;
- no parallel package systems;
- no class/interface that exists only to mirror a design noun;
- no adapter abstraction unless an unstable/external/replaced implementation boundary actually exists;
- no mandatory dependency on experimental providers;
- no duplicated schema definitions across backend/frontend.

The correct solution may contain more small files while still having fewer concepts and less total duplicated logic.
