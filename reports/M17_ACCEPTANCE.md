# M17 Acceptance ? Final Independent Certification

## Verdict
**PASS** ? Post-M9 program complete. Stable P0/P1 = 0; clean-room, security/reliability, black-box
author/user/operator and final traceability all PASS; release readiness bundle complete.

## Required qualification actions (per milestones/M17_QUALIFICATION.md)
| Action | Result |
|---|---|
| 1. Re-read milestone Goal reports + blockers | PASS ? G20A-E reports; BLOCKERS/KNOWN_FAILURES empty (no open internal P0/P1) |
| 2. Broad regression set | PASS ? `uv run python scripts/quality.py`: 640 pytest + 1 EXTERNAL_BLOCKED skip + ruff + pyright + architecture |
| 3. Architecture/type/lint/drift | PASS ? architecture PASS; pyright 0 errors; ruff clean; SDK TS typecheck/lint/22 tests |
| 4. Replay/branch/determinism | PASS ? golden replay; G20B backup/restore/replay; G20D branch/replay; G20C flags-on replay determinism |
| 5. Rights/security/source | PASS ? G20C curated 65 tests (0 failed); G20D author rights/no-Core; rights/source rows VERIFIED |
| 6. ACCEPTANCE_MATRIX + traceability | Done ? M17 rows appended; final traceability 44 rows, 0 GAP |
| 7. M17_ACCEPTANCE.md | This file |

## Gate-specific PASS condition
MET: stable P0/P1 = 0; clean-room, security/reliability, black-box and final traceability all PASS;
release readiness bundle complete (docs/RELEASE_READINESS.md, docs/POST_V5_ROADMAP.md,
PACK_MANIFEST 94/94 verified).

## Evidence (exact commands)
- `uv run python scripts/quality.py` -> 640 passed, 1 skipped (EXTERNAL_BLOCKED live PostgreSQL),
  ruff/pyright/architecture PASS.
- `npm run typecheck && npm run lint && npm test` (packages/sdk_ts) -> 22 passed.
- `uv run python scripts/clean_room_certify.py` -> exit 0, 7/7 steps PASS.
- `uv run python scripts/security_reliability_certify.py` -> exit 0, 65 curated tests PASS.
- `uv run python scripts/blackbox_final_acceptance.py` -> exit 0, 4 personas PASS.
- `uv run python scripts/traceability.py` -> 44 requirements / 63 goals / 16 kernels, validation clean.

## Residual risks / limitations
- External blockers explicit and narrow: real renderers/XR (WX-PRJ-8.2-003), real licensed source data
  (WX-SRC-EXTERNAL-001), live PostgreSQL/PITR, real providers/object storage/SSO/multi-node. None are
  claimed as completed.
- M16 research stays experimental behind OFF flags; promotion requires further evidence and user
  authorization (distributed hosting REJECTED ? ADR 0055).

## Stop rule
Program stops at the local checkpoint (tag `m17-final-certification`); release version tag
(`v5.0-R1-rc1`) is proposed and awaits user authorization. No remote push/deploy was performed.

## Environment
Windows/PowerShell; Python 3.12 via uv (cache `.uv-cache`); SQLite profile; Node for SDK TS.
