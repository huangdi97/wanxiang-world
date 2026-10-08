# G93F — Reputation / Social Role

Date: 2026-08-27
Status: PASS

## Implemented contract

G93F adds an immutable, evidence-backed reputation projection with explicit
`local` and `global` scopes. A local view may carry an observer actor, while a
global view is an aggregate that can combine observations from multiple
observers. Scope, subject, dimension, observer, event refs, evidence refs,
time, score bounds, and deterministic projection keys are typed and validated.

Only committed events, direct observations, and memory observations are valid
reputation evidence. Belief and rumor are rejected at the event boundary;
neither can silently become World Truth or a social score. New evidence is
aggregated with a bounded weighted change and produces the existing scalar
`StateDelta` plus source/event provenance. Provider output is a proposal only;
explicit reviewer approval and an exact before-state check are required before
advancing the non-canonical reputation projection.

Social roles are a separate immutable projection, not institution `Role`
records and not permissions. Eligibility is derived from the reviewed
reputation state and a bounded threshold. Assignment also requires explicit
review; an ineligible proposal fails closed. No organization projection,
canonical entity, event stream, branch, or persistence schema is mutated.

## Reproducible evidence

- `tests/unit/substrate/test_g93f_reputation_social_role.py`: 4 passed,
  covering local/global scope, observer visibility, weighted bounded change,
  stale/review/authority checks, social-role review and separation, and
  rejection of both belief and rumor evidence.
- `tests/integration/test_g93f_reputation_social_role_product_chain.py`: 1
  passed. A private rights-approved source traversed OneClickAuthoring,
  WorldPackage, PlayableService, Preview, and SQLite-backed WorldRuntime. The
  actual committed `set_status` event was used as evidence for the reputation
  proposal and social-role projection.
- The integration asserted unchanged canonical semantic hash, revision, event
  count, and restore/replay hash after both projections advanced. The
  `EvolutionCommitPolicy` validated the generated StateDelta provenance.
- `scripts/sdk_baseline.py`: `routes=62 ts=5 py=1893` after the additive public
  evolution surface.

## Quality and boundary gates

- Focused G93F regression: `5 passed, 1 warning`.
- Full repository pytest: `1355 passed, 1 skipped, 2 warnings` in
  `320.68s`; the single skip is the documented PostgreSQL
  `EXTERNAL_BLOCKED` profile.
- Ruff check and format check: PASS (`2508 files already formatted`).
- Pyright: 0 errors, 0 warnings, 0 informations.
- `scripts/architecture_check.py`: PASS.
- `scripts/kernel_guard.py`: `0 violation(s)`.
- `git diff --check`: PASS (only Git's CRLF normalization warnings).
- No private source was uploaded, no source text was modified, no model was
  trained, and no v5.6 work was started.

G93F is PASS and is ready for the required commit
`g93f: Reputation / Social Role`. Gate 30 remains pending until G93H completes
the integrated 30-day Actor/Relationship/Organization qualification. Gate 24,
G93G-G97J, and the remaining v5.5 release gates remain pending; v5.5 stays
`IN_PROGRESS / NOT_ACCEPTED`.
