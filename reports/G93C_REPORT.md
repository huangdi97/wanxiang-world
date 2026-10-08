# G93C — Persona Adaptation

Date: 2026-08-27  
Status: PASS

## Implemented contract

`PersonaTraitState` defines six bounded slow-variable dimensions: trust,
caution, openness, resolve, empathy, and discipline. `PersonaObservation` is
an event-bound signal with a direction, strength, and world-time. The
adaptation policy requires a multi-event window and a minimum time span;
observations outside the actor/trait/window are ignored.

`propose_persona_adaptation` computes a deterministic weighted signed change,
clamps it to the policy's maximum change, and emits a single-trait
`PersonaAdaptationProposal` carrying the existing typed `PersonaDelta` plus
all evidence refs. A single event, short window, or full-persona rewrite cannot
pass. Proposals start in `review` and `review_persona_adaptation` records an
immutable allowlisted reviewer decision; the policy/actor/provider layer never
owns canonical Commit Authority.

## Reproducible evidence

- `tests/unit/substrate/test_g93c_persona_adaptation.py`: 4 passed, covering
  trait dimensions, multi-event windowing, maximum change bounds, one-event
  rejection, short-window rejection, immutable review, and reviewer policy.
- `tests/integration/test_g93c_persona_adaptation_product_chain.py`: 1 passed.
  A private rights-approved source traversed OneClickAuthoring,
  PlayableService, Preview, and SQLite WorldRuntime. A committed product
  event supplied the observation lineage; an approved persona proposal was
  applied only to the detached actor projection, while canonical hash,
  event stream, and replay remained unchanged.

## Quality and boundary gates

- G93A/G93B regressions plus G93C focused tests: 21 passed; one existing
  Hypothesis collection warning.
- Ruff check: PASS.
- Pyright on the changed evolution package and G93A-G93C tests: 0 errors,
  0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.

G93C is PASS and committed. Gate 30 remains pending until G93H's complete
30-day Actor/Relationship/Organization qualification. G93D-G97J and Gate 24
remain pending; v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No private source
was uploaded, no model was trained, and no v5.6 work was started.
