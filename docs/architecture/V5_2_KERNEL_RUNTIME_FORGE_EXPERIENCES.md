# V5.2 Kernel / Runtime / Forge / Experiences Responsibility Boundaries

> G34A: final responsibility boundaries so v5.2 concepts never grow into
> parallel mega-systems.

## The four responsibilities

| Responsibility | Owns | Physical owner (current repo) | Rules |
|---|---|---|---|
| **Kernel** | Reality Root, Identity/Fact/Event/Constraint, State/Ontology/Law Commit, Commit Boundary, World Ledger, Snapshot/Replay, Branch/Worldline isolation, World Semantic ISA, Version Context, World Definition identity | `packages/domain`, `packages/runtime`, `packages/persistence` (infra port) | Never imports Runtime/Forge/Web/ORM; world-specific content forbidden |
| **Runtime** | World Host, Living World, Agent/Scheduler, Population, Co-Sim, Body/Spatial/Temporal, Perception/Belief/Memory, Capability Fabric | `packages/substrate` (runtime slice: host, population, agency, spatial, temporal, body, cosim, observation, epistemic, capability, session, lifecycle, queue) | Never imports apps/api; never mutates canonical state directly |
| **Forge** | Source Registry, Compiler, Distillation, Genesis, Evolution (policy/scheduler/distillation/promotion), Package Registry, Completion Ledger | `packages/substrate` (forge slice: sources, compiler, packages, ledger, evolution, lineage) | Produces Candidates / Proposals only; approval + Commit boundary gates activation |
| **Experiences** | Session, Embodiment/Lease, Projection, Studio, Product surfaces, SDK | `packages/application`, `packages/sdk_ts`, `apps/api` | Read-only projections + command submission through backend; UI never holds authority |

## Import rules (enforced by scripts/architecture_check.py + this doc)

1. `packages/domain` + `packages/runtime` (Kernel): no fastapi/sqlalchemy/alembic/
   wanxiang_api/wanxiang_persistence/httpx/requests/openai/pydantic.
2. `packages/substrate` (Runtime/Forge): no fastapi/sqlalchemy/alembic/
   wanxiang_api/wanxiang_persistence/httpx/requests/openai.
3. `packages/persistence`: no fastapi/wanxiang_api; owns ORM behind ports.
4. `apps/api`: no sqlalchemy/alembic/wanxiang_persistence (composition root uses
   adapters via ports).
5. Domain -> Runtime -> Application/Persistence -> Substrate -> Apps/API
   (one direction; no cycles).

## No-God-Engine rule

The only production classes with "Engine" in the name are:
- `wanxiang_runtime.replay.ReplayEngine` (Kernel replay; required).
- `wanxiang_research.planner.PlannerEngine` (EXPERIMENTAL research; flag OFF).
- `wanxiang_persistence.database.create_engine_for` (SQLAlchemy factory function).

Forbidden: RealityRootEngine, SemanticISAEngine, WorldlineEngine, LineageManager,
EvolutionManager, DistillationEngine ? any new God Object requires a Kernel
Change Proposal (01_KERNEL_FREEZE_POLICY after M35; ADR + guard + negative test
before then).
