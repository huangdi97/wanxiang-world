# V5.1 Code-Minimality Ledger

> Maintained per Goal. Before/after metrics are computed with
> `uv run python scripts/v51_metrics.py`. The ledger records consolidation actions,
> new abstractions and their justification.

## Baseline (G21A) — before

| Package | Files | LOC | Classes | Funcs | Public names |
|---|---|---|---|---|---|
| packages/domain | 18 | 1239 | 58 | 18 | 76 |
| packages/substrate | 188 | 15531 | 331 | 128 | 459 |
| packages/runtime | 11 | 1083 | 17 | 13 | 30 |
| packages/application | 7 | 727 | 9 | 2 | 11 |
| packages/persistence | 9 | 559 | 11 | 2 | 13 |
| packages/observability | 5 | 303 | 7 | 8 | 15 |
| packages/evidence | 1 | 5 | 0 | 0 | 0 |
| packages/model_providers | 1 | 5 | 0 | 0 | 0 |
| packages/research | 12 | 1411 | 61 | 1 | 62 |
| apps/api | 13 | 969 | 30 | 14 | 44 |
| TOTAL | 265 | 21832 | 524 | 186 | 710 |

## Baseline findings (flagged registry/manager/service/engine names)

- substrate: ActionRegistry, AdjudicationService, AdjudicatorRegistry, CheckpointService, HostRegistry, InMemoryPackageRegistry, LeaseService, LifecycleService, PackageRegistry, PerspectiveService, ProjectionService, RecoveryService, RegistryLifecycle, SessionService, SkillRegistry, SourceRegistry
- runtime: ReplayEngine, ResolverRegistry
- research: ExperimentRegistry, LeaseRegistry, PlannerEngine (EXPERIMENTAL)
- persistence: create_engine_for (function)
- apps/api: ExperiencePlayerService, FamilyPortalService, HeritageWorkbenchService, LearnService, OperatorConsoleService, StrategyWorkbenchService, StudioService

Consolidation candidates to evaluate in G21C/G21F: overlapping registries (PackageRegistry vs InMemoryPackageRegistry; AdjudicatorRegistry vs ResolverRegistry; HostRegistry vs RegistryLifecycle), Service facades in apps/api, empty stub packages (evidence, model_providers).

## New long-lived abstractions introduced (per Goal)

| Goal | Abstraction | Justification | Status |
|---|---|---|---|
| G21A | scripts/v51_metrics.py | reusable deterministic metrics for minimality ledger | KEEP |
| G21A | reports/V5_1_PRE_MIGRATION_BASELINE.md | reproducible pre-migration freeze | KEEP (report) |

## Per-Goal deltas

| Goal | Additions (files/LOC) | Deletions (files/LOC) | Net LOC | Notes |
|---|---|---|---|---|
| G21A | +1 script (+~60 LOC), +4 reports | 0 | +~60 | no production code change |

## New long-lived abstractions introduced (per Goal)

| Goal | Abstraction | Justification | Status |
|---|---|---|---|
| G21A | scripts/v51_metrics.py | reusable deterministic metrics for minimality ledger | KEEP |
| G21B | tests/architecture/test_v51_traceability.py | reproducible traceability completeness check | KEEP |

| Goal | Additions (files/LOC) | Deletions (files/LOC) | Net LOC | Notes |
|---|---|---|---|---|
| G21B | +1 test (+~70 LOC), +1 report | 0 | +~70 | documentation + test only |
| G21C | scripts/v51_forensics.py | deterministic duplicate-abstraction scanner for minimality audits | KEEP |
| G21C | +1 script (+~150 LOC), +1 report, +1 test (+~60 LOC) | 0 | +~210 | forensics only, no production change |
