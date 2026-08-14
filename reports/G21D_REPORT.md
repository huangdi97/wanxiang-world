# Goal G21D Acceptance Report — Dependency Graph & Physical Package Simplification Plan

## Status
PASS

## Objective
Define the minimum physical dependency topology without forcing cosmetic repository churn.

## Delivered
- `scripts/v51_dependency_graph.py` — deterministic AST package dependency scanner; writes `reports/V5_1_PACKAGE_DEPENDENCY_GRAPH.md`.
- `docs/architecture/V5_1_PHYSICAL_PACKAGE_MAPPING.md` — 16-kernel → physical-package mapping, dependency topology, forbidden-dependency summary, proposed minimal moves.
- `tests/architecture/test_v51_dependency_topology.py` — 2 checks: golden edge set pinned (topology drift detection), mapping doc covers all 16 kernels. 2 passed.
- Updated traceability matrix, code-minimality ledger, PLAN/STATUS/CHANGELOG/DECISIONS.

## Topology (verified)
- domain (bottom, framework-free) -> runtime -> application/persistence -> substrate -> apps/api. research -> domain (isolated). No cycles (architecture_check PASS).
- Existing forbidden-import boundaries (architecture_check.py) already enforce core independence; no new rules required.

## Finding: layering inversion (P2)
- Five substrate modules import `wanxiang_application.world_runtime.WorldRuntime` (lifecycle/service.py, skills/runtime.py, population/scheduler.py, host/host.py, queue/queue.py).
- Not a cycle, but substrate -> application violates target direction. Planned minimal fix: narrow `WorldRuntimePort` Protocol consumed by those five modules; application WorldRuntime implements it. Executed later (G21F/G25B) with call-site evidence.

## Minimal moves (no mass rename, no 16-package split)
| Move | Kind | When | Risk |
|---|---|---|---|
| Break substrate->application via WorldRuntimePort | ADAPT | G21F/G25B | medium |
| Delete/repurpose empty stub packages evidence, model_providers | DELETE | G21E | low |
| None other | - | - | - |

## Verification
- Import-cycle test: PASS (architecture_check + existing tests).
- Forbidden-dependency tests: PASS (architecture_check).
- Golden dependency edge set pinned by test.
- Ruff/Pyright on new files: PASS.
- Golden replay regression: unaffected (no production change).

## PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix
| Item | Status |
|---|---|
| Dependency topology documented + pinned | PASS |
| 16-kernel mapping | PASS |
| substrate->application inversion | P2 finding, planned move |
| M16 research namespace | EXPERIMENTAL |

## Remaining risks
- WorldRuntimePort refactor must keep the five substrate consumers' behavior identical (covered by existing integration tests in G21F/G25B).

## Changed files
- added: scripts/v51_dependency_graph.py, reports/V5_1_PACKAGE_DEPENDENCY_GRAPH.md, docs/architecture/V5_1_PHYSICAL_PACKAGE_MAPPING.md, tests/architecture/test_v51_dependency_topology.py, reports/G21D_REPORT.md; updated: PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md, reports/V5_1_TRACEABILITY_MATRIX.md, reports/V5_1_CODE_MINIMALITY_LEDGER.md.

## Local commit
- Message: `v5.1 g21d: dependency graph & physical package simplification plan`
