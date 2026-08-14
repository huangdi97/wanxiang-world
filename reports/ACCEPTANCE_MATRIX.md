# Acceptance Matrix ? Wanxiang Engineering Program

Maintained throughout the program. Status: PASS | FAIL | EXTERNAL_BLOCKED | PENDING.
Columns: Requirement ID | Source section | Owning Goal | Test/evidence | Current status | Last verified commit | Notes.

## M0 ? Reproducible Engineering Base

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M0-01 | EPA ?19 | GOAL_00A | Fresh bootstrap documented in `docs/runbook/DEVELOPMENT.md`; uv/pnpm installs executed | PASS | 9134801 | |
| M0-02 | EPA ?19 | GOAL_00A | Python toolchain reproducible (`uv sync --all-groups --all-packages`) | PASS | 9134801 | |
| M0-03 | EPA ?19 | GOAL_00A | tests/lint/typecheck pipelines work (ruff, pyright, pytest, pnpm suite) | PASS | 9134801 | |
| M0-04 | EPA ?19 | GOAL_00B | Architecture import guards fail on a fixture violation (negative tests) | PASS | 3410300 | |
| M0-05 | EPA ?19 | GOAL_00A | Ledgers/ADRs/evidence format exist | PASS | 9134801 | |

## M1 ? Authoritative World Exists (03_ACCEPTANCE_TESTING_AND_EVIDENCE.md ?4)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| A1 | Acceptance ?4 | GOAL_01F | valid commit changes canonical state exactly once | PASS | c45b64e | test_a1 |
| A2 | Acceptance ?4 | GOAL_01F | invalid command does not mutate state | PASS | c45b64e | test_a2 |
| A3 | Acceptance ?4 | GOAL_01F | duplicate command idempotency | PASS | c45b64e | test_a3 |
| A4 | Acceptance ?4 | GOAL_01F | stale revision structured rejection | PASS | c45b64e | test_a4 |
| A5 | Acceptance ?4 | GOAL_01F | snapshot + remaining replay equal semantic hash | PASS | c45b64e | test_a5 |
| A6 | Acceptance ?4 | GOAL_01F | full replay from initial baseline | PASS | c45b64e | test_a6 |
| A7 | Acceptance ?4 | GOAL_01F | branch isolation (child does not mutate parent) | PASS | c45b64e | test_a7 |
| A8 | Acceptance ?4 | GOAL_01F | deterministic seed/version reproducibility | PASS | c45b64e | test_a8 |
| A9 | Acceptance ?4 | GOAL_01F | corrupt stream fails explicitly | PASS | c45b64e | test_a9 |
| A10 | Acceptance ?4 | GOAL_01F | migration compatibility with prior fixture | PASS | c45b64e | test_a10 + tests/migration |

## M2 ? Deterministic Living World Exists (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M2-01 | M2 gate | GOAL_02A | Spatial topology/access: reachability, capacity, occupancy, zones | PASS | 8c0c7cf | |
| M2-02 | M2 gate | GOAL_02B | Temporal: monotonic clock, schedules, recurrence, deadlines | PASS | 38acada | |
| M2-03 | M2 gate | GOAL_02C | Material: custody != ownership; custody != knowledge; containers | PASS | 250dd0b | |
| M2-04 | M2 gate | GOAL_02D | Body/condition constrains actions | PASS | 84568a4 | |
| M2-05 | M2 gate | GOAL_02E | Institution roles/duties/permissions affect actions | PASS | 3472a69 | |
| M2-06 | M2 gate | GOAL_02F | Autonomous multi-rate scheduler, deterministic, bounded | PASS | aa2f99f | |
| M2-07 | M2 gate | GOAL_02A-F | 72h integrated living-world scenario | PASS | (m2 commit) | test_m2_qualification |

