# Post-M9 Command Matrix (G13A)

| Command | Exit | Evidence | Reproducible |
|---|---|---|---|
| `uv run python scripts/quality.py` | 0 | ruff, pyright, 385 pytest, architecture PASS | yes |
| `npm run typecheck` (packages/sdk_ts) | 0 | tsc --noEmit clean | yes |
| `npm run lint` (packages/sdk_ts) | 0 | eslint clean | yes |
| `npm test` (packages/sdk_ts) | 0 | 21 tests passed | yes |
| `uv run pytest --collect-only -q` | 0 | 385 tests collected, no skips | yes |
| migration head | n/a | head 0002_add_event_seq_index derived offline from files | yes (offline) |
| `git status --porcelain` | 0 | PACK_MANIFEST.md modified; post-M9 pack untracked | yes |

Notes: `npm test` initially hit `EPERM: spawn` inside the sandbox; rerun outside the sandbox passed (environment boundary, not a product failure).
