# G94A — Pattern Observation Store

Date: 2026-08-27  
Milestone: M91  
Status: **PASS**

## Delivered scope

`PatternObservationStore` is an immutable, rebuildable derived cache over the
existing `CommittedEvent` stream. It provides deterministic half-open windows,
typed behavior/relationship/exchange/organization observations, feature values,
aggregate statistics, committed event references, serialization, and a cache
hash. Entity, relation, actor, and operation references are retained without
copying source payload fields into a new truth store.

The implementation does not own or mutate an EventStore, Branch, Canonical
State, Package Registry, Source Registry, Candidate system, or Commit Authority.
No persistence schema or migration was required because the cache is
rebuildable and not persisted as canonical data.

## Evidence

- Unit tests: `tests/unit/substrate/test_g94a_pattern_observation_store.py` —
  2 passed. They cover all four observation kinds, windows, features,
  statistics, event refs, order-independent rebuild hashing, duplicate/mixed
  history rejection, and invalid windows.
- Integration test:
  `tests/integration/test_g94a_pattern_observation_store_product_chain.py` —
  1 passed. A private rights-approved source traversed
  `OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
  WorldRuntime`; the cache rebuilt from real committed events and from reversed
  input with identical output. Canonical hash, revision, event refs, replay,
  and source bytes remained unchanged.
- Focused quality: `3 passed, 1 warning`; Ruff and target Pyright passed.
- Architecture/minimality/SDK evidence: architecture test passed; current
  deterministic metrics are `57452` production LOC / `526` production files,
  `16` registries, `25` services, `5` engines, `41` ports, `37` state classes,
  `30` stores, `0` cycles, `1` commit path, `0` oversized modules, and
  `hard_invariants_ok=True`; SDK baseline is `routes=62 ts=5 py=1907`.

## Acceptance boundary

G94A is accepted as a store-only foundation. It does not claim repeated
patterns, emergence, automatic truth, or a v5.5 release. G94B-G94H and the
remaining M91-M94 certification gates are still required.

## Commit

Required commit: `g94a: Pattern Observation Store`.
