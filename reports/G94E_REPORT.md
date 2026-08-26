# G94E — Institution Candidate

Date: 2026-08-27
Status: **PASS**
Commit: `g94e: Institution Candidate`

## Scope

G94E adds the institution-candidate layer required by M91. It deliberately
reuses the existing `InstitutionCandidate` and explicit
`InstitutionPromotionChain`; it does not create a second candidate system,
second history, or second commit path.

The existing candidate record now retains structured rule, role, resource,
process, provenance, and reviewer references. A pure derivation helper accepts
only a `NormCandidate`, validates the required structure, and preserves the
norm detection/scope/event lineage. A separate pure review helper records an
approved reviewer only after the structure is complete. Review does not call
Commit Authority, activate a norm, mutate Constitution/Law, or alter canonical
history. Existing institution-law promotion remains an explicit, approved
operation through the pre-existing controlled chain.

## Evidence

- Unit: `tests/unit/substrate/test_g94e_institution_candidate.py` — 2 passed.
- Product chain: `tests/integration/test_g94e_institution_candidate_product_chain.py` — 1 passed.
- Focused Ruff check and format check: PASS.
- Focused Pyright target: PASS.
- Product-chain path: private rights-approved source → OneClickAuthoring →
  WorldPackage → Preview → PlayableService → SQLite WorldRuntime.
- The integration evidence derives repeated committed events from the runtime,
  builds a scoped NormCandidate, derives structured institution evidence,
  reviews it with an approved reviewer, and verifies canonical revision/hash,
  event history, and replay remain unchanged.
- Negative coverage rejects incomplete role/resource/process structure and an
  unauthorized reviewer; no manager or single helper can auto-commit.

## Boundary result

G94E is complete and locally verified. It does not by itself promote the
remaining M91 emergence gates or release v5.5. G94F-G97J and the remaining
M91-M94 acceptance gates remain pending.
