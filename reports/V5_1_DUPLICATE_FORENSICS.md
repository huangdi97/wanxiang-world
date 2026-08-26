# V5.1 Duplicate-Abstraction Forensics (G21C)

> Deterministic AST scan. Groups: registry/catalog, state models, stores,
> services/managers, engines, ports, oversized modules, commit paths.
## registry_classes (16)

| path | name | line |
|---|---|---|
| packages/research/src/wanxiang_research/distributed_host.py | LeaseRegistry | 38 |
| packages/research/src/wanxiang_research/results.py | ExperimentRegistry | 46 |
| packages/runtime/src/wanxiang_runtime/resolver.py | ResolverRegistry | 29 |
| packages/substrate/src/wanxiang_substrate/actions/registry.py | ActionRegistry | 8 |
| packages/substrate/src/wanxiang_substrate/distill/protocol.py | DistillerRegistry | 54 |
| packages/substrate/src/wanxiang_substrate/domains/capability.py | DomainRegistry | 38 |
| packages/substrate/src/wanxiang_substrate/host/host.py | HostRegistry | 107 |
| packages/substrate/src/wanxiang_substrate/lineage/presence.py | PresenceRegistry | 71 |
| packages/substrate/src/wanxiang_substrate/packages/registry.py | PackageRegistry | 15 |
| packages/substrate/src/wanxiang_substrate/packages/registry.py | InMemoryPackageRegistry | 24 |
| packages/substrate/src/wanxiang_substrate/preview/scope.py | PreviewRegistry | 26 |
| packages/substrate/src/wanxiang_substrate/resolution/registry.py | AdjudicatorRegistry | 15 |
| packages/substrate/src/wanxiang_substrate/skills/registry.py | SkillRegistry | 13 |
| packages/substrate/src/wanxiang_substrate/sources/adapter.py | AdapterRegistry | 114 |
| packages/substrate/src/wanxiang_substrate/sources/registry.py | SourceRegistry | 31 |
| packages/substrate/src/wanxiang_substrate/workshop/registry.py | WorldRegistryCatalog | 99 |

## state_classes (37)

| path | name | line |
|---|---|---|
| packages/domain/src/wanxiang_domain/entity.py | EntityState | 34 |
| packages/domain/src/wanxiang_domain/entity.py | RelationState | 49 |
| packages/domain/src/wanxiang_domain/state.py | CanonicalState | 16 |
| packages/runtime/src/wanxiang_runtime/snapshot.py | StoredSnapshot | 17 |
| packages/runtime/src/wanxiang_runtime/state.py | InMemoryCanonicalState | 31 |
| packages/substrate/src/wanxiang_substrate/actor_continuity/projection.py | ActorContinuitySnapshot | 73 |
| packages/substrate/src/wanxiang_substrate/actor_continuity/projection.py | ActorContinuityProjection | 95 |
| packages/substrate/src/wanxiang_substrate/actor_continuity/relationship_model.py | RelationshipState | 56 |
| packages/substrate/src/wanxiang_substrate/authoring/living_ports.py | ReplayState | 25 |
| packages/substrate/src/wanxiang_substrate/authoring/model.py | AuthoringSnapshot | 49 |
| packages/substrate/src/wanxiang_substrate/authoring/scenario_engine.py | InitialSnapshot | 25 |
| packages/substrate/src/wanxiang_substrate/capability/model.py | CapabilityState | 32 |
| packages/substrate/src/wanxiang_substrate/capability/model.py | LearnerState | 112 |
| packages/substrate/src/wanxiang_substrate/cosim/adapter.py | FakeSimulatorState | 34 |
| packages/substrate/src/wanxiang_substrate/evolution/actor_evolution.py | ActorEvolutionState | 42 |
| packages/substrate/src/wanxiang_substrate/evolution/explainability.py | EvolutionExplainabilityProjection | 149 |
| packages/substrate/src/wanxiang_substrate/evolution/organization_model.py | OrganizationLifecycleState | 131 |
| packages/substrate/src/wanxiang_substrate/evolution/persona_adaptation.py | PersonaTraitState | 23 |
| packages/substrate/src/wanxiang_substrate/evolution/promotion/pipeline.py | GenesisSnapshot | 26 |
| packages/substrate/src/wanxiang_substrate/evolution/qualification.py | EvolutionProjectionSnapshot | 23 |
| packages/substrate/src/wanxiang_substrate/evolution/reputation_model.py | ReputationState | 66 |
| packages/substrate/src/wanxiang_substrate/evolution/reputation_model.py | ReputationProjection | 113 |
| packages/substrate/src/wanxiang_substrate/evolution/social_role.py | SocialRoleProjection | 99 |
| packages/substrate/src/wanxiang_substrate/genealogy/privacy.py | ConsentState | 19 |
| packages/substrate/src/wanxiang_substrate/lifecycle/model.py | LifecycleState | 87 |
| packages/substrate/src/wanxiang_substrate/long_horizon/lod.py | LODState | 88 |
| packages/substrate/src/wanxiang_substrate/material/errors.py | InvalidMaterialState | 26 |
| packages/substrate/src/wanxiang_substrate/projection/errors.py | UnauthorizedProjection | 14 |
| packages/substrate/src/wanxiang_substrate/projection/model.py | ProjectionSnapshot | 42 |
| packages/substrate/src/wanxiang_substrate/rc001/instantiate.py | InitialSnapshot | 59 |
| packages/substrate/src/wanxiang_substrate/reality/quest.py | QuestProjection | 61 |
| packages/substrate/src/wanxiang_substrate/recovery/errors.py | CorruptSnapshot | 18 |
| packages/substrate/src/wanxiang_substrate/recovery/errors.py | NoSnapshot | 22 |
| packages/substrate/src/wanxiang_substrate/session/embodiment.py | EmbodimentState | 26 |
| packages/substrate/src/wanxiang_substrate/session/model.py | HandoffState | 54 |
| packages/substrate/src/wanxiang_substrate/spatial/errors.py | InvalidSpatialState | 34 |
| packages/substrate/src/wanxiang_substrate/spatial/model.py | SpatialSnapshot | 91 |

