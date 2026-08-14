# Decisions ? Wanxiang Engineering Program

ADRs live in `docs/decisions/` (`NNNN-slug.md`); this file is the index.

| ADR | Title | Status |
|---|---|---|
| 0001 | Toolchain and workspace layout (M0) | accepted |
| 0002 | Architecture guard mechanism (AST-based, no bespoke framework) | accepted |
| 0003 | Domain contracts: dataclass value objects + manual versioned serialization (no Pydantic in domain) | accepted |
| 0004 | Commit atomicity: append port is the commit point; state is immutable with pure apply | accepted |
| 0005 | ComponentData carries explicit component_id (typed component identity) | accepted |
| 0006 | Event store head is the concurrency authority; event_seq (not wall clock) orders history | accepted |
| 0007 | Fork semantics: child revision = fork_revision + own event count; fork-aware authority/replay | accepted |
| 0008 | Persistence: SQLAlchemy confined to persistence package; JSON-as-text payloads for PG compatibility | accepted |
| 0009 | State-aware deterministic resolvers; synthetic micro-world resolvers live in application (not Core) | accepted |
| 0010 | API composition root (app.py) may wire persistence adapters; routes remain thin (guard exemption) | accepted |
| 0011 | Spatial substrate rides on versioned entity components (no new migration); resolvers through M1 authority | accepted |
| 0012 | Temporal substrate: world clock advanced only by commands; schedules/deadlines/recurrence as versioned components | accepted |
| 0013 | Material substrate: custody != ownership; custody != knowledge; versioned components, no migration | accepted |
| 0014 | Body/condition substrate: bounded facets, capability check blocks spatial movement, facet privacy | accepted |
| 0015 | Institution substrate: role/membership/permission/duty as versioned components; permission decisions carry provenance | accepted |
| 0016 | Population/scheduler substrate: validated StateReader cache + SQL aggregate last_event_seq; deterministic autonomous scheduler | accepted |
| 0017 | M2 milestone: integrated 72h living-world qualification test (combined synthetic world) | accepted |
| 0018 | Observation/perspective: derived read-model with rule_refs audit; sealed payload never in observations | accepted |
| 0019 | Epistemic graph: beliefs/memories as versioned components; corrections link (no silent overwrite); actor-scoped access | accepted |
| 0020 | Agency runtime: propose-only policies; order lifecycle with typed transitions | accepted |
| 0021 | Action/affordance/validator: versioned action registry + side-effect-free validator | accepted |
| 0022 | Resolution/adjudication: adjudicator registry by (action, version); seeded RNG; delta dry-run before commit | accepted |
| 0023 | Skill runtime: versioned skill registry; execution state as versioned skill.instance component | accepted |
| 0024 | Capability & learning: bounded capability (level 0..10, mastery/confidence 0..1), evidence-backed CapabilityDelta, deterministic clamped LearningPolicy | accepted |
| 0025 | Package registry: portable manifests, deterministic resolution, content hashes, default-deny executable trust, manifest schema migration | accepted |
| 0026 | Source gate: immutable sources + review stages E0..E5, rights+stage eligibility, injection default-deny, conflicting claims retained | accepted |
| 0027 | Structured compiler: safe readers, deterministic pipeline with stable hash, provenance-bound candidates, PDF/OCR/video explicitly unsupported | accepted |
| 0028 | Completion ledger: truth-label promotion graph, immutable review decisions, canon lock + override, rights gate, version diff | accepted |
| 0029 | Package install: transactional install with exact pins, portable export, explicit upgrade (fork on incompatible), v2 never mutates v1 instances | accepted |
| 0030 | World host: orchestration boundary, not a second Commit Authority; lifecycle modes gate commands | accepted |
| 0031 | Session/lease: one primary embodiment controller per actor; sessions never duplicate actor state | accepted |
| 0032 | Shadow/handoff: advice-only shadow; deterministic controller resumes on release | accepted |
| 0033 | Projection: server-composed DTOs with rights/knowledge filters and debug privilege | accepted |
| 0034 | Studio/Phaser slices: typed view models over server projections; renderers EXTERNAL_BLOCKED | accepted |
| 0035 | Persistent lifecycle: canonical host.lifecycle entity, deterministic transitions, virtual clock drivers | accepted |
| 0036 | Command queue: bounded dedup intake, serialized drain, structured statuses, backpressure | accepted |
| 0037 | Recovery: committed-events crash boundary, snapshot/event-replay fallback, resource budgets | accepted |
| 0038 | Reality bridge: normalized observations on a bus, never canonical truth | accepted |
| 0039 | Observation fusion: dedup + conflict sets, claims/proposals only, versioned policy | accepted |
| 0040 | Challenge compiler: executable specs with prerequisites/safety/rights/evidence/outcomes | accepted |
| 0041 | Director runtime: proposals only; persona changes need actor-logic review | accepted |
| 0042 | Experiment runtime: deterministic multi-seed runs, findings + validity envelope | accepted |
| 0043 | Mansion qualification: unrelated domain on the same core, no Core hacks | accepted |
| 0044 | Red Chamber slice: real data EXTERNAL_BLOCKED; Source Gate fixtures PASS | accepted |
| 0045 | Genealogy: GEDCOM subset, claims-not-truth, privacy/persona modes | accepted |
| 0046 | Heritage: IIIF/Linked Art adapters, distinct twin identities, replayable biography | accepted |
| 0047 | Co-sim: SimulationAdapter contract; adapters never own commit authority | accepted |
| 0048 | Campaign: synthetic factions/units/regions/orders with fog-of-war | accepted |
| 0049 | Liaoshen pack: real data EXTERNAL_BLOCKED; generic M8 not blocked | accepted |
| 0050 | Release qualification: stability/backup/SDK/adapters/security with labeled external checks | accepted |

## Decision log (inline quick notes)

- 2026-08-11: Repository begins as a fresh `git init` on `main`; the batch control
  documents shipped in the workspace are committed as the initial baseline, then
  Goal checkpoints follow the `goal <id>: ...` convention.
| 0051 | G13E: ReplayEngine checks event_seq and revision independently; child branches pass start_seq=1 (branch-local seq restarts, revision continues from fork); snapshot continuation uses baseline.revision+1 | accepted |
| 0052 | G14D: restore_and_replay validates snapshot baselines against event history (semantic hash + versions); invalid/unreadable snapshots fall back to authoritative replay with snapshot_rejected observable | accepted |
| 0053 | G14H: CoSimOrchestrator checkpoint includes the orchestrator clock so restore+continue realigns barriers; mismatched checkpoints are explicit errors | accepted |
| 0054 | G17F: package resolver honors explicit root_version pins (seed before traversal); yank blocks new installs but preserves metadata | accepted |
