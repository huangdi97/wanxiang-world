# Implementation Status

## M0 ? Reproducible Engineering Base (PASS, 2026-08-12)

- uv workspace, strict ruff/pyright/pytest, TypeScript baseline, quality gate,
  ledgers/ADR structure, architecture guards.

## M1 ? Authoritative World Exists (PASS, 2026-08-12)

- Domain core contracts (`packages/domain`): ids, versions, errors, hierarchy,
  entity/relation/component, command, delta, event, hashing, snapshot, run,
  evidence/rights foundations, versioned serialization.
- Runtime (`packages/runtime`): immutable canonical state + pure apply,
  Commit Authority (preconditions, invariants, audit), EventStore contract +
  in-memory adapter, replay engine, snapshot store, branch fork/repository,
  state diff, resolver registry.
- Application (`packages/application`): WorldRuntime orchestration, synthetic
  micro-world resolvers, WorldEnvironment facade.
- Persistence (`packages/persistence`): SQLAlchemy adapters + Alembic
  migrations (0001, 0002), durable replay.
- Transport (`apps/api`): thin FastAPI routes, OpenAPI, structured errors.
- Acceptance: A1-A10 PASS; 130 tests; golden replay fixture; no LLM key.

## Next dependency

- G02A Spatial Topology & Access (do not start until M1 evidence is reviewed).

- G02B Temporal System & Schedules ? PASS (2026-08-13): monotonic world clock
  (command-advanced, backward rejected), calendars, appointments/deadlines/
  recurring duties with deterministic bounded expansion, schedule conflict +
  window constraints; restart/replay stable; 168 tests green.

- G02C Material, Container, Custody & Information Payload ? PASS (2026-08-13):
  items/containers/custody/ownership/info payloads on versioned components;
  custody != ownership and custody != knowledge; containment cycle prevention,
  capacity, explicit consume/damage; 182 tests green.

- G02D Body & Condition Constraints ? PASS (2026-08-13): bounded condition
  facets with deterministic transitions; capability check blocks otherwise-valid
  spatial movement; facet privacy; 192 tests green.

- G02E Institution, Authority, Duty & Norm ? PASS (2026-08-13): roles,
  time-scoped memberships, delegated permissions with provenance, duties and
  sanctions; restricted places require permission; expired roles cannot grant
  authority; 202 tests green.

- G02F Population Resolution & Autonomous Scheduler ? PASS (2026-08-13):
  multi-rate autonomous scheduler (focus/lightweight/duty/aggregate), budgets,
  deterministic 72h micro-town run with no user input; validated StateReader
  cache; 211 tests green.

## M3 ? Bounded Agents Can Live Inside the World (PASS, 2026-08-13)

## M4 ? Worlds Can Be Authored, Reviewed, Installed and Instantiated (PASS, 2026-08-13)

## M5 ? Human Can Enter a Persistent World Without Becoming the Authority (PASS, 2026-08-13)

## M6 ? Reality-Coupled Context and Controlled Experiments Work Safely (PASS, 2026-08-13)

## M7 ? Multiple Unrelated Domains Prove Core Generality (PASS, 2026-08-13)

## M8 ? Mechanistic External Models Participate Without Owning Canonical State (PASS, 2026-08-13)

## M9 ? Release-qualified Wanxiang Platform Foundation (PASS, 2026-08-13)

- G12A Stability / G12B Backup / G12C SDK / G12D Research / G12E 3D / G12F Foundry / G12G Gateway / G12H Security ? PASS.
- Final reports written; RELEASE_READINESS documented; 385 Python + 21 TS tests.

- G11A SimulationAdapter + FakeSimulator ? PASS.
- G11B Multi-rate Co-Sim Orchestrator ? PASS.
- G11C/D Synthetic Campaign + Logistics/Fog-of-war ? PASS.
- G11E Batch Experiment/Strategy Evaluation ? PASS.
- G11F Liaoshen pack (real data EXTERNAL_BLOCKED) ? PASS.

- G08A Mansion 7-day living world ? PASS.
- G08B Red Chamber source gate (real data EXTERNAL_BLOCKED) ? PASS.
- G09A GEDCOM interop / G09B family world / G09C privacy-persona ? PASS.
- G10A IIIF / G10B Linked Art / G10C semantic twin / G10D museum biography ? PASS.

