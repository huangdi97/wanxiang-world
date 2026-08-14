# Changelog ? Wanxiang Engineering Program

## 2026-08-11 ? Batch initialization

- Repository initialized (`git init`, branch `main`).
- Pre-implementation audit written (`reports/PRE_IMPLEMENTATION_AUDIT.md`).
- Ledgers created: PLAN, STATUS, DECISIONS, BLOCKERS, KNOWN_FAILURES, CHANGELOG, AGENTS.
- Batch scope: GOAL_00A .. GOAL_01F + M1 qualification. Stop after M1 PASS.

## 2026-08-11 ? GOAL_00A PASS

- uv workspace + 7 Python packages (src layout, py.typed), strict ruff/pyright/pytest config.
- `packages/observability`: settings loading, secret redaction, structured logging.
- TypeScript baseline (`packages/sdk_ts`) with strict tsconfig, ESLint, Vitest; all gates green.
- `scripts/quality.py` stable quality gate; CI workflow; docker-compose baseline.
- Ledgers/ADR structure/runbook created; ADR-0001 accepted.
- Checkpoint: `goal 00A: establish reproducible engineering foundation`.

## 2026-08-12 ? GOAL_00B PASS (M0 PASS)

- `scripts/architecture_check.py`: forbidden imports, import cycles, file-size,
  secret and placeholder guards; integrated into `scripts/quality.py`.
- `docs/architecture/MODULE_BOUNDARIES.md`, `reports/ACCEPTANCE_MATRIX.md` created.
- Architecture guard negative tests (17 tests total green).
- Reports: `reports/goal_00B_report.md`, `reports/M0_ENGINEERING_BASE_ACCEPTANCE.md`.
- Milestone tag `m0-engineering-base` created at M0 PASS.

## 2026-08-12 ? GOAL_01A PASS

- `packages/domain` core contracts: ids, versions, time, errors, hierarchy,
  entity, command, delta, event, hashing, state, snapshot, run, evidence, rights.
- Versioned serialization (command/delta + history contracts) with schema-version
  rejection; semantic hashing excluding wall-clock/audit fields.
- `docs/architecture/CORE_CONTRACTS.md`; ADR-0003.
- 48 tests green (unit + property).

## 2026-08-12 ? GOAL_01B PASS

- Commit Authority with preconditions, immutable canonical state, pure
  apply_delta, invariant registry, append-port atomicity, audit records.
- EventAppendPort + in-memory adapter (failure injection); ResolverRegistry seam.
- ComponentData gains component_id; ADRs 0004-0005.
- 63 tests green; docs/architecture/COMMIT_AUTHORITY.md.

## 2026-08-12 ? GOAL_01C PASS

- EventStore contract (append/load/idempotency/integrity) + InMemoryEventStore.
- Optimistic concurrency via store head; stale writers raise StaleRevision.
- Reusable contract suite (in-memory now; SQLite adapter in 01E).
- 75 tests green; docs/architecture/EVENT_STORE.md; ADR-0006.

## 2026-08-12 ? GOAL_01D PASS

- ReplayEngine (fork-aware, contiguous seq, version checks), SnapshotStore +
  in-memory adapter, branch fork/repository, state diff.
- Commit Authority branch_base_revision; golden replay fixture v1 committed.
- 93 tests green; docs/architecture/REPLAY_BRANCHING.md; ADR-0007.

## 2026-08-12 ? GOAL_01E PASS

- SQLAlchemy adapters (event store, snapshot store, branch/instance/audit repos).
- Alembic migrations 0001_initial + 0002_add_event_seq_index; migration tests.
- SqlAlchemyEventStore in shared contract suite; durable replay == golden hash.
- 111 tests green; docs/architecture/PERSISTENCE.md; ADR-0008.

## 2026-08-13 ? M9 PASS + G12A-H PASS (P9 phase) + FINAL RELEASE REPORT

- M9 qualification PASS: 30-day/1000+ tick stability, backup/restore/migration,
  OpenAPI/TS SDK, research/3D/foundry/gateway adapters, security checks
  (385 Python + 21 TS tests); tag `m9-release-qualified`.
- G12A stability; G12B backup; G12C SDK/OpenAPI; G12D research adapters; G12E
  projection3d contracts; G12F asset foundry; G12G digital-human gateway; G12H
  security.
- Final reports: FINAL_PROGRAM_COMPLETION_REPORT, ARCHITECTURE_CONFORMANCE_FINAL,
  MIGRATION_REPLAY_COMPATIBILITY_FINAL, SECURITY_RIGHTS_FINAL,
  LONG_RUN_STABILITY_FINAL, docs/RELEASE_READINESS.
- Program complete: M1?M9 PASS, 55 goals, local checkpoints only; no push/deploy.
## 2026-08-13 ? M8 PASS + G11A-F PASS (P8 phase)

- M8 qualification PASS: two fake simulators at different rates, deterministic
  multi-rate orchestrator, explicit proposal arbitration, campaign
  logistics/movement/fog-of-war, batch experiments with distributions and
  ValidityEnvelope (372 tests); tag `m8-cosimulation-strategy`.
- G11A adapter; G11B orchestrator; G11C/D campaign; G11E batch evaluation; G11F
  Liaoshen template (real data EXTERNAL_BLOCKED).
- ADRs 0047-0049; checkpoint `m8: qualify milestone`.
## 2026-08-13 ? M7 PASS + G08A-G10D PASS (P7 phase)

