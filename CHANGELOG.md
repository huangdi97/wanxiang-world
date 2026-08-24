# Changelog ? Wanxiang Engineering Program

## 2026-08-16 ? GitHub public delivery (v5.3.0-rc1)

- Published `huangdi97/wanxiang-world` PUBLIC (origin remote, master pushed,
  remote SHA == local HEAD 7b0674c).
- GitHub Actions CI green on the pushed branch (6 jobs; run 31942590763).
- Tag `v5.3.0-rc1` + GitHub Release created.
- Added Apache-2.0 LICENSE, NOTICE, README_EN, CONTRIBUTING, SECURITY,
  CODE_OF_CONDUCT, DATA_AND_ASSET_RIGHTS; refreshed README; expanded CI.
- CI-driven fixes: pnpm version pin, secret-scan fixture false positive,
  canonical (CRLF-normalized) v5.2 baseline hashes, migration round-trip URL
  pin, live PG profile migration + psycopg2 driver, TS op count 10->17.
- Committed user-prepared v5.3 M43-M50 planning docs as planning material
  (not qualified). Report: reports/GITHUB_DELIVERY_REPORT.md.

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

## 2026-08-14 ? G18G PASS (M15 phase)

- Added `wanxiang_api/learn_service.py` (challenge discovery, evidence-backed capability deltas, biography),
  `tests/integration/test_g18g_learn_challenge.py` (3 tests) + reports.
- Checkpoint: `g18g: learn / challenge experience completion`.

## 2026-08-14 ? G18H PASS + M15 PASS (M15 gate)

- Added `wanxiang_api/operator_console_service.py` + `tests/integration/test_g18h_operator_console.py` (3 tests)
  + product-surface qualification + M15 acceptance reports.
- M15 gate PASS: G18A-H suites (25 passed), full gate 579 passed + 1 EXTERNAL_BLOCKED skip.
- Checkpoint: `g18h: operator/admin/source/rights/evaluation console & m15 qualification`. M16 begins next.

## 2026-08-14 ? G19A PASS (M16 phase)

- Added `packages/research/` (wanxiang_research experimental namespace, feature flags OFF, experiment registry),
  `docs/RESEARCH_GOVERNANCE.md`, `tests/integration/test_g19a_research_flags.py` (3 tests), M16 baseline + reports.
- Checkpoint: `g19a: research namespace, feature flags, benchmarks & promotion rules`.

## 2026-08-14 ? G19B PASS (M16 phase)

- Added `wanxiang_research/ai_compiler.py` (extraction schema, provider Port, deterministic fixture,
  SemanticExtractor + review_diff), `tests/integration/test_g19b_ai_compiler.py` (4 tests) + research report.
- Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19b: ai-assisted world compiler semantic extraction research`.

## 2026-08-14 ? G19C PASS (M16 phase)

- Added `wanxiang_research/persona_memory.py` (MemoryStore, compaction, PersonaDrift),
  `tests/integration/test_g19c_persona_memory.py` (3 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19c: long-horizon persona, memory metabolism & drift evaluation research`.

## 2026-08-14 ? G19D PASS (M16 phase)

