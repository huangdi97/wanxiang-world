# Codex Tonight Master Execution Prompt — Wanxiang P0 + P1

> This is the executable controller for the first long engineering batch.  
> Scope: Engineering Constitution + Authoritative World Foundation only.  
> Stop condition: M1 Authoritative World Acceptance PASS, or a genuine unrecoverable external environment blocker that prevents even deterministic local engineering work.

---

## COPY THE BLOCK BELOW INTO CODEX DESKTOP

Read the repository and all required program documents before changing production code.

Normative reading order:

1. `docs/spec/WANXIANG_v5_MASTER_SPEC.md`
2. `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md`
3. `02_ENGINEERING_STANDARDS.md`
4. `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`
5. `AGENTS.md` if present
6. `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
7. all Goal files listed below
8. current repository tree, git status, git log, existing tests and configuration

Do not infer product requirements from old chat history. The v5 master spec is the product Source of Truth. The Engineering Program Architecture controls implementation order and acceptance.

### Objective for this execution batch

Build and verify the engineering foundation and the authoritative deterministic world kernel up through Milestone M1. The result must be a maintainable foundation on which Living World Substrate can safely be built later.

### Execute these Goals continuously and in order

1. `goals/GOAL_00A_REPOSITORY_FOUNDATION.md`
2. `goals/GOAL_00B_ARCHITECTURE_GUARDS.md`
3. `goals/GOAL_01A_CORE_CONTRACTS.md`
4. `goals/GOAL_01B_COMMIT_AUTHORITY.md`
5. `goals/GOAL_01C_EVENT_STORE.md`
6. `goals/GOAL_01D_REPLAY_BRANCH.md`
7. `goals/GOAL_01E_PERSISTENCE_MIGRATION.md`
8. `goals/GOAL_01F_MINIMAL_WORLD_VERTICAL_SLICE.md`

Do **not** begin G02 living substrate, cognition, Studio, Phaser, real Red Chamber, family, museum, campaign, Reality Bridge or Co-Simulation after finishing this batch. Stop after the M1 acceptance report and checkpoint are complete.

### Non-negotiable runtime invariants

- LLMs, clients, rules, humans, sensors and simulators never directly mutate Canonical World State.
- All required canonical changes flow through validation/resolution as applicable and Commit Authority.
- Canonical history is event-sourced and replayable.
- Snapshot is an optimization/baseline, not a substitute for event history.
- Branch writes never mutate parent branch history.
- Duplicate command retry cannot duplicate world effects.
- Stale branch revision cannot silently overwrite later state.
- Domain/World/Scenario/Instance/Branch/Session/Projection terminology must not be collapsed.
- Specific worlds are never hard-coded into Core.
- Core tests must run without an LLM key.
- No TODO, placeholder, NotImplemented, static JSON response or mock-only path may be used to claim completion.

### Engineering behavior

For routine technical decisions, choose the simplest maintainable option consistent with the documents and record non-trivial decisions in `DECISIONS.md` or an ADR. Do not interrupt for ordinary library/layout choices.

If the repository is empty or incomplete, initialize it according to Goal 00A. If equivalent mature tooling already exists, preserve it when it satisfies the contracts; do not rewrite merely for preference.

Maintain a modular monolith. Do not introduce microservices, distributed queues, Kafka/NATS/Redis or Kubernetes in this batch.

### Code quality

Enforce the engineering standards, including:
- small cohesive modules;
- default production file target <= 300 lines;
- no growing generic manager/service/utils dumping grounds;
- domain layer independent of FastAPI/SQLAlchemy/LLM SDKs;
- explicit ports at persistence/external boundaries;
- typed public APIs;
- explicit error taxonomy;
- no hidden global mutable singleton;
- constructors without hidden I/O;
- no business logic in transport routes;
- no direct ORM mutation from runtime/domain/plugin callers;
- migrations for persisted schema changes;
- schema/version metadata for persisted/external contracts;
- structured logs/audit with secrets/private payload protection.

If existing code violates these constraints and lies on the path required by this batch, refactor it as part of the relevant Goal rather than layering new code on top of poor structure.

### Goal execution protocol

For each Goal:

1. read the entire Goal file and dependencies;
2. inspect existing implementation and tests;
3. update `PLAN.md` / `STATUS.md` to mark the Goal ACTIVE;
4. write/adjust tests early enough to drive invariant behavior;
5. implement the smallest complete architecture that satisfies Scope;
6. run Goal-specific tests frequently;
7. run lint/typecheck/architecture/migration checks as applicable;
8. fix internal failures; do not skip/delete tests to proceed;
9. inspect changed files for poor cohesion, duplication, dead code, generic dumping grounds and architecture leakage;
10. refactor before acceptance when needed;
11. run the Goal acceptance commands;
12. write `reports/goal_<id>_report.md` with concrete evidence;
13. update `STATUS`, `PLAN`, `DECISIONS`, `BLOCKERS`, `KNOWN_FAILURES`, `CHANGELOG`;
14. create a local final checkpoint commit `goal <id>: <summary>` only after PASS;
15. automatically continue to the next Goal.

Do not push to a remote and do not deploy production.

### Blocker handling

Treat failing tests, type errors, architecture violations, migration errors, missing internal modules and resolvable ambiguities as internal engineering problems. Resolve them; do not ask the user.

Only mark `EXTERNAL_BLOCKED` for genuine external dependencies (private data, permissions, credentials, unavailable external systems/hardware) after the internal interface/fake/test path is complete. This P0/P1 batch should require no external data or LLM key, so external blocking should be rare.

### M1 final qualification

After Goal 01F, run a dedicated M1 system acceptance using a clearly synthetic micro-world. It must prove the entire authoritative path, not isolated mocks:

```text
instantiate deterministic synthetic world
→ submit valid command
→ validate
→ resolve
→ produce ProposedWorldDelta
→ atomic Commit Authority
→ ordered event persisted
→ branch revision advanced
→ query canonical state
→ create snapshot
→ commit more events
→ discard/rebuild derived current state
→ restore snapshot + replay remaining events
→ compare final canonical semantic hash
→ fork child branch
→ commit child-only mutation
→ prove parent unchanged
→ retry duplicate command
→ prove no duplicate effect
→ submit stale-revision command
→ prove structured conflict and no mutation
```

Also test at least one rejected invalid command and one corrupt/incompatible replay fixture.

Run the complete quality suite on the final tree.

Create:
- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`
- updated `reports/ACCEPTANCE_MATRIX.md`
- `docs/IMPLEMENTATION_STATUS.md` section for M0/M1

M1 is PASS only if deterministic acceptance succeeds without an LLM key and no required test is skipped.

### Final stop

When M1 PASS is complete:
- update `STATUS.md` to show M0 and M1 PASS;
- ensure working tree is clean except intentionally documented artifacts;
- create final local checkpoint commit if required by the Goal/report sequence;
- summarize implemented capabilities, key ADRs, tests, limitations and the next dependency (`G02A Spatial Topology & Access`);
- STOP. Do not autonomously start the next phase.
