# G94B — Repeated Pattern Detector

Date: 2026-08-27  
Milestone: M91  
Status: **PASS**

## Delivered scope

`RepeatedPatternDetector` reads only the G94A immutable observation cache. Its
reference algorithm groups by typed kind/key, counts occurrences and distinct
windows, evaluates support over the requested half-open range, computes a
bounded deterministic confidence score, and emits concrete missing-window
counterexamples. `RepeatedPatternPolicy` makes all thresholds explicit.

Detection is a read-only result. `qualified`/`meets_threshold` is not truth,
does not create a Candidate, and cannot submit a command or alter canonical
state. Same-window duplicate observations do not satisfy multi-window
stability, and sparse/one-off signals remain visible as unqualified results.

## Evidence

- Unit tests: `tests/unit/substrate/test_g94b_repeated_pattern_detector.py` —
  2 passed. They cover deterministic qualified repetition, confidence and
  event refs, one-off and same-window false positives, concrete counterexamples,
  threshold validation, and the convenience facade.
- Integration test:
  `tests/integration/test_g94b_repeated_pattern_detector_product_chain.py` —
  1 passed. A private rights-approved source traversed
  `OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
  WorldRuntime`; repeated committed actor actions produced a qualified
  behavior detection while canonical hash, event history, and replay remained
  unchanged.
- Focused quality: `3 passed, 1 warning`; Ruff, format, and target Pyright
  passed.
- The M91 minimality allowance now records 7 bounded abstractions for the
  observation/detector foundation; no second history, registry, runtime, or
  commit path was added.

## Acceptance boundary

G94B validates deterministic detection and false-positive handling only. It
does not claim habit, norm, institution, culture, universal emergence, or a
v5.5 release. G94C-G94H and the later M92-M94 certification gates remain
required.

## Commit

Required commit: `g94b: Repeated Pattern Detector`.