- Added `wanxiang_research/cognitive_lod.py` (tiered LOD + event wakeups),
  `tests/integration/test_g19d_cognitive_lod.py` (3 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19d: cognitive lod & large-population scheduling research`.

## 2026-08-14 ? G19E PASS (M16 phase)

- Added `wanxiang_research/planner.py` (Planner Port, HeuristicPlanner, validate/rollout),
  `tests/integration/test_g19e_planner.py` (3 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19e: world-model / planner proposal engine research`.

## 2026-08-14 - G19F PASS (M16 phase)

- Added `wanxiang_research/generative_assets.py` (AssetManifest, AssetFoundryPipeline, SceneProjector; semantic binding to entity/package/revision + rights/provenance; regeneration versions instead of overwriting; explicit fallback markers), `tests/integration/test_g19f_generative_assets.py` (5 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19f: generative asset / scene pipeline & semantic binding research`.

## 2026-08-14 - G19G PASS (M16 phase)

- Added `wanxiang_research/digital_human.py` (AvatarIdentity, Utterance, PresenceGateway, DeterministicTextAvatar, LatencyProbe; rights-first presence routing, provider outage fallback, interruption, latency/ordering measurement, command-payload utterances), `tests/integration/test_g19g_digital_human.py` (7 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19g: advanced digital human / xr presence research`.

## 2026-08-14 - G19H PASS (M16 phase)

- Added `wanxiang_research/sim_federation.py` (SimulatorAdapter Port, deterministic Tick/Precise/Flaky simulators, FederationScheduler with checkpoint/restore, ConflictResolver with explicit precedence, FederationCoordinator/CommitProposal), `tests/integration/test_g19h_sim_federation.py` (7 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19h: multi-simulator federation & co-simulation research`.

## 2026-08-14 - G19I PASS (M16 phase)

- Added `wanxiang_research/reality_stream.py` (SensorReading, SyntheticSensorStream, StreamIngestor with dedupe/skew/staleness, ObservationLog, ObservationFusion, RealityReplay), `tests/integration/test_g19i_reality_stream.py` (8 tests) + research report. Decision: KEEP_EXPERIMENTAL.
- Checkpoint: `g19i: reality/digital-twin streaming & observation fusion research`.

## 2026-08-14 - G19J + M16 PASS (research expansion)

- Added `wanxiang_research/distributed_host.py` (partition_for, LeaseRegistry/LeaderElection single-writer leases, OrderedChannel idempotent delivery, PartitionCache, HostBenchmark), `tests/integration/test_g19j_distributed_host.py` (6 tests) + research/milestone reports (M16_ACCEPTANCE, M16_RESEARCH_EXPANSION_QUALIFICATION).
- M16 gate PASS: 628 pytest + 1 EXTERNAL_BLOCKED skip, ruff/pyright/architecture PASS. Decision: 9 tracks KEEP_EXPERIMENTAL; distributed hosting REJECTED for promotion (2.2x overhead, no correctness gain) - modular monolith stays stable default. ADR 0055.
- Checkpoint: `g19j: distributed world host / sharding experiment & m16 research qualification`; tag `m16-research-expansion`.

## 2026-08-14 - G20A PASS (M17 phase)

- Regenerated design traceability from source; added `reports/FINAL_DESIGN_TRACEABILITY.md` + `reports/final_design_traceability.json`. Closure: 44 requirements (42 VERIFIED, 2 EXTERNAL_BLOCKED, 0 GAP), 16 kernels, 63 goals. External blockers narrow (real renderers/XR; real licensed source data). M16 research tracks remain experimental, not v5.0 requirements.
- Checkpoint: `g20a: final mother-spec traceability & requirement closure`.

## 2026-08-14 - G20B PASS (M17 phase)

- Added `scripts/clean_room_certify.py` (automated 7-step clean-room certification) + `reports/CLEAN_ROOM_CERTIFICATION.md` + `tests/integration/test_g20b_clean_room.py` (5 tests). All steps PASS: clean tree, reproducible release manifest (sha==HEAD), 0001->head migration, golden replay hash, backup/restore round-trip, external sample pack, reference world install+instantiate.
- Checkpoint: `g20b: clean-room build, install, upgrade, restore & replay certification`.

## 2026-08-14 - G20C PASS (M17 phase)

- Added `scripts/security_reliability_certify.py` (curated security/chaos re-run + all-flags-ON stable check) + `reports/FINAL_SECURITY_RELIABILITY_CERTIFICATION.md` + `tests/integration/test_g20c_security_reliability.py` (3 tests). Curated suite: 65 passed, 0 failed, 0 skipped; golden replay hash identical with all 7 research flags enabled.
- Checkpoint: `g20c: final independent security, reliability & chaos re-run`.

## 2026-08-14 - G20D PASS (M17 phase)

- Added `scripts/blackbox_final_acceptance.py` (4-persona black-box acceptance: author, operator, end user, surfaces) + `reports/BLACKBOX_FINAL_ACCEPTANCE.md` + `tests/integration/test_g20d_blackbox_acceptance.py` (4 tests). All personas PASS via public SDK/API only; no internal imports or DB edits.
- Checkpoint: `g20d: black-box external author + reference world final acceptance`.

## 2026-08-14 - G20E PASS + M17 (final certification; program complete)

- Added `docs/RELEASE_READINESS.md`, `docs/POST_V5_ROADMAP.md`, `reports/FINAL_PROGRAM_COMPLETION_REPORT.md`, `reports/M17_FINAL_CERTIFICATION.md`, `reports/G20E_REPORT.md`.
- Final gate: 640 pytest + 1 EXTERNAL_BLOCKED skip; ruff/pyright/architecture PASS; TS SDK 22 tests; PACK_MANIFEST 94/94 verified.
- Fixed release-blocking regression: pytest collected clean-room scratch files (tests/_arch_tmp) - added pytest `norecursedirs` + best-effort cleanup in scripts/clean_room_certify.py.
- Version freeze proposal `v5.0-R1-rc1`; release tag NOT created (awaits user authorization); nothing pushed/deployed. Local checkpoint tag `m17-final-certification`.
- Checkpoint: `g20e: final release readiness, version freeze & post-v5 roadmap`.

## 2026-08-14 - V5.1 G21A PASS (M18 phase)

- Committed the v5.1-R1 program pack (README_FIRST_V5_1, program docs 00-09, docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md, goals/GOAL_G21A..G28I, milestones/M18..M25) as part of the baseline checkpoint so the program is reproducible from a single commit.
- Added `scripts/v51_metrics.py` (deterministic code-minimality metrics), `reports/V5_1_PRE_MIGRATION_BASELINE.md` (freeze: HEAD 436ee3d, 640+1 quality gate, golden replay hash 7d17aba7..., fixture sha256 C158F47D..., migration head 0002), `reports/V5_1_CODE_MINIMALITY_LEDGER.md`, `reports/V5_1_TRACEABILITY_MATRIX.md`.
- M17 baseline re-verified reproducibly: `uv run python scripts/quality.py` -> ruff/pyright/architecture PASS, 640 passed + 1 EXTERNAL_BLOCKED skip; golden replay narrow regression 26 passed. No production code changed.
- Checkpoint: `v5.1 g21a: v5.0/m17 baseline freeze & repository inventory`.

## 2026-08-14 - V5.1 G21B PASS (M18 phase)

- Built `reports/V5_1_TRACEABILITY_MATRIX.md`: 37 v5.1 deltas classified (D01-D37) with owner/evidence/action; no REPLACE without ADR; MERGE only for runtime registries (forensics first).
- Added `tests/architecture/test_v51_traceability.py` (4 completeness checks) -> 4 passed.
- Key decisions: RuntimeControlTransaction is ADD-only (never a World Commit); Ontology/Law commits are ADAPT through the single authority pipeline; evidence/model_providers stub packages are DELETE candidates; M16 research stays EXPERIMENTAL.
- Checkpoint: `v5.1 g21b: v5.1 delta traceability & existing-code classification`.

## 2026-08-14 - V5.1 G21C PASS (M18 phase)

- Added `scripts/v51_forensics.py` (deterministic AST scan) + `reports/V5_1_DUPLICATE_FORENSICS.md` (10 registries, 18 state models, 16 stores, 15 services, 2 engines, 23 ports, 0 oversized modules, 1 commit path) + dispositions.
- Confirmed exactly one CommitAuthority commit path; capability `_apply_delta` produces proposals only.
- Strong MERGE candidate found: duplicate SnapshotStore/InMemorySnapshotStore in runtime vs recovery.checkpoint (consolidate in G21F/G21G).
- Checkpoint: `v5.1 g21c: duplicate abstraction, registry, state & manager forensics`.

## 2026-08-14 - V5.1 G21D PASS (M18 phase)

- Added `scripts/v51_dependency_graph.py` + `reports/V5_1_PACKAGE_DEPENDENCY_GRAPH.md` + `docs/architecture/V5_1_PHYSICAL_PACKAGE_MAPPING.md` (16-kernel -> physical-package mapping) + `tests/architecture/test_v51_dependency_topology.py` (golden edge set pinned).
- Topology verified acyclic: domain -> runtime -> application/persistence -> substrate -> apps/api; no cycles; forbidden imports already enforced.
- P2 finding: five substrate modules import application.WorldRuntime (substrate->application inversion); planned minimal fix via WorldRuntimePort (G21F/G25B).
- Checkpoint: `v5.1 g21d: dependency graph & physical package simplification plan`.


## 2026-08-14 - V5.2 G29A PASS (M26 phase)

- Committed the v5.2-R1 program pack (README_FIRST_V5_2_CN, program docs 00-10, docs/spec/WANXIANG_v5_2_MASTER_SPEC.md, goals/G29A..G37G, milestones/M26..M34, ALL_IN_ONE ??) as part of the baseline checkpoint for single-commit reproducibility.
- M25 real state verified: `uv run python scripts/quality.py` -> ruff/format/pyright/architecture PASS, 649 passed + 1 EXTERNAL_BLOCKED skip (live PostgreSQL). Pre-existing failures fixed: BOM ruff panic (test_v51_forensics.py), v51_metrics.py pyright strict, corrupted guard scripts from the v5.2 prep edit.
- Deleted empty stub packages `packages/evidence` + `packages/model_providers` (zero call sites; v5.1 G21B/G21D DELETE disposition) and removed all references (pyproject, guards, golden edges, bootstrap, uv.lock).
- Frozen deterministic golden fixtures `tests/fixtures/v5_2_baseline/` (events/snapshot/branch/worldpack/api/manifest; combined hash `f27b77249f14c6ef5b8b1b10689e69659e9405d6ccf6f0c75d3f4be952c47ecf`) + generator script + 6-test reproducibility guard.
- Baseline audit: 263 files / 21,822 LOC; 11 registries, 0 managers, 15 services, 3 engines; migration head 0002 unchanged.
- Checkpoint: `g29a: ???????? M25 ????`.


## 2026-08-14 - V5.2 G29B PASS (M26 phase)

- Produced `reports/V5_2_CODE_DISPOSITION_ACTUAL.md`: actual inventory of 8 packages + apps/api + 2 migrations + 164 test files + 29 scripts; all duplicates classified with call-site evidence (11 registries KEEP, 18 state models, 16 stores, 15 services, 3 engines, 23 ports).
- Confirmed exactly one commit path; no unused port; no world-specific leakage into domain/runtime Core.
- DELETE stubs (evidence/model_providers) already removed in G29A; single MERGE candidate identified: substrate recovery snapshot store -> runtime SnapshotStore port (G29C).
- Checkpoint: `g29b: ??????????`.


## 2026-08-14 - V5.2 G29C PASS (M26 phase)

- Merged duplicate recovery snapshot store into the single runtime SnapshotStore port (`CheckpointStore` adapter + deprecated `InMemorySnapshotStore` alias; removed recovery-local `SnapshotStore` Protocol). store_classes 16->15, ports 23->22, commit_paths stays 1.
- Confirmed no global service locator exists; no new global mutable registry; no Manager duplicates (0 Managers).
- Added adapter-semantics + deprecation-alias tests; 32-test targeted regression green.
- Checkpoint: `g29c: ???? Registry ? Manager`.


## 2026-08-14 - V5.2 G29D PASS (M26 phase)

- Verified State/Event/Audit derivation: events authoritative, snapshots cache, audit reference view; no second state table; no route/provider ORM writes (guard-enforced).
- Added 2 integration tests: drop-all-derived-state rebuild (same semantic hash) and audit-references-events (no delta duplication, deleting audit doesn't change replay hash).
- Checkpoint: `g29d: ?? State Event Audit ????`.


## 2026-08-14 - V5.2 G29E PASS (M26 phase)

- ADR 0064: v5.2 dependency direction (domain -> runtime -> application/persistence -> substrate -> apps/api; Kernel never depends on Runtime/Forge/Web/ORM; World content never in Kernel).
- Resolved the P2 substrate->application inversion: new consumer-owned `wanxiang_substrate.runtime_port.WorldRuntimePort` (current_state/submit_command/events); five substrate modules (host/queue/scheduler/skills/lifecycle) now use the port; zero `wanxiang_application` imports left in substrate; golden topology + graph + forensics regenerated.
- Checkpoint: `g29e: ???????`.


## 2026-08-14/15 - V5.2 G29F PASS (M26 phase)

- Extended false_completion_scan with empty-body + static-success AST scans; scan clean: placeholders=0 dead=0 empty=0 static=2 (documented) hardcoded=10 (schema maps).
- Classified all fake-named production classes as deterministic reference implementations (KEEP); research flags all OFF, distributed_host marked REJECTED (ADR 0055).
- Checkpoint: `g29f: ?? Fake Placeholder ??????`.


## 2026-08-15 - V5.2 G29G PASS (M26 phase)

- Added `scripts/v52_minimality_budget.py` (repeatable budget: LOC/files/classes/functions, registries/managers/services/engines/ports/stores/schema models, cycles, commit paths) + `reports/V5_2_MINIMALITY_BUDGET.md` + JSON; M27-M34 incremental budget table (no absolute LOC cap).
- Refactored `scripts/v51_metrics.py` to expose reusable `compute_metrics()` (behavior unchanged).
- Added 3 reproducibility tests. M26 snapshot: 264 files / 21,901 LOC / 10 registries / 0 managers / 15 services / 2 engines / 23 ports / 0 cycles / 1 commit path.
- Checkpoint: `g29g: ???????????`.


## 2026-08-15 - V5.2 G29H PASS + M26 GATE PASS

- Ran the full M26 milestone gate: `uv run python scripts/quality.py` -> 664 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS.
- Fixed gate FAILs: WorldRuntimePort.submit_command param renamed for pyright protocol match; SnapshotStore deprecated alias restored (API compat); SDK baseline regenerated (non-breaking additions).
- M26 = PASS (reports/M26_QUALIFICATION.md). Architecture map + baseline hash frozen (f27b7724...). Commit: `g29h: M26 ??????`.


## 2026-08-15 - V5.2 G30A PASS (M27 phase)

- Added `wanxiang_domain.reality_root` (REALITY_ROOT_SEMANTICS + RealityRootContract Protocol) mapping Distinction/Relation/Transition/Commitment/History onto existing core contracts; no domain rules; exported in domain __init__.
- 7 contract tests (minimal synthetic world via the contract; single authority boundary; append-only deterministic history).
- Checkpoint: `g30a: Reality Root ????`.


## 2026-08-15 - V5.2 G30B PASS (M27 phase)

- Added `wanxiang_domain.constitution`: ConstitutionId/ConstitutionVersion/ConstitutionManifest (immutable roots vs mutable law layers), ROOT_CONSTITUTION (platform, no self-amendment), legacy_default_constitution() (v5.0/v5.1 compat), order-preserving primitive round-trip.
- 5 tests: schema round-trip, no shared mutable objects, legacy compat, root immutability, world-definition binding.
- Checkpoint: `g30b: World Constitution ?????`.


## 2026-08-15 - V5.2 G30C PASS (M27 phase)

- Wired constitution enforcement into the runtime Invariant Registry: protected platform identities (sys_reality_root/sys_commit_boundary/sys_commit_authority/sys_constitution) cannot be mutated or related to by world deltas; kernel invariants always run (priority) and cannot be overridden.
- Added ConstitutionViolation error + 7 tests (rejection with no state mutation; kernel priority; normal deltas not blocked).
- Checkpoint: `g30c: Constitution ???????`.


## 2026-08-15 - V5.2 G30D PASS (M27 phase)

- Added `wanxiang_domain.world_isa`: 8-instruction typed ISA (WorldIsaOp) with version/schema round-trip; DECLARE/ASSERT/RETRACT/PROPOSE reduce to existing deltas; VALIDATE/COMMIT/FORK/PROMOTE map to use cases; no DB write; business actions stay upper.
- 10 tests (unknown version/instruction fail; reductions; no DB import).
- Checkpoint: `g30d: World Semantic ISA ????`.


## 2026-08-15 - V5.2 G30E PASS (M27 phase)

- Added `wanxiang_runtime.isa_pipeline.execute_isa`: ISA instructions execute through the existing CommitAuthority/fork_branch/validation pipeline; PROMOTE emits PromotionUseCase only (parent untouched). 5 tests incl. ISA-vs-business-action semantic parity and no-second-stream.
- Checkpoint: `g30e: ISA ?????? Commit ????`.


## 2026-08-15 - V5.2 G30F PASS (M27 phase)

- Unified World Commit kinds (state/ontology/law) on CommitRequest with delta_schema_version; kind validated before commit and recorded on AuditRecord; "capability" rejected.
- Added RuntimeControlTransaction + RuntimeControlLedger (substrate capability): runtime control changes are NOT World Commits (never enter event stream).
- 5 tests; 67-test regression green.
- Checkpoint: `g30f: ?? World Commit ??`.


## 2026-08-15 - V5.2 G30G PASS (M27 phase)

- Added FactScopePolicy (canonical/public/org/actor/hypothesis/reconstruction) with write-authority partition, commit-required canonical promotion, and projection visibility filtering; ProjectionService filters ledger.fact entities by scope/rights.
- 5 tests (no belief->canonical by scope edit; no cross-role leak; admin override).
- Checkpoint: `g30g: Fact Scope ? Authority Partition`.


## 2026-08-15 - V5.2 G30H PASS (M27 phase)

- Added version_context module: VersionContext (constitution/semantic/law/domain/runtime), immutable revision log, legacy adapter for v5.0/v5.1 events, SnapshotVersionContext freeze. Golden v5.1 replay hash unchanged; replay deterministic across Law/Ontology evolution.
- 6 tests.
- Checkpoint: `g30h: Event Snapshot ???????`.


## 2026-08-15 - V5.2 G30I PASS + M27 GATE PASS

- Full M27 gate: 714 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS; commit_paths 1; old replay hash unchanged.
- Fixed 3 M27-test quality nits (B017 blind exception asserts, errors.py blank lines) surfaced by full regression; budget anchor updated (ports 24).
- M27 = PASS (reports/M27_QUALIFICATION.md). Commit: `g30i: M27 Root Constitution ISA ????`.


## 2026-08-15 - V5.2 G31A PASS (M28 phase)

- Added worldline identity model: WorldDefinition (read-only versioned), WorldlineIdentity, InstanceIdentity (definition/genesis/constitution/runtime refs), WorldlineFork (branch fork == worldline fork over BranchAncestry).
- 4 tests (definition immutable; WorldPack unchanged by running; fork round-trip; instance identity).
- Checkpoint: `g31a: World Definition ? Worldline ????`.


## 2026-08-15 - V5.2 G31B PASS (M28 phase)

- Added lineage package: LineageNode/LineageEdge/LineageGraph (DAG with cycle rejection, ancestors/descendants/common-ancestors, versions/rights/provenance refs; no history copies).
- 5 tests (tree/DAG fixtures, cycle + duplicate rejection).
- Checkpoint: `g31b: World Lineage Graph ????`.


## 2026-08-15 - V5.2 G31C PASS (M28 phase)

- Migration 0003_add_lineage (lineage_nodes/edges, downgrade-safe); LineageRepository (save/load graph); branch lineage derived from the existing branches table (no duplication).
- 5 migration tests (fresh upgrade, old-DB upgrade keeps replay hash, downgrade, repository round-trip, branch-lineage derivation).
- Checkpoint: `g31c: Lineage Repository ???`.


## 2026-08-15 - V5.2 G31D PASS (M28 phase)

- Added WorldHypervisor over the existing WorldHost/HostRegistry: instance/worldline routing, per-instance ResourceBudget + RuntimeProfile binding, route verification on every command.
- 3 integration tests (same-ID isolation, interleaved routing, budget enforcement).
- Checkpoint: `g31d: World Hypervisor ?????`.


## 2026-08-15 - V5.2 G31E PASS (M28 phase)

- Added OriginIdentity/PresenceRef/PresenceRegistry: explicit presence + translation/sync policies; no implicit cross-world write-back; identity conflicts rejected unless mapped.
- 4 tests.
- Checkpoint: `g31e: Interworld Identity ? Presence`.


## 2026-08-15 - V5.2 G31F PASS (M28 phase)

- Added hybrid-genesis compatibility analysis: 6 semantic checks, MergePlan candidate or rejection (no fake git-merge, no auto-resolve); parent histories never rewritten.
- 5 tests.
- Checkpoint: `g31f: Hybrid Genesis ??????????`.


## 2026-08-15 - V5.2 G31G PASS (M28 phase)

- Added GET-only lineage API (ancestors/descendants/promotion-origin), regenerated OpenAPI SDK contract (13 routes, drift green), Studio read-only lineage projection.
- 2 API contract tests (queries + read-only surface).
- Checkpoint: `g31g: Lineage API SDK Studio ????`.


## 2026-08-15 - V5.2 G31H PASS + M28 GATE PASS

- Full M28 gate: 747 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS.
- Fixed persistence->substrate inversion by moving lineage graph to domain (substrate re-exports); updated migration-head constants (0003) across release_build/clean_room_certify/tests; budget anchor registries 11.
- Generated deterministic lineage fixture + mermaid visualization; added parent-isolation + multi-instance replay tests.
- M28 = PASS (reports/M28_QUALIFICATION.md). Commit: `g31h: M28 Lineage Hypervisor ????`.


## 2026-08-15 - V5.2 G32A PASS (M29 phase)

- Added evolution policy stack: versioned WorldPolicy (actor/capability/social/institution/ontology/law/promotion) + PlatformPolicy (model/plugin/domain/runtime/constitution) with independent permissions and traceable versions.
- 3 tests.
- Checkpoint: `g32a: Evolution Policy Stack`.


## 2026-08-15 - V5.2 G32B PASS (M29 phase)

- Added multi-scale evolution scheduler (actor/relation/group/institution/world cadences; modular activation, no full scans, linear long-run growth, deterministic).
- 4 tests.
- Checkpoint: `g32b: ???????`.


## 2026-08-15 - V5.2 G32C PASS (M29 phase)

- Added ActorEvolutionTracker with separated capability (reuses CapabilityDelta) and persona (explicit PersonaDelta) channels + trajectory provenance; skill gain never changes persona hash.
- 4 tests.
- Checkpoint: `g32c: Actor Capability ? Persona ????`.


## 2026-08-15 - V5.2 G32D PASS (M29 phase)

- Added SocialPatternDistiller: windowed relation/group/norm pattern detection -> CandidateEnvelope (threshold-gated, origin/provenance); never writes Canon.
- 4 tests.
- Checkpoint: `g32d: Relation Group Social Pattern Distillation`.


## 2026-08-15 - V5.2 G32E PASS (M29 phase)

- Added InstitutionPromotionChain: candidate evidence -> stability validation -> human/policy approval -> LawCommit (kind=law); unapproved candidates never change Gamma; LawCommits replayable.
- 4 tests.
- Checkpoint: `g32e: Institution Organization Rule ??`.


## 2026-08-15 - V5.2 G32F PASS (M29 phase)

- Added OntologyCandidate/LawCandidate + OntologyLawEvolution validation against constitution mutable layers and policy (no permission escalation); branch-local ontology/law never pollutes parent.
- 3 tests.
- Checkpoint: `g32f: Ontology Law ?????`.


## 2026-08-15 - V5.2 G32G PASS (M29 phase)

- Added telemetry envelope + policy (opt-in consent, trajectory rights/retention) + revocable cross-world dataset.
- 3 tests.
- Checkpoint: `g32g: Evolution Telemetry ?????`.


## 2026-08-15 - V5.2 G32H PASS + M29 GATE PASS

- Full M29 gate: 774 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS.
- Added synthetic society long-run test (habit->norm->institution controlled chain; no auto gate-crossing; replay/branch deterministic); documented the structural static-success guard; M28 test switched to set comparison.
- M29 = PASS (reports/M29_QUALIFICATION.md). Commit: `g32h: M29 ??????????`.


## 2026-08-15 - V5.2 G33A PASS (M30 phase)

- Added promotion ladder (L0-L8): level requirements (evidence/stability/cross-scenario/approval), one-step-at-a-time, L7/L8 explicit approval, versioned policy.
- 4 tests.
- Checkpoint: `g33a: ?? Abstraction Ladder`.


## 2026-08-15 - M35-M42 program start (G38A audit)

- Committed the M35-M42 program pack (README_FIRST, 00-08 program docs, CODEX_COPY_PASTE_M35_M42_CN.txt, WANXIANG_M35_M42_ALL_IN_ONE_CN.md, goals/G38A..G45H, milestones/M35..M42, PACK_MANIFEST/README updates).
- G38A independent M34 audit: full quality gate 778 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS; golden samples frozen (baseline f27b7724..., replay 7d17aba7..., lineage fixture, migration head 0003). Finding: **M34 NOT complete** (v5.2 M30-M34 pending).
- Checkpoint: `g38a: ???? M34`.


## 2026-08-15 - V5.2 G33B PASS (M30 phase, remediation)

- Added WorldlinePromotionPipeline (distill -> Source/Rights/Invariant review -> freeze GenesisSnapshot -> assemble new WorldDefinition id -> record promotion lineage edge); parent definition/source worldline never mutated; derived world re-instantiable.
- 4 tests.
- Checkpoint: `g33b: Worldline ? Derived World Promotion Pipeline`.


## 2026-08-15 - V5.2 G33C PASS (M30 phase, remediation)

- Added PromotionControlLedger (append-only, replayable); withdrawal only changes derived-definition installability/registry status; source history never deleted; parent replay unchanged.
- 3 tests.
- Checkpoint: `g33c: Promotion ?????????`.


## 2026-08-15 - V5.2 G33D PASS (M30 phase, remediation)

- Added CrossWorldDistiller over the authorized telemetry dataset: cross-world pattern discovery with anonymized world origins; candidates never auto-activate (explicit approval).
- 3 tests.
- Checkpoint: `g33d: Cross-world Distillation`.


## 2026-08-15 - V5.2 G33E PASS (M30 phase, remediation)

- Added PlatformFeedbackLab: sandbox gate (benchmark/invariant/security/cost/determinism), platform-only approval, versioned Domain/Runtime release; rollback status-only (events never rewritten).
- 3 tests.
- Checkpoint: `g33e: ???? Sandbox Benchmark Approval`.


## 2026-08-15 - V5.2 G33F PASS (M30 phase, remediation)

- Added promotion/lineage API (promotion-candidates, admin-gated promotions, lineage compare) + Studio candidate/approval/lineage-diff views; OpenAPI regenerated (16 routes).
- 5 tests (403 unauthorized, backend-authority UI action, compare, SDK contract).
- Checkpoint: `g33f: Lineage ? Promotion API Studio`.


## 2026-08-15 - V5.2 G33G PASS + M30 GATE PASS

- Full M30 gate: 798 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS.
- Added synthetic promotion + cross-world candidate e2e test; lineage read-only test updated for admin-gated promotions POST.
- M30 = PASS (reports/M30_QUALIFICATION.md). Commit: `g33g: M30 Promotion Cross-world ????`.


## 2026-08-15 - V5.2 G34A PASS (M31 phase, remediation)

- Documented final Kernel/Runtime/Forge/Experiences responsibility boundaries + import rules + No-God-Engine rule; added conformance test (Kernel import isolation, engine set pinned).
- 3 tests.
- Checkpoint: `g34a: Kernel Runtime Forge Experiences ????`.


## 2026-08-15 - V5.2 G34B PASS (M31 phase, remediation)

- WorldPack Definition schema v5.2: added optional constitution/genesis/evolution/lineage refs (canonical includes only when set -> legacy hashes preserved); extended the existing packages/migration.py with v2->v3 + migrate_to_v52 (idempotent); added wxpack migrate CLI.
- 4 tests; 135-test package/baseline regression green; golden worldpack hash unchanged.
- Checkpoint: `g34b: WorldPack Definition schema v5.2 迁移`.


## 2026-08-15 - V5.2 G34C PASS (M31 phase, remediation)

- Migration 0004_add_world_metadata: world_instances definition/constitution/evolution refs + lineage kind index; downgrade restores old schema.
- 3 tests (old-DB upgrade keeps count/hash, downgrade, backup/restore path); 11 migration tests green.
- Checkpoint: `g34c: 数据库与 Ledger 兼容迁移`.


## 2026-08-15 - V5.2 G34D PASS (M31 phase, remediation)

- Backward-replay verification against M26 golden fixtures: old snapshot restore, old events replay, old branch fork under v5.2 (parent unchanged); new fields via legacy defaults; semantic hashes match baseline; no data-clearing.
- 4 tests.
- Checkpoint: `g34d: 旧 Event Snapshot Branch 向后回放`.


## 2026-08-15 - V5.2 G34E PASS (M31 phase, remediation)

- Added constitution API endpoint + TS SDK client; regenerated OpenAPI (17 routes); old world/branch endpoints preserved (no breaking removal); old-client smoke test.
- 3 tests.
- Checkpoint: `g34e: API SDK Client 兼容`.


## 2026-08-15 - V5.2 G34F PASS (M31 phase, remediation)

- Extended benchmarks.py with lineage query; added 4 performance/complexity regression tests (commit/replay/tick/lineage bounds + determinism). replay 1200 ev ~35ms, lineage 400-node ~23ms.
- Checkpoint: `g34f: 性能与复杂度回归`.


## 2026-08-15 - V5.2 G34G PASS + M31 GATE PASS

- Full M31 gate: 819 passed + 1 EXTERNAL_BLOCKED skip; ruff/format/pyright/architecture PASS.
- Fixed migration-head constants (0004) and isolated the shared action rate-limiter for API smoke tests (public reset helper).
- Generated V5_2_BACKWARD_COMPATIBILITY.md + M31_QUALIFICATION.md.
- M31 = PASS. Commit: `g34g: M31 全平台兼容资格验收`.


## 2026-08-15 - V5.2 G35A EXTERNAL_BLOCKED (M32 phase, remediation)

- Real《红楼梦》full-text source EXTERNAL_BLOCKED (no legal/traceable edition in env; read-only + no network/rights verification); no model-memory canon. Registered exact missing needs in reports/RED_CHAMBER_SOURCE_GATE.md.
- Source registration mechanism verified with a synthetic fixture (3 tests: checksum reproducible, rights/review non-empty, no fabricated canon).
- Checkpoint: `g35a: 红楼梦来源策略与合法版本登记`.


## 2026-08-15 - V5.2 G35B PASS (M32 phase, remediation; mechanism)

- Added chapter/segment SourceLocator (read-only segmentation, offsets + chapter ids, back-linkable slices, stable hash); mechanism verified on synthetic corpus; real《红楼梦》text EXTERNAL_BLOCKED (G35A).
- 4 tests.
- Checkpoint: `g35b: 章节分段与可引用 Source Locator`.

## 2026-08-15 ? G35C PASS (M32)

- Identity/alias distillation: pure `IdentityDistiller` (segment -> mention -> identity key)
  + evidence-backed `AliasClaim` (G35B locators) + `IdentityReviewGate` (human/rule;
  no-evidence/unresolvable-locator/unauthorized reviewers rejected).
- `identity_to_claim()` bridges approved identities into the G04B ClaimCandidate/
  EvidenceLink pipeline; no second registry/engine/claim model.
- SDK baseline: routes=17 ts=5 py=965 (additive). 7 new unit tests PASS;
  architecture conformance PASS; ruff/pyright clean.
- Real《红楼梦》text remains EXTERNAL_BLOCKED (G35A); mechanism verified on
  synthetic corpus only.
- Checkpoint: `g35c: 人物与别名 Identity Distillation`.

## 2026-08-15 ? G35D PASS (M32)

- Place/object/organization + topology distillation: `EntityDistiller` (pure) + `EntityConnection`
  + `EntityReviewGate`; unverifiable details route to Completion (completion_notes never evidence).
- Shared `evidence_ok()` extracted (G35C IdentityReviewGate ADAPTED, behavior unchanged) so evidence
  rules never drift between gates.
- SDK baseline: routes=17 ts=5 py=979 (additive). 8 new unit tests PASS; architecture PASS;
  ruff/pyright clean. Real《红楼梦》text remains EXTERNAL_BLOCKED (G35A).
- Checkpoint: `g35d: 空间组织物品 Distillation`.

## 2026-08-15 ? G35E PASS (M32)

- Past/Character/Future canon compilation: `CanonCompiler` + `CompiledCanon`;
  FutureCanon is control-plane-only (runtime_view never contains future claims);
  per-character canon via character_canon(key).
- SDK baseline: routes=17 ts=5 py=986 (additive). 6 new unit tests PASS; architecture PASS;
  ruff/pyright clean. Real《红楼梦》text remains EXTERNAL_BLOCKED (G35A).
- Checkpoint: `g35e: Past Character Future Canon 编译`.

## 2026-08-15 ? G35F PASS (M32)

- Generic narrative/household domain pack (no RedChamberCore, no Red Chamber proper nouns):
  ritual/visit/letter/message actions+resolvers through Commit Authority; access-gated sick
  visits; sealed letter payloads (material reuse); message relay; duty/access queries.
- SDK baseline: routes=17 ts=5 py=1004 (additive). 6 new unit tests PASS; architecture PASS;
  ruff/pyright clean. Real《红楼梦》text remains EXTERNAL_BLOCKED (G35A).
- Checkpoint: `g35f: Narrative Household HistoricalChina Domain 复用与补齐`.

## 2026-08-15 ? G35G PASS (M32)

- Character relation / knowledge-boundary distillation: CharacterDistiller + CharacterFact/RelationClaim
  + KnowledgeBoundary; private facts of others hidden unless granted; future facts control-plane only;
  Completion/Interpretive separated; anonymized key-choice fixture (identity-agnostic).
- SDK baseline: routes=17 ts=5 py=1012 (additive). 8 new unit tests PASS; architecture PASS;
  ruff/pyright clean. Real《红楼梦》text remains EXTERNAL_BLOCKED (G35A).
- Checkpoint: `g35g: Character Relation Knowledge Boundary Distillation`.

## 2026-08-15 ? G35H PASS (M32)

- Completion ledger review: CompletionRecord (support refs/confidence/review status) + CompletionReviewLedger
  (E0-E5 stage semantics; can_enter_canon default false; E4/E5 terminal) + CompletionStudio + batch CLI.
- SDK baseline: routes=17 ts=5 py=1021 (additive). 9 new unit tests PASS; architecture PASS;
  ruff/pyright clean. Real《红楼梦》text remains EXTERNAL_BLOCKED (G35A).
- Checkpoint: `g35h: Completion Ledger 与审核`.

## 2026-08-15 ? G35I PASS + M32 GATE PASS

- RedChamber WorldPack assembly: WorldPackAssembler + literary_constitution + GenesisSpec +
  HMAC signature/deps; validate/install/export/import + dry-run; no Core hardcode.
- M32 gate: full quality 878 passed + 1 skipped (PostgreSQL EXTERNAL_BLOCKED); architecture PASS;
  routes=17 ts=5 py=1028. MECHANISM PASS - real《红楼梦》corpus remains EXTERNAL_BLOCKED (G35A).
- Checkpoints: `g35i: 编译 RedChamber World Definition 与 Scenario`; M32 gate qualified.

## 2026-08-15 ? G36A PASS (M33)

- RC-001 instantiation: genesis through single Commit Authority, immutable initial snapshot,
  lineage root; synthetic anonymized content (real canon EXTERNAL_BLOCKED).
- Checkpoint: `g36a: 实例化 RC-001 与固定世界快照`.

## 2026-08-15 ? G36B PASS (M33)

- RC-001 spatial run: visibility/acoustic/privacy/access + MovementProfile travel time;
  synthetic anonymized map (real canon EXTERNAL_BLOCKED).
- Checkpoint: `g36b: 红楼梦空间可见可听私密运行`.

## 2026-08-15 ? G36C PASS (M33)

- RC-001 NPC schedule/duty/body/social policy (deterministic daily schedule + population resolution).
- Checkpoint: `g36c: 人物职责 NPC 日程身体与社会制度`.

## 2026-08-15 ? G36D PASS (M33)

- Material/information continuity: read-and-remember (read forms observation memory),
  hide/gift/medicine continuity verified; synthetic objects (real canon EXTERNAL_BLOCKED).
- Checkpoint: `g36d: 信件诗稿礼物药物的物质与信息连续性`.

## 2026-08-15 ? G36E PASS (M33)

- Perception/belief/memory + message propagation (rumour/misunderstanding; future canon isolation).
- Checkpoint: `g36e: Perception Belief Memory 与消息传播`.

## 2026-08-15 ? G36F PASS (M33)

- Embodiment + ShadowPolicy handoff: intent/co-drive/full-control modes, handoff events,
  shadow never decides major (mechanism; no fabricated canon).
- Checkpoint: `g36f: 林霹玉 Embodiment ShadowPolicy Handoff`.

## 2026-08-15 ? G36G PASS (M33)

- Three world strategies: canonical replay / soft canon (attractor) / living open (baseline compare).
- Checkpoint: `g36g: Canonical Replay Soft Canon Living Open 三策略`.

## 2026-08-15 ? G36H PASS (M33)

- Experience Studio minimal surface: map/characters/actions/events/source/completion/branch views.
- Checkpoint: `g36h: 红楼梦 Experience Studio 最小可用面`.

## 2026-08-15 ? M33 GATE PASS

- M33 living-world mechanism qualified: 911 passed + 1 skipped (PostgreSQL EXTERNAL_BLOCKED);
  baseline regenerated (routes=17 ts=5 py=1070); architecture PASS. Real corpus EXTERNAL_BLOCKED.
- Checkpoint: M33 gate qualified.

## 2026-08-15 ? G37A PASS (M34)

- Seven-day automated scenario: deterministic reference run + separate optional LLM run.
- Checkpoint: `g37a: 红楼梦七日场景自动化执行`.

## 2026-08-15 ? G37B PASS (M34)

- Three-worldline generation + comparison (parent hash verified; children never mutate parent).
- Checkpoint: `g37b: Canon 用户 无干预三世界线比较`.

## 2026-08-15 ? G37C PASS (M34)

- Long-horizon evolution + promotion candidate (gate-gated derived world).
- Checkpoint: `g37c: 红楼梦长时演化与 Promotion Candidate`.

## 2026-08-15 ? G37D PASS (M34)

- Replay/crash-recovery/chaos checks (snapshot/restart, corruption, duplicate/stale, reconnect, provider isolation).
- Checkpoint: `g37d: 红楼梦 Replay Crash Recovery Chaos`.

## 2026-08-15 ? G37E-G PASS + M34 GATE PASS (V5_2_PLATFORM_PASS)

- Final minimality/architecture audit; full regression 930 passed + 1 skipped;
  SDK baseline routes=17 ts=5 py=1093.
- Final certification: V5_2_PLATFORM_PASS (RED_CHAMBER_REAL EXTERNAL_BLOCKED until a
  legal, traceable edition is available); local tag v5.2-platform-pass; no push/deploy.
- Checkpoints: `g37e`, `g37f`, `g37g`, M34 gate, tag `v5.2-platform-pass`.

## 2026-08-15 ? G38A PASS (M35)

- G38A re-run: M34 independently verified COMPLETE at platform level (V5_2_PLATFORM_PASS);
  M34 evidence suite 68 passed; goldens reproducible. Real corpus EXTERNAL_BLOCKED.
- Checkpoint: `g38a: 独立复核 M34`.

## 2026-08-15 ? M35 GATE PASS (Kernel v1 freeze)

- Kernel v1 ABI + golden frozen; change guard active; gap audit; minimality; corpus/perf
  baselines; 940 passed + 1 skipped; architecture PASS; kernel_guard 0 violations.
- Tag `m35-kernel-v1-freeze`. Real corpus EXTERNAL_BLOCKED.

## 2026-08-15 ? G39 mechanism PASS (M36)

- Full Corpus -> Canon Graph (scenes/character/source/timeline/canon graphs + coverage/resume).
- Checkpoint: `g39: Full Corpus & Canon Graph (M36 mechanism)`.

## 2026-08-15 ? M36 GATE PASS

- Full-corpus/canon-graph mechanism qualified: 946 passed + 1 skipped; canon_graph
  split for size budget; SDK baseline py=1118. Real corpus EXTERNAL_BLOCKED.
- Checkpoint: M36 gate qualified.

## 2026-08-15 ? M37 GATE PASS

- Full semantic world mechanism qualified: 956 passed + 1 skipped; SDK baseline py=1126;
  Core proper-noun scan empty. Real corpus EXTERNAL_BLOCKED.
- Checkpoint: M37 gate qualified; tag `m37-semantic-world`.

## 2026-08-15 ? M38 GATE PASS

- Full living-runtime mechanism qualified: 963 passed + 1 skipped; SDK baseline py=1140.
  Real corpus EXTERNAL_BLOCKED. Tag `m38-living-world`.

## 2026-08-15 ? M39 GATE PASS

- Studio/Experience mechanism qualified: 968 passed + 1 skipped; SDK baseline py=1152.
  Real corpus EXTERNAL_BLOCKED. Tag `m39-product`.

## 2026-08-15 ? M40 GATE PASS

- Long-horizon/derived-world mechanism qualified: 974 passed + 1 skipped; SDK baseline py=1164.
  Real corpus EXTERNAL_BLOCKED. Tag `m40-long-horizon`.

## 2026-08-15 ? M41 GATE PASS

- Cross-domain generality mechanism qualified: 978 passed + 1 skipped; SDK baseline py=1169.
  External data EXTERNAL_BLOCKED. Tag `m41-generality`.

## 2026-08-15 ? M42 GATE PASS (FINAL)

- v5.2 production release mechanism certified: 982 passed + 1 skipped; SDK baseline
  routes=17 ts=5 py=1176; architecture PASS; kernel_guard 0 violations.
- Final certification: V5_2_PRODUCTION_PASS (RED_CHAMBER_REAL EXTERNAL_BLOCKED).
  Tag `m42-v5.2-production`. No push/deploy; v5.3 not started.

## 2026-08-25 — M57 World Compiler / Package / Preview

- Added the revision-pinned `WorldDraft` compiler boundary and formal world
  package assembly/validation.
- Added deterministic incremental rebuild planning and isolated `preview://`
  installs with package hash checks.
- Added a reference preview runtime that reuses WorldHost and the existing
  Commit Authority; completion gaps remain non-canon metadata and block publish.
- M57 G60A-G60H qualified: targeted tests, Ruff, Pyright, and architecture guard
  passed. Real copyrighted/private sources and optional providers remain out of
  Git and out of this reference qualification.

## 2026-08-25 — M58 Authoring Studio / API / CLI

- Added one deterministic, no-API AuthoringService shared by direct calls, the
  `/studio` API, and `wxworld reference` CLI.
- Added source registration, checkpointed start/cancel/resume, candidate review,
  WorldDraft/package compilation, and isolated preview routes without adding a
  second commit path.
- Qualified G61A-G61H with 19 targeted tests, OpenAPI/SDK baseline refresh,
  Ruff, Pyright, and architecture guard. Missing OCR capability remains an
  explicit `OCR_REQUIRED` failure; private/copyrighted source bytes stay out of
  Git.

## 2026-08-25 — M59 Cross-source E2E / Hardening

- Added Blob-resolver EPUB coverage to the shared no-API source-to-preview
  path, with content-hash verification and pre-ingest archive security.
- Added bounded source chunking, deterministic recovery records, and a
  content/version hash cache for large synthetic inputs.
- Hardened job idempotency so changed bytes cannot silently reuse an existing
  job fingerprint; unreviewed sources remain `REVIEW_REQUIRED` and cannot be
  compiled.
- Qualified G62A-G62H and the M59 gate on synthetic/reference evidence.

## 2026-08-25 — M60 Book-scale Semantic World Understanding

- Extended the shared semantic analyzer with reversible life arcs, temporal
  conflict/unknown views, knowledge graph observations, spatial topology,
  object biographies, institution norms, and explicit quality proxies.
- Attached deterministic semantic metadata to the existing Forge pipeline; no
  Core or Commit Authority path was added.
- Qualified G63A-G63I on a multi-chapter synthetic novel; metrics remain
  reference proxies and real book/private-corpus claims remain blocked by
  provenance and rights boundaries.

## 2026-08-25 — M61 Multi-source / Multi-version Fusion

- Added source-family role/version views, cross-source alignment records,
  explicit provenance relation edges, conflict impact, and preserve-dissent
  policy metadata.
- Added incremental supplemental fusion and rights-compatible candidate views
  without deleting alternatives or adding a second authority.
- Qualified G64A-G64H on deterministic two-version synthetic evidence.

## 2026-08-25 — M62 Multimodal / External Source Ports

- Added explicit OCR, vision, and ASR provider capability failures and
  proposal-only reference behavior.
- Added deterministic SRT/WebVTT subtitle cues, IIIF/API observation port,
  and hash/rights/privacy-aware source bundle manifests.
- Qualified G65A-G65H without API keys or network access; scanned PDFs remain
  `OCR_REQUIRED` when no OCR provider exists.

## 2026-08-25 — M63 Domain Inference / Composition / Gap Packs

- Added deterministic domain fingerprints, composite dependency locks, explicit
  gap packs, DomainCapabilityCandidate scaffolds, and consent-gated reuse.
- Added an application-level deterministic validation sandbox with honest
  non-OS-isolation labeling; no domain package is auto-installed.
- Qualified G66A-G66H on no-API synthetic candidates.

## 2026-08-25 — M64 Completion / Consistency

- Added missingness dependency graphs, typed E1-E5 completion candidates,
  constraint checks for temporal/identity/topology/ownership/knowledge/
  organization/scenario/package/rights, and bounded uncertainty calibration.
- Kept unknowns and blocking gaps explicit; no completion can silently enter
  E0 Canon.
- Qualified G67A-G67H on no-API deterministic evidence.

## 2026-08-25 — M65 Scenario / Genesis Auto Authoring

- Added deterministic scenario mining and three Genesis modes: canonical
  replay, soft canon, and living open.
- Added immutable initial-snapshot candidates, bounded activation sets,
  explicit canon policies, runtime profiles, and source-version-derived seeds.
- Qualified G68A-G68H with the M58-M65 no-API regression; no runtime commit or
  silent E0 promotion is performed.

## 2026-08-25 — M66 Worldness Validation / Simulation Closure

- Added ten-dimensional worldness scoring and a bounded seven-day accelerated
  reference simulation with replay hashes.
- Added failure localization, candidate-only repair/recompile cycles, branch
  isolation proofs, and explicit determinism envelopes.
- Qualified G69A-G69H without adding a canonical mutation path or provider
  dependency.

## 2026-08-25 — M67 Autonomous Authoring Orchestrator

- Added the single topological authoring DAG with stage pre/postcondition,
  retry, timeout, budget, and cost metadata.
- Added provider selection constraints, deterministic stop/next-action policy,
  candidate/provider/token/network/storage/time budget records, and
  checkpoint-backed resume.
- Qualified G70A-G70H on the no-API reference path without a second authority.

## 2026-08-25 — M68 Minimal Human Review / Active Review Studio

- Added impact-aware scoring and a policy-gated review inbox with bounded
  human queue, stable impact preview, and idempotent batch decisions.
- Added rule/human audit provenance and Studio API inbox/batch/audit surfaces
  over the existing ReviewLedger.
- Qualified G71A-G71H on no-API TestClient E2E; unknowns remain deferred and
  cannot become E0 Canon.