- M7 qualification PASS: mansion 7-day living world, Red Chamber source gate
  (real data EXTERNAL_BLOCKED), family GEDCOM/claims/privacy, heritage
  IIIF/Linked Art/twin/biography (366 tests); tag `m7-domain-generality`.
- G08A mansion; G08B red chamber slice; G09A GEDCOM; G09B family world; G09C
  privacy/persona; G10A IIIF; G10B Linked Art; G10C semantic twin; G10D museum
  biography.
- ADRs 0043-0046; checkpoint `m7: qualify milestone`.
## 2026-08-13 ? M6 PASS + G07A-E PASS (P6 phase)

- M6 qualification PASS: fake physical observations (duplicates/conflicts) ->
  bridge -> fusion -> opportunity/challenge -> director proposal through
  normal commit -> multi-seed experiment from fixed baseline (349 tests); tag
  `m6-reality-experiments`.
- G07A reality bridge; G07B observation fusion; G07C challenge compiler; G07D
  director runtime; G07E experiment runtime/validity envelope.
- ADRs 0038-0042; checkpoint `m6: qualify milestone`.
## 2026-08-13 ? G06A-C PASS; M5 re-qualified with lifecycle & recovery

- G06A `wanxiang_substrate.lifecycle`: 7 lifecycle modes, deterministic
  transitions, canonical `host.lifecycle` persistence, virtual clock drivers,
  catch-up policy.
- G06B `wanxiang_substrate.queue`: bounded command queue with dedup,
  serialized drain, structured statuses and backpressure.
- G06C `wanxiang_substrate.recovery`: checkpoint validation, snapshot/event
  replay fallback, resource budgets.
- M5 re-qualified: lifecycle persists across restart, multi-client queue
  idempotency/conflict, crash-restart hash continuity (335 tests); tag
  `m5-human-in-world-without-authority` moved to this commit.
## 2026-08-13 ? M5 PASS + G05A-F PASS (P5 phase)

- M5 qualification PASS: hosted world + Studio/Phaser sessions, embodiment
  lease (one primary controller), human commits, shadow advice-only, release +
  deterministic resume, clients disconnect while world continues, process
  restart preserves canonical semantic hash, reconnect rebuilds projection;
  tag `m5-human-in-world-without-authority`.
- G05A world host (orchestration boundary, not commit authority); G05B
  session/embodiment lease; G05C shadow/human control handoff; G05D projection
  API with server-side rights/knowledge filters; G05E Studio TS slice; G05F
  Phaser TS slice (React/Phaser rendering EXTERNAL_BLOCKED).
- 320 Python tests + 14 TS tests green; ADRs 0030-0034; checkpoint
  `m5: qualify milestone`.
## 2026-08-13 ? M4 PASS + G04E PASS (P4 phase)

- M4 qualification PASS: author -> Source Gate -> compiler -> ledger canon ->
  registry -> install (pinned) -> instantiate -> export/re-import -> publish v2
  without mutating the v1 instance (replay-stable); milestone tag
  `m4-worlds-authored-installed`.
- G04E: `wanxiang_substrate.packages.install`: transactional install
  (resolve -> hash verify -> trust -> compatibility -> InstallRecord with exact
  pins), portable export with stable hash, explicit upgrade with fork-required
  incompatibility detection.
- 309 tests green; ADR-0029; docs/architecture/PACKAGE_INSTALL.md;
  reports/g04e_report.md + reports/M4_ACCEPTANCE.md; checkpoint
  `goal g04e: package install, export & migration compatibility`.
## 2026-08-13 ? G04D PASS (P4 phase)

- `wanxiang_substrate.ledger`: truth-label taxonomy (canon/source_backed/
  completion/model_inference/reconstruction/user_fiction) with deterministic
  promotion graph, CompletionLedger with immutable ReviewDecision history,
  canon lock + override, rights gate, package-version diff and audit snapshot.
- 302 tests green; ADR-0028; docs/architecture/COMPLETION_LEDGER.md;
  reports/g04d_report.md; checkpoint `goal g04d: completion ledger & review
  workflow`.
## 2026-08-13 ? G04C PASS (P4 phase)

- `wanxiang_substrate.compiler`: safe readers (json strict, restricted YAML
  subset, markdown explicit sections, text facts), deterministic
  StructuredCompiler (read -> validate -> compile -> emit) with stable result
  hash, provenance-bound CandidateObjects, structured diagnostics, review
  export; PDF/OCR/video explicitly unsupported (not faked).
- 293 tests green; ADR-0027; docs/architecture/STRUCTURED_COMPILER.md;
  reports/g04c_report.md; checkpoint `goal g04c: structured compiler mvp`.
## 2026-08-13 ? G04B PASS (P4 phase)

- `wanxiang_substrate.sources`: immutable SourceRecord + review stages E0..E5,
  RightsEnvelope, ClaimCandidate/EvidenceLink (conflicting claims coexist),
  SourceRegistry with append-only audit, pure SourceGate (rights + stage +
  injection scan), versioned SourcePolicy, approved/rejected/conflicting/
  malicious fixtures.
- 283 tests green; ADR-0026; docs/architecture/SOURCE_GATE.md;
  reports/g04b_report.md; checkpoint `goal g04b: source registry & source
  gate`.
## 2026-08-13 ? G04A PASS (P4 phase)

