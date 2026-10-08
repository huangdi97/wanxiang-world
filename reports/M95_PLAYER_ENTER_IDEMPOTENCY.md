# M95 Player Enter Idempotency Remediation

**Conclusion:** `PASS` for the automated persisted-entry remediation; M95
human acceptance remains `USER_INPUT_REQUIRED` and Gate 80 remains `LOCKED`.

## Incident

On the local M95 Player build, clicking `以此角色进入` returned the generic
connection error. The real request was a 500 caused by
`sqlite3.IntegrityError: UNIQUE constraint failed: world_instances.instance_id`
for `prv_playable_1`. The Player surface was only hiding the server error.

## Root cause and fix

`PlayableService` reconstructs its in-memory preview install after a process
restart, while the canonical SQLite world instance remains durable. Preview
instantiation therefore attempted to create the same world instance again.

The application runtime now exposes a read-only root-branch lookup. Preview
instantiation reuses an existing durable root for the matching install and
skips only the initial entity/relation seeding. New worlds still use the
existing Host and Commit Authority path. An instance with zero or multiple
root branches fails closed with a typed persistence error.

During the first manual verification, the verifier itself held an active
embodiment lease for `ent_alice`. A second entry correctly hit the one-primary-
controller rule, but the API returned 500 and the Player mapped the structured
error to the generic connection message. The API now returns 409 for lease
conflicts, the Player reads structured `code`/`message` fields, and the Chinese
surface explains that the character is already in another session. The
verification lease was explicitly released before handoff.

## Evidence

| Check | Result | Reproduction |
|---|---|---|
| Architecture guard | `PASS` | `uv run python scripts/architecture_check.py` |
| Ruff + Pyright | `PASS` | Targeted changed-file checks |
| Unit/integration/API regression | `PASS` | `uv run pytest tests/unit/substrate/test_compile_preview.py tests/integration/test_playable_service.py tests/api/test_player_experience_remediation.py -q` → `8 passed` |
| Real SQLite runtime restart | `PASS` | `test_enter_reuses_persisted_preview_after_runtime_restart` uses two runtimes over the same upgraded SQLite database and verifies no duplicate events |
| Current M95 server route | `PASS` | Against `sqlite:///./.pytest-tmp/m95-human-zh/wanxiang.db`: plaza `200`, enter `200`, instance `prv_playable_1` |
| Lease conflict contract | `PASS` | First enter `200`, duplicate actor entry `409 embodiment_lease_conflict`, leave `200`, re-entry `200` |
| Player cache/error surface | `PASS` | Player HTML sends `Cache-Control: no-store`; structured lease conflict is no longer rendered as a connection failure |
| Browser journey | `PASS` | `uv run pytest tests/integration/test_m95_player_experience_browser.py -q` with host Playwright permission → `1 passed` |

The initial sandbox-only browser attempt was blocked before browser startup by
Windows `WinError 5`; the host-permission run passed. This is an execution
environment boundary, not a product failure.

## Evidence boundary

- `IMPLEMENTED`: durable preview lookup and idempotent Player entry on the
  existing canonical world instance.
- `VALIDATED`: changed-file architecture/type/lint checks, SQLite restart
  regression, current local HTTP route, and browser journey.
- `EXPERIMENTAL`: Prompt Genesis and bounded long-horizon / World Lab /
  emergence remain bounded/experimental.
- `NOT_PROVEN`: human comprehension, immersion, agency, consequence
  interpretation, and real-player acceptance.
- `EXTERNAL_BLOCKED`: live PostgreSQL and heavy physical/visual E2E remain
  unverified in this environment.

No tag, GitHub Release, push, v5.6 branch, or model-training work was created.
