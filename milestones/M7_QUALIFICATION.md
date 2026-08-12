# M7 Qualification — Multiple Unrelated Domains Prove Core Generality

> Phase: P7 — Domain Generality Qualification  
> Run after `G10D` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P7 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Pass system qualification using at least three unrelated domain families: synthetic mansion/literature, family genealogy/archive, and heritage/museum. Real Red Chamber data is used only if Source Gate allows it.

## Required Proofs

- Synthetic mansion passes seven-day persistence/control/knowledge/material/branch checks without Core hacks.
- Family supports GEDCOM round-trip profile, source retention, conflicting claims and living-person privacy.
- Family persona modes clearly distinguish evidence/reconstructed/creative outputs and enforce revocation.
- Heritage supports IIIF references plus selected Linked Art/CIDOC mapping profile.
- Physical object, digital surrogate, semantic twin and reconstruction remain distinct.
- Object biography/conservation history is replayable and rights/cultural protocols are enforced.
- Domain-specific rules remain plugins/packages above Core.
- Real-source slices may be EXTERNAL_BLOCKED, but Source Gate negative/positive fixture behavior must PASS.

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
- `reports/M7_ACCEPTANCE.md`
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
- record exact hash in `reports/M7_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M7 PASS, continue automatically to `G11A`. Do not ask the user for routine confirmation.
