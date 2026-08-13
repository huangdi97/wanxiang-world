# Goal G13A Acceptance Report — Post-M9 Baseline Freeze & Independent Evidence Capture

## Status
PASS (read-mostly baseline freeze; M9 checkpoint independently verified healthy)

## Objective
Establish an independent, reproducible post-M9 audit baseline before any new fixes, so later claims can be compared against immutable repository and runtime evidence.

## M9 checkpoint verification (independent)
| Check | Command | Result |
|---|---|---|
| Full Python quality gate | `uv run python scripts/quality.py` (with `UV_CACHE_DIR=./.uv-cache`) | PASS — ruff check, ruff format, pyright 0 errors, **385 pytest passed**, architecture conformance PASS |
| TS SDK typecheck | `npm run typecheck` (packages/sdk_ts) | PASS — tsc --noEmit clean |
| TS SDK lint | `npm run lint` (packages/sdk_ts) | PASS — eslint clean |
| TS SDK tests | `npm test` (packages/sdk_ts) | PASS — 21 tests passed |
| Test collection | `uv run pytest --collect-only -q` | 385 collected; **0 skipped / 0 xfail** |
| Migration head | offline parse + `uv run alembic current` on disposable DB | head `0002_add_event_seq_index` (0001_initial → 0002) |
| Disposable clean bootstrap | `WANXIANG_DATABASE_URL=sqlite:///./.cache/bootstrap_g13a.db uv run alembic upgrade head` | PASS — tables: alembic_version, audit_traces, branches, events, snapshots, world_instances |
| Git state | `git status` / `git log` | HEAD `91f0b1f` = tag `m9-release-qualified`; PACK_MANIFEST.md modified; post-M9 pack files untracked |
| Pack integrity | SHA-256 comparison of PACK_MANIFEST.md entries vs files | 94/94 match, 0 mismatches |

Note: `npm test` first failed inside the sandbox with `EPERM: spawn` (esbuild service); rerun outside the sandbox passed — environment boundary, not a product failure. Recorded in the command matrix.

## Baseline deliverables
- `reports/POST_M9_BASELINE.md` — repository SHA, environment, immutable hashes, migration state, test inventory, marker signals.
- `reports/post_m9_baseline.json` — machine-readable baseline (schema v1.0).
- `reports/POST_M9_COMMAND_MATRIX.md` — exact commands, exit codes, evidence.
- `scripts/capture_post_m9_baseline.py` — reproducible capture script (stdlib only, no network).

## Marker signal inventory (unclassified by design; G13D/G13G classify severity)
| Marker | Count (repo-wide, docs+tests+goals, excluding .venv/node_modules/.git/.uv-cache/reports/data) |
|---|---|
| TODO | 150 |
| FIXME | 139 |
| NotImplemented | 147 |
| placeholder | 152 |
| stub | 3 |
| mock-only | 137 |
| static-fake | 6 |
| XXX | 1 |

Production packages/apps placeholder scan (architecture guard) is clean; the markers above are concentrated in docs/tests/goal specs and will be triaged in G13D/G13G without weakening guards.

## GAP_CANDIDATES (recorded, not silently accepted)
1. No standalone `openapi.json` artifact in the repo; the TS SDK is a typed client over an embedded stable OpenAPI document with determinism tests. Verify artifact/drift policy in G13B/G13E.
2. `data/wanxiang.db` exists as a local runtime artifact (gitignored); disposable clean bootstrap verified migrations from scratch; no persistent test DB is committed.
3. STATUS.md contains duplicated M2-M9 goal rows from prior batch appends; historical records are preserved as-is (not rewritten), and the post-M9 section is appended.

## Key immutable hashes (full list in POST_M9_BASELINE.md)
- `docs/spec/WANXIANG_v5_MASTER_SPEC.md` SHA-256 recorded in baseline JSON.
- `uv.lock`, `pnpm-lock.yaml`, `alembic.ini`, `docker-compose.yml`, CI workflow, `packages/sdk_ts/src/openapi.ts` all hashed.

## Documentation / ledger updates
- `PLAN.md`, `STATUS.md`, `CHANGELOG.md` updated; post-M9 pack integrated per `23_POST_M9_HANDOFF_PROTOCOL.md` (no history rewritten).

## Remaining limitations
- Real external sources/providers/hardware remain EXTERNAL_BLOCKED as labeled in M9; generic capability and deterministic substitutes are present.
- Baseline is a snapshot in time; hash evidence anchors later forensics goals.

## Final checkpoint
- commit: `g13a: post-m9 baseline freeze & independent evidence capture`