- G07A Reality Bridge ? PASS (2026-08-13): physical observations normalized + bus delivery, never canonical truth.
- G07B Observation Fusion ? PASS (2026-08-13): dedup/conflict sets/proposals only, versioned policy.
- G07C Challenge Compiler ? PASS (2026-08-13): opportunities -> executable specs with prerequisites/outcomes.
- G07D Director Runtime ? PASS (2026-08-13): proposals only, persona review gate, projection-only directives.
- G07E Experiment Runtime ? PASS (2026-08-13): multi-seed deterministic runs, findings + validity envelope.

- G05A World Host ? PASS (2026-08-13): orchestration boundary, lifecycle modes, host registry.
- G05B Session/Embodiment/Lease ? PASS (2026-08-13): one primary controller per actor, lease lifecycle.
- G05C Shadow/Human Control Handoff ? PASS (2026-08-13): handoff state machine, advice-only shadow.
- G05D Projection API & Filters ? PASS (2026-08-13): server-side perspective/rights filters, sealed/private redaction, debug privilege.
- G05E Studio TS Slice ? PASS (2026-08-13): typed view models + Vitest (React render EXTERNAL_BLOCKED).
- G05F Phaser TS Slice ? PASS (2026-08-13): map/token view models + Vitest (Phaser render EXTERNAL_BLOCKED).
- G06A Persistent Lifecycle ? PASS (2026-08-13): 7 modes, canonical persistence, virtual clock, catch-up.
- G06B Command Queue ? PASS (2026-08-13): bounded dedup intake, serialized drain, structured statuses.
- G06C Crash Recovery/Checkpoint/Budget ? PASS (2026-08-13): snapshot fallback, hash-preserving restart, budgets.

- G04A Package, Schema & Dependency Registry ? PASS (2026-08-13): portable manifests, semantic constraints, deterministic resolver, content hashes, default-deny executable trust, manifest migration; 275 tests green.

- G04B Source Registry & Source Gate ? PASS (2026-08-13): immutable sources + review stages E0..E5, rights envelopes, conflicting claim candidates with evidence links, audited transitions, pure SourceGate with injection detection; 283 tests green.

- G04C Structured Compiler MVP ? PASS (2026-08-13): safe readers (json/yaml-subset/markdown/text), deterministic pipeline with stable hash, provenance-bound candidates, PDF/OCR/video explicitly unsupported; 293 tests green.

- G04D Completion Ledger & Review Workflow ? PASS (2026-08-13): truth-label taxonomy, immutable review decisions, canon lock + override, rights gate, package-version diff; 302 tests green.

- G04E Package Install, Export & Migration Compatibility ? PASS (2026-08-13): transactional install with exact pins + lock hash, portable export with stable hash, explicit upgrade (fork on incompatible), v2 does not mutate v1-pinned instances; 309 tests green; M4 vertical PASS.

- G03A Observation & Perspective Isolation ? PASS (2026-08-13): observations
  derived from events + spatial/acoustic/rights; sealed payload content never
  leaks; private/group visibility; 220 tests green.

- G03B Belief, Memory & Temporal Epistemic Graph ? PASS (2026-08-13): actor-local
  beliefs/memories with corrections (lineage), contradictions, forgetting and
  bounded compaction; actor-scoped access; 228 tests green.

- G03C Actor & Organization Runtime ? PASS (2026-08-13): propose-only policies,
  order lifecycle with typed transitions, actor states, organization views;
  236 tests green.

- G03D Action, Affordance & Validator ? PASS (2026-08-13): versioned action
  registry + side-effect-free validator (schema/actor/permission/reachability/
  epistemic/resources); affordances; 244 tests green.

- G03F Skill Runtime ? PASS (2026-08-13): versioned skills (definition/step/instance), registry with reference skills, SkillRuntime executing every step through the authoritative path, permission gate at start, failure marks instance failed; 255 tests green.

- G03G Capability & Learning ? PASS (2026-08-13): bounded capability (level 0..10, mastery/confidence 0..1), practice/assessment evidence records, deterministic clamped LearningPolicy, capability resolvers through Commit Authority, skill step capability gates; 265 tests green.

