# G93B — Capability Growth

Date: 2026-08-27  
Status: PASS

## Implemented contract

`CapabilityCandidate` now records actor, target capability, domain reference,
practice and assessment evidence refs, composition refs, accumulated practice
count, success/failure counts, bounded before/after capability values, and
provenance. `CapabilityPrerequisite` requires a domain-supported capability
and a bounded minimum level. Candidate creation rejects targets outside the
declared domain, missing prerequisites, unavailable composition skills, and
absence of practice/composition evidence.

Validation requires at least three accumulated practice counts, assessment
evidence, one successful outcome, and no failure majority. Failure-dominant
evidence remains an explicit invalid result and cannot silently promote. A
valid candidate produces `CapabilityPromotionProposal` containing both the
typed G93A `CapabilityEvolutionDelta` and the existing `CapabilityDelta` input
for the normal `capability.apply_delta` resolver. `action_payload()` only
serializes resolver fields; it does not submit a command.

Independent practice records are accumulated before applying the existing
learning policy, so three one-count records produce one level of growth rather
than three zero-level floors. This reuses the existing capability policy and
does not create another capability store or authority.

## Reproducible evidence

- `tests/unit/substrate/test_g93b_capability_growth.py`: 5 passed, including
  impossible domain support, missing prerequisites/composition, failure
  majority, validation identity, and successful promotion.
- `tests/integration/test_g93b_capability_growth_product_chain.py`: 1 passed.
  A private rights-approved source traversed OneClickAuthoring,
  PlayableService, Preview, and SQLite WorldRuntime. After a real embodied
  action, a validated watchkeeping candidate was submitted through the
  existing `capability.apply_delta` resolver; the committed actor skill was
  replay-equal and carried the candidate evidence refs.

## Quality and boundary gates

- G93A regressions plus G93B focused tests: 16 passed; one existing Hypothesis
  collection warning.
- Ruff check: PASS.
- Pyright on the changed evolution package and G93A/G93B tests: 0 errors,
  0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.

G93B is PASS and committed. M90 Gate 30 remains pending until the complete
G93H 30-day Actor/Relationship/Organization qualification. G93C-G97J and
Gate 24 remain pending; v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No private
source was uploaded, no model was trained, and no v5.6 work was started.
