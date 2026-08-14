# Codex Master Prompt — Wanxiang v5.1 Minimal-Core Consolidation & Migration, M18 → M25

## Mission

Upgrade the already-built Wanxiang repository from the verified v5.0/M0–M17 implementation to the v5.1-R1 mother specification **without a greenfield rewrite**, while reducing duplicate architecture and keeping the permanent core as small, readable, upgradeable and testable as possible.

Execute every Goal in `06_V5_1_GOALS_INDEX.md` in order and every Milestone Gate M18–M25. Do not stop for routine confirmation.

## Source of truth

Highest product/architecture authority:

`docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`

Engineering execution authority for this migration:

- this master prompt;
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`;
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`;
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`;
- current Goal;
- milestone qualification.

Existing M0–M17 engineering standards remain in force when not superseded by a stricter v5.1 rule.

## Start protocol

Before changing production code:

1. inspect Git status/history and repository layout;
2. read M17 certification/release-readiness artifacts if present;
3. run the narrow critical regression proving Commit/Event/Replay/Branch/Persistence/Host/Package/SDK still work;
4. create `reports/V5_1_PRE_MIGRATION_BASELINE.md` with commit hash, schema versions, event fixture hashes, package fixture hashes, test commands/results and known blockers;
5. do not trust old PASS labels without reproducible evidence.

If M17 is materially broken, repair baseline regressions first and document them. Do not reimplement M0–M17 when healthy.

## Change classification rule

Every meaningful existing implementation encountered in M18 must be classified:

`KEEP_AS_IS | KEEP | MERGE | ADAPT | DELETE | REPLACE | EXPERIMENTAL`.

`REPLACE` requires an ADR explaining why adaptation cannot preserve the v5.0 contract safely.

## Minimal-code rule

A new abstraction is allowed only if it does at least one of the following:

- carries a new irreducible v5.1 semantic contract;
- replaces/merges two or more duplicate concepts;
- isolates an unstable/external provider boundary;
- is required to preserve version/migration/replay compatibility;
- materially improves testability without duplicating behavior.

Do not create classes/services/packages merely because their names appear in the design document.

## Absolute invariants

- one world mutation boundary;
- one authoritative committed history;
- no LLM/UI/Director/Sensor/Simulator/Provider/Compiler direct canonical mutation;
- child branch cannot mutate parent;
- committed history is not silently rewritten;
- v5.0 event histories remain replayable or have explicit deterministic migration;
- Runtime Effect and World Effect remain separate;
- package/provider/runtime upgrades cannot bypass Evidence/Rights/Security/Invariant checks;
- core tests do not require external LLM/API keys.

## Commit semantics

Implement exactly three **World** commit kinds through one pipeline:

`STATE | ONTOLOGY | LAW`.

Do **not** implement `CapabilityCommit` as a fourth World Commit. Runtime provider changes are `RuntimeControlTransaction` records.

## Physical architecture rule

Do not force a directory rewrite if current modules already satisfy the target dependency boundaries. Prefer import-boundary enforcement and selective moves over repository-wide renames.

Never create 16 services for the 16 logical kernels. Never create three giant Meaning/Reality/Experience services.

## Capability runtime rule

Runtime composition must be typed and explicit. A central composition root may resolve/construct providers, but domain/runtime business code must not repeatedly query a global service locator.

## Continuous execution

For each Goal:

1. read it fully;
2. inspect relevant implementation/tests;
3. update PLAN/STATUS;
4. implement smallest coherent change;
5. delete superseded/dead code in the same Goal when safe;
6. run focused tests and applicable architecture/type/lint/migration/replay checks;
7. update traceability and code-minimality inventory;
8. write the Goal report;
9. update DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG;
10. create local Git checkpoint only after acceptance passes;
11. continue automatically.

At each milestone execute its qualification file. PASS continues automatically.

## External blockers

Missing real Red Chamber/Liaoshen/family/heritage sources, provider credentials, real sensors, commercial digital-human services or unavailable hardware may be `EXTERNAL_BLOCKED` for that narrow integration only. Generic contracts, deterministic fakes, source gates, rights/security tests and synthetic qualification must still be completed.

## Never fake completion

Do not count as completion:

- interface without a used implementation;
- route returning static JSON;
- test-only fake on a mandatory production path;
- TODO/FIXME/pass/NotImplemented in acceptance path;
- renamed old code without semantic migration;
- a new registry that simply wraps an old registry;
- a new Engine facade with no required behavior;
- benchmark/report text without reproducible command/evidence.

## Git

Local commits are required after passing Goals. Do not push, force-push, deploy, publish packages or mutate external systems unless separately authorized by the user.

## Final stop

Stop only after M25 qualification and final reports are complete, including:

- `reports/V5_1_FINAL_TRACEABILITY.md`
- `reports/V5_1_BACKWARD_COMPATIBILITY.md`
- `reports/V5_1_MINIMAL_CORE_AUDIT.md`
- `reports/V5_1_REPLAY_MIGRATION_CERTIFICATION.md`
- `reports/V5_1_CROSS_DOMAIN_CERTIFICATION.md`
- `reports/M25_V5_1_FINAL_CERTIFICATION.md`
- `reports/V5_1_PROGRAM_COMPLETION_REPORT.md`
- `docs/V5_1_IMPLEMENTATION_STATUS.md`
- `docs/V5_1_RELEASE_READINESS.md`

Stable P0/P1 gaps must be zero. Experimental/External-Blocked items must be explicit and not described as stable completion.
