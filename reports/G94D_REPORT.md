# G94D — Social Norm Candidate

Date: 2026-08-27  
Milestone: M91  
Status: **PASS**

## Delivered scope

`NormCandidate` is a population-level, immutable candidate record derived from
a qualified repeated detection. It preserves a local/global scope, population
refs, occurrence/window support, source and exception event refs, exception
rate, confidence, and optional committed-event-linked reward/sanction outcome
evidence. `NormPromotionPolicy` supplies explicit small-sample, support,
exception, confidence, and outcome-correlation thresholds.

`NormEvaluation` is pure review input. Small populations are rejected at
construction; exception-heavy and weakly supported candidates remain
ineligible. No candidate method owns a Commit Authority, EventStore, or
canonical mutation path, and no evaluation is treated as automatic truth.

## Evidence

- Unit tests: `tests/unit/substrate/test_g94d_norm_candidate.py` — 2 passed.
  They cover population/scope, committed reward/sanction correlation,
  small-sample rejection, exception ceilings, and typed outcome validation.
- Integration test:
  `tests/integration/test_g94d_norm_candidate_product_chain.py` — 1 passed.
  Repeated committed status events over two subjects from a private
  rights-approved source → WorldPackage → Preview → PlayableService → SQLite
  WorldRuntime formed and evaluated a scoped norm candidate while canonical
  hash and replay remained unchanged.
- Focused quality: `3 passed, 1 warning`; Ruff, format, and target Pyright
  passed.
- M91 minimality now records 14 bounded abstractions across observation,
  detection, actor-candidate, and norm-candidate layers. No second history,
  registry, runtime, or Commit Authority was introduced.

## Acceptance boundary

G94D proves population support, exceptions, scope, and outcome correlation only.
It does not claim an activated norm, institution, culture, universal
emergence, or a v5.5 release. G94E-G94H and later M92-M94 gates remain
required.

## Commit

Required commit: `g94d: Social Norm Candidate`.
