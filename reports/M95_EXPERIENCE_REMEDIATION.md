# M95 Experience Remediation

**Status:** `M95_REMEDIATION_REQUIRED`

**Release status:** `v5.5.0` is not released. Gate 80 remains `LOCKED`.

This report records the Player Experience remediation requested after the
previous M95 precheck. It does not alter the historical Gates 1–60, Gates
62–66, or the existing acceptance matrix.

## Scope delivered

- Added an independent Chinese Player surface at `/`, `/experience/ui`, and
  `/player`; the existing English technical surface at `/studio/ui` remains
  Studio-only.
- Added server-backed player projections for world detail, scene, time,
  environment, current event, people, memories, relations, chronicle, and
  committed changes. World cards now expose only player-safe availability,
  counts, and continuation state.
- Added first-class home shelves for 推荐世界、我的世界、最近经历、我的角色;
  the World Plaza also has public/recent/mine classification and search.
  Continue summaries are derived from the same event stream and show the
  last place, leave-time world tick, real post-leave records when present, and
  the last committed change.
- Added detail fields for era/place/environment/now/mode, explicit character
  knowledge boundaries, and the visible “以此角色进入” / “成为此人” actions.
  The play view renders region/place/time/environment, opportunities, items,
  goals, relations, and recent memories from the Player projection.
- Added Chinese world/character metadata and a deterministic Chinese action
  path. Actions still compile to a proposal and pass through the existing
  Commit Authority/runtime path.
- Added one immutable Player i18n catalog shared by the server projection and
  browser asset. `zh-CN` is the explicit default; `en-US` is optional only
  when selected by query/header, and browser locale never silently changes
  the Player surface.
- Leave and continue reuse the same instance and branch. No frontend state is
  treated as Canonical Reality.
- Added a repeatable local human-test server and a sanitized SQLite evidence
  runner.

## Automated evidence

The fixture is creator-owned synthetic data only. Source bytes are not stored
in the artifact.

| Evidence | Result | Reproduction |
|---|---|---|
| Architecture guard | `PASS` | `uv run python scripts/architecture_check.py` |
| Kernel guard | `PASS` | `uv run python scripts/kernel_guard.py` |
| Python quality | `PASS` | `uv run python scripts/quality.py` → `1471 passed, 1 skipped, 2 warnings`; final line `All quality checks passed.` |
| TS SDK lint/typecheck | `PASS` | `pnpm -r lint`; `pnpm -r typecheck` |
| TS SDK tests | `PASS` | `pnpm -r test` → 6 files, 22 tests |
| TS SDK build | `PASS` | `pnpm -r build` |
| Player i18n catalog | `PASS` | `uv run pytest -q tests/api/test_player_experience_remediation.py` → `5 passed`; default/fallback/explicit `en-US` plus safe Player surface assertions |
| Browser journey | `PASS` | `uv run pytest -q tests/integration/test_m95_player_experience_browser.py -m e2e --basetemp <unique-local-basetemp>` → `1 passed` with host Playwright permission |
| Frozen budget + prior Studio browser | `PASS` | `5 passed` targeted gate run; current port count remains 44 |
| OpenAPI export | `PASS` | `uv run python scripts/export_openapi.py` → `70 paths / 74 operations` |

The sandbox-only Playwright run and the first sandbox-only TS test run hit
Windows process-creation permissions (`WinError 5` / `spawn EPERM`). The same
tests passed with the host permission required by this machine; these are
environment boundaries, not product results.

## SQLite route trace

Artifact: `artifacts/v55_stable/m95/player_experience_remediation.json`

- Source: `m95_human_zh_source`, SHA-256
  `9d132fecd52aaa0e446011af337e303274911392377ddf99034035444c4532ac`.
- Job: `m95_human_zh_job`.
- Package: `world:wd_m95_human_zh_job`.
- Profile: `experience:world:wd_m95_human_zh_job`.
- World instance: `prv_playable_1`.
- Branch: `br_6159b1fd52874dd29c1ef058024f634c`.
- Actor: `ent_alice`, displayed to the Player as `沈砚`.
- Canonical revision advanced from `3` to `4` after the Chinese action
  `让自己保持清醒`.
- Post-action canonical and replay hashes are both
  `b92128440812d009341fb7c58777366b4d43819851517412ffde292e7eeed038`.
- The trace records four committed event refs and the same instance after
  leave/continue.

The refreshed event refs are `evt_37e9c7c5612a4ff6b43f3fcdc320da9f`,
`evt_4fc4fdddb4124d98a26b3bb5bec2d43b`,
`evt_9fa3723516d64152a2ca1892ec709139`, and
`evt_efc2785e9d7846f78ce347e6c36c3287`.

Artifact SHA-256: `3c3080d112c82dbe1186439753e52a4443a181378030f24c1c869b3df692907e`

## UI review

The Player surface was reviewed at desktop and mobile widths. The Impeccable
design record is [DESIGN.md](../DESIGN.md). Local review render hashes are:

- desktop: `6abf3205301e5b8ad8ea201f879ddb680d11118b3205f2e44d9a0bdd3b410335`
- mobile: `f37f4fd828173c7ec7f6ea4211812c65637dfe28cb4bfd0943cfd98a17f2d530`

The Player DOM contains Chinese user-facing copy and does not render
WorldPackage, Candidate, Commit, RuntimeProfile, raw JSON, state hashes,
event IDs, branch IDs, or profile IDs.

## Evidence boundary

- `IMPLEMENTED`: Chinese Player UI, friendly projections, server-backed
  continuity, real action/commit/diff/replay path, SQLite/browser automation,
  and local human-test build.
- `VALIDATED`: deterministic API chain, SQLite persistence, replay equality,
  architecture/quality gates, TS contract, and browser navigation.
- `EXPERIMENTAL`: Prompt Genesis and bounded long-horizon / World Lab /
  emergence remain explicitly bounded/experimental.
- `NOT_PROVEN`: human comprehension, immersion, agency, consequence
  interpretation, and real-player acceptance.
- `EXTERNAL_BLOCKED`: live PostgreSQL and heavy physical/visual E2E have no
  real environment in this run.

Therefore M95/G98D is still `USER_INPUT_REQUIRED`; Gates 62–66 remain
unchanged and are not PASS. The fillable packet is
[M95_PLAYER_TEST_PACKET_ZH_CN.md](M95_PLAYER_TEST_PACKET_ZH_CN.md).

No tag, GitHub Release, push, v5.6 branch, or model-training work was created.
