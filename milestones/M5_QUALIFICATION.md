# M5 Qualification — Human Can Enter a Persistent World Without Becoming the Authority

> Phase: P5 — Host, Human Control and Projection  
> Run after `G06C` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P5 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Run a hosted synthetic world with Studio and Phaser clients. Acquire an embodiment lease, take over one actor, commit actions, release control, allow the AI/deterministic policy to resume, disconnect all clients while the world continues, restart the process, reconnect, and verify authoritative continuity.

## Required Proofs

- WorldHost is an orchestration boundary, not a second Commit Authority.
- Exactly one primary embodiment controller exists per actor.
- ShadowPolicy cannot compete for authoritative body control.
- Projection filters enforce knowledge/rights server-side.
- Studio edits and Phaser movement use command APIs and cannot mutate client-local truth into canonical truth.
- Lifecycle modes persist independently of sessions.
- Multi-client retries/conflicts remain idempotent and revision-safe.
- Crash recovery, lease recovery and scheduler restoration preserve canonical semantic hash.

## Required Regression

Run all applicable:
- M1 authoritative commit/event/replay/branch/idempotency/stale-revision qualification;
- every earlier milestone's synthetic acceptance scenario or its stable automated regression equivalent;
- architecture conformance tests;
- persistence/migration/replay compatibility;
- rights and projection leakage tests;
- no-LLM deterministic test profile;
- lint/typecheck/build;
- changed-file/file-size/cohesion audit;
- TODO/FIXME/NotImplemented/placeholder scan in milestone-owned production paths;
- secret/private-data scan.

## Evidence

Create:
- `reports/M5_ACCEPTANCE.md`
- update `reports/ACCEPTANCE_MATRIX.md`
- update `docs/IMPLEMENTATION_STATUS.md`
- update `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`

Every criterion must be labeled `PASS`, `FAIL`, `EXTERNAL_BLOCKED` or `NOT_APPLICABLE`, with command/test/path evidence.

## Milestone Verdict Rules

- Internal platform criteria must be PASS. Do not use `EXTERNAL_BLOCKED` for engineering work that can be implemented locally.
- A real-data/real-hardware/third-party-service slice explicitly allowed by the Goal may be `EXTERNAL_BLOCKED` if the interface, fake/fixture, negative gate and all local behavior are complete.
- A failing earlier milestone regression makes this milestone FAIL until repaired.
- Do not weaken old tests to reach PASS.

## Git Checkpoint

After PASS:
- create a local milestone checkpoint/tag or commit according to repository convention;
- record exact hash in `reports/M5_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M5 PASS, continue automatically to `G07A`. Do not ask the user for routine confirmation.
