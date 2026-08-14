# Final Design Traceability & Requirement Closure (G20A / M17)

Source of truth: `docs/spec/WANXIANG_v5_MASTER_SPEC.md` (v5.0-R1). Regenerated from source after
M10-M16 via `uv run python scripts/traceability.py` (44 requirements, 63 goals, 16 kernels;
validation clean) and validated by `tests/architecture/test_traceability.py`.

## Closure summary

| Status | Count |
|---|---|
| VERIFIED | 42 |
| EXTERNAL_BLOCKED | 2 |
| GAP | 0 |
| PARTIAL | 0 |
| Total | 44 |

No stable-platform P0/P1 requirement is GAP. Every VERIFIED row carries an implementation owner and a
test pointer (enforced by the validator). Research-only M16 ideas are NOT converted into v5.0
requirements; they remain experimental behind OFF flags.

## Coverage by Plane

| Plane | VERIFIED | EXTERNAL_BLOCKED | Total |
|---|---|---|---|
| World Reality | 20 | 0 | 20 |
| Agency & Capability | 6 | 0 | 6 |
| Orchestration & Control | 4 | 0 | 4 |
| Hosting & Experience | 7 | 1 | 8 |
| World Definition | 5 | 1 | 6 |

## Coverage by Kernel (all 16)

| Kernel | Rows | Status |
|---|---|---|
| Canonical State Kernel (5.1) | 5 | VERIFIED=5 |
| Living World Substrate (5.2) | 7 | VERIFIED=7 |
| Physical Context / Reality Bridge (5.3) | 2 | VERIFIED=2 |
| Co-Simulation Fabric (5.4) | 1 | VERIFIED=1 |
| Event / Branch / Temporal Kernel (5.5) | 5 | VERIFIED=5 |
| Perception-Belief-Memory Kernel (6.1) | 2 | VERIFIED=2 |
| Actor / Organization Runtime (6.2) | 1 | VERIFIED=1 |
| Skill-Action-Affordance Kernel (6.3) | 2 | VERIFIED=2 |
| Capability & Learning Kernel (6.4) | 1 | VERIFIED=1 |
| Opportunity-Challenge-Event Kernel (7.1) | 1 | VERIFIED=1 |
| Embodiment / Director / Experiment Kernel (7.2) | 3 | VERIFIED=3 |
| World Host / Lifecycle / Multiplayer Kernel (8.1) | 5 | VERIFIED=5 |
| Projection / Rendering / Network Gateway (8.2) | 3 | VERIFIED=2, EXTERNAL_BLOCKED=1 |
| Source / Evidence Kernel (4.1) | 4 | VERIFIED=3, EXTERNAL_BLOCKED=1 |
| World Compiler & Completion Compiler (4.2) | 1 | VERIFIED=1 |
| Package / Schema / Dependency Registry (4.3) | 1 | VERIFIED=1 |

## Cross-cutting concerns (all VERIFIED)

hierarchy, commit_authority, event_sourcing, replay, branch, snapshot, source_gate, rights_privacy,
host_boundary, projection_filters, cosim_boundary, determinism, security_ops, stability,
backup_restore, sdk_openapi, worldness, domain_generality.

## Post-M9 (M10-M16) requirement closure review

- M10 (G13A-I): forensics, replay/branch/migration, rights/source gates, P0/P1 closure -> requirements
  WX-EVT-5.5-001..004, WX-SRC-4.1-001/002, WX-RGT-001 re-verified with independent audits.
- M11 (G14A-I): concurrency/atomicity/chaos/adversarial -> WX-EVT-5.5-001/003, WX-HST-8.1-002/003,
  WX-SEC-001, WX-RB-5.3-001/002 hardened.
- M12 (G15A-J): reference worlds + worldness -> WX-WOR-001, WX-DOM-001 verified on synthetic_full.
- M13 (G16A-J): production ops -> WX-SEC-001, WX-BKP-001, WX-STB-001, sdk_openapi verified.
- M14 (G17A-H): SDK/authoring/registry -> WX-PKG-4.3-001 verified; resolver pin fixed.
- M15 (G18A-H): product surfaces -> WX-PRJ-8.2-001/002 verified (server truth + authz E2E).
- M16 (G19A-J): research expansion -> no v5.0 requirement change; all tracks experimental behind flags.

## Exact external blockers (stable platform)

1. `WX-PRJ-8.2-003` - Renderers (Phaser/Godot/Babylon) and digital-human/XR presence require external
   renderers/devices: EXTERNAL_BLOCKED. Server-composed projection API + network gateway (8.2-001/002)
   are VERIFIED; generic contracts proven with deterministic substitutes.
2. `WX-SRC-EXTERNAL-001` - Real Red Chamber / Liaoshen / family / heritage source data and real IIIF
   endpoints require licensed external data: EXTERNAL_BLOCKED. Source/evidence kernel (4.1-001/002)
   verified against approved fixtures.

## Evidence

- `uv run python scripts/traceability.py` -> "wrote 44 requirements, 63 goals, 16 kernels; validation clean".
- `uv run pytest tests/architecture/test_traceability.py -q` -> passed (part of full gate).
- Full M17 gate: `uv run python scripts/quality.py` -> 628+ pytest, ruff/pyright/architecture PASS.
- Machine-readable: `reports/final_design_traceability.json`.