- `wanxiang_substrate.packages`: PackageManifest/SemanticVersion/
  VersionConstraint/PackageLock, deterministic DependencyResolver (cycles,
  conflicts, missing), InMemoryPackageRegistry with content-hash verification,
  default-deny ExecutableExtensionPolicy, manifest schema migration v1->v2,
  compatibility matrix, synthetic town package graph.
- 275 tests green; ADR-0025; docs/architecture/PACKAGE_REGISTRY.md;
  reports/g04a_report.md; checkpoint `goal g04a: package, schema &
  dependency registry`.
## 2026-08-13 ? M3 PASS + G03G PASS (P3 phase)

- M3 qualification PASS: observation -> belief -> correction -> multi-step
  skill -> bounded capability change vertical with knowledge isolation
  (`tests/integration/test_m3_qualification.py`); milestone tag
  `m3-bounded-agents`.
- G03G: `wanxiang_substrate.capability`: bounded CapabilityState (level 0..10,
  mastery/confidence 0..1), PracticeRecord/AssessmentEvidence with evidence
  refs, deterministic LearningPolicy (clamped), CapabilityQuery,
  `capability.record_practice` / `capability.record_assessment` /
  `capability.apply_delta` resolvers; SkillRuntime step capability gates.
- 265 tests green; ADR-0024; docs/architecture/CAPABILITY_LEARNING.md;
  reports/g03g_report.md + reports/M3_ACCEPTANCE.md; checkpoint
  `goal g03g: capability & learning`.
## 2026-08-13 ? G03F PASS (P3 phase)

- `wanxiang_substrate.skills`: versioned SkillDefinition/SkillStep/
  SkillInstance, SkillRegistry with deliver-letter (3 steps) and inspect-object
  reference skills, `skill.start` / `skill.set_state` resolvers, and
  SkillRuntime (execute/pause/resume/cancel). Every step is submitted through
  WorldRuntime (validate -> resolve -> commit); skill state persists as a
  versioned `skill.instance` component.
- 255 tests green; ADR-0023; docs/architecture/SKILL_RUNTIME.md;
  reports/g03f_report.md; checkpoint `goal g03f: skill runtime`.
## 2026-08-13 ? G03E PASS (P3 phase)

- `wanxiang_substrate.resolution`: Adjudication + provenance + uncertainty,
  SeededRng, adjudicator registry by (action, version), reference deterministic
  transfer + seeded gamble, version pinning.
- 250 tests green; ADR-0022; docs/architecture/RESOLUTION_ADJUDICATION.md;
  reports/g03e_report.md; checkpoint `goal g03e: resolver, adjudication &
  deterministic policies`.

## 2026-08-13 ? G03D PASS (P3 phase)

- `wanxiang_substrate.actions`: versioned action registry + reference actions,
  side-effect-free ActionValidator (schema/actor/permission/reachability/
  epistemic/resources), affordance computation.
- 244 tests green; ADR-0021; docs/architecture/ACTION_VALIDATOR.md;
  reports/g03d_report.md; checkpoint `goal g03d: action, affordance & validator`.

## 2026-08-13 ? G03C PASS (P3 phase)

- `wanxiang_substrate.agency`: propose-only policy ports (deterministic/rule/
  human), order lifecycle with typed transitions, actor states, organization
  views.
- 236 tests green; ADR-0020; docs/architecture/AGENCY_RUNTIME.md;
  reports/g03c_report.md; checkpoint `goal g03c: actor & organization runtime`.

## 2026-08-13 ? G03B PASS (P3 phase)

- `wanxiang_substrate.epistemic`: belief/memory graph with corrections
  (lineage links), contradictions retained, forgetting + bounded compaction,
  actor-scoped access grants.
- 228 tests green; ADR-0019; docs/architecture/EPISTEMIC_GRAPH.md;
  reports/g03b_report.md; checkpoint `goal g03b: belief, memory & temporal
  epistemic graph`.

## 2026-08-13 ? G03A PASS (P3 phase)

- `wanxiang_substrate.observation`: PerspectiveService derives observations
  from events + spatial/acoustic/rights; sealed payload content never leaks;
  private/group visibility; announce action.
- 220 tests green; ADR-0018; docs/architecture/OBSERVATION_PERSPECTIVE.md;
  reports/g03a_report.md; checkpoint `goal g03a: observation & perspective
  isolation`.

## 2026-08-13 ? M2 PASS (Deterministic Living World Exists)

- Integrated 72h micro-town scenario passes (spatial + temporal + material +
  body + institution + population), no user input; M1 invariants green.
- 212 tests green; reports/M2_ACCEPTANCE.md; matrix updated;
  tag `m2-deterministic-living-world`. Next: G03A (P3).

## 2026-08-13 ? G02F PASS (M2 phase)

- `wanxiang_substrate.population`: multi-rate autonomous scheduler submitting
  commands through M1 authority (deterministic ids, bounded budgets), micro-town
  fixture; 72h run with no user input.
- WorldRuntime validated StateReader cache + SQL aggregate last_event_seq.
- 211 tests green; ADR-0016; docs/architecture/POPULATION_SCHEDULER.md;
  reports/g02f_report.md; checkpoint `goal g02f: population resolution &
  autonomous scheduler`.

## 2026-08-13 ? G02E PASS (M2 phase)

- `wanxiang_substrate.institution`: roles, time-scoped memberships, delegated
  permissions with provenance, duties, sanctions; restricted places require
  permission; expired roles cannot grant authority.
