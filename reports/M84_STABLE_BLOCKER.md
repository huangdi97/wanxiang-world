# M84 Stable Certification — NOT ACCEPTED

Date: 2026-08-26  
Branch: `feature/source-to-living-world`  
Scope: v5.4 stable certification only; no v5.5 and no model training.

## Decision

**NOT ACCEPTED for `v5.4.0` stable.** The M84 engineering and delivery gates
available on the current public feature branch pass, but the stable-release
contract is not satisfied because the first real Chinese book remains
`NOT_ACCEPTED` in the unchanged source-of-truth report
`reports/REAL_BOOK_LIVING_WORLD_ACCEPTANCE_2026-08-25.md`.

This is the unique remaining blocker. The report records, under the
rights-approved diagnostic, zero candidates and `coverage=0`; it explicitly
records that no WorldPackage, Preview, Worldness, Living Instance, or
Commit/Replay evidence existed. That report has not been edited or replaced.

The accepted M79 real chain is a **second** private EPUB source, and the
accepted M82 chain is a public historical GEDCOM fixture. Neither is evidence
that the first Chinese book passed. The final acceptance contract therefore
does not permit a stable tag or stable GitHub Release.

## Evidence that is accepted but insufficient to release

### M82 family qualification

`reports/M82_GEDCOM_QUALIFICATION.md` and
`artifacts/m79_m84/real_gedcom_product_evidence.json` record the supplied
public historical GEDCOM product chain. It is real Family product validation,
not private living-family user validation, and its raw file is not in Git.

### M84 clean-clone and regression gates

The final GitHub feature-branch clean clone at the current code delivery
passed:

- `uv sync --all-groups --all-packages` and `pnpm install --frozen-lockfile`;
- Alembic migration through `0004_add_world_metadata (head)`;
- `scripts/clean_room_certify.py`: all seven checks PASS;
- CLI reference smoke: publishable WorldPackage, Preview, Living, Worldness
  passed, Commit/Replay equality, and branch isolation;
- Studio socket smoke: `/healthz` and `/studio/ui` PASS;
- Python: `1219 passed, 1 skipped, 2 warnings`; the skip is the unavailable
  local PostgreSQL profile, not a product success claim;
- ruff, format, pyright, architecture, TypeScript lint/typecheck, 22 Vitest
  tests, and TypeScript build all PASS.

The required GitHub Actions run for the code repair was run `32879104870`;
all six jobs succeeded, including PostgreSQL, Python, API/package/SDK,
release-smoke, safety, and TypeScript. A documentation-only follow-up commit
will trigger the same required workflow again; a green workflow does not waive
the first-book source acceptance requirement.

## Rights and source safety

No private book or GEDCOM was copied into Git or modified. No Candidate was
hand-filled, no coverage was hardcoded, and compiler/Worldness gates were not
disabled. The public historical family fixture does not prove consent or
privacy validation for living users; those boundaries remain covered only by
the existing privacy/security tests.

## Required next action

Re-run the **same original private Chinese book bytes** through the real
CLI/API/Studio chain after the semantic-distillation data-flow repair. Only a
new, sanitized acceptance report with WorldPackage, Preview, measured
Worldness, Living Instance, Commit/Replay, and an `ACCEPTED` decision can clear
this blocker. Until then, preserve the original `NOT_ACCEPTED` report and do
not create or move `v5.4.0`.

## Resolution (2026-08-26)

The blocker was cleared by re-running the same local source after the
semantic-distillation repair. The real CLI and API/Studio evidence is now
`ACCEPTED`: 11,549 candidates, measured coverage `0.8333333333333334`,
WorldPackage, Preview, Worldness, Living, Commit/Replay, and branch isolation.
See `reports/M84_FIRST_BOOK_REQUALIFICATION.md` and
`artifacts/m79_m84/real_book_reacceptance_product_evidence.json`.

This historical blocker report remains preserved; it is not rewritten into a
false PASS record.
