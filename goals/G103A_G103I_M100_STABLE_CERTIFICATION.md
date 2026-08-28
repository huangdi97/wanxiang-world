# G103A–G103I — M100 v5.5 Stable Certification

## G103A — Aggregate Stable gates
Read Gates 61–79 from evidence, never from manually edited status alone. Build a consistency guard analogous to the RC latest-authoritative-qualification rule. Gate 80 stays LOCKED until predicate true.
Commit: `g103a: aggregate v5.5 stable acceptance evidence`

## G103B — RC burn-in + full regression
Run the repository's full applicable Python/TS quality, architecture/kernel guards, migrations, package/API/SDK, Playable/Studio, release-build, safety and critical v5.4/v5.5 regressions. Preserve the live PostgreSQL external boundary if environment is absent.
Commit: `g103b: complete v5.5 stable full regression`

## G103C — Semantic invariants / rights / security
Explicitly requalify Source/Canon immutability, provider proposal-only, replay/branch/recovery, rights/privacy/security/resource controls and private-source/secret scans. No private source export.
Commit: `g103c: requalify stable semantic and safety invariants`

## G103D — Clean clone certification
From a clean isolated clone of the exact candidate SHA, install all groups/packages, migrate, quickstart, lineage/replay, clean-room, Studio/CLI/API and TypeScript/Python gates. Record migration head and candidate SHA.
Commit: `g103d: certify v5.5 stable clean clone`

## G103E — Remote delivery / required CI
Push release branch without force. Verify remote SHA == local HEAD and every required GitHub Actions job succeeds. Do not create tag if any required job fails or is missing.

## G103F — Stable release notes / evidence boundary
Create release notes that explicitly separate IMPLEMENTED / VALIDATED / EXPERIMENTAL-BOUNDED / NOT_PROVEN / EXTERNAL_BLOCKED. Preserve v5.4 and rc1 identity and historical NOT_ACCEPTED evidence.
Commit: `g103f: prepare v5.5 stable release evidence`

## G103G — Stable tag and Release
Only when Gates 61–77 and 79 are ACCEPTED and Gate 78 is acceptable optional status:
- create annotated `v5.5.0` at the exact accepted candidate commit;
- push tag without force;
- create GitHub Release non-draft, non-prerelease;
- set Gate 80 to `ACCEPTED_FOR_STABLE` only after remote identity is verified.

## G103H — Post-release verification
Fresh checkout of `v5.5.0`; install/migrate/quickstart/replay/clean-room/Studio/TS/Python/release artifact checks. Verify `v5.4.0` and `v5.5.0-rc1` remain unchanged.

## G103I — Final report and STOP
Write:
- `reports/V55_STABLE_RELEASE_REPORT.md`
- final machine-readable stable evidence artifact
- final matrix with Gate 80 result
- STATUS/CHANGELOG only as appropriate

Final statement must say whether Prompt Genesis/long-horizon/World Lab/emergence remain EXPERIMENTAL/BOUNDED, whether Godot was real or external-blocked, and whether live PostgreSQL was actually verified.

Then STOP. Do not enter v5.6. Do not train a Wanxiang-owned model. Do not create a v5.6 branch automatically.
Commit: `g103i: finalize v5.5 stable certification`
