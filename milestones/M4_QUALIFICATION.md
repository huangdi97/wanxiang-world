# M4 Qualification — Worlds Can Be Authored, Reviewed, Installed and Instantiated

> Phase: P4 — World Definition, Evidence and Packages  
> Run after `G04E` PASS.  
> This gate is system-level and must exercise real internal paths, not isolated mocks.

## Objective

Prove that the combined capabilities delivered in P4 satisfy the master specification without regressing M1 or earlier milestones.

## Mandatory Scenario

Author a synthetic Domain Pack + World Pack + Scenario using supported JSON/YAML/Markdown inputs, run them through Source/Review/Compiler/Registry, install them, instantiate a pinned world, export/re-import, then publish a v2 package without silently mutating the v1 instance.

## Required Proofs

- Package hierarchy and dependency/version resolution are deterministic.
- Untrusted executable extensions are denied by default.
- Source Gate blocks unapproved/rights-denied/malicious content from canonical compilation.
- Conflicting claims survive as separate evidence-backed candidates.
- Compiler MVP supports only declared formats; unsupported PDF/OCR/video is explicit, not faked.
- Canon/completion/model/reconstruction/user-fiction labels are preserved.
- Install/export round-trip works and package hashes/version pins are checked.
- Package/schema migration compatibility is tested.

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
- `reports/M4_ACCEPTANCE.md`
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
- record exact hash in `reports/M4_ACCEPTANCE.md`;
- do not push unless explicitly requested.

## Continuation

If M4 PASS, continue automatically to `G05A`. Do not ask the user for routine confirmation.