## store_classes (29)

| path | name | line |
|---|---|---|
| packages/application/src/wanxiang_application/ports.py | WorldInstanceStore | 16 |
| packages/domain/src/wanxiang_domain/errors.py | CorruptEventStream | 69 |
| packages/persistence/src/wanxiang_persistence/event_store.py | SqlAlchemyEventStore | 26 |
| packages/persistence/src/wanxiang_persistence/snapshot_store.py | SqlAlchemySnapshotStore | 22 |
| packages/research/src/wanxiang_research/persona_memory.py | MemoryStore | 24 |
| packages/research/src/wanxiang_research/reality_stream.py | SensorStream | 47 |
| packages/research/src/wanxiang_research/reality_stream.py | SyntheticSensorStream | 51 |
| packages/runtime/src/wanxiang_runtime/ports.py | EventStore | 39 |
| packages/runtime/src/wanxiang_runtime/ports.py | InMemoryEventStore | 62 |
| packages/runtime/src/wanxiang_runtime/snapshot.py | SnapshotStore | 22 |
| packages/runtime/src/wanxiang_runtime/snapshot.py | InMemorySnapshotStore | 66 |
| packages/substrate/src/wanxiang_substrate/assets/storage.py | ObjectStore | 35 |
| packages/substrate/src/wanxiang_substrate/assets/storage.py | LocalObjectStore | 44 |
| packages/substrate/src/wanxiang_substrate/assets/storage.py | InMemoryObjectStore | 93 |
| packages/substrate/src/wanxiang_substrate/capability/runtime_control.py | RuntimeControlLedger | 33 |
| packages/substrate/src/wanxiang_substrate/draft/store.py | DraftStore | 20 |
| packages/substrate/src/wanxiang_substrate/evidence/conflict.py | ConflictLedger | 38 |
| packages/substrate/src/wanxiang_substrate/evolution/promotion/control.py | PromotionControlLedger | 29 |
| packages/substrate/src/wanxiang_substrate/jobs/store.py | JobStore | 35 |
| packages/substrate/src/wanxiang_substrate/ledger/completion.py | CompletionReviewLedger | 86 |
| packages/substrate/src/wanxiang_substrate/ledger/ledger.py | CompletionLedger | 30 |
| packages/substrate/src/wanxiang_substrate/long_horizon/budget.py | CostBudgetLedger | 98 |
| packages/substrate/src/wanxiang_substrate/long_horizon/checkpoint.py | RunCheckpointStore | 94 |
| packages/substrate/src/wanxiang_substrate/playable/store.py | PlayableStore | 57 |
| packages/substrate/src/wanxiang_substrate/playable/store.py | InMemoryPlayableStore | 79 |
| packages/substrate/src/wanxiang_substrate/recovery/checkpoint.py | CheckpointStore | 31 |
| packages/substrate/src/wanxiang_substrate/review/decisions.py | ReviewLedger | 37 |
| packages/substrate/src/wanxiang_substrate/sources/blob.py | SourceBlobStore | 51 |
| packages/substrate/src/wanxiang_substrate/workshop/store.py | WorkshopDraftStore | 16 |

