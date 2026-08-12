# Resolver, Adjudication & Deterministic Policies (G03E)

Ownership: `wanxiang_substrate.resolution` (auditable resolution outcomes).

## Model

- `Adjudication`: action type + version + seed + outcome + ProposedWorldDelta +
  explanation + observability + provenance + uncertainty.
- `ResolverVersionPin`: pins the resolver version for an action in a
  run/world context (missing version fails explicitly).
- `SeededRng`: deterministic RNG owned by the adjudicator (seed + stream +
  counter); no globals.

## Reference adjudicators

- `DeterministicTransferAdjudicator`: deterministic resource transfer (delta
  only; uncertainty 0).
- `GambleAdjudicator`: seeded probabilistic success/failure with provenance
  (`rule:seeded_gamble:v<version>:seed<seed>`).

## Service

`AdjudicationService.resolve(command, state, seed, pins)` returns an
Adjudication and dry-runs the delta on a copy to prove compatibility before
Commit Authority. It never commits; the delta is submitted through the normal
authoritative path.

## Compatibility

- Resolver versions are pinned per action; a missing/incompatible version
  raises `ResolverVersionError` (no silent substitution).
- Outcomes are replayable: same seed + version -> same adjudication.
