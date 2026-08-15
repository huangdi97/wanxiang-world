# V5.2 Minimality Budget (G29G)

Code minimality is a continuous acceptance metric. No arbitrary absolute
LOC cap: per-milestone *incremental* allowances on new abstractions (each
with mandatory justification in `V5_2_CODE_MINIMALITY_LEDGER.md`) plus
hard invariants that must hold at every milestone.

## M26 baseline snapshot

| Metric | Count |
|---|---|
| Production files | 344 |
| Production LOC | 30802 |
| Public classes | 694 |
| Public functions | 296 |
| Registries | 11 |
| Managers | 0 |
| Services | 15 |
| Engines | 2 |
| Ports | 24 |
| Stores | 18 |
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

Every new abstraction must answer the four questions in
`reports/V5_2_CODE_MINIMALITY_LEDGER.md`; otherwise it is not added.
