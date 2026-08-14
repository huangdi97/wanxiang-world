# M0–M17 → v5.1 Migration Map

## Keep / adapt map

| Existing capability | Action | v5.1 role |
|---|---|---|
| Commit Authority | KEEP + ADAPT | Authority Microkernel implementation |
| Event Store | KEEP | World Ledger storage foundation |
| Snapshot / Replay / Branch | KEEP + VERSION-CONTEXT EXTEND | committed-history reconstruction |
| Persistence / migrations | KEEP | schema/event/runtime compatibility |
| Living World Substrate | KEEP | Reality Engine capability |
| World Host / scheduler | KEEP | Runtime host |
| Perception / Belief / Memory | KEEP | Agent Harness inputs / actor trajectory |
| Actor / Organization | KEEP | Agency runtime |
| Skill / Action / Affordance | KEEP | Agency/world action contracts |
| Source / Evidence / Rights | KEEP | Meaning/Distillation evidence boundary |
| Compiler / Completion | ADAPT | Foundational Distillation pipeline |
| Package Registry | KEEP + EXTEND | World/Domain/Scenario + RuntimeProfile metadata |
| Reality Bridge | KEEP | observation provider |
| Co-Simulation | KEEP | Simulation provider |
| Projection / Embodiment | KEEP | Experience layer |
| SDK / package tooling | KEEP + ABI UPDATE | external ecosystem |
| Security / chaos / evaluation | KEEP | bounded-evolution promotion gates |
| experimental M16 research | AUDIT | adapt, keep experimental or reject |

## Merge candidates

- overlapping plugin/provider/model/simulator/projection registries → Runtime Capability Catalog;
- duplicate append-only/audit storage machinery → shared stream infrastructure with typed ledger facades;
- duplicate current-state caches/read models → one authoritative projection strategy per concern;
- duplicate API/TS schemas → generated schema pipeline;
- duplicate manager/service wrappers → direct application use cases or explicit composition root.

## Delete candidates

Delete only after call-site/test evidence proves safe:

- second canonical-state implementations;
- direct-mutation bypasses;
- dead/unused interfaces;
- fake production paths;
- static JSON runtime substitutes;
- giant legacy managers superseded by cohesive modules;
- untyped global service locators;
- duplicate registries with no independent semantics;
- experimental provider forks used as core dependencies.

## New irreducible v5.1 additions

- semantic-space/law/constitution version context;
- three World Commit kinds in one authority pipeline;
- GenesisSpec;
- Ontology/Law candidates and commits;
- CandidateEnvelope + Distiller protocol;
- Evolutionary Distillation;
- Runtime Capability model/composition/lifecycle;
- RuntimeProfile;
- Stable World ABI;
- Actor Trajectory Ledger;
- Runtime Control Ledger;
- Bounded Runtime Evolution orchestration.
