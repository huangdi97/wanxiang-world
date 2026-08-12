# M6 Qualification — Reality-Coupled Context and Controlled Experiments Work Safely

> Phase: P6 — Reality, Opportunities, Director and Experiments  
> Run after `G07E` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P6 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Feed deterministic fake physical observations with duplicates/conflicts into Reality Bridge, fuse them, generate at least one opportunity/challenge, let a Director propose an external event under constraints, and run a multi-seed experiment from a fixed baseline.

## Required Proofs

- PhysicalObservation remains observation, never direct truth.
- Fusion preserves conflicting inputs/provenance and emits only claims/proposals.
- ChallengeSpec includes executable prerequisites, safety/rights/evidence and verifiable outcome requirements.
- Director layers cannot directly commit or rewrite actor beliefs/personality.
- Experiment branches never mutate baseline.
- Results include run/seed/version metrics, assumptions and ValidityEnvelope.
- Same deterministic experiment spec reproduces the same result set.
- All proposals still traverse normal validation/adjudication/commit.

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
- `reports/M6_ACCEPTANCE.md`
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
- record exact hash in `reports/M6_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M6 PASS, continue automatically to `G08A`. Do not ask the user for routine confirmation.