## M3 ? Bounded Agents Can Live Inside the World (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M3-01 | M3 gate | GOAL_03A | Observation/perspective isolation: derived read-model, sealed payload, private/group visibility | PASS | 7238461 | |
| M3-02 | M3 gate | GOAL_03B | Belief/memory/epistemic graph: corrections, contradictions, forgetting, actor-scoped access | PASS | 00419ef | |
| M3-03 | M3 gate | GOAL_03C | Actor/org runtime: propose-only policies, order lifecycle, typed transitions | PASS | c7790ff | |
| M3-04 | M3 gate | GOAL_03D | Action/affordance/validator: versioned registry, side-effect-free validation | PASS | b126b7d | |
| M3-05 | M3 gate | GOAL_03E | Resolver/adjudication: deterministic policies, seeded RNG, provenance | PASS | edadaf3 | |
| M3-06 | M3 gate | GOAL_03F | Skill runtime: step expansion through authoritative path, permission gate, failure handling | PASS | 6006fd2 | |
| M3-07 | M3 gate | GOAL_03G | Capability & learning: bounded evidence-backed capability change; skill prerequisites | PASS | goal g03g | |
M3 verdict: PASS (2026-08-13, tag m3-bounded-agents; reports/M3_ACCEPTANCE.md).
M4 verdict: PASS (2026-08-13, tag m4-worlds-authored-installed; reports/M4_ACCEPTANCE.md).
M5 verdict: PASS (2026-08-13, re-qualified with G06; tag m5-human-in-world-without-authority; reports/M5_ACCEPTANCE.md).
M6 verdict: PASS (2026-08-13, tag m6-reality-experiments; reports/M6_ACCEPTANCE.md).
M7 verdict: PASS (2026-08-13, tag m7-domain-generality; reports/M7_ACCEPTANCE.md).
M8 verdict: PASS (2026-08-13, tag m8-cosimulation-strategy; reports/M8_ACCEPTANCE.md).
M9 verdict: PASS (2026-08-13, tag m9-release-qualified; reports/M9_ACCEPTANCE.md).
PROGRAM verdict: PASS (M1-M9; reports/FINAL_PROGRAM_COMPLETION_REPORT.md).

## M4 ? Worlds Can Be Authored, Reviewed, Installed and Instantiated (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M4-01 | M4 gate | GOAL_04A | Package/schema/dependency registry: deterministic resolution, cycles/conflicts, content hash, trust, migration | PASS | goal g04a | |
| M4-02 | M4 gate | GOAL_04B | Source registry & gate: immutable sources, rights/stage eligibility, injection default-deny, conflicting claims | PASS | goal g04b | |
| M4-03 | M4 gate | GOAL_04C | Structured compiler: safe readers, deterministic candidates with provenance, PDF/OCR/video unsupported | PASS | goal g04c | |
| M4-04 | M4 gate | GOAL_04D | Completion ledger: truth labels, immutable review, canon lock + override, rights gate, diffs | PASS | goal g04d | |
| M4-05 | M4 gate | GOAL_04E | Install/export/migration: transactional install, exact pins, export roundtrip, v2 does not mutate v1 | PASS | goal g04e | |
| M4-06 | M4 gate | GOAL_04A-E | M4 vertical: author->review->install->instantiate synthetic package end-to-end | PASS | goal g04e | test_m4_qualification |

