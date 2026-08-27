# G97E — Experience Product E2E

Date: 2026-08-27  
Status: PASS

## Scope

G97E verifies the browser-facing Experience/Studio product chain, including
the Workshop private-visibility path. The test uses a synthetic private,
rights-approved text source with `training_allowed=false`; it does not use or
modify the original 2026-08-25 323,815-character book. The original real-book
acceptance remains `NOT_ACCEPTED`.

## Real browser product chain

`tests/integration/test_g97e_browser_experience_product_chain.py` starts the
real FastAPI application over a migrated SQLite `WorldRuntime`, serves the
embedded Studio page on an OS-selected HTTP port, and drives it with Chromium
through Playwright. The browser actions and same-origin API calls cover:

`Studio UI → one-click authoring → draft/build/preview → publish → Workshop
from-source(private) → private PlayableWorldProfile → World Plaza → Character
→ embodiment entry → Free Action → committed StateDiff → Leave → Continue`.

The browser asserts the rendered Studio title and controls before using the
UI buttons. It then uses browser-page `fetch` calls for the product operations
that have no corresponding visible control (Workshop, profile creation,
character creation, and permission probes), keeping the test on the public
HTTP/API surface rather than calling internal helpers.

## Measured evidence

| Measure | Result |
|---|---:|
| Browser engine | Chromium via Playwright; local system Chrome in this run |
| Served backend | FastAPI over real migrated SQLite WorldRuntime |
| Studio authoring | one-click → draft → build → preview succeeded |
| Publish | `/studio/jobs/{job_id}/publish` returned `publishable=true` |
| Workshop | source mode returned a private playable profile with publishable=true |
| Plaza privacy | owner sees the private profile; guest world list does not |
| Character/entry | `ent_alice` created and embodiment entry succeeded |
| Action | `set status to awake` returned proposed action, event ID, and non-empty StateDiff |
| Leave/Continue | same instance ID and post-commit state hash after Continue |
| Source export | source text absent from serialized browser/API response evidence |

Studio, Workshop, PlayableService, and the runtime are composed by the same
application factory. The browser therefore exercises server truth and the
normal Commit Authority path; it does not write canonical state through DOM
state, JavaScript-local state, or a provider.

## Rights and authority boundaries

The fixture is private and rights-approved for qualification only. The browser
does not upload the original private book, and no source payload is returned
in the checked response bundle. Private profile visibility is enforced by the
server-side Plaza/profile policy and is checked with a separate guest header.
Provider/model output is not involved in the world commit; the action uses the
existing bounded IntentCompiler → Commit Authority path.

This is a product and authorization qualification, not a claim of scientific
validity, universal world coverage, or predictive/live-world performance. No
compiler/worldness gate was disabled, no Candidate was hand-filled, no
coverage was hardcoded, and no model was trained.

## Quality and CI evidence

- Real browser test: `1 passed, 1 warning` in 3.61s under the authorized
  Windows browser-run environment.
- Full quality: `1450 passed, 1 skipped, 2 warnings` in 417.49s (6:57).
- The one skip is the documented PostgreSQL `EXTERNAL_BLOCKED` profile because
  `WANXIANG_POSTGRES_TEST_URL` is not configured locally.
- Ruff check and format check: PASS.
- Full Pyright: `0 errors, 0 warnings`.
- `scripts/architecture_check.py`: PASS.
- `scripts/kernel_guard.py`: 0 violations.
- `git diff --check`: PASS.
- CI now installs the locked Playwright Chromium runtime with
  `uv run playwright install --with-deps chromium` before the Python test job.

G97E is PASS for the browser Experience/Studio scope. Gate 51 is now
ACCEPTED. The original real-book `NOT_ACCEPTED` boundary, remaining release
gates, v5.6 prohibition, and no-training boundary remain in force.

