# M2 Qualification — Deterministic Living World Exists

> Phase: P2 — Living World Substrate  
> Run after `G02F` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P2 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Run a source-neutral synthetic house/micro-town for at least 72 in-world hours with multiple actors, rooms/portals, schedules, material objects, a sealed information payload, body constraints, duties/permissions and background population scheduling.

## Required Proofs

- World time is monotonic and can pause/advance without wall-clock dependence.
- Spatial reachability, access, capacity and occupancy invariants hold.
- Material custody/ownership/container state is conserved; acquiring a sealed message does not imply reading it.
- Body/condition state can block or alter an otherwise valid action/schedule.
- Institution roles/duties/permissions affect allowed actions.
- With no user input, scheduler advances the world deterministically under resource budgets.
- Snapshot/replay/branch/idempotency/stale-revision invariants from M1 remain green.
- Same initial snapshot + seed + versions yields identical final semantic hash and ordered committed events.

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
- `reports/M2_ACCEPTANCE.md`
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
- record exact hash in `reports/M2_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M2 PASS, continue automatically to `G03A`. Do not ask the user for routine confirmation.