- 202 tests green; ADR-0015; docs/architecture/INSTITUTION_SUBSTRATE.md;
  reports/g02e_report.md; checkpoint `goal g02e: institution, authority, duty
  & norm`.

## 2026-08-13 ? G02D PASS (M2 phase)

- `wanxiang_substrate.body`: bounded condition facets, mobility/fatigue
  capability, visibility/privacy, deterministic exert/rest transitions.
- Spatial move rejects fatigued/immobile actors (BodyConstraintViolation).
- 192 tests green; ADR-0014; docs/architecture/BODY_SUBSTRATE.md;
  reports/g02d_report.md; checkpoint `goal g02d: body & condition constraints`.

## 2026-08-13 ? G02C PASS (M2 phase)

- `wanxiang_substrate.material`: items/containers/custody/ownership/info
  payloads on versioned components; transfer/move/consume/damage/seal/read
  resolvers through M1 authority; sealed-letter epistemic separation.
- Containment cycle prevention, capacity, custody conservation; no new migration.
- 182 tests green; ADR-0013; docs/architecture/MATERIAL_SUBSTRATE.md;
  reports/g02c_report.md; checkpoint `goal g02c: material, container, custody
  & information payload`.

## 2026-08-13 ? G02B PASS (M2 phase)

- `wanxiang_substrate.temporal`: WorldClock (command-advanced, monotonic),
  Calendar, Appointment/Deadline/RecurringEvent with deterministic bounded
  recurrence, TemporalQuery, resolvers, calendar fixture.
- Backward advance -> BackwardTimeError; schedule conflicts -> ScheduleConflict;
  window violations -> TimeWindowViolation; restart keeps due events exactly once.
- 168 tests green; ADR-0012; docs/architecture/TEMPORAL_SUBSTRATE.md;
  reports/g02b_report.md; checkpoint `goal g02b: temporal system & schedules`.

## 2026-08-13 ? G02A PASS (M2 phase begins)

- `packages/substrate` spatial substrate: model, query (topology/path/capacity/
  access/zones), resolvers (move/set_portal_state/instantiate), house fixture.
- Spatial state on versioned components; no new migration; M1 replay untouched.
- 153 tests green; ADR-0011; docs/architecture/SPATIAL_SUBSTRATE.md;
  reports/g02a_report.md; checkpoint `goal g02a: spatial topology & access`.

## 2026-08-12 ? GOAL_01F PASS (M1 PASS)

- Application layer: WorldRuntime, synthetic micro-world resolvers,
  WorldEnvironment facade; FastAPI thin transport with structured errors/OpenAPI.
- M1 acceptance A1-A10 PASS on SQLite; API e2e + environment tests.
- 130 tests green; reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md; acceptance
  matrix updated; docs/IMPLEMENTATION_STATUS.md.
- Milestone tag `m1-authoritative-world` created at M1 PASS.
- Batch stop condition reached: do not begin G02A in this batch.

## 2026-08-14 ? G13A PASS (M10 phase)

- Independently verified the claimed M9 checkpoint: `uv run python scripts/quality.py`
  -> ruff / pyright / 385 pytest / architecture PASS; TS SDK 21 tests PASS
  (initial `EPERM: spawn` was sandbox-only, passed outside sandbox).
- Integrated the Post-M9 execution pack (10-23, goals G13A-G20E, milestone gates
  M10-M17) per `23_POST_M9_HANDOFF_PROTOCOL.md`; PACK_MANIFEST.md updated;
  94/94 SHA-256 entries verified against files.
- Added reproducible baseline capture `scripts/capture_post_m9_baseline.py` and
  `reports/POST_M9_BASELINE.md`, `reports/post_m9_baseline.json`,
  `reports/POST_M9_COMMAND_MATRIX.md`, `reports/G13A_REPORT.md`.
- Disposable clean bootstrap: Alembic 0001 -> 0002 (head) on a fresh SQLite DB PASS.
- Checkpoint: `g13a: post-m9 baseline freeze & independent evidence capture`.

## 2026-08-14 ? G13B PASS (M10 phase)

- Added `scripts/traceability.py` (stable WX-<plane>-<section>-NNN IDs, 16 kernels,
  44 requirements, 63-goal mapping) with validator and markdown/JSON generators.
- Produced `reports/DESIGN_IMPLEMENTATION_TRACEABILITY.md`,
  `reports/design_implementation_traceability.json`,
  `reports/KERNEL_COVERAGE_SUMMARY.md`, `reports/G13B_REPORT.md`.
- Added `tests/architecture/test_traceability.py` (7 tests) enforcing unique IDs,
  valid statuses, full kernel coverage, VERIFIED implementation/test ownership,
  goal mapping integrity and JSON currency.
- Checkpoint: `g13b: design-to-implementation traceability matrix`.

## 2026-08-14 ? G13C PASS (M10 phase)

- Added `scripts/architecture_forensics.py` (AST dependency graph, forbidden-import,
  persistence-leakage, CommitAuthority call-site, direct-write and cycle audits).
- Produced `reports/ARCHITECTURE_FORENSICS.md`, `reports/DEPENDENCY_GRAPH.md`,
  `reports/CANONICAL_MUTATION_PATHS.md`, `reports/architecture_forensics.json`,
  `reports/G13C_REPORT.md`.
