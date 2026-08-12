# M9 Qualification — Release-qualified Wanxiang Platform Foundation

> Phase: P9 — Release Qualification and Advanced Adapters  
> Run after `G12H` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P9 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Run complete release qualification: long-duration synthetic world, full regression from M1-M8, backup/restore/migrations, SDK generation/examples, research/projection/foundry/digital-human adapter contracts, and supported local/private deployment security checks.

## Required Proofs

- At least 30 in-world days and 1000+ commit/scheduler cycles complete with no invariant failure and bounded resource growth.
- Backup restored into a clean environment reproduces canonical hashes and old fixture databases migrate/replay.
- OpenAPI/TypeScript SDK generation is reproducible; public API vocabulary/version policy is documented.
- Gymnasium/PettingZoo adapters preserve authority and epistemic filtering when optional dependencies are installed.
- Godot/Babylon projection contracts, Asset Foundry and Digital Human/XR gateways remain non-authoritative.
- Rights prevent unauthorized asset/voice/face generation calls.
- Security tests cover secrets, uploads/source injection, admin/debug/private/export access and audit protection.
- Fresh-clone local startup/runbook works; external-only environment checks are explicitly labeled rather than falsely passed.
- Complete architecture, migration, replay, source-gate, rights, projection-leakage and long-run regression matrix is green.

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
- `reports/M9_ACCEPTANCE.md`
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
- record exact hash in `reports/M9_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M9 PASS, continue automatically to `FINAL RELEASE REPORT`. Do not ask the user for routine confirmation.
