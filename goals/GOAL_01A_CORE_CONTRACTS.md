# GOAL 01A — Core Semantic Contracts

## Objective

Define a minimal, durable, framework-independent set of typed semantic contracts required by the authoritative world kernel, including identity, versioning, commands, events, deltas, snapshots, branches, claims/evidence/rights foundations and structured errors.

## Scope

Core contracts only. They must be rich enough for G01B–G01F but must not pre-build later Living World Substrate, cognition, skills or domain packages.

At minimum evaluate/define:
- WorldInstance identity;
- Branch identity/revision/ancestry metadata;
- Entity / Component / Relation minimal identity contracts;
- Command/ActionIntent base envelope sufficient for deterministic micro-world;
- ProposedWorldDelta;
- CommittedEvent envelope;
- CanonicalState representation boundary;
- Snapshot metadata;
- Run metadata if needed for determinism;
- Claim/Evidence references as foundational first-class concepts;
- RightsEnvelope/decision foundation sufficient to avoid redesign later;
- schema/runtime version identifiers;
- structured error taxonomy.

## Non-goals

- no spatial/body/schedule model;
- no Temporal Epistemic Graph;
- no complete Rights product policy;
- no Source Registry compiler;
- no World Package implementation;
- no SQLAlchemy models in domain;
- no HTTP routes required.

## Required reading

- master spec sections on first-class objects, canonical state, world hierarchy, rights/provenance, versioning;
- Program Architecture event/commit/version contracts;
- Engineering Standards.

## Architecture constraints

- framework-independent;
- serialized forms are explicit and versioned;
- avoid one universal `dict[str, Any]` event/delta model;
- support extension without adding real-world-specific core enums;
- distinguish world time from wall-clock commit time;
- distinguish Proposal from CommittedEvent.

## Deliverables

- typed domain modules organized by responsibility;
- error hierarchy;
- serialization contracts/version metadata;
- domain contract tests;
- architecture doc explaining ownership and extension points.

## Implementation tasks

1. Define strong ID/value types where useful without excessive ceremony.
2. Define branch revision/event sequence semantics explicitly.
3. Define command envelope including idempotency/causation/correlation fields as needed.
4. Define `ProposedWorldDelta` in a way that can be validated/applied but does not permit arbitrary hidden mutation.
5. Define immutable committed event envelope.
6. Define canonical state read model boundary and semantic hashing strategy inputs; avoid hashing non-semantic wall-clock/debug fields.
7. Define snapshot metadata and version fields.
8. Define foundational Claim/Evidence reference contracts; a source is not automatically a fact.
9. Define foundational RightsEnvelope/decision hooks while keeping full policy later.
10. Define schema version and incompatible-version errors.
11. Write serialization round-trip tests.
12. Write property tests for valid IDs/revisions and rejected invalid values.
13. Ensure domain has zero forbidden framework imports.
14. Document decisions where multiple representations were plausible.

## Tests

- construction/validation tests;
- serialization round trip;
- invalid revision/version cases;
- semantic hash stability for equivalent deterministic canonical state;
- typecheck and architecture tests.

## Acceptance criteria

- later Commit/EventStore can be implemented without changing fundamental names/ownership;
- no SQLAlchemy/FastAPI imports in domain;
- Proposal and Commit records are distinct;
- branch/event sequence version semantics documented;
- rights/evidence foundations exist early enough to prevent later schema breakage;
- tests pass without external services.

## Failure / blocker handling

Resolve ambiguity using master semantics and record ADR. Do not overbuild generic metamodels to cover every future domain.

## Documentation updates

- `docs/architecture/CORE_CONTRACTS.md`;
- DECISIONS;
- acceptance matrix;
- goal report.

## Git / checkpoint requirements

`goal 01A: define authoritative world core contracts`
