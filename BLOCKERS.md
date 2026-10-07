# Blockers ? Wanxiang Engineering Program

Updated 2026-10-07: R7 locally executable implementation is closed at
`f7b719d` with green CI and exact-SHA qualification. Remaining
open rows are genuine human/external qualification or older unrelated corpus
work; they are not converted into implementation work.

| Date | Goal | Type | Description | Status |
|---|---|---|---|---|
| 2026-08-15 | G35A | EXTERNAL | Real《红楼梦》full-text edition: no legal/traceable public-domain text in the environment (read-only, no network/rights-verification); needs URI/checksum/edition/rights-grant before any Canon compilation; no model-memory canon | OPEN (unblocks M36/M37 real-corpus work) |
| 2026-08-15 | G38A (resolved) | INTERNAL | v5.2 M30-M34 remediation COMPLETE + G38A re-run PASS (M34 V5_2_PLATFORM_PASS). M35 kernel freeze certified. | CLOSED (2026-08-15) |
| 2026-08-14 | G16B (carried) | EXTERNAL | Live PostgreSQL instance was unavailable on the original host. | CLOSED for current R7 qualification (2026-10-07): GitHub Actions starts PostgreSQL 16 and the live profile passes 4/4; historical host limitation remains documented |
| 2026-08-28 | G98A / M95 | EXTERNAL | Host Git had no HTTPS remote helper, so `git fetch`/`ls-remote` could not refresh refs. | CLOSED (2026-09-25): `git ls-remote --heads origin` and a non-force push of `release/v5.5-stable-certification` both succeed; see `artifacts/v55_stable/m100/remote_delivery.json` |
| 2026-08-28 | G98A / M95 | INPUT | The exact v5.5 master filename named by the Stable execution prompt was absent from this checkout. | CLOSED (2026-09-25): the canonical R7 design master and its Goal are now tracked in-repo; the older v5.5 master filename is superseded and was never guessed |
| 2026-08-29 | G98D/G98E / M95 | INPUT | No genuine human player session, ratings, notes, or blocker reproduction has been supplied; the automated route is not human acceptance. | OPEN as `WAITING_HUMAN` (Gates 62?66 = `USER_INPUT_REQUIRED`); requires a real tester to complete `reports/M95_PLAYER_TEST_PACKET_ZH_CN.md` |
| 2026-08-29 | G103E / M100 | EXTERNAL | Candidate release branch and candidate Actions run were absent from the public GitHub query. | CLOSED (2026-09-25): remote branch present at `a9be096`, exact-SHA run `36194471592` succeeded with every workflow-declared job green |
| 2026-08-29 | G103G/G103H / M100 | RELEASE | Gate 80 is `LOCKED`; no `v5.5.0` tag or GitHub Release exists, so tag-based post-release verification is not applicable. | OPEN: Gate 79 is now `PASS`; the only blockers are Gates 62?66 (`WAITING_HUMAN`). No tag/release will be created without the user's explicit confirmation |
| 2026-09-26 | R7 / Phase B | SCOPE | Cordis-native R7 implementation and qualification. | CLOSED (2026-10-07): all locally executable R7 Goal slices implemented; Gates A–J PASS within declared bounded/reference scopes; see `reports/r7/15_R7_FINAL_CLOSURE_REPORT.md` |
| 2026-09-25 | R7 / Phase B | EXTERNAL | Godot/real-engine E2E remains unavailable on this host. Live PostgreSQL is now qualified in CI. | OPEN only for Godot / Gate 78 `EXTERNAL_BLOCKED`; PostgreSQL row closed by run `37582984372` |
| 2026-09-26 | R7 / DSH | EXTERNAL | Live model-backed official DeepSeek Harness runtime/credentials are not available. | OPEN as `EXTERNAL_BLOCKED` for live E2E only; official SDK adapter + protocol/bridge/reference harness are implemented and tested |
