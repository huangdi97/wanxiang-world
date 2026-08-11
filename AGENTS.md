# AGENTS.md ? Wanxiang Engineering Contribution Rules

Non-negotiable rules for any Codex/agent/human modifying this repository.

## Authority

- `docs/spec/WANXIANG_v5_MASTER_SPEC.md` is the product source of truth.
- `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md` controls execution order.
- Goal files under `goals/` are the executable contracts for each bounded unit.
- Code/tests are evidence, never permission to silently change the spec.

## World authority (hard invariant)

- Only **Commit Authority** may mutate Canonical World State.
- LLMs, humans, clients, sensors, plugins, resolvers, projections and adapters
  produce Commands / Intents / Observations / ProposedWorldDeltas only.
- No transport route, UI component, model provider or plugin is a commit authority.

## Event sourcing (hard invariant)

- Canonical history is append-only and replayable.
- Snapshot is an optimization/baseline, never a replacement for event history.
- Child branches never mutate parent history.
- Duplicate command retries never duplicate world effects.
- Stale branch revision is rejected with a typed conflict.

## Engineering rules

- Modular monolith; no microservices/Kafka/NATS/Redis/K8s in this batch.
- Domain layer must not import FastAPI/SQLAlchemy/Alembic/LLM SDKs.
- Persistence (ORM) stays in the persistence package; higher layers use ports.
- No global mutable singletons; constructors do no hidden I/O.
- Production files target <= 300 lines; split by concern.
- No TODO/placeholder/NotImplemented/mock-only path may be counted as completion.
- No LLM API key is required for core tests.
- Do not push remote or deploy unless explicitly authorized.

## Goal protocol

1. Read Goal + dependencies; 2. mark ACTIVE in PLAN/STATUS; 3. tests early;
4. implement smallest complete architecture; 5. run quality gates; 6. write
`reports/goal_<id>_report.md`; 7. update ledgers; 8. local commit `goal <id>: ...`
only after PASS; 9. continue to next Goal. Stop after M1 PASS.
