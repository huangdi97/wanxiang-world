# Goal G29E Acceptance Report ? ???????

## Status
PASS

## Objective
Converge responsibilities to Kernel/Runtime/Forge/Experiences/Infrastructure
without pointless directory moves; establish the dependency-direction ADR and
remove the substrate->application boundary violation.

## Delivered
1. **ADR (DECISIONS 0064)** ? dependency direction for v5.2 physical boundaries:
   domain -> runtime -> application/persistence -> substrate -> apps/api; Kernel
   (domain+runtime) never depends on Runtime/Forge/Web/ORM; World content never
   enters Kernel.
2. **Resolved the P2 substrate->application inversion** (v5.1 G21D finding):
   - New consumer-owned port `wanxiang_substrate.runtime_port.WorldRuntimePort`
     (narrow: `current_state` / `submit_command` / `events`) + `WorldCreateResult`.
   - The five substrate modules (host/host, queue/queue, population/scheduler,
     skills/runtime, lifecycle/service) now depend on the port instead of
     `wanxiang_application.world_runtime.WorldRuntime`.
   - `rg wanxiang_application packages/substrate` -> zero imports (was 5).
   - Application `WorldRuntime` satisfies the port structurally; no behavior change.
3. Updated golden topology (substrate edge `(application, domain, runtime)` ->
   `(domain, runtime)`), regenerated dependency graph + forensics reports, and
   updated `docs/architecture/V5_1_PHYSICAL_PACKAGE_MAPPING.md`.

## Verification (commands + results)
| Command | Result |
|---|---|
| `rg wanxiang_application packages/substrate --glob "*.py"` | zero hits (was 5) |
| `uv run pytest tests/architecture/test_v51_dependency_topology.py -q` | 2 passed (new golden edges) |
| `uv run pytest tests/architecture/test_v51_forensics.py -q` | 3 passed |
| `uv run pytest tests/integration/test_command_queue.py tests/integration/test_autonomous_scheduler.py tests/integration/test_g14e_host_multiplayer.py tests/integration/test_capability_learning.py -q` | 22 passed |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/v51_dependency_graph.py` | graph regenerated; substrate = (domain, runtime) |
| `uv run python scripts/v51_forensics.py` | commit_paths 1; ports 23 (WorldRuntimePort added) |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Dependency-direction ADR | PASS (DECISIONS 0064) |
| Low-risk module moves | PASS (5 substrate modules -> port; no high-churn moves needed) |
| Kernel does not depend on Runtime/Forge/Web/ORM | PASS (guards unchanged and green) |
| World content not in Kernel | PASS (verified G29B; no world leakage) |
| No new import cycles | PASS (topology + architecture_check) |
| No new duplicate abstraction | PASS (WorldRuntimePort reviewed, single boundary port) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/runtime_port.py, reports/G29E_REPORT.md
- modified: host/host.py, queue/queue.py, population/scheduler.py, skills/runtime.py,
  lifecycle/service.py, tests/architecture/test_v51_dependency_topology.py,
  docs/architecture/V5_1_PHYSICAL_PACKAGE_MAPPING.md,
  reports/V5_1_PACKAGE_DEPENDENCY_GRAPH.md, reports/V5_1_DUPLICATE_FORENSICS.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g29e: ???????`