- Added `tests/architecture/test_architecture_forensics.py` (11 tests): repository
  clean (0 forbidden/leakage/writes/cycles, single CommitAuthority constructor),
  detector anti-tests, projection/StateReader no-write-API, duplicate-command
  idempotency through the event store.
- Checkpoint: `g13c: architecture, dependency & canonical-mutation forensics`.

## 2026-08-14 ? G13D PASS (M10 phase)

- Fixed architecture-guard placeholder bug: `scan_placeholders` only ever checked the first
  pattern (TODO); now scans all marker patterns (regression test covers every marker).
- Fixed OpenAPI/SDK schema drift: FastAPI app is now the single source of truth;
  `scripts/export_openapi.py` exports `packages/sdk_ts/src/openapi-contract.json`
  (10 ops); TS SDK test consumes the real contract; Python drift test detects manual edits.
- Added `scripts/false_completion_scan.py` and reports (FALSE_COMPLETION_AUDIT,
  SURFACE_INTEGRATION_MAP, SCHEMA_DRIFT_AUDIT) + `tests/architecture/test_false_completion.py`
  (7 tests). Dead code = 0; hardcoded candidates classified as legitimate literals.
- Quality gate: ruff/pyright clean, 410 pytest PASS, TS 22 tests PASS.
- Checkpoint: `g13d: placeholder, fake, dead-path & surface integration audit`.

## 2026-08-14 ? G13E PASS (M10 phase)

- Fixed P0: child-branch cold replay / restore_and_replay failed (CorruptEventStream) because
  ReplayEngine conflated branch-local event_seq with global revision. Replay now checks the two
  counters independently with an explicit start_seq (child branches pass 1; snapshot continuation
  defaults to baseline.revision+1). StateReader and WorldRuntime wired accordingly.
- Added `scripts/history_forensics.py` and reports (REPLAY_GOLDEN_CORPUS, VERSION_COMPATIBILITY_MATRIX,
  HISTORY_COMPATIBILITY_FORENSICS) + `tests/integration/test_g13e_history.py` (7 tests: golden corpus,
  unsupported versions fail explicitly, version-pinned drift rejection, child cold replay/restore,
  migration hash preservation, corruption guard).
- Quality gate: ruff/pyright clean, 417 pytest PASS, architecture PASS.
- Checkpoint: `g13e: event, replay, branch, migration & version forensics`.

## 2026-08-14 ? G13F PASS (M10 phase)

- Added `scripts/security_forensics.py` and reports (THREAT_MODEL_POST_M9, RIGHTS_ENFORCEMENT_MATRIX,
  SECURITY_RIGHTS_SOURCE_FORENSICS) + `tests/integration/test_g13f_security.py` (5 adversarial tests:
  unapproved-source gating, conflicting-claim provenance, denied-rights projection/export, prompt-injection
  isolation, secret scan + log redaction).
- No P0/P1 rights/source/security bypass found; all enforcement server-side; secrets scan clean.
- Quality gate: ruff/pyright clean, 422 pytest PASS, architecture PASS.
- Checkpoint: `g13f: security, rights, provenance, privacy & source-gate forensics`.

## 2026-08-14 ? G13G PASS (M10 phase)

- Added `scripts/maintainability_audit.py` and reports (MAINTAINABILITY_AUDIT, TEST_QUALITY_AUDIT,
  UPGRADEABILITY_AUDIT) + `tests/integration/test_g13g_maintainability.py` (6 tests).
- Fixed silent exception swallow in `population/scheduler.py`: rejected scheduler actions are now counted
  and surfaced as `SchedulerRunResult.rejected_events` (deterministic; additive contract).
- 5 complexity hotspots classified as tracked P2 closure candidates; 9 `Any` params justified at external
  boundaries; 0 files over 300 lines; 0 cycles.
- Quality gate: ruff/pyright clean, 428 pytest PASS, architecture PASS.
- Checkpoint: `g13g: maintainability, complexity, test quality & upgradeability audit`.

## 2026-08-14 ? G13H PASS (M10 phase)

- Documented all three internally actionable P0 gaps found by G13A-G13G (child-branch replay corruption,
  placeholder-guard blind spot, OpenAPI/SDK drift) as CLOSED with root cause, fix commit and regression tests.
- P0 open count = 0; P0-focused regression set 36 passed; full gate PASS (428 tests).
- Checkpoint: `g13h: p0 gap closure wave`.

## 2026-08-14 ? G13I PASS + M10 PASS (M10 gate)

- P1 open = 0 (SDK drift closed G13D; P0s closed G13D/E); P2 tracked (7 items with rationale).
- M10 independent requalification PASS: clean bootstrap, M1-M9 milestone set (21), replay corpus,
  security probes, forensics, full quality gate (428 pytest + ruff + pyright + architecture).
- Added M10_ACCEPTANCE.md, M10_INDEPENDENT_REQUALIFICATION.md, P1_P2_GAP_BACKLOG.md,
  DESIGN_IMPLEMENTATION_TRACEABILITY_FINAL_M10.md; ACCEPTANCE_MATRIX M10 rows.
- Checkpoint: `g13i: p1/p2 gap closure & m10 independent requalification`. M11 begins next.

## 2026-08-14 ? G14A PASS (M11 phase)

- Added `tests/integration/test_g14a_concurrency.py` (5 deterministic adversarial tests: lost-update,
  duplicate-across-restart idempotency, out-of-order delivery, instance isolation, burst validity) and
  `reports/CONCURRENCY_ADVERSARIAL.md`.