## M3 ? Bounded Agents Can Live Inside the World (PASS, 2026-08-13)

## M4 ? Worlds Can Be Authored, Reviewed, Installed and Instantiated (PASS, 2026-08-13)

## M5 ? Human Can Enter a Persistent World Without Becoming the Authority (PASS, 2026-08-13)

## M6 ? Reality-Coupled Context and Controlled Experiments Work Safely (PASS, 2026-08-13)

## M7 ? Multiple Unrelated Domains Prove Core Generality (PASS, 2026-08-13)

## M8 ? Mechanistic External Models Participate Without Owning Canonical State (PASS, 2026-08-13)

## M9 ? Release-qualified Wanxiang Platform Foundation (PASS, 2026-08-13)

- G12A Stability / G12B Backup / G12C SDK / G12D Research / G12E 3D / G12F Foundry / G12G Gateway / G12H Security ? PASS.
- Final reports written; RELEASE_READINESS documented; 385 Python + 21 TS tests.

- G11A SimulationAdapter + FakeSimulator ? PASS.
- G11B Multi-rate Co-Sim Orchestrator ? PASS.
- G11C/D Synthetic Campaign + Logistics/Fog-of-war ? PASS.
- G11E Batch Experiment/Strategy Evaluation ? PASS.
- G11F Liaoshen pack (real data EXTERNAL_BLOCKED) ? PASS.

- G08A Mansion 7-day living world ? PASS.
- G08B Red Chamber source gate (real data EXTERNAL_BLOCKED) ? PASS.
- G09A GEDCOM interop / G09B family world / G09C privacy-persona ? PASS.
- G10A IIIF / G10B Linked Art / G10C semantic twin / G10D museum biography ? PASS.

- G07A Reality Bridge ? PASS (2026-08-13): physical observations normalized + bus delivery, never canonical truth.
- G07B Observation Fusion ? PASS (2026-08-13): dedup/conflict sets/proposals only, versioned policy.
- G07C Challenge Compiler ? PASS (2026-08-13): opportunities -> executable specs with prerequisites/outcomes.
- G07D Director Runtime ? PASS (2026-08-13): proposals only, persona review gate, projection-only directives.
- G07E Experiment Runtime ? PASS (2026-08-13): multi-seed deterministic runs, findings + validity envelope.

- G05A World Host ? PASS (2026-08-13): orchestration boundary, lifecycle modes, host registry.
- G05B Session/Embodiment/Lease ? PASS (2026-08-13): one primary controller per actor, lease lifecycle.
- G05C Shadow/Human Control Handoff ? PASS (2026-08-13): handoff state machine, advice-only shadow.
- G05D Projection API & Filters ? PASS (2026-08-13): server-side perspective/rights filters, sealed/private redaction, debug privilege.
- G05E Studio TS Slice ? PASS (2026-08-13): typed view models + Vitest (React render EXTERNAL_BLOCKED).
- G05F Phaser TS Slice ? PASS (2026-08-13): map/token view models + Vitest (Phaser render EXTERNAL_BLOCKED).
- G06A Persistent Lifecycle ? PASS (2026-08-13): 7 modes, canonical persistence, virtual clock, catch-up.
- G06B Command Queue ? PASS (2026-08-13): bounded dedup intake, serialized drain, structured statuses.
- G06C Crash Recovery/Checkpoint/Budget ? PASS (2026-08-13): snapshot fallback, hash-preserving restart, budgets.

- G04A Package, Schema & Dependency Registry ? PASS (2026-08-13): portable manifests, semantic constraints, deterministic resolver, content hashes, default-deny executable trust, manifest migration; 275 tests green.

- G04B Source Registry & Source Gate ? PASS (2026-08-13): immutable sources + review stages E0..E5, rights envelopes, conflicting claim candidates with evidence links, audited transitions, pure SourceGate with injection detection; 283 tests green.

- G04C Structured Compiler MVP ? PASS (2026-08-13): safe readers (json/yaml-subset/markdown/text), deterministic pipeline with stable hash, provenance-bound candidates, PDF/OCR/video explicitly unsupported; 293 tests green.

