# G94F — Culture / Ontology Candidate

Date: 2026-08-27
Milestone: M91
Status: **PASS**
Commit: `g94f: Culture / Ontology Candidate`

## Delivered scope

G94F reuses the existing `OntologyCandidate` and `OntologyLawEvolution`; it
does not add a second candidate system, canonical history, Constitution store,
or commit path. `OntologyCandidate` now retains evidence refs, measured
cross-window intervals, NormCandidate refs, InstitutionCandidate refs,
provenance refs, and an explicit reviewer decision.

`OntologyCandidatePolicy` is intentionally strict: by default it requires
three independent NormCandidates, three distinct evidence windows, at least
two observed windows per norm and six total observed windows, support and
confidence of at least 0.9, exception rate no higher than 0.1, stability of at
least 0.85, low derived complexity, and high interpretability. The pure
derivation helper rejects weak, duplicate, single-window, or mixed-pattern
evidence. The pure review helper accepts only the existing authorized reviewer
roles. Evidence-backed candidates cannot pass ontology validation until they
are explicitly reviewed.

## Evidence

- Unit: `tests/unit/substrate/test_g94f_ontology_candidate.py` — 3 passed.
- Product chain: `tests/integration/test_g94f_ontology_candidate_product_chain.py` — 1 passed.
- Focused result: `4 passed, 1 warning`; Ruff, format, and target Pyright pass.
- Full quality: `1381 passed, 1 skipped, 2 warnings`; Ruff, format, Pyright,
  pytest, and architecture conformance all pass. The PostgreSQL skip remains
  the documented `EXTERNAL_BLOCKED` live profile.
- Product-chain path: private rights-approved source → OneClickAuthoring →
  WorldPackage → Preview → PlayableService → SQLite WorldRuntime.
- The integration run derived three disjoint repeated detections and three
  NormCandidates from nine real playable committed actions, reused a reviewed
  InstitutionCandidate, and then created/reviewed the ontology candidate.
- Constitution hash, package manifest hash, canonical revision/hash, event
  history, and replay equality remained unchanged. No Constitution/Law/Canon
  mutation occurred.
- Negative coverage rejects weak or non-cross-window evidence, unauthorized
  review, and ontology validation before explicit review; no universal
  emergence claim is made.

## Acceptance boundary

G94F is complete and locally verified. It proves a strict, evidence-backed
candidate path only; it does not claim universal emergence or an ontology
commit. G94G-G97J and the remaining M91-M94 acceptance gates remain pending.
