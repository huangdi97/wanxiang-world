# G91D — Canon Attractor Policy

Date: 2026-08-26  
Status: PASS

## Result

`CanonAttractorPolicy` computes normalized canon-distance metrics over explicit
soft and hard constraints. A major divergence is a measured result and a
proposal to fork a worldline; it is not a forced actor action. The assessment
retains the observed choice, marks free will preserved, and leaves actual
branch creation to the existing runtime branch authority.

No policy method changes actor goals, canonical state, event history, or
belief/memory projections. A small divergence recommends continuing the same
worldline; a hard violation or threshold crossing recommends a branch.

## Evidence

- `tests/unit/substrate/test_g91d_canon_attractor.py`: 3 passed.
- `uv run ruff check`, format check, and `uv run pyright` on changed files:
  PASS; 0 errors and 0 warnings.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.

G91D is complete and committed. Gate 17/18/19 remain pending until the M88
qualification; G91E is next and v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`.
No model training or v5.6 work was performed.