- G04D Completion Ledger & Review Workflow ? PASS (2026-08-13): truth-label taxonomy, immutable review decisions, canon lock + override, rights gate, package-version diff; 302 tests green.

- G04E Package Install, Export & Migration Compatibility ? PASS (2026-08-13): transactional install with exact pins + lock hash, portable export with stable hash, explicit upgrade (fork on incompatible), v2 does not mutate v1-pinned instances; 309 tests green; M4 vertical PASS.

- G03E Resolver, Adjudication & Deterministic Policies ? PASS (2026-08-13):
  adjudicator registry by (action, version), seeded RNG, provenance +
  uncertainty, version pinning; delta dry-run before commit; 250 tests green.

## M71-M78 current implementation checkpoint (2026-08-25)

This user-authorized continuation supersedes the historical M70 STOP for this
task only. G74A-G80G are implemented: semantic distillation consumes stable
source locators in bounded batches and emits provenance-bound candidates;
rights and provider absence are typed; CLI/API/Studio share one authoring
service; Worldness exposes ten measurements; and the living runtime records
Commit Authority action, replay equality and branch isolation.

Real-source evidence records 3,918 parsed nodes/segments, 164 batches, 11,549
candidates, coverage 0.8333333333, package/preview/publish, Worldness passed
at 0.99, a committed `set_status` event with replay equality, and an unchanged
parent branch. G81G-G81J are PASS for implementation commit `f7685ec` and
Actions run `32821744579`, whose six required jobs are green. The final
evidence-only commit must still pass its own Actions run before `rc2`; v5.5
and training remain out of scope.

## M79 second real-book qualification (2026-08-25)

M79/G82A-G82G is PASS for a private local EPUB through the generic binary
source path. The run produced 28,510 parsed nodes/segments, 1,188 completed
bounded semantic batches, 25,315 provenance-bound candidates, measured
coverage of 0.8333333333333334, WorldPackage/Preview, Worldness
0.9733333333333333, Living Instance, Commit/Replay equality and branch
isolation. Evidence is sanitized in `reports/M79_REAL_EPUB_QUALIFICATION.md`
and `artifacts/m79_m84/real_second_book_product_evidence.json`; no private
path, digest or source text is tracked.

## M82 real GEDCOM qualification (2026-08-26)

M82/G85A-G85G is PASS for the supplied local GEDCOM through the generic
GEDCOM parser, locator, semantic distillation, WorldDraft, WorldPackage,
Preview, Worldness, Living Instance, Commit/Replay, and branch-isolation
path. The real run measured 326 provenance-bound candidates, coverage `1.0`,
Worldness `0.99`, 19 entities, 79 relations, and 55 events. Evidence is
sanitized in `reports/M82_GEDCOM_QUALIFICATION.md` and
`artifacts/m79_m84/real_gedcom_product_evidence.json`; the official GEDCOM 7
in-memory import/locator smoke is in
`artifacts/m79_m84/gedcom7_official_smoke.json`. The historical/public fixture
does not constitute private living-family user validation.

M84/G87A-G87H is active. No stable v5.4.0 tag/release, v5.5 work, or model
training is authorized until the M84 evidence gates pass.

## M84 stable-release decision (2026-08-26)

M84 clean-clone, regression, source-safety, and GitHub delivery evidence is
complete through G87E. Stable release remains `NOT_ACCEPTED` because the
unchanged first real Chinese book report still records zero candidates and
zero coverage in its rights-approved diagnostic. The accepted second EPUB and
public historical GEDCOM generalization runs are not a substitute. No stable
tag/release was created. See `reports/M84_STABLE_BLOCKER.md`.

## M84 first-book requalification (2026-08-26)

The same original private Chinese book now completes the real CLI/API/Studio
chain after the semantic-distillation repair: 11,549 candidates, measured
coverage `0.8333333333333334`, WorldPackage, Preview, Worldness, Living,
Commit/Replay, and branch isolation. The pre-repair NOT_ACCEPTED report is
preserved unchanged; sanitized ACCEPTED evidence is recorded in
`reports/M84_FIRST_BOOK_REQUALIFICATION.md`. Stable release gates may proceed
after the documentation commit's required Actions are green.
