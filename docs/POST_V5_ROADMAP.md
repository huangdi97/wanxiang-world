# Post-v5 Roadmap (from M16 research + M17 external blockers)

Scope: this roadmap captures PROMOTE/KEEP_EXPERIMENTAL/REJECT decisions and external blockers with
evidence. It does NOT invent G21 work; new goals would be scoped separately by the user.

## M16 research decisions (evidence in reports/G19x_REPORT.md + M16_ACCEPTANCE.md)
| Track | Goal | Decision | Post-v5 direction |
|---|---|---|---|
| Research namespace/flags/promotion rules | G19A | KEEP_EXPERIMENTAL (infrastructure) | v5.1 governance seam |
| AI-assisted world compiler extraction | G19B | KEEP_EXPERIMENTAL | v5.1 candidate (needs real LLM provider + benchmark parity) |
| Long-horizon persona memory & drift | G19C | KEEP_EXPERIMENTAL | v5.1 candidate (drift < threshold over 90d run) |
| Cognitive LOD / population scheduling | G19D | KEEP_EXPERIMENTAL | v5.1 candidate (large-population scheduler) |
| World-model / planner proposals | G19E | KEEP_EXPERIMENTAL | v5.1 candidate (learned provider + goal-scoring benchmark) |
| Generative asset/scene pipeline | G19F | KEEP_EXPERIMENTAL | v5.1 candidate (real generators/renderers + rights audit) |
| Digital human / XR presence | G19G | KEEP_EXPERIMENTAL | v5.1 candidate (real avatar/XR + SLA + identity rights audit) |
| Multi-simulator federation | G19H | KEEP_EXPERIMENTAL | v6 candidate (real FMI simulators + determinism parity) |
| Reality/digital-twin streaming | G19I | KEEP_EXPERIMENTAL | v6 candidate (real authorized feeds + fusion parity + privacy audit) |
| Distributed world host / sharding | G19J | **REJECT promotion** | Re-evaluate only with new workload evidence; modular monolith stays default |

## External-blocker-driven roadmap
- **Renderers/XR (WX-PRJ-8.2-003)**: integrate Phaser/Godot/Babylon + digital-human/XR when devices
  and licensed assets are available; server projection/network contracts already VERIFIED.
- **Real source data (WX-SRC-EXTERNAL-001)**: licensed Red Chamber / Liaoshen / family / heritage
  corpora and real IIIF endpoints; source/evidence kernel already VERIFIED on approved fixtures.
- **Live PostgreSQL/PITR**: enable the postgres profile against a real instance (test_g16b).
- **Real providers**: LLM, speech/avatar, authorized sensor feeds, object storage, SSO/vuln-scanning.
- **Multi-node hosting**: only re-open distribution if a workload benchmark shows benefit (G19J REJECT).

## Stable defaults (unchanged)
- Modular monolith; Commit Authority sole writer; append-only replayable event history; branch
  isolation; rights/source gates server-enforced; deterministic tests free of paid APIs.
- All research flags remain OFF; no research code is promoted to stable defaults.
