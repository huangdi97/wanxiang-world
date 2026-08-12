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

## Decision log (inline quick notes)

- 2026-08-11: Repository begins as a fresh `git init` on `main`; the batch control
  documents shipped in the workspace are committed as the initial baseline, then
  Goal checkpoints follow the `goal <id>: ...` convention.
