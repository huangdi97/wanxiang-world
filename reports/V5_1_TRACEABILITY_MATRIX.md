# V5.1 Traceability Matrix

> Spec requirement -> current owner -> current evidence -> action. One row per material
> v5.1 delta. Classification: KEEP_AS_IS | KEEP | MERGE | ADAPT | DELETE | REPLACE | EXPERIMENTAL.
> REPLACE requires an ADR (none proposed in M18 without one). Generated at G21B; extended per Goal.

## Legend

- Owner = existing module(s) that carry the semantic today.
- Evidence = tests/artifacts proving the capability exists (named below; all paths repo-relative).
- Action = smallest required action for v5.1 (KEEP/MERGE/ADAPT/DELETE/REPLACE/EXPERIMENTAL).

## Delta matrix

| # | v5.1 delta | Current owner | Evidence | Action |
|---|---|---|---|---|
| D01 | World Reality Calculus: Distinction→Identity, Relation→typed Relation/scoped Fact, Transition→Delta/Event, Commitment→Commit boundary | wanxiang_domain (entity.py, delta.py, event.py, ids.py, serialization.py); wanxiang_runtime (state.py apply_delta, authority.py) | tests/unit/runtime/test_replay.py, tests/integration/test_m1_acceptance.py, reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md | ADAPT — document semantic mapping (reports/V5_1_REALITY_CALCULUS_MAPPING.md in G22A); no new engine. |
| D02 | Three World Commit kinds STATE/ONTOLOGY/LAW in one authority pipeline | wanxiang_runtime/authority.py (single CommitAuthority, CommitRequest.delta), wanxiang_domain/event.py (CommittedEvent) | tests/contract/ (commit atomicity/idempotency/stale-revision), reports/CANONICAL_MUTATION_PATHS.md | ADAPT — add typed commit-kind field + validation in one pipeline (G22C); no separate commit engines. |
| D03 | No CapabilityCommit as 4th World Commit; runtime changes = RuntimeControlTransaction | none today (new) | n/a | ADD — RuntimeControlTransaction semantic (G25H) recorded in Runtime Control Ledger, never in World Ledger. |
| D04 | Semantic space Σ / law set Γ / constitution version context for replay interpretation | wanxiang_domain/versions.py (SchemaVersion, RuntimeVersion, PackageVersion); CommittedEvent.rule_version/schema_version | tests/unit/runtime/test_replay.py (IncompatibleVersion), REPLAY_GOLDEN_CORPUS.md | ADAPT — extend version context (semantic-space/law-set/constitution ids) + event envelope (G22E/G22F); old events carry version context, never silently reinterpreted. |
| D05 | Fact Space with explicit scope; scope change never silently promotes to canonical | substrate/epistemic (beliefs/memories), substrate/sources + ledger (truth labels E0..E5 / canon promotion), domain/evidence.py, domain/rights.py | tests/contract + tests/integration (G03B, G04B, G04D), reports/RIGHTS_ENFORCEMENT_MATRIX.md | ADAPT — shared scoped-Fact contract (G22B); keep authority separation; reuse existing promotion gates. |
| D06 | Genesis semantics: GenesisSpec consumed from WorldPack+Scenario+overrides; Designer/True/Evolutionary | substrate/packages (model.py, registry.py, install.py, migration.py); application/world_runtime.py instantiate | tests/integration (G04A/G04E/G05A), reports/REGISTRY_LIFECYCLE_QUALIFICATION.md | ADAPT — GenesisSpec initialization contract (G23A/G23B); NO second package registry. |
| D07 | Ontology candidate & OntologyCommit (expand Σ) | none (new semantics); candidate machinery exists in sources/ledger (truth promotion) | n/a | ADD — ontology candidates + typed OntologyCommit through the same authority (G23C); candidate never auto-promotes. |
| D08 | Law candidate & LawCommit (change Γ) | rule/runtime versioning exists (RuntimeVersion); scenario rules in packages | n/a | ADD — law candidates + typed LawCommit (G23D); constitutional layer not modifiable by ordinary agents. |
| D09 | Branch-local ontology/law evolution + merge policy | wanxiang_runtime/branch.py, replay fork semantics, ADR 0007 | tests/integration (G15F branch/time-travel), reports/WORLDLINE_COMPARISON_QUALIFICATION.md | ADAPT — branch-local evolution + merge policy (G23E); child never mutates parent. |
| D10 | Ω possibility space as candidate/derived policy (minimal persistence) | substrate/reality/experiment.py, research/planner.py (EXPERIMENTAL) | tests/integration test_g19e_planner, reports/WORLD_MODEL_PLANNER_RESEARCH.md | ADAPT — Ω as candidate/derived policy (G23F); no enumerable possibility universe persisted. |
| D11 | CandidateEnvelope, origin class & provenance contract | substrate/compiler (compiler.py, validate.py), sources (registry/gate), ledger (CompletionLedger) | tests/integration (G04B/G04C/G04D) | ADAPT — one CandidateEnvelope contract (G24A) over existing compiler outputs. |
| D12 | Minimal Distiller protocol & orchestration; Foundational Distillation reusing compiler | substrate/compiler/compiler.py + readers.py (structured compiler) | tests/integration test_g04c / compiler tests, reports/SCHEMA_DRIFT_AUDIT.md | ADAPT — Distiller protocol over existing compiler (G24B/G24C); distillers are providers, not engines. |
| D13 | Reusable typed distillers (Identity/Relation/Event/Persona/Rule/Skill/Ontology) | compiler readers + domain contracts (entity/relation/event), epistemic persona/memory | tests/unit, tests/property | ADAPT — typed distillers (G24D); reuse existing value objects. |
| D14 | Evolutionary Distillation from committed history (candidates only) | none stable; research/ (planner, memory) EXPERIMENTAL | research reports | ADAPT/EXPERIMENTAL — G24F produces candidates only; no model summary write-back to canon. |
| D15 | Evidence binding, review & completion-level consolidation | substrate/ledger (CompletionLedger, TruthLabel), sources gate | tests/integration test_g04d, reports/P0_GAP_BACKLOG.md | KEEP/ADAPT — consolidate levels (G24E); promotion gates preserved. |
| D16 | Anti-self-evidence / canon escalation / feedback-loop protection | ledger promotion rules, source gate injection scan | tests/integration (G04B/G04D adversarial), reports/SECURITY_RIGHTS_SOURCE_FORENSICS.md | ADAPT — explicit guard tests (G24G); never weaken promotion rules. |
| D17 | Domain distillation profiles without core hardcoding | substrate genealogy/heritage/campaign + research adapters | tests/integration (G15I), reports/MULTI_DOMAIN_REFERENCE_QUALIFICATION.md | ADAPT — profiles live outside core (G24H). |
| D18 | RuntimeCapability distinct from ActorCapability | substrate/capability (ActorCapability: level/mastery/confidence) | tests/integration test_g03g | ADAPT — introduce RuntimeCapability semantic (G25A); keep ActorCapability as-is. |
| D19 | Typed service contracts & single composition root | apps/api/app.py composition root; application/world_runtime.py | tests/api, reports/ARCHITECTURE_CONFORMANCE_FINAL.md | ADAPT — formalize single typed composition root (G25B); no global service locator. |
| D20 | Dependency DAG, scope & provider lifecycle | package resolver (packages/resolver.py), host lifecycle, research adapters | tests/integration (G04A/G17F), reports/REGISTRY_LIFECYCLE_QUALIFICATION.md | ADAPT — runtime provider DAG/scope/lifecycle (G25C); reuse resolver semantics. |
| D21 | RuntimeProfile separated from WorldPack | packages/model.py (manifests); no RuntimeProfile today | tests/integration test_g04a | ADAPT — RuntimeProfile metadata (G25D) under existing package system. |
| D22 | Stable World ABI v1 | apps/api routes (10), sdk_ts, packages/sdk.py; reports/SDK_API_BASELINE.md | reports/SDK_API_BASELINE.md, tests/api, TS 22 tests | ADAPT — narrow versioned ABI (G25E); no mutable authority/ORM handles exposed. |
| D23 | AgentHarnessProvider adaptation of existing policies | substrate/agency/policy.py (Scripted/Rule/SmallModel/LLM/Human/Hybrid policies) | tests/integration test_g03e (deterministic policies) | ADAPT — AgentHarnessProvider wraps existing policies (G25F); DSH optional. |
| D24 | Runtime Capability Catalog & legacy registry merge | substrate registries: packages/registry.py, sources/registry.py, skills/registry.py, resolution/registry.py, action registry, host registry | tests/integration per registry | MERGE — one typed Runtime Capability Catalog (G25G) after forensic evidence (G21C/G21F); no duplicate registries. |
| D25 | RuntimeControlTransaction & reversible runtime effects | none (new); package install/upgrade transactional machinery exists | tests/integration test_g04e (transactional install) | ADD — typed runtime control transaction (G25H); runtime dispose cannot undo world history. |
| D26 | Triple ledgers: World / Actor Trajectory / Runtime Control | runtime/audit.py (AuditRecord); event store append-only; substrate/ledger is CompletionLedger (different concern) | tests/contract (audit), event store tests | ADAPT — shared append-only stream infra + three typed ledger facades (G26A-G26D); never one untyped blob. |
| D27 | Cross-ledger correlation & trace identity | domain/ids.py (TraceId, CorrelationId, CausationId) | tests/contract | ADAPT — trace correlation across ledgers (G26E); reuse existing id semantics. |
| D28 | Reproducibility manifest & runtime revision pinning | runtime/versions, package lock (PackageLock), RELEASE manifest | reports/CLEAN_ROOM_CERTIFICATION.md, test_g20b | ADAPT — reproducibility manifest (G26F). |
| D29 | Bounded Runtime Evolution: proposal→sandbox→shadow branch→evaluation→approval→activation→rollback | research flags, package install/upgrade, experiment runtime, chaos/security suites | reports (G19A, G14*, G20C) | ADAPT — orchestration reusing shadow branches + invariant/chaos suites (G27A-G27G); transactional activation. |
| D30 | Constitutional attack / self-modification adversarial qualification | architecture_check.py, security suites (G20C) | reports/FINAL_SECURITY_RELIABILITY_CERTIFICATION.md | ADAPT — adversarial tests (G27H); ordinary agents can never modify constitution/authority/branch/evidence-rights. |
| D31 | Backward migration: v5.0 persisted worlds/events/snapshots/packages | migrations (0001,0002), replay, package migration | REPLAY_GOLDEN_CORPUS.md, test_g20b, test_g16b | KEEP/ADAPT — G28A-G28B qualify v5.0 fixtures under v5.1 semantics. |
| D32 | Cross-domain qualification (Family/Heritage/Campaign/Narrative) | substrate genealogy/heritage/cosim.campaign + reference worlds | tests/integration (G15I/G15J), reference_worlds/ | KEEP — G28C-G28E requalify with v5.1 semantics; real source data EXTERNAL_BLOCKED. |
| D33 | Product surfaces / host / external adapter compatibility | apps/api services (7 surface services), host, projection | reports/PRODUCT_SURFACE_CONTRACT_AUDIT.md, tests/api | KEEP/ADAPT — G28F; surfaces consume one server truth. |
| D34 | Minimal-core / dead-code final audit | scripts/v51_metrics.py, false_completion_scan.py, architecture_check.py | baseline ledger | ADAPT — G28G final audit; zero stable P0/P1. |
| D35 | Clean-room build/upgrade/restore/replay certification | scripts/clean_room_certify.py | reports/CLEAN_ROOM_CERTIFICATION.md | KEEP — G28H re-run under v5.1. |
| D36 | M16 research tracks (9) | packages/research (planner, generative_assets, digital_human, sim_federation, reality_stream, distributed_host, persona/memory, cognitive lod, ai_compiler) | research reports | EXPERIMENTAL — audit in G21C; keep behind OFF flags; do not promote without evidence. |
| D37 | Empty stub packages (evidence, model_providers) | packages/evidence (5 LOC), packages/model_providers (5 LOC); only referenced by test_bootstrap/false_completion_scan | test_bootstrap.py | DELETE/ADAPT — evaluate in G21C/G21E; no live imports. |

