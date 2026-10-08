# G93H — M90 30d Evolution Qualification

Date: 2026-08-27
Status: PASS

## Scope

G93H qualifies a 30-day run with nonzero, bounded changes in all three
evolution planes: Actor, Relationship, and Organization. The qualification
compares typed baseline/evolved projection snapshots while preserving the
existing source, package, Commit Authority, append-only event history, and
replay path.

## Implemented contract

- `EvolutionProjectionSnapshot` records source/package identity, canonical and
  replay hashes, event references, typed actor/relationship/organization
  fingerprints, evidence refs, and validated delta IDs.
- `EvolutionRunComparison` requires the same run/source/package, an
  append-only canonical prefix, replay equality, a positive 30-day/3,000-tick
  horizon, and nonzero changes in all three projection planes.
- Actor persona adaptation reuses the existing multi-observation,
  review-gated `PersonaDelta` path.
- Relationship evolution reuses the existing `RelationshipGraph` projection
  and reviewed typed relationship deltas.
- Organization lifecycle reuses the existing reviewed organization projection;
  temporal permission checks evaluate authority at the proposal event tick.

No new canonical state, EventStore, Branch, PackageRegistry, SourceRegistry, or
Commit Authority was introduced. Projection advancement did not append
canonical events. The event-tick authority fix closes a real temporal-policy
bug; it does not bypass authority or lower an acceptance threshold.

## Reproducible evidence

The integration test
`tests/integration/test_g93h_m90_30d_evolution_qualification.py` uses a
deterministic private, rights-approved qualification source with
`training_allowed=false`. It traverses the existing `OneClickAuthoring` →
WorldPackage → Preview resolver → PlayableService → real SQLite WorldRuntime
chain. The source payload and content hash are asserted unchanged before and
after the run.

- Horizon: 30 days × 100 world ticks/day = 3,000 world ticks.
- Canonical history: baseline revision/event count 2; evolved revision/event
  count 212; the baseline event-reference tuple remains the evolved prefix.
- Projection changes: 1 Actor persona fingerprint, 1 Relationship fingerprint,
  and 1 Organization fingerprint changed; all three are nonzero and bounded.
- Validated evolution deltas: 7 (1 persona, 2 relationship, 4 organization).
- Evidence refs: 13 unique committed-event/source refs in the evolved snapshot.
- Replay: evolved canonical hash equals the restored/replayed hash.
- Focused G93H tests: `3 passed, 1 warning`.

## Quality and boundary gates

- `scripts/quality.py`: PASS — `1362 passed, 1 skipped, 2 warnings` in
  `327.99s`; the single skip is the documented PostgreSQL
  `EXTERNAL_BLOCKED` profile.
- Ruff check and format check: PASS (`2518 files already formatted`).
- Pyright: `0 errors, 0 warnings, 0 informations`.
- `scripts/architecture_check.py`: PASS.
- `scripts/kernel_guard.py`: `0 violation(s)`.
- Duplicate-abstraction forensics: `oversized_modules=0`, `commit_paths=1`.
- M90 minimality snapshot: 524 production files, 57,036 LOC, 0 cycles, 1
  commit path, `hard_invariants_ok=true`.
- SDK baseline: `routes=62 ts=5 py=1903`.
- No private source was uploaded, no source text was modified, no model was
  trained, and no v5.6 work was started.

G93H/M90 is PASS. Gate 30 is ACCEPTED. The required local commit is
`g93h: M90 30d Evolution Qualification`; G93I is next. Gate 24 and the
remaining M91-M94 gates are still pending, so v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED` and no v5.5 release candidate is authorized.
