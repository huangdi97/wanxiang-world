# README FIRST — Wanxiang v5.1 Minimal-Core Consolidation & Migration Program

This pack is the **post-M17 v5.1 compatibility/consolidation program** for Wanxiang.

It assumes M0–M17 were previously implemented/certified, but **does not trust those claims blindly**. It first freezes and audits the repository, then performs a compatibility-first migration to the v5.1-R1 mother spec.

## Mission

Implement the complete v5.1-R1 semantic/runtime delta with the **smallest durable code surface** possible:

- keep proven v5.0/M0–M17 capabilities;
- merge duplicate abstractions, registries, managers, state models and infrastructure;
- delete dead, fake, shadow or superseded implementations;
- adapt existing Commit/Event/Replay/Branch/Host/Compiler/SDK code instead of rewriting healthy systems;
- add only irreducible v5.1 semantics: Reality Calculus contracts, three World Commit kinds, Genesis semantics, Distillation Fabric, Runtime Capability Fabric, Stable World ABI, triple ledgers, bounded runtime evolution;
- preserve v5.0 persisted worlds, event histories, packages and SDK behavior through explicit migration/compatibility tests;
- finish with cross-domain, clean-room and code-minimality qualification.

## Execution order

Read:

1. `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
2. `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
3. `02_CODEX_V5_1_MASTER_PROMPT.md`
4. `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
5. `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
6. `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
7. `06_V5_1_GOALS_INDEX.md`
8. `07_MILESTONE_GATES_M18_M25.md`
9. `08_CONTINUOUS_EXECUTION_RESUME_PROTOCOL.md`
10. `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
11. current Goal file

Then execute **G21A → G28I continuously**, running each milestone gate M18 → M25 in order.

## Critical rule

Do **not** convert every design noun into a class/service/package. The mother spec defines logical semantics. Physical code must remain minimal.

`World Reality Calculus` is a semantic contract, not a reason to create a new giant engine.

`Meaning / Reality / Experience Engine` are architecture views/facades, not three mandatory physical services.

`5 Planes / 16 Kernels` remain logical boundaries, not 16 services.

## Final stop

Stop only when M25 passes or a repository/environment blocker prevents all further independent work. Do not push or production-deploy unless the user separately authorizes it.
