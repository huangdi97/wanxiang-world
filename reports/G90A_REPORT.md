# G90A — Workshop Information Architecture

Date: 2026-08-26
Status: PASS

## Evidence

- `WorldWorkshop.home()` exposes one World home with Source, Prompt, Hybrid,
  Scenario, Experience, Publishing, Review, and Registry panels.
- The three creation modes are explicit and share the same
  `WorkshopDraftStore`; there is no mode-specific editor store.
- Workshop drafts are immutable revisions. A stale editor revision raises the
  typed `DraftRevisionConflict` and cannot overwrite a newer draft.
- The product-side draft record stores only references to WorldDraft/package
  inputs. It does not own Canonical World State, events, branches, candidates,
  or Commit Authority.

## Checks

- `pytest -q tests/unit/substrate/test_g90a_workshop.py`: 2 passed
- Ruff check/format: PASS
- Pyright: 0 errors
- `scripts/architecture_check.py`: PASS

G90B is next. M87 and v5.5 remain `IN_PROGRESS / NOT_ACCEPTED` until the full
Workshop qualification is complete.