- Checkpoint: `g14a: concurrency, race, idempotency & lost-update adversarial qualification`.

## 2026-08-14 ? G14B PASS (M11 phase)

- Added `tests/integration/test_g14b_crash_atomicity.py` (5 tests: before-append, after-append restart,
  checkpoint, retry classification, lifecycle restart) and `reports/CRASH_ATOMICITY_MATRIX.md`.
- Recovery policy documented: events authoritative; snapshots/caches discardable; idempotent exactly-once retries.
- Checkpoint: `g14b: crash, atomicity & mid-commit recovery qualification`.

## 2026-08-14 ? G14C PASS (M11 phase)

- Added `tests/integration/test_g14c_fault_injection.py` (FaultyEventStore + 4 tests: fail-closed append,
  load-fault recovery, bounded retry storm, API 500 during fault) and `reports/DEPENDENCY_FAULT_INJECTION.md`.
- Checkpoint: `g14c: database, storage, network & dependency fault injection`.

## 2026-08-14 ? G14D PASS (M11 phase)

- Fixed P1: restore_and_replay silently accepted corrupted snapshot baselines (wrong hash, no error).
  Snapshots are now validated against event history and rejected with fallback to authoritative replay
  (snapshot_rejected observable).
- Added `scripts/history_diagnostics.py` (read-only corruption scan) and
  `tests/integration/test_g14d_corruption.py` (7 tests) + reports.
- Checkpoint: `g14d: event, snapshot, branch & history corruption adversarial qualification`.

## 2026-08-14 ? G14E PASS (M11 phase)

- Added `tests/integration/test_g14e_host_multiplayer.py` (4 tests: reconnect resync, multi-client queue
  ordering/idempotency, slow-client backpressure, lease uniqueness/recovery) and
  `reports/HOST_MULTIPLAYER_CHAOS.md`.
- Checkpoint: `g14e: world host, multiplayer, reconnect, ordering & backpressure chaos`.

## 2026-08-14 ? G14F PASS (M11 phase)

- Added `tests/integration/test_g14f_hostile_input.py` (6 tests: opaque identifiers, content-hash rejection,
  default-deny executable policy, dependency-conflict rollback, prompt-injection-as-data, size/format limits)
  and `reports/HOSTILE_PACKAGE_SOURCE_QUALIFICATION.md` (trust model + limitation).
- Checkpoint: `g14f: hostile package, plugin & source input qualification`.

## 2026-08-14 ? G14G PASS (M11 phase)

- Added `tests/integration/test_g14g_auth_privacy.py` (5 tests: cross-branch isolation, perspective filters,
  debug privilege, revocation of media/source rights, append-only audit) and
  `reports/AUTH_RIGHTS_PRIVACY_ADVERSARIAL.md`.
- Checkpoint: `g14g: authorization, rights, privacy & data-leak adversarial qualification`.

## 2026-08-14 ? G14H PASS (M11 phase)

- Fixed P1: CoSimOrchestrator checkpoint omitted the clock, breaking restore+continue; clock now part of checkpoint.
- Added `tests/integration/test_g14h_byzantine.py` (5 tests: proposals never commit, deterministic arbitration,
  fail-fast timeout, checkpoint mismatch detection, byzantine observation rejection/conflict) and reports.
- Checkpoint: `g14h: simulationadapter & external-system byzantine behavior qualification`.

## 2026-08-14 ? G14I PASS + M11 PASS (M11 gate)

- Added `tests/integration/test_g14i_resource_fuzz.py` (4 tests) + reports (RESOURCE_EXHAUSTION_CHAOS,
  M11_ADVERSARIAL_QUALIFICATION, M11_ACCEPTANCE).
- Restored no-swallow invariant by refactoring snapshot fallback to a flag-based path; split
  `snapshot_policy.py` to keep world_runtime <= 300 lines.
- M11 gate PASS: G14A-H adversarial suites (45 tests) + full gate 473 pytest + ruff/pyright/arch.
- Checkpoint: `g14i: resource exhaustion, fuzz, long-run chaos & m11 qualification`. M12 begins next.

## 2026-08-14 ? G15A PASS (M12 phase)

- Added `docs/REFERENCE_WORLD_CONTRACT.md`, `scripts/reference_world_conformance.py`,
  `tests/integration/test_g15a_reference_world_contract.py` (3 tests), acceptance reports.
- Black-box world pack contract: build/install without Core changes; harness catches missing metadata.
- Checkpoint: `g15a: reference world contract & external pack boundary`.

## 2026-08-14 ? G15B PASS (M12 phase)

- Added `reference_worlds/synthetic_full/` (synthetic full world: 5 places, 4 people, guild, objects,
  beliefs, scenario seeds) built/installed/instantiated via the public path.
- Added `tests/integration/test_g15b_synthetic_world.py` (4 tests) + build report.
- Checkpoint: `g15b: comprehensive synthetic reference world package`.

## 2026-08-14 ? G15C PASS (M12 phase)

- Added `tests/integration/test_g15c_seven_day.py` (7-day autonomous run on the synthetic full world,
  periodic hashes/checkpoints, replay verification, emergent events, no-starvation, no-leak) + reports.
- Checkpoint: `g15c: seven-day autonomous living-world qualification`.

## 2026-08-14 ? G15D PASS (M12 phase)

- Added `tests/integration/test_g15d_embodiment.py` (embodiment lease takeover, human command, shadow advice,
  conflicting takeover rejected, exit + autonomous advance, handoff resume, re-entry perspective) + reports.
