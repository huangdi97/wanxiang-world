# Release Readiness ? Wanxiang v5.0-R1 (M0-M17)

Status: **READY for controlled local release; remote push/tag/deploy requires explicit user authorization.**
Version proposal: `v5.0-R1-rc1` (release candidate; application version `0.1.0`).

## Version freeze (proposal)
- Freeze target: `v5.0-R1` (release candidate `rc1`). Local milestone checkpoint tag: `m17-final-certification`.
- The release version tag (e.g., `v5.0-R1-rc1`) is **proposed, not created**: per G20E, no automatic
  push/tag/deploy without user authorization. Nothing was pushed to any remote.
- Release notes (summary): deterministic event-sourced world core with Commit Authority only; 16
  kernels / 5 planes; 44 v5.0-R1 requirements (42 VERIFIED, 2 EXTERNAL_BLOCKED, 0 GAP); SQLite profile
  with backup/restore/replay; public SDK + FastAPI transport; product surfaces over one server truth;
  M16 research tracks behind OFF flags.

## Tested environments (exact)
| Environment | Result |
|---|---|
| Windows / PowerShell; Python 3.12 via uv; SQLite profile | 640 pytest passed + 1 EXTERNAL_BLOCKED skip |
| ruff check + ruff format | PASS |
| pyright strict | 0 errors |
| architecture_check (forbidden imports/cycles/size/secrets/placeholders) | PASS |
| TypeScript SDK (packages/sdk_ts): tsc --noEmit, eslint, vitest | 22 tests passed |
| Clean-room build/install/upgrade/restore/replay (`scripts/clean_room_certify.py`) | PASS (7/7 steps) |
| Final security/reliability/chaos re-run (`scripts/security_reliability_certify.py`) | PASS (65 curated tests) |
| Black-box final acceptance (`scripts/blackbox_final_acceptance.py`) | PASS (author/operator/end-user/surfaces) |
| PACK_MANIFEST.md integrity | 94/94 entries verified (sha256 + size) |

## Evidence (final M17 gate)
- `uv run python scripts/quality.py` -> 640 passed, 1 skipped, ruff/pyright/architecture PASS.
- `npm run typecheck && npm run lint && npm test` (packages/sdk_ts) -> 22 passed.
- `reports/M17_FINAL_CERTIFICATION.md`, `reports/FINAL_PROGRAM_COMPLETION_REPORT.md`,
  `reports/M17_ACCEPTANCE.md`, `reports/CLEAN_ROOM_CERTIFICATION.md`,
  `reports/FINAL_SECURITY_RELIABILITY_CERTIFICATION.md`, `reports/BLACKBOX_FINAL_ACCEPTANCE.md`,
  `reports/FINAL_DESIGN_TRACEABILITY.md`.

## Known limitations / EXTERNAL_BLOCKED (explicit, not completed)
1. Real renderers (Phaser/Godot/Babylon) and digital-human/XR presence ? WX-PRJ-8.2-003 (external devices).
2. Real Red Chamber / Liaoshen / family / heritage source data and real IIIF endpoints ? WX-SRC-EXTERNAL-001 (licensed data).
3. Live PostgreSQL profile (PITR/WAL) ? requires a real instance; SQLite is the certified deterministic path.
4. Real object storage, SSO/vuln-scanning services, real LLM providers, real authorized sensor feeds, real multi-node hosting ? EXTERNAL_BLOCKED.
5. No real-person likeness/voice without an approved fixture (rights-first).

## Research decisions (M16) ? v5.1/v6
See `docs/POST_V5_ROADMAP.md`. All 10 research tracks executed with evidence; 9 KEEP_EXPERIMENTAL
(v5.1/v6 candidates), 1 REJECT (distributed hosting: 2.2x overhead, no correctness gain).

## Release candidate reproduction
- The release candidate is reproducible from the local Git checkpoint at tag `m17-final-certification`
  (final HEAD). Clean-room certification (build_manifest reproducible, sha == HEAD) passed.
- PACK_MANIFEST.md (94 files) verified at final HEAD.

## Awaits user decision
- Authorize creating/tagging/pushing the release version (proposed `v5.0-R1-rc1`) if desired.
- Authorize any promotion of M16 research tracks (none are stable by default).
