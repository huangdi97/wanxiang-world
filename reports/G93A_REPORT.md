# G93A — Evolution Delta Taxonomy

Date: 2026-08-27  
Status: PASS

## Implemented contract

The substrate now exposes six immutable, explicitly typed records:
`StateDelta`, `BeliefDelta`, `RelationshipDelta`,
`CapabilityEvolutionDelta`, `PersonaDelta`, and `OrganizationDelta`. Each
record carries schema version, record version, a bounded typed payload, reason,
and `EvolutionProvenance` with source/event references. Scalar state,
confidence, relationship, and capability values are validated at construction;
there is no generic evolution `payload`, `data`, or `metadata` field.

`EvolutionCommitPolicy` validates evidence-bearing proposals and produces only
an `EvolutionCommitReceipt` after the caller supplies an existing canonical
event reference, branch revision, and authority reference. It never mutates a
world, appends an event, or creates a second store. A producer labelled as
Commit Authority is rejected, preserving the existing authority boundary.

The old actor capability/persona tracker now reuses the typed `PersonaDelta`
record while retaining its backwards-compatible constructor and strict rule
that capability application cannot change persona state.

## Reproducible evidence

`tests/unit/substrate/test_g93a_evolution_delta_taxonomy.py`: 5 passed. The
tests cover all six kinds, deterministic fingerprints, schema/scalar
invariants, absence of a generic blob, evidence requirements, and the
proposal/receipt policy.

`tests/integration/test_g93a_evolution_delta_product_chain.py`: 1 passed. It
uses a private, rights-approved local source through OneClickAuthoring,
PlayableService, Preview, and a real SQLite WorldRuntime. A real embodied
action is committed first; all six evolution records then reference that
source and committed event. Their validation and receipt creation leave the
canonical state hash and event count unchanged.

## Quality and boundary gates

- Existing actor-evolution regression plus G93A focused tests: 10 passed.
- Ruff check: PASS.
- Pyright on the changed evolution package and G93A tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.
- `git diff --check`: PASS.
- SDK API baseline regenerated: 62 routes, 5 TypeScript symbols, 1,812 Python
  public names; only additive G93A symbols were recorded.

G93A is PASS and Gate 29 is accepted. G93B-G97J, Gate 24, and the remaining
M90-M94 release gates remain pending. v5.5 remains `IN_PROGRESS /
NOT_ACCEPTED`. No private source was uploaded, no source was modified, no
model was trained, and no v5.6 work was started.
