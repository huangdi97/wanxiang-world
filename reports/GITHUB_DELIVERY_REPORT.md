# GitHub Public Delivery Report — Wanxiang (v5.3.0-rc1)

Date: 2026-08-16
Scope: POST-COMPLETION GITHUB DELIVERY / RELEASE RECOVERY for the certified
Wanxiang monorepo. No Goal/Milestone was re-implemented; no v5.4 work started.

## 1. Repository identity

| Field | Value |
|---|---|
| Owner | `huangdi97` |
| Name | `wanxiang-world` |
| Visibility | `PUBLIC` |
| URL | https://github.com/huangdi97/wanxiang-world |
| Remote (origin) | https://github.com/huangdi97/wanxiang-world.git |
| Branch | `master` |
| Description | Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS |

Repository created with `gh repo create wanxiang-world --public --source=. --remote=origin`
(no history rewritten, no force push). Verified with `gh repo view` and
`git remote -v`.

## 2. Commit / SHA verification

- Local final HEAD (certified code state): `7b0674c00e92dcabf1072655503355e2bbc6ccd3`
- Remote `master` SHA: `7b0674c00e92dcabf1072655503355e2bbc6ccd3`
- Verification: `git ls-remote origin master` == `git rev-parse HEAD` -> **SHA MATCH**
- History preserved: the v5.2 M42 production certification commit
  `847ad55` (`m42-v5.2-production`) is an ancestor of the pushed branch.

## 3. GitHub Actions CI (must run green on remote)

Final run: **success**
- Run ID: `31942590763`
- Run URL: https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763
- Conclusion: `completed` / `success` on SHA `7b0674c`

All 6 jobs:

| Job | Result | URL |
|---|---|---|
| Repository safety / secret scan / forbidden tracked files | success | https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763/job/95153805755 |
| python (ruff / format / pyright / pytest / quality / kernel_guard) | success | https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763/job/95153805752 |
| PostgreSQL migration + integration | success | https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763/job/95153805684 |
| API / package / SDK generation + drift | success | https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763/job/95153805687 |
| ts (pnpm lint / typecheck / test / build) | success | https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763/job/95153805715 |
| Release build + clean-room certification smoke | success | https://github.com/huangdi97/wanxiang-world/actions/runs/31942590763/job/95153805702 |

Earlier failing runs and root causes fixed (no job deleted, no
continue-on-error, no skipped/weakened tests):
1. `31941423593` — safety secret-scan false positive on an intentional
   secret-detection fixture (fake key now assembled at runtime);
   pnpm version mismatch (pinned 11.16.0); baseline manifest hashes were
   Windows-CRLF-only (now canonical CRLF-normalized, test + generator
   updated); migration round-trip depended on the ambient default sqlite URL
   `./data/wanxiang.db` (now pinned to the test DB); live PG profile passed a
   postgresql:// URL into the SQLite-file helper (now migrates PG directly).
2. `31942425812` — ruff format on one edited test; missing psycopg2 driver in
   the PG job (now `uv run --with psycopg2-binary`); stale TS operation count
   in `openapi.test.ts` (10 -> 17, matching the exported contract).

## 4. Tag & Release

- Annotated tag: `v5.3.0-rc1` -> `7b0674c00e92dcabf1072655503355e2bbc6ccd3`
  (pushed: https://github.com/huangdi97/wanxiang-world/tree/v5.3.0-rc1)
- GitHub Release: https://github.com/huangdi97/wanxiang-world/releases/tag/v5.3.0-rc1

## 5. Public-release safety audit (completed before repo creation)

- Secret pattern scan (`ghp_`, `sk-`, `AKIA`, `AIza`, `BEGIN PRIVATE KEY`):
  0 real matches (one intentional test fixture, since neutralized for the
  naive scanner; guard behavior unchanged).
- Forbidden tracked files: no `.env`, `.pem`, `.p12`, `.jks`, `.key`,
  `.sqlite`, `.db`, `id_rsa` tracked.
- No large binaries (>5MB) tracked; `data/` untracked; no model caches.
- Restricted corpus: `sources/red_chamber/` contains only `README.md` +
  `MANIFEST_TEMPLATE.yaml`. No 《红楼梦》 edition text, modern annotated
  edition, or scanned copy is published (Source Gate -> honest
  `EXTERNAL_BLOCKED`; see `DATA_AND_ASSET_RIGHTS.md`).
- No user/family privacy data, no local databases, no logs with sensitive
  content were pushed.

## 6. Open-source files published

`README.md` (updated), `README_EN.md`, `LICENSE` (Apache-2.0), `NOTICE`,
`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
`DATA_AND_ASSET_RIGHTS.md`, `.env.example` (placeholders only), `.gitignore`,
`.gitattributes`, `.github/workflows/ci.yml`.

## 7. Working-tree policy

The delivery commit also committed the user-prepared v5.3 M43-M50 planning
documents (root policies 01-12, `goals/G46A`-`G53L`,
`milestones/M43`-`M50`) **as planning material as-is**. They are NOT marked
qualified/implemented; no ledger status for those goals was changed. The
certified baseline remains v5.2 / M42.

## 8. Limitations

- 《红楼梦》 real-text Source Gate: EXTERNAL_BLOCKED (no legally
  redistributable edition in environment); corpus excluded, not faked.
- Local Windows sandbox boundaries (not code defects, Linux CI passes):
  - 3 pytest tests hit `tmp_path` PermissionError during collection on this
    sandbox (test_kernel_guard x2, test_completion_ledger_review x1).
  - `pnpm -r test` locally hit esbuild `spawn EPERM` (missing
    `@esbuild/win32-x64`); the Linux CI ts job passes.
- No external LLM API key is required by core tests or CI.

## 9. Evidence commands (local)

- `uv run ruff check .` -> PASS; `ruff format --check .` -> PASS
- `uv run pyright` -> 0 errors
- `uv run pytest -q` -> 979 passed + 1 skipped + 3 Windows-sandbox tmp_path errors
- `uv run python scripts/kernel_guard.py` -> 0 violations
- `uv run python scripts/architecture_check.py` -> PASS
- `pnpm -r lint / typecheck / build` -> PASS (test: see limitation above)
- `scripts/clean_room_certify.py` local FAIL on scratch-dir ACL only;
  Linux CI release-smoke job PASSes all 7 clean-room steps.
