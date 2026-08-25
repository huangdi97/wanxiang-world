# G74A-G81J Real Book → Living World Qualification

Date: 2026-08-25
Branch: `feature/source-to-living-world`
Scope: v5.4 remediation only; no v5.5 and no model training.

## Decision state

`ACCEPTED`. Local implementation, full quality, and real-source product
evidence pass. The pushed implementation commit `f7685ec164a4a3050a53ea04ebd05432b95658f7`
passed all six required jobs in GitHub Actions run `32821744579`. The historical
`reports/REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md` remains the preserved
pre-repair `NOT_ACCEPTED` source-of-truth report.

## Source and boundary

The same private local file was used without editing or copying it into the
repository. Public evidence intentionally withholds its local path and raw
fingerprint; the full values were checked locally before this report was
sanitized for the public branch:

| Field | Value |
|---|---|
| Path | `private-local-source` |
| Raw bytes | `937500` |
| Raw SHA-256 | withheld from public evidence; verified locally |
| Git tracked | `false` |
| Source access | `private` |
| Review/rights diagnostic | `E3`, package inclusion approved |

The CLI reads file bytes and decodes them without newline normalization, so the
source record hash is the raw-file hash. Source content remains data-channel
input; no source-specific title logic, source rewriting, hand-filled
Candidate, hardcoded coverage, disabled compiler/worldness gate, or internal
helper replacement was used.

The original failure evidence is preserved in
`artifacts/real_book_living_world_acceptance_2026-08-25/` and remains
`NOT_ACCEPTED`: 0 candidates and zero coverage before the semantic data-flow
repair.

## Real CLI evidence

Command:

```text
uv run python scripts/wxworld.py reference --profile book --file <private-local-source> --job-id real_book_final_cli_raw_20260825 --semantic-provider local --publish --instantiate --worldness
```

Observed in `artifacts/real_book_living_world_acceptance_2026-08-25/final_cli_summary.json`:

- 3,918 parsed nodes and segments; 164 bounded batches; 164 completed provider calls; 0 retries.
- 11,549 provenance-bound candidates from `local_semantic_v1`; coverage `0.8333333333333334`.
- Published WorldPackage `world:wd_real_book_final_cli_raw_20260825`, manifest hash recorded, and `preview://preview_1`.
- Worldness passed with score `0.99` and ten evidence dimensions.
- Living instance `prv_preview_1` committed `set_status` at event sequence 3856; proposal validation, replay equality and branch isolation are true.

No-provider negative path on the same raw file is typed and terminal:
`semantic_provider_required`, product state `SEMANTIC_PROVIDER_REQUIRED`,
checkpoint `parsed_nodes=3918`, `segments=3918`, `batches=164`; it does not
produce an empty success.

## Real API and Studio evidence

The same raw bytes were decoded into the API request and sent through
`POST /studio/one-click` with the configured local semantic provider. The
recorded API chain is:

`one-click 201 → status/draft/review 200 → build 200 → preview 200 → instantiate 200 → worldness 200 → enter 200 → publish 200`.

The API produced 11,549 candidates, draft coverage `0.8333333333333334`, a
WorldPackage and Preview, ten Worldness evidence names, committed/replay-equal
action, isolated branch, and 2,764 entered entities. `/studio/ui` returned 200
with file upload and Worldness controls. The random-port socket smoke returned
health `ok`, socket `passed`, and Studio status `true` on port 30139.

## Goal matrix

| Milestone | Goals | Result and evidence |
|---|---|---|
| M71 | G74A-G74G | PASS: frozen NOT_ACCEPTED regression, source-to-candidate trace, typed product states, terminal checkpoint/error handling, empty-scenario guard, regression tests. |
| M72 | G75A-G75G | PASS: Chinese chapter/section parsing, non-empty 3,918-node segmentation, bounded 24-segment batches, stable locators, semantic dispatch, exposed progress/stage errors. |
| M73 | G76A-G76J | PASS: shared SemanticDistillationService, private-safe structured provider port, supported candidate kinds, retry/checkpoint accounting, reversible fusion, locator/evidence/provider/schema provenance. |
| M74 | G77A-G77H | PASS: independent rights gates, measured coverage, review inbox/audit, draft/compiler states, missingness, non-empty real WorldDraft. |
| M75 | G78A-G78H | PASS: typed compiler results, real WorldPackage/Preview, ten-dimensional measured Worldness evidence, bounded repair loop, Observe→Propose→Validate→Commit→Replay. |
| M76 | G79A-G79H | PASS: Living Instance identity/version fields, Perception enter path, committed generic action, replay/restore proof and isolated branch. |
| M77 | G80A-G80H | PASS: CLI lifecycle commands, API living routes, browser Studio flow, Build/Preview/Worldness/Enter controls, random-port smoke, shared backend use cases. |
| M78 | G81A-G81J | PASS: same-source CLI/API/Studio evidence, typed no-provider path, performance/security/regression gates, feature-branch push, six required Actions jobs, final evidence and STOP boundary. |

## Local gates

- `uv run ruff check .`: PASS.
- `uv run ruff format --check .`: PASS, 2,169 files formatted.
- `uv run pyright`: PASS, 0 errors/warnings/information.
- `uv run pytest -q`: `1205 passed, 1 skipped, 2 warnings`; the only skip is the explicitly external PostgreSQL live profile.
- `uv run python scripts/architecture_check.py`: PASS.
- `uv run python scripts/studio_socket_smoke.py`: PASS.

## Delivery decision

`v5.4.0-rc2` is now permitted by the acceptance gate, but is created only in
the next step after the final evidence-only commit and its docs-only Actions
run are green. `v5.4.0-rc1` remains the latest tag until then. Do not enter
v5.5 or train a model.

## Remote Actions evidence

Run: [32821744579](https://github.com/huangdi97/wanxiang-world/actions/runs/32821744579)
Head: `f7685ec164a4a3050a53ea04ebd05432b95658f7`

All required jobs passed: Repository safety, Python, PostgreSQL migration and
integration, API/package/SDK drift, TypeScript, and release build/clean-room
certification.
