# M3 Qualification — Bounded Agents Can Live Inside the World

> Phase: P3 — Agency, Cognition and Action Runtime  
> Run after `G03G` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P3 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Use a deterministic synthetic scenario with at least two actors and one organization. One actor observes a private/partial event, forms a belief, later receives a correction, executes a multi-step skill, and changes a bounded capability. Another actor must not receive knowledge they never observed or were not told.

## Required Proofs

- Observation, belief, memory and canonical truth are separate data concepts.
- Temporal epistemic graph preserves contradiction/correction lineage.
- Actors and organizations propose through policies; no policy owns Commit Authority.
- Affordances and ActionValidator reject unreachable, unauthorized or epistemically impossible actions.
- Resolver outputs auditable adjudication/proposed deltas with version/seed provenance.
- Skill execution is resumable and every step still passes normal validation.
- Capability change requires declared practice/assessment evidence and remains bounded.
- Knowledge-leakage and deterministic policy tests pass.

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
- `reports/M3_ACCEPTANCE.md`
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
- record exact hash in `reports/M3_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M3 PASS, continue automatically to `G04A`. Do not ask the user for routine confirmation.
