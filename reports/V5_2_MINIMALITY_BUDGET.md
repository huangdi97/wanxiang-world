# V5.2 Minimality Budget (G29G)

Code minimality is a continuous acceptance metric. No arbitrary absolute
LOC cap: per-milestone *incremental* allowances on new abstractions (each
with mandatory justification in `V5_2_CODE_MINIMALITY_LEDGER.md`) plus
hard invariants that must hold at every milestone.

## M26 baseline snapshot

| Metric | Count |
|---|---|
| Production files | 390 |
| Production LOC | 35188 |
| Public classes | 785 |
| Public functions | 318 |
| Registries | 14 |
| Managers | 0 |
| Services | 17 |
| Engines | 2 |
| Ports | 26 |
| Stores | 23 |
| State/schema models | 22 |
| Import cycles | 0 |
| Commit paths | 1 |
| Oversized modules (>300 lines) | 0 |

Hard invariants hold: **True** (0 cycles, 1 commit path).

## Incremental budgets M27-M34

| Milestone | New-abstraction allowance | Note | Hard constraints |
|---|---|---|---|
| M26 | 0 | Baseline freeze + convergence; no net new abstractions (dedupe only). | 0 cycles; 1 commit path; no second Event/Branch/Registry/State |
| M27 | 3 | Reality Root / Constitution / ISA are thin semantic layers over existing contracts; allow minimal value types + ISA verbs mapped to the existing pipeline. | no RealityRootEngine/SemanticISAEngine god objects; no second commit pipeline |
| M28 | 4 | Worldline / Lineage Graph / Hypervisor; lineage must reuse branch history semantics. | no second branch system; no WorldLineageManager god object |
| M29 | 3 | Evolution Policy Stack as configuration over one runtime; scheduler + distillations are functions. | no third runtime for canon modes; no per-distiller pipeline |
| M30 | 3 | Promotion pipeline + cross-world distillation reuse Candidate/Invariant machinery. | no World Merge as git-merge; no auto platform promotion |
| M31 | 2 | Compatibility migrations + thin API extensions only. | migrations have rollback/compat; no new API namespace copy |
| M32 | 1 | Red Chamber content (World/Domain/Experience) must NOT add Core abstractions. | no Core special-casing for red_chamber; no model-memory Canon |
| M33 | 1 | Red Chamber instance runtime; reuse Living World substrate. | no second Runtime; no Core hack for RC-001 |
| M34 | 0 | Final acceptance: verification + evidence only; no new abstractions. | working tree clean or explained; no failed-test skips |
| M51 | 5 | Source->LivingWorld Forge baseline: unified Job/JobCheckpoint/JobStore/JobService + typed job errors; reuses single commit path (jobs never mutate canon). | 1 commit path; no second source registry; jobs propose only |
| M52 | 12 | Source Registry & Adapter Foundation: convergence fields, blob refs, SourceAdapter ABI + AdapterRegistry, book/structured/asset adapters, ingestion security gate. All adapters propose only; single SourceRegistry. | 1 commit path; single source registry; no fake extraction |
| M53 | 8 | Parse/Segment/Stable Locator: ParsedDocument IR, StructureParser, segment model + format locators, incremental cache, parse checkpoint, diagnostics API. All propose only; single locator/source-registry. | 1 commit path; single source registry; no fake extraction |
| M54 | 10 | Distillation & Candidate Fabric: unified CandidateEnvelope, distiller DAG + registry, reference passes (identity/event/relation/character/object), candidate clustering. Candidates propose only; no Canon. | 1 commit path; no Canon from candidates; no second envelope |
| M55 | 8 | Evidence/Rights/Review/Completion core: evidence bindings, conflict ledger, rights gate, review ledger, E0-E5 completion + planner, review API routes. All decisions append-only/reversible; no Canon promotion. | 1 commit path; no last-write-wins; no auto canon |
| M56 | 9 | Domain Matching & WorldDraft: domain capability registry + recommender + resolver, WorldDraft v1 + store, coverage, scenario mining, genesis draft. Drafts are compile intermediates, never runtime state. | 1 commit path; no second runtime state; no per-world domain fork |

Every new abstraction must answer the four questions in
`reports/V5_2_CODE_MINIMALITY_LEDGER.md`; otherwise it is not added.