- Checkpoint: `g15d: human embodiment, exit, re-entry & control continuity qualification`.

## 2026-08-14 ? G15E PASS (M12 phase)

- Added `tests/integration/test_g15e_material_info.py` (3 tests: exclusive containers, custody!=knowledge,
  causal read path, branch divergence + replay) + reports.
- Checkpoint: `g15e: material custody, information propagation & social continuity qualification`.

## 2026-08-14 ? G15F PASS (M12 phase)

- Added `tests/integration/test_g15f_worldlines.py` (baseline + two intervention worldlines, ancestry,
  parent-unchanged, per-worldline replay, semantic diff, historical read) + reports.
- Checkpoint: `g15f: branch, time-travel & counterfactual worldline comparison qualification`.

## 2026-08-14 ? G15G PASS (M12 phase)

- Added `tests/integration/test_g15g_ninety_day.py` (90-day run, LOD, sampled replay spot checks) + reports.
- Checkpoint: `g15g: extended 90-day virtual run & population-lod qualification`.

## 2026-08-14 ? G15H PASS (M12 phase)

- Added `tests/integration/test_g15h_red_chamber.py` (3 tests: source-gate canonical gating, label
  distinguishability, provenance retention) + reports. Real corpus EXTERNAL_BLOCKED with exact needs.
- Checkpoint: `g15h: red chamber source-gated qualified reference slice`.

## 2026-08-14 ? G15I PASS (M12 phase)

- Added `tests/integration/test_g15i_multidomain.py` (4 tests: genealogy, heritage, campaign, public-interface
  only) + reports. Real slices EXTERNAL_BLOCKED.
- Checkpoint: `g15i: family, heritage & campaign source-gated reference suites`.

## 2026-08-14 ? G15J PASS + M12 PASS (M12 gate)

- Added `tests/integration/test_g15j_worldness_certification.py` (3 tests) + reports
  (WORLDNESS_CERTIFICATION, M12_REFERENCE_WORLD_QUALIFICATION, M12_ACCEPTANCE).
- M12 gate PASS: worldness 12/12, black-box scenario, 24 M12 suites, full gate 497 tests.
- Checkpoint: `g15j: cross-domain worldness certification & m12 qualification`. M13 begins next.

## 2026-08-14 ? G16A PASS (M13 phase)

- Added `docs/PRODUCTION_TOPOLOGY.md`, production-profile validation in `wanxiang_observability/config.py`
  (fail-fast ConfigError for missing required production config), `tests/integration/test_g16a_config_secrets.py`
  (5 tests) + reports.
- Checkpoint: `g16a: production topology, configuration & secret-management foundation`.

## 2026-08-14 ? G16B PASS (M13 phase)

- Added `tests/integration/test_g16b_postgres.py` (offline Postgres DDL compile, portable-path check,
  storage-independent hash, live profile gated by env) + reports. Live Postgres EXTERNAL_BLOCKED + runbook.
- Checkpoint: `g16b: postgresql production persistence & migration qualification`.

## 2026-08-14 ? G16C PASS (M13 phase)

- Added `tests/integration/test_g16c_background_queue.py` (3 tests: idempotent at-least-once, failed-job
  retry, queue-pressure safety) + reports.
- Checkpoint: `g16c: background execution, work queue & scheduler reliability`.

## 2026-08-14 ? G16D PASS (M13 phase)

- Added content-addressed `assets/storage.py` (AssetRef + ObjectStore Port + LocalObjectStore + rights check),
  `assets/errors.py`, and `tests/integration/test_g16d_asset_storage.py` (4 tests) + reports.
- Checkpoint: `g16d: asset/object storage, media rights & durable artifact handling`.

## 2026-08-14 ? G16E PASS (M13 phase)

- Added `wanxiang_observability/tracing.py` (OTel-compatible facade: spans + metrics + in-memory exporter),
  `tests/integration/test_g16e_observability.py` (3 tests), runbook + reports.
- Checkpoint: `g16e: opentelemetry observability, slos & operational diagnostics`.

## 2026-08-14 ? G16F PASS (M13 phase)

- Added API rate limiter + payload guard (`wanxiang_api/limits.py`), 413 handler, SBOM generator
  (`scripts/generate_sbom.py` -> artifacts/SBOM_INFO.md + sbom.json), `tests/integration/test_g16f_security_hardening.py`
  (4 tests) + reports.
- Checkpoint: `g16f: production security hardening, authn/authz, rate limits & supply-chain controls`.

## 2026-08-14 ? G16G PASS (M13 phase)

- Added `scripts/backup_restore.py` (backup + restore with integrity manifest), `tests/integration/test_g16g_backup_restore.py`
  (3 tests), runbook + game-day report.
- Checkpoint: `g16g: backup, restore, pitr-like recovery & disaster game day`.

## 2026-08-14 ? G16H PASS (M13 phase)

- Added `scripts/release_build.py` (reproducible release manifest + migration preflight),
  `tests/integration/test_g16h_release.py` (3 tests), release process doc + reports.
- Checkpoint: `g16h: ci/cd, release artifacts, rolling migration & rollback qualification`.

## 2026-08-14 ? G16I PASS (M13 phase)

- Added `scripts/benchmarks.py` (repeatable commit/replay benchmarks with environment capture),
  `tests/integration/test_g16i_performance.py` (3 tests), capacity/cost report + benchmark JSON.
