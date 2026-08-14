# V5.1 Pre-Migration Baseline — v5.0/M17 Freeze

Generated: 2026-08-14 (G21A)
Status: FROZEN — this file records the reproducible pre-v5.1 state of the repository.

## 1. Git baseline

- Branch: `master`
- HEAD commit: `436ee3dd7a8c4601d44c04bce9dec5519dad305d` — `docs: add m17 acceptance report and acceptance matrix rows`
- Local tag at baseline: `m17-final-certification`
- Working tree: tracked tree clean; untracked = v5.1 program pack (README_FIRST_V5_1.md, 00–09 program docs, docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md, goals/GOAL_G21A..G28I, milestones/M18..M25, CODEX_COPY_PASTE_V5_1.txt, WANXIANG_V5_1_MINIMAL_CORE_M18_M25_ALL_IN_ONE.md)
- No remote configured push/deploy performed. Nothing pushed.

## 2. Environment

- Windows/PowerShell; Python 3.12.7 (`.venv`); uv 0.9.18; Node for TS SDK.
- uv cache redirected to repo-local `.uv-cache` for this run (user-level uv cache was sandbox-blocked; not a product issue).

## 3. Quality gate (M17 baseline re-verified, not trusted from memory)

Command: `uv run python scripts/quality.py` (with `UV_CACHE_DIR=E:\AI\wanxiang\.uv-cache`)

| Check | Result |
|---|---|
| ruff check . | All checks passed |
| ruff format --check . | 1087 files already formatted |
| pyright (strict) | 0 errors, 0 warnings, 0 informations |
| pytest -q | 640 passed, 1 skipped (EXTERNAL_BLOCKED: live PostgreSQL), 2 warnings |
| architecture_check.py | Architecture conformance: PASS |

Total runtime ~5 min. This reproduces the M17 final gate exactly (640 + 1 skip).

Narrow critical regression (G21A required): `uv run pytest tests/unit/runtime/test_golden_replay.py tests/integration/test_g13e_history.py tests/integration/test_m1_acceptance.py tests/integration/test_persistence_sqlite.py -q` -> 26 passed.

## 4. Production inventory (packages + apps)

| Package | Files | LOC | Public classes | Public funcs | Public names |
|---|---|---|---|---|---|
| packages/domain | 18 | 1239 | 58 | 18 | 76 |
| packages/substrate | 188 | 15531 | 331 | 128 | 459 |
| packages/runtime | 11 | 1083 | 17 | 13 | 30 |
| packages/application | 7 | 727 | 9 | 2 | 11 |
| packages/persistence | 9 | 559 | 11 | 2 | 13 |
| packages/observability | 5 | 303 | 7 | 8 | 15 |
| packages/evidence | 1 | 5 | 0 | 0 | 0 |
| packages/model_providers | 1 | 5 | 0 | 0 | 0 |
| packages/research | 12 | 1411 | 61 | 1 | 62 |
| apps/api | 13 | 969 | 30 | 14 | 44 |
| **TOTAL** | **265** | **21832** | **524** | **186** | **710** |

Tests: 155 files, ~16,280 LOC. SDK TS: 17 source files (TS), 22 passing tests at M17.

## 5. Persistence / migrations

- Alembic head: `0002_add_event_seq_index` (down: `0001_initial`).
- SQLite profile default; PostgreSQL profile EXTERNAL_BLOCKED (no live instance).
- Migrations: `migrations/versions/0001_initial.py`, `migrations/versions/0002_add_event_seq_index.py`.

## 6. Golden fixtures & replay hashes

- `tests/fixtures/golden_replay_v1.json` — SHA-256 `C158F47D0ED13E9379F54722C32CE010532BDA6091201E829C5ACAD5622DAD43`
  - 5 events, final revision 5; replayed semantic hash `7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00` (matches fixture; verified by test_golden_replay / test_g13e_history / test_m1_acceptance / test_persistence_sqlite).
- Synthetic micro-world replay hash `0964e48a7d03fe52bc227395d8332b24a18798e3c0c1a293f63231d88941aed5` (per reports/REPLAY_GOLDEN_CORPUS.md).
- Reference world: `reference_worlds/synthetic_full/synthetic_full.py` SHA-256 `01168CF31E0733453F822E6EAEDDE36F77590E4059AC374BD6C82EDCE26DB26A`; README SHA-256 `9A5ED5261993ACC36D9DF545A62F227C291164A72239D0AAA676B578414E3507`.

## 7. Public API / SDK / schema versions

- API routes (apps/api): 10 (`/healthz`, `/worlds`, `/worlds/{id}`, `/worlds/{id}/events`, `/worlds/{id}/state`, `/worlds/{id}/actions`, `/worlds/{id}/branches`, `/worlds/{id}/branches/compare`, `/worlds/{id}/checkpoint`, `/worlds/{id}/replay`) per reports/SDK_API_BASELINE.md.
- Python public names (stable packages): 832; TypeScript surface symbols: 5.
- Package versions: all workspace packages 0.1.0; apps/api 0.1.0.
- PACK_MANIFEST.md: 94/94 entries verified at M17 final HEAD (reports/FINAL_PROGRAM_COMPLETION_REPORT.md).

## 8. Known blockers (baseline)

- `BLOCKERS.md`: empty (no open internal blockers).
- `KNOWN_FAILURES.md`: empty.
- External blockers carried from M17 (explicit, narrow, not claimed as completed): real renderers/XR; real licensed source data (Red Chamber/Liaoshen/family/heritage); live PostgreSQL; real providers/object storage/SSO/multi-node; real sensors/hardware.
- M16 research tracks (packages/research, 9 tracks) are EXPERIMENTAL behind OFF flags; distributed hosting REJECTED for promotion (ADR 0055).

## 9. Integrity note

This baseline freeze includes the v5.1 program contract files (pack docs, master spec, Goal contracts G21A–G28I, milestone gates M18–M25) as part of the same local checkpoint so that the program is reproducible from a single commit. No production code was changed by G21A.
