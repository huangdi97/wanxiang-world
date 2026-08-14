# V5.1 Physical Package Mapping & Dependency Plan (G21D)

> Target topology without cosmetic churn. Logical 16 kernels map onto physical
> packages; no 16-package/service split is required (R11).

## 1. Current physical topology (verified by scripts/v51_dependency_graph.py)

| Package | v5.1 target responsibility | imports | direction |
|---|---|---|---|
| packages/domain | core (identity/fact/transition/commit contracts) | (none) | bottom |
| packages/runtime | core (authority/replay/branch/state/ports) | domain | upward |
| packages/application | application orchestration facade | domain, runtime | upward |
| packages/substrate | definition+runtime+agency+experience (modular monolith substrate) | domain, runtime | upward (clean; inversion resolved in G29E) |
| packages/persistence | infrastructure (SQLAlchemy adapters) | domain, runtime | upward |
| packages/observability | infrastructure (telemetry) | (none) | - |
| packages/evidence | definition (evidence/rights) — EMPTY STUB | (none) | DELETE candidate |
| packages/model_providers | infrastructure (LLM provider ports) — EMPTY STUB | (none) | DELETE candidate |
| packages/research | EXPERIMENTAL research namespace | domain | isolated |
| packages/sdk_ts | infrastructure (TS SDK, generated OpenAPI contract) | (none) | generated |
| apps/api | infrastructure (API composition root, ADR 0010 exemption) | application, domain, persistence, runtime, substrate | top |

No import cycles exist (architecture_check detects and passes). Domain is framework-free
(fastapi/sqlalchemy/alembic/pydantic/httpx/requests/openai forbidden and enforced).

## 2. Layering inversion (RESOLVED in G29E)

The P2 substrate -> application inversion (five modules importing
`wanxiang_application.world_runtime.WorldRuntime`) is resolved: a consumer-owned
`wanxiang_substrate.runtime_port.WorldRuntimePort` Protocol now declares the narrow
slice substrate needs (current_state / submit_command / events); the application's
`WorldRuntime` satisfies it structurally. Substrate has zero `wanxiang_application`
imports (verified by `rg`), and the runtime boundary stays at one composition root.

## 3. 16-kernel -> physical package mapping

| Logical kernel (mother spec) | Physical owner |
|---|---|
| Source/Evidence Kernel (4.1) | substrate/sources + substrate/ledger (CompletionLedger) + domain/evidence |
| World Compiler & Completion (4.2) | substrate/compiler + substrate/ledger |
| Package/Schema/Dependency Registry (4.3) | substrate/packages (PackageRegistry + resolver + trust) |
| Canonical State Kernel (5.1) | runtime/state (InMemoryCanonicalState) + domain/state (contract) |
| Living World Substrate (5.2) | substrate/spatial, temporal, material, body, institution, population |
| Reality Bridge (5.3) | substrate/reality/bridge + fusion |
| Co-Simulation Fabric (5.4) | substrate/cosim |
| Event/Branch/Temporal Kernel (5.5) | runtime (authority, replay, branch) + persistence/event_store |
| Perception-Belief-Memory (6.1) | substrate/observation + epistemic + agency/query |
| Actor/Org Runtime (6.2) | substrate/agency + institution |
| Skill-Action-Affordance (6.3) | substrate/skills + actions |
| Capability & Learning (6.4) | substrate/capability |
| Opportunity-Challenge-Event (7.1) | substrate/reality/challenge + director |
| Embodiment/Director/Experiment (7.2) | substrate/session + reality/director + reality/experiment |
| World Host/Lifecycle/Multiplayer (8.1) | substrate/host + lifecycle + queue |
| Projection/Rendering/Gateway (8.2) | substrate/projection + gateway |

## 4. Forbidden dependencies (already enforced by scripts/architecture_check.py)

- domain: no fastapi/sqlalchemy/alembic/pydantic/httpx/requests/openai
- runtime: no fastapi/sqlalchemy/alembic/wanxiang_api/wanxiang_persistence/httpx/requests
- substrate: no fastapi/sqlalchemy/alembic/wanxiang_api/wanxiang_persistence/httpx/requests/openai
- persistence: no fastapi/wanxiang_api
- apps/api: no sqlalchemy/alembic/wanxiang_persistence (composition root uses adapters via ports)

## 5. Proposed minimal moves (only where a boundary violation exists)

| Move | Kind | When | Risk |
|---|---|---|---|
| Break substrate->application via WorldRuntimePort | ADAPT | DONE in G29E | low; structural typing, call-site tests green |
| Delete empty stub packages evidence/model_providers (or repurpose) | DELETE | G21E (after call-site evidence) | low |
| None other — current topology already satisfies target | - | - | - |

No mass rename, no 16-package split, no new top-level packages are proposed.