## service_classes (25)

| path | name | line |
|---|---|---|
| packages/substrate/src/wanxiang_substrate/authoring/semantic_distillation.py | SemanticDistillationService | 50 |
| packages/substrate/src/wanxiang_substrate/authoring/service.py | AuthoringService | 26 |
| packages/substrate/src/wanxiang_substrate/jobs/service.py | JobService | 17 |
| packages/substrate/src/wanxiang_substrate/lifecycle/service.py | LifecycleService | 19 |
| packages/substrate/src/wanxiang_substrate/long_horizon/checkpoint.py | LongRunCheckpointService | 127 |
| packages/substrate/src/wanxiang_substrate/long_horizon/compaction.py | CompactionService | 107 |
| packages/substrate/src/wanxiang_substrate/observation/query.py | PerspectiveService | 29 |
| packages/substrate/src/wanxiang_substrate/parsing/checkpoint.py | ParseCheckpointService | 14 |
| packages/substrate/src/wanxiang_substrate/playable/entry.py | CharacterEntryService | 37 |
| packages/substrate/src/wanxiang_substrate/playable/service.py | PlayableService | 37 |
| packages/substrate/src/wanxiang_substrate/projection/service.py | ProjectionService | 32 |
| packages/substrate/src/wanxiang_substrate/recovery/checkpoint.py | CheckpointService | 86 |
| packages/substrate/src/wanxiang_substrate/recovery/recovery.py | RecoveryService | 31 |
| packages/substrate/src/wanxiang_substrate/resolution/service.py | AdjudicationService | 14 |
| packages/substrate/src/wanxiang_substrate/session/service.py | SessionService | 16 |
| packages/substrate/src/wanxiang_substrate/session/service.py | LeaseService | 50 |
| packages/substrate/src/wanxiang_substrate/workshop/genesis_provider.py | PromptGenesisProviderService | 150 |
| packages/substrate/src/wanxiang_substrate/workshop/service.py | WorkshopService | 40 |
| apps/api/src/wanxiang_api/experience_player_service.py | ExperiencePlayerService | 25 |
| apps/api/src/wanxiang_api/family_portal_service.py | FamilyPortalService | 22 |
| apps/api/src/wanxiang_api/heritage_workbench_service.py | HeritageWorkbenchService | 20 |
| apps/api/src/wanxiang_api/learn_service.py | LearnService | 23 |
| apps/api/src/wanxiang_api/operator_console_service.py | OperatorConsoleService | 22 |
| apps/api/src/wanxiang_api/strategy_workbench_service.py | StrategyWorkbenchService | 44 |
| apps/api/src/wanxiang_api/studio_service.py | StudioService | 24 |

## engine_classes (5)

| path | name | line |
|---|---|---|
| packages/research/src/wanxiang_research/planner.py | PlannerEngine | 47 |
| packages/runtime/src/wanxiang_runtime/replay.py | ReplayEngine | 21 |
| packages/substrate/src/wanxiang_substrate/authoring/completion_engine.py | CompletionEngine | 178 |
| packages/substrate/src/wanxiang_substrate/authoring/scenario_engine.py | ScenarioEngine | 78 |
| packages/substrate/src/wanxiang_substrate/epistemic/belief_revision.py | BeliefRevisionEngine | 91 |

## ports (41)

