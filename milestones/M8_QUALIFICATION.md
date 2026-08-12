# M8 Qualification — Mechanistic External Models Can Participate Without Owning Canonical State

> Phase: P8 — Co-Simulation and Strategy  
> Run after `G11F` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P8 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Run a synthetic campaign with at least two deterministic fake simulators operating at different rates, organization orders, logistics/resource flow, movement constraints and fog-of-war; then execute batch experiments across multiple seeds/variants.

## Required Proofs

- SimulationAdapter implements the complete declared contract including checkpoint/restore/assumptions/validity.
- Adapters receive slices/snapshots and only emit events/proposed deltas.
- Multi-rate/event-driven ordering is deterministic and restartable.
- Conflicting simulator proposals are adjudicated explicitly.
- Campaign logistics/position/resource invariants hold.
- Faction observations/beliefs respect fog-of-war.
- Batch results are distributions with verification/validation/ValidityEnvelope metadata.
- Liaoshen real pack never fabricates missing history and may be EXTERNAL_BLOCKED without blocking generic M8.

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
- `reports/M8_ACCEPTANCE.md`
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
- record exact hash in `reports/M8_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M8 PASS, continue automatically to `G12A`. Do not ask the user for routine confirmation.