## Classification summary (G21B)

- KEEP_AS_IS: D15 (mostly), D31, D32, D33 (mostly), D35
- KEEP: D15, D31, D32, D33, D35
- ADAPT: D01, D02, D04, D05, D06, D09, D10, D11, D12, D13, D15, D16, D17, D18, D19, D20, D21, D22, D23, D25 (parts), D26, D27, D28, D29, D30, D34
- MERGE: D24 (with G21C/G21F forensics)
- ADD (new irreducible semantics): D03, D07, D08, D25
- DELETE candidates: D37 (evidence/model_providers stubs, pending call-site evidence)
- EXPERIMENTAL: D36, D14 (evolutionary distillation research seam)
- REPLACE: none proposed (no ADR needed)

## Conflicts with prior M16 experiments

- D18/D24 overlap with research sim_federation/distributed_host: federated/distributed hosting REJECTED for promotion (ADR 0055); capability fabric absorbs only typed-contract/dependency ideas, not the rejected architecture.
- D23 (AgentHarnessProvider) references DeepSeek Harness/Cordis as OPTIONAL provider only (R9); core never depends on it.
- D26 triple ledgers must not merge with the existing CompletionLedger (a content/truth ledger, different concern) into one untyped table.

## Completeness check (G21B acceptance)

All material v5.1 deltas above are classified (D01-D37). Mother-spec sections covered: 0.1-0.14 (reality calculus/commits/genesis), 3-9.11 (planes/kernels/buses/ledgers/runtime evolution), 101-111 (distillation), 112-120 (capability fabric/ABI). No delta left UNCLASSIFIED.
