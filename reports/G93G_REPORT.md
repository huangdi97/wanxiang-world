# G93G — Evolution Explainability

Date: 2026-08-27
Status: PASS

## Implemented contract

G93G adds a queryable explanation projection over the existing typed G93A
evolution deltas. An `EvolutionExplanation` retains the typed delta itself,
its deterministic fingerprint, delta reason, subject kind/ref, projection
ref, source refs, event refs, and optional explicit trajectory refs. The
explanation is derived from the delta and cannot create a new canonical event,
state, branch, or store. All six delta kinds remain validated by the existing
`EvolutionCommitPolicy`.

The projection supports lookup by delta, subject, projection, and actor
trajectory link. `TrajectoryExplanationLink` links an existing
`ActorEvolutionState.trajectory` entry only when its explicit provenance ref
is present in the explanation. Relationship and organization explanations
retain their typed subject and actor references. A provider-only delta with no
source/event provenance is rejected, so hidden provider state cannot be the
sole explanation for an evolution result.

## Reproducible evidence

- `tests/unit/substrate/test_g93g_evolution_explainability.py`: 3 passed,
  covering actor trajectory links, reason/source/event/fingerprint queries,
  relationship and organization subjects, and provider-only/invalid-link
  rejection.
- `tests/integration/test_g93g_evolution_explainability_product_chain.py`: 1
  passed. A private rights-approved source traversed OneClickAuthoring,
  WorldPackage, PlayableService, Preview, and SQLite-backed WorldRuntime. The
  actual committed `set_status` event supplied source/event lineage to actor,
  relationship, and organization explanations; the actor trajectory link was
  built from the existing tracker.
- The integration asserted canonical semantic hash, revision, event count,
  and restore/replay hash were unchanged while the explanation projection
  advanced. Each typed delta passed `EvolutionCommitPolicy` validation.
- `scripts/sdk_baseline.py`: `routes=62 ts=5 py=1900`.

## Quality and boundary gates

- Focused G93G regression: `4 passed, 1 warning`.
- Full repository pytest: `1359 passed, 1 skipped, 2 warnings` in
  `327.05s`; the single skip is the documented PostgreSQL
  `EXTERNAL_BLOCKED` profile.
- Ruff check and format check: PASS (`2512 files already formatted`).
- Pyright: 0 errors, 0 warnings, 0 informations.
- `scripts/architecture_check.py`: PASS.
- `scripts/kernel_guard.py`: `0 violation(s)`.
- `git diff --check`: PASS (only Git's CRLF normalization warnings).
- No private source was uploaded, no source text was modified, no model was
  trained, and no v5.6 work was started.

G93G is PASS and is ready for the required commit
`g93g: Evolution Explainability`. Gate 31 is ACCEPTED. Gate 30 remains
pending until G93H completes the integrated 30-day Actor/Relationship/
Organization qualification. Gate 24, G93H-G97J, and the remaining v5.5
release gates remain pending; v5.5 stays `IN_PROGRESS / NOT_ACCEPTED`.