| path | name | line |
|---|---|---|
| packages/application/src/wanxiang_application/ports.py | WorldInstanceStore | 16 |
| packages/application/src/wanxiang_application/ports.py | AuditSink | 30 |
| packages/domain/src/wanxiang_domain/reality_root.py | RealityRootContract | 79 |
| packages/domain/src/wanxiang_domain/state.py | CanonicalState | 16 |
| packages/research/src/wanxiang_research/ai_compiler.py | ExtractionProvider | 25 |
| packages/research/src/wanxiang_research/digital_human.py | AvatarProvider | 52 |
| packages/research/src/wanxiang_research/generative_assets.py | AssetGenerator | 81 |
| packages/research/src/wanxiang_research/planner.py | Planner | 25 |
| packages/research/src/wanxiang_research/reality_stream.py | SensorStream | 47 |
| packages/research/src/wanxiang_research/sim_federation.py | SimulatorAdapter | 38 |
| packages/runtime/src/wanxiang_runtime/branch.py | BranchRepository | 14 |
| packages/runtime/src/wanxiang_runtime/ports.py | EventAppendPort | 25 |
| packages/runtime/src/wanxiang_runtime/ports.py | EventStore | 39 |
| packages/runtime/src/wanxiang_runtime/resolver.py | CommandValidator | 23 |
| packages/runtime/src/wanxiang_runtime/snapshot.py | SnapshotStore | 22 |
| packages/substrate/src/wanxiang_substrate/actor_continuity/reprioritization_policy.py | GoalReprioritizationPolicy | 20 |
| packages/substrate/src/wanxiang_substrate/actor_continuity/reprioritization_policy.py | GoalProposalProvider | 80 |
| packages/substrate/src/wanxiang_substrate/agency/policy.py | PolicyContext | 13 |
| packages/substrate/src/wanxiang_substrate/agency/policy.py | Policy | 21 |
| packages/substrate/src/wanxiang_substrate/assets/foundry.py | AssetGenerator | 38 |
| packages/substrate/src/wanxiang_substrate/assets/storage.py | ObjectStore | 35 |
| packages/substrate/src/wanxiang_substrate/authoring/living_ports.py | LivingRuntimePort | 15 |
| packages/substrate/src/wanxiang_substrate/authoring/living_ports.py | ReplayState | 25 |
| packages/substrate/src/wanxiang_substrate/authoring/living_ports.py | BranchResult | 29 |
| packages/substrate/src/wanxiang_substrate/authoring/multimodal.py | ExternalSourceConnector | 117 |
| packages/substrate/src/wanxiang_substrate/authoring/providers.py | Provider | 52 |
| packages/substrate/src/wanxiang_substrate/cosim/adapter.py | SimulationAdapter | 19 |
| packages/substrate/src/wanxiang_substrate/distill/protocol.py | Distiller | 18 |
| packages/substrate/src/wanxiang_substrate/packages/registry.py | PackageRegistry | 15 |
| packages/substrate/src/wanxiang_substrate/playable/service_model.py | SubmittedResult | 14 |
| packages/substrate/src/wanxiang_substrate/playable/service_model.py | EventLike | 19 |
| packages/substrate/src/wanxiang_substrate/playable/state_diff.py | NarrativeRenderer | 133 |
| packages/substrate/src/wanxiang_substrate/playable/store.py | PlayableStore | 57 |
| packages/substrate/src/wanxiang_substrate/preview/runtime.py | CreatedWorld | 43 |
| packages/substrate/src/wanxiang_substrate/preview/runtime.py | ReplayResult | 48 |
| packages/substrate/src/wanxiang_substrate/preview/runtime.py | PreviewRuntimePort | 52 |
| packages/substrate/src/wanxiang_substrate/reality/bridge.py | ObservationAdapter | 21 |
| packages/substrate/src/wanxiang_substrate/reality/challenge.py | OpportunityDetector | 204 |
| packages/substrate/src/wanxiang_substrate/runtime_port.py | WorldRuntimePort | 29 |
| packages/substrate/src/wanxiang_substrate/sources/adapter.py | SourceAdapter | 49 |
| packages/substrate/src/wanxiang_substrate/workshop/genesis_provider.py | PromptGenesisProvider | 28 |

## oversized_modules (0)

(none)

## commit_paths (1)

| path | name | line |
|---|---|---|
| packages/runtime/src/wanxiang_runtime/authority.py | commit | 91 |