## M5 ? Human Can Enter a Persistent World Without Becoming the Authority (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M5-01 | M5 gate | GOAL_05A | WorldHost orchestration boundary; lifecycle modes; not a commit authority | PASS | goal g05a | |
| M5-02 | M5 gate | GOAL_05B | One primary embodiment controller per actor; lease lifecycle | PASS | goal g05b | |
| M5-03 | M5 gate | GOAL_05C | Shadow cannot commit; handoff resumes deterministic controller | PASS | goal g05c | |
| M5-04 | M5 gate | GOAL_05D | Projection server-side rights/knowledge filters; debug privilege | PASS | goal g05d | |
| M5-05 | M5 gate | GOAL_05E | Studio TS slice consumes projections; bounded commands | PASS | goal g05e | React render EXTERNAL_BLOCKED |
| M5-06 | M5 gate | GOAL_05F | Phaser TS slice map/tokens/movement via projection API | PASS | goal g05f | Phaser render EXTERNAL_BLOCKED |
| M5-07 | M5 gate | GOAL_05A-F | M5 vertical: lease->takeover->commit->release->disconnect->restart->reconnect hash continuity | PASS | m5 commit | test_m5_qualification |
| M5-08 | M5 gate | GOAL_06A | Lifecycle persists independently of sessions; pause/advance/background | PASS | goal g06a | test_lifecycle + m5_g06 proofs |
| M5-09 | M5 gate | GOAL_06B | Multi-client retries/conflicts idempotent and revision-safe | PASS | goal g06b | test_command_queue |
| M5-10 | M5 gate | GOAL_06C | Crash/lease recovery + scheduler restoration preserve canonical hash | PASS | goal g06c | test_recovery + m5_g06 proofs |
## M6 ? Reality-Coupled Context and Controlled Experiments Work Safely (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M6-01 | M6 gate | GOAL_07A | PhysicalObservation + Reality Bridge: normalize/validate/poll; never canonical truth | PASS | goal g07a | |
| M6-02 | M6 gate | GOAL_07B | Fusion: dedup, conflict sets preserved, claims/proposals only | PASS | goal g07b | |
| M6-03 | M6 gate | GOAL_07C | ChallengeSpec with prerequisites/safety/rights/evidence/outcomes | PASS | goal g07c | |
| M6-04 | M6 gate | GOAL_07D | Director proposes; cannot commit or rewrite actors without review | PASS | goal g07d | |
| M6-05 | M6 gate | GOAL_07E | Experiment: multi-seed deterministic runs, metrics, validity envelope | PASS | goal g07e | |
| M6-06 | M6 gate | GOAL_07A-E | M6 vertical: observations->fusion->challenge->director->experiment | PASS | m6 commit | test_m6_qualification |
## M7 ? Multiple Unrelated Domains Prove Core Generality (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M7-01 | M7 gate | GOAL_08A | Mansion 7-day persistence/control/knowledge/material/branch | PASS | goal g08a | |
| M7-02 | M7 gate | GOAL_08B | Red Chamber Source Gate positive/negative; real data EXTERNAL_BLOCKED | PASS | goal g08b | |
| M7-03 | M7 gate | GOAL_09A | GEDCOM round-trip + sources + extension preservation | PASS | goal g09a | |
| M7-04 | M7 gate | GOAL_09B | Family conflicting claims + lineage | PASS | goal g09b | |
| M7-05 | M7 gate | GOAL_09C | Living privacy/consent/revocation + persona modes | PASS | goal g09c | |
| M7-06 | M7 gate | GOAL_10A | IIIF manifest ingest (real endpoints EXTERNAL_BLOCKED) | PASS | goal g10a | |
| M7-07 | M7 gate | GOAL_10B | Linked Art / CIDOC mapping profile | PASS | goal g10b | |
| M7-08 | M7 gate | GOAL_10C | Semantic twin distinct identities + conservation history | PASS | goal g10c | |
| M7-09 | M7 gate | GOAL_10D | Museum biography labels + curator gate | PASS | goal g10d | |
| M7-10 | M7 gate | GOAL_08A-10D | M7 mandatory: 3 domain families on one core | PASS | m7 commit | qualification + mansion tests |
## M8 ? Mechanistic External Models Participate Without Owning Canonical State (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M8-01 | M8 gate | GOAL_11A | SimulationAdapter full contract + fake simulator; no commit authority | PASS | goal g11a | |
| M8-02 | M8 gate | GOAL_11B | Multi-rate orchestrator deterministic + restartable; explicit arbitration | PASS | goal g11b | |
| M8-03 | M8 gate | GOAL_11C | Synthetic campaign domain (factions/units/terrain/resources/orders) | PASS | goal g11c | |
| M8-04 | M8 gate | GOAL_11D | Logistics/resource flow, movement constraints, fog-of-war | PASS | goal g11d | |
| M8-05 | M8 gate | GOAL_11E | Batch results as distributions with ValidityEnvelope | PASS | goal g11e | |
| M8-06 | M8 gate | GOAL_11F | Liaoshen real pack EXTERNAL_BLOCKED; generic M8 not blocked | PASS | goal g11f | |
| M8-07 | M8 gate | GOAL_11A-F | M8 vertical: campaign + 2 simulators + batch experiments | PASS | m8 commit | test_m8_qualification |
## M9 ? Release-qualified Wanxiang Platform Foundation (07_MILESTONE_GATES_M2_M9.md)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M9-01 | M9 gate | GOAL_12A | 30 in-world days + 1000+ cycles, bounded growth | PASS | goal g12a | |
| M9-02 | M9 gate | GOAL_12B | Backup restore reproduces canonical hash; migrations replay | PASS | goal g12b | |
| M9-03 | M9 gate | GOAL_12C | OpenAPI/TS SDK reproducible; version policy documented | PASS | goal g12c | |
| M9-04 | M9 gate | GOAL_12D | Gym/PettingZoo adapters preserve authority + epistemic filters | PASS | goal g12d | |
| M9-05 | M9 gate | GOAL_12E | Godot/Babylon projection contracts non-authoritative | PASS | goal g12e | |
| M9-06 | M9 gate | GOAL_12F | Asset Foundry non-authoritative with geometry validation | PASS | goal g12f | |
| M9-07 | M9 gate | GOAL_12G | Digital Human/XR gateway rights gate | PASS | goal g12g | |
| M9-08 | M9 gate | GOAL_12H | Security: secrets/uploads/access/audit | PASS | goal g12h | |
| M9-09 | M9 gate | GOAL_12A-H | Full M1-M8 regression matrix green; final reports | PASS | m9 commit | 385 + 21 tests |
## Architecture gates (02_ENGINEERING_STANDARDS.md ?16)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| ARCH-01 | Standards ?16 | GOAL_00B | domain -> fastapi/sqlalchemy/alembic detected | PASS | 3410300 | negative tests |
| ARCH-02 | Standards ?16 | GOAL_00B | runtime -> apps.api detected | PASS | 3410300 | |
| ARCH-03 | Standards ?16 | GOAL_00B | plugin/model provider -> persistence internals detected | PASS | 3410300 | |
| ARCH-04 | Standards ?16 | GOAL_00B | import cycles detected | PASS | 3410300 | |
| ARCH-05 | Standards ?16 | GOAL_00B | substrate package guard (fastapi/sqlalchemy/persistence) | PASS | 8c0c7cf | |
## M10 gate (2026-08-14)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M10-01 | M10 gate | G13A | Post-M9 baseline freeze + independent evidence capture | PASS | g13a | hashes, command matrix, clean bootstrap |
| M10-02 | M10 gate | G13B | Design-to-implementation traceability (16 kernels, 44 rows) | PASS | g13b | validator tests |
| M10-03 | M10 gate | G13C | Architecture/dependency/canonical-mutation forensics | PASS | g13c | 0 bypass, single CommitAuthority |
| M10-04 | M10 gate | G13D | Placeholder/fake/dead-path/surface/drift audit (guard bug + SDK drift fixed) | PASS | g13d | drift aligned 10/10 |
| M10-05 | M10 gate | G13E | Event/replay/branch/migration/version forensics (P0 child replay fixed) | PASS | g13e | corpus + version matrix |
| M10-06 | M10 gate | G13F | Security/rights/provenance/privacy/source-gate forensics | PASS | g13f | 8 threats mitigated, 6 rights enforced |
| M10-07 | M10 gate | G13G | Maintainability/complexity/test-quality/upgradeability audit | PASS | g13g | 0 over-threshold; swallow fixed |
| M10-08 | M10 gate | G13H | P0 gap closure wave | PASS | g13h | P0 open = 0 |
| M10-09 | M10 gate | G13I | P1/P2 closure + M10 independent requalification | PASS | g13i | full gate 428 tests |
## M11 gate (2026-08-14)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M11-01 | M11 gate | G14A | Concurrency/race/idempotency/lost-update | PASS | g14a | |
| M11-02 | M11 gate | G14B | Crash/atomicity/mid-commit recovery | PASS | g14b | |
| M11-03 | M11 gate | G14C | DB/storage/network fault injection | PASS | g14c | |
| M11-04 | M11 gate | G14D | History corruption adversarial (snapshot validation fixed) | PASS | g14d | |
| M11-05 | M11 gate | G14E | Host/multiplayer/reconnect/backpressure | PASS | g14e | |
| M11-06 | M11 gate | G14F | Hostile package/plugin/source input | PASS | g14f | |
| M11-07 | M11 gate | G14G | Authorization/rights/privacy/data-leak | PASS | g14g | |
| M11-08 | M11 gate | G14H | SimulationAdapter byzantine (orchestrator checkpoint fixed) | PASS | g14h | |
| M11-09 | M11 gate | G14I | Resource/fuzz/long-run chaos + M11 qualification | PASS | g14i | 473 tests total |
## M12 gate (2026-08-14)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M12-01 | M12 gate | G15A | Reference world contract + external pack boundary | PASS | g15a | conformance harness |
| M12-02 | M12 gate | G15B | Comprehensive synthetic reference world package | PASS | g15b | |
| M12-03 | M12 gate | G15C | Seven-day autonomous living-world | PASS | g15c | |
| M12-04 | M12 gate | G15D | Embodiment exit/re-entry control continuity | PASS | g15d | |
| M12-05 | M12 gate | G15E | Material/information/social continuity | PASS | g15e | |
| M12-06 | M12 gate | G15F | Branch/time-travel/counterfactual worldlines | PASS | g15f | |
| M12-07 | M12 gate | G15G | 90-day run + population LOD | PASS | g15g | |
| M12-08 | M12 gate | G15H | Red Chamber source-gated slice | PASS | g15h | real data EXTERNAL_BLOCKED |
| M12-09 | M12 gate | G15I | Family/heritage/campaign suites | PASS | g15i | real data EXTERNAL_BLOCKED |
| M12-10 | M12 gate | G15J | Cross-domain worldness certification + M12 | PASS | g15j | 12/12 worldness criteria; 497 tests |
## M13 gate (2026-08-14)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M13-01 | M13 gate | G16A | Production topology/config/secret foundation | PASS | g16a | fail-fast prod config |
| M13-02 | M13 gate | G16B | PostgreSQL persistence/migration | PASS | g16b | live PG EXTERNAL_BLOCKED |
| M13-03 | M13 gate | G16C | Background queue/scheduler reliability | PASS | g16c | |
| M13-04 | M13 gate | G16D | Asset/object storage + media rights | PASS | g16d | content-addressed |
| M13-05 | M13 gate | G16E | OTel observability/SLOs | PASS | g16e | |
| M13-06 | M13 gate | G16F | Security hardening/authz/rate limits/SBOM | PASS | g16f | 429/413 + SBOM |
| M13-07 | M13 gate | G16G | Backup/restore/PITR/game day | PASS | g16g | |
| M13-08 | M13 gate | G16H | CI/CD/release artifacts/rollback | PASS | g16h | |
| M13-09 | M13 gate | G16I | Performance/capacity/cost/budgets | PASS | g16i | measured envelope |
| M13-10 | M13 gate | G16J | Private/staging deploy + M13 | PASS | g16j | 532 tests + 1 skip |
## M14 gate (2026-08-14)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M14-01 | M14 gate | G17A | SDK contract + semver/compat | PASS | g17a | baseline snapshot |
| M14-02 | M14 gate | G17B | Authoring CLI + validation | PASS | g17b | |
| M14-03 | M14 gate | G17C | External author docs | PASS | g17c | |
| M14-04 | M14 gate | G17D | Conformance/certification harness | PASS | g17d | |
| M14-05 | M14 gate | G17E | Plugin trust/signing/capabilities | PASS | g17e | |
| M14-06 | M14 gate | G17F | Registry lifecycle | PASS | g17f | resolver pin fixed |
| M14-07 | M14 gate | G17G | Black-box external sample pack | PASS | g17g | |
| M14-08 | M14 gate | G17H | Ecosystem qualification + M14 | PASS | g17h | 554 tests + 1 skip |
## M15 gate (2026-08-14)

| Req ID | Source | Owning Goal | Test/evidence | Status | Last verified commit | Notes |
|---|---|---|---|---|---|---|
| M15-01 | M15 gate | G18A | IA + server-truth contract | PASS | g18a | |
| M15-02 | M15 gate | G18B | Studio / World IDE | PASS | g18b | |
| M15-03 | M15 gate | G18C | Experience Player continuity | PASS | g18c | |
| M15-04 | M15 gate | G18D | Strategy / Experiment Workbench | PASS | g18d | |
| M15-05 | M15 gate | G18E | Family Portal | PASS | g18e | |
| M15-06 | M15 gate | G18F | Heritage / Museum Workbench | PASS | g18f | |
| M15-07 | M15 gate | G18G | Learn / Challenge Experience | PASS | g18g | |
| M15-08 | M15 gate | G18H | Operator/Admin console + M15 | PASS | g18h | 579 tests + 1 skip |
