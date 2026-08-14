# Kernel Coverage Summary (G13B)

## 16 logical kernels

| Kernel | Plane | Rows | Statuses |
|---|---|---|---|
| Canonical State Kernel (5.1) | World Reality | 5 | VERIFIED=5 |
| Living World Substrate (5.2) | World Reality | 7 | VERIFIED=7 |
| Physical Context / Reality Bridge (5.3) | World Reality | 2 | VERIFIED=2 |
| Co-Simulation Fabric (5.4) | World Reality | 1 | VERIFIED=1 |
| Event / Branch / Temporal Kernel (5.5) | World Reality | 5 | VERIFIED=5 |
| Perception-Belief-Memory Kernel (6.1) | Agency & Capability | 2 | VERIFIED=2 |
| Actor / Organization Runtime (6.2) | Agency & Capability | 1 | VERIFIED=1 |
| Skill-Action-Affordance Kernel (6.3) | Agency & Capability | 2 | VERIFIED=2 |
| Capability & Learning Kernel (6.4) | Agency & Capability | 1 | VERIFIED=1 |
| Opportunity-Challenge-Event Kernel (7.1) | Orchestration & Control | 1 | VERIFIED=1 |
| Embodiment / Director / Experiment Kernel (7.2) | Orchestration & Control | 3 | VERIFIED=3 |
| World Host / Lifecycle / Multiplayer Kernel (8.1) | Hosting & Experience | 5 | VERIFIED=5 |
| Projection / Rendering / Network Gateway (8.2) | Hosting & Experience | 3 | VERIFIED=2 EXTERNAL_BLOCKED=1 |
| Source / Evidence Kernel (4.1) | World Definition | 4 | VERIFIED=3 EXTERNAL_BLOCKED=1 |
| World Compiler & Completion Compiler (4.2) | World Definition | 1 | VERIFIED=1 |
| Package / Schema / Dependency Registry (4.3) | World Definition | 1 | VERIFIED=1 |

## Cross-cutting concerns

| Concern | Requirement IDs |
|---|---|
| hierarchy | WX-HIER-001 |
| commit_authority | WX-AUTH-001 |
| event_sourcing | WX-EVT-5.5-001 |
| replay | WX-EVT-5.5-002, WX-EVT-5.5-004 |
| branch | WX-EVT-5.5-003 |
| snapshot | WX-EVT-5.5-002 |
| source_gate | n/a |
| rights_privacy | WX-RGT-001 |
| host_boundary | WX-HST-8.1-001 |
| projection_filters | WX-PRJ-8.2-001 |
| cosim_boundary | WX-COS-5.4-001 |
| determinism | WX-EVT-5.5-004, WX-DET-001 |
| security_ops | WX-SEC-001 |
| stability | WX-STB-001 |
| backup_restore | WX-BKP-001 |
| sdk_openapi | WX-PRJ-8.2-002 |
| worldness | WX-WOR-001 |
| domain_generality | WX-DOM-001 |

All 16 kernels have at least one requirement row with implementation and test ownership.