- Checkpoint: `g16i: performance, capacity, cost & resource-budget qualification`.

## 2026-08-14 ? G16J PASS + M13 PASS (M13 gate)

- Added `scripts/ops_deploy.py`, `tests/integration/test_g16j_deploy_ops.py` (4 tests), ops index +
  production qualification + M13 acceptance reports.
- M13 gate PASS: G16A-J suites (35 passed + 1 EXTERNAL_BLOCKED skip), full gate 532 passed + 1 skip.
- Checkpoint: `g16j: private/staging deployment, operator runbooks & m13 production qualification`. M14 begins next.

## 2026-08-14 ? G17A PASS (M14 phase)

- Added `docs/SDK_COMPATIBILITY_POLICY.md`, `scripts/sdk_baseline.py` + SDK_API_BASELINE + sdk_api_baseline.json
  (10 routes / 5 TS / 832 Python names), `tests/integration/test_g17a_sdk_contract.py` (3 tests).
- Checkpoint: `g17a: public sdk contract, semantic versioning & compatibility policy`.

## 2026-08-14 ? G17B PASS (M14 phase)

- Added `scripts/wxpack.py` (scaffold/validate/build CLI), `tests/integration/test_g17b_authoring_cli.py`
  (3 tests), CLI doc + reports.
- Checkpoint: `g17b: package authoring cli, scaffolder & schema validation`.

## 2026-08-14 ? G17C PASS (M14 phase)

- Added `docs/sdk/EXTERNAL_AUTHOR_GUIDE.md`, `tests/integration/test_g17c_author_docs.py` (2 tests).
- Checkpoint: `g17c: external author documentation & reference templates`.

## 2026-08-14 ? G17D PASS (M14 phase)

- Added `wxpack.py certify` (static + forbidden-import + runtime dry-run with versioned report),
  `tests/integration/test_g17d_certification.py` (2 tests) + harness doc/report.
- Checkpoint: `g17d: third-party package conformance & certification harness`.

## 2026-08-14 ? G17E PASS (M14 phase)

- Added `packages/trust_model.py` (signing seam, capabilities, CapabilityGate, audit),
  `tests/integration/test_g17e_plugin_trust.py` (4 tests), trust model doc + reports.
- Checkpoint: `g17e: plugin trust, signing, capability permissions & isolation policy`.

## 2026-08-14 ? G17F PASS (M14 phase)

- Added `packages/lifecycle.py` (publish/deprecate/yank/upgrade_candidate/pin install) and fixed the resolver
  root-version pin (P1). Added `tests/integration/test_g17f_registry_lifecycle.py` (4 tests) + reports.
- Checkpoint: `g17f: registry publish, install, upgrade, deprecation & dependency resolution`.

## 2026-08-14 ? G17G PASS (M14 phase)

- Added `scripts/blackbox_sample.py` (clean-room external sample), `tests/integration/test_g17g_blackbox_sample.py`
  (2 tests) + reports.
- Checkpoint: `g17g: black-box external sample pack built outside core repository internals`.

## 2026-08-14 ? G17H PASS + M14 PASS (M14 gate)

- Added `tests/integration/test_g17h_ecosystem.py` (2 tests) + ecosystem qualification + M14 acceptance reports.
- M14 gate PASS: G17A-H suites (22 passed), full gate 554 passed + 1 EXTERNAL_BLOCKED skip.
- Checkpoint: `g17h: ecosystem documentation, certification & m14 qualification`. M15 begins next.

## 2026-08-14 ? G18A PASS (M15 phase)

- Added `docs/PRODUCT_SURFACE_ARCHITECTURE.md`, `scripts/product_surface_audit.py`,
  `tests/integration/test_g18a_product_surfaces.py` (3 tests) + reports.
- Checkpoint: `g18a: product surface information architecture & server-truth contract`.

## 2026-08-14 ? G18B PASS (M15 phase)

- Added `wanxiang_api/studio_service.py` (diagnose/replay/diff/admin-gated debug + audit),
  `tests/integration/test_g18b_studio_ide.py` (3 tests) + reports.
- Checkpoint: `g18b: studio / world ide completion`.

## 2026-08-14 ? G18C PASS (M15 phase)

- Added `wanxiang_api/experience_player_service.py` (session/projection/revision-aware act/resync),
  `tests/integration/test_g18c_experience_player.py` (4 tests) + reports.
- Checkpoint: `g18c: experience player web/2d continuity completion`.

## 2026-08-14 ? G18D PASS (M15 phase)

- Added `wanxiang_api/strategy_workbench_service.py` (deterministic experiment runs + arbitration),
  `tests/integration/test_g18d_strategy_workbench.py` (3 tests) + reports.
- Checkpoint: `g18d: strategy / experiment workbench completion`.

## 2026-08-14 ? G18E PASS (M15 phase)

- Added `wanxiang_api/family_portal_service.py` (rights-filtered family views + GEDCOM export),
  `tests/integration/test_g18e_family_portal.py` (3 tests) + reports.
- Checkpoint: `g18e: family portal completion`.

## 2026-08-14 ? G18F PASS (M15 phase)

- Added `wanxiang_api/heritage_workbench_service.py` (object view, curator-gated export, conservation history),
  `tests/integration/test_g18f_heritage_workbench.py` (3 tests) + reports.
- Checkpoint: `g18f: heritage / museum workbench completion`.
