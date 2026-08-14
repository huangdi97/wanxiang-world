# Minimal-Core Code Constitution

## 1. Prime directive

Prefer **semantic richness in data/contracts** and **implementation minimalism in permanent core code**.

## 2. Hard anti-bloat rules

- No design-noun-driven class creation.
- No `WorldRealityCalculusEngine` unless executable behavior exists that cannot live in current core semantics.
- No separate `StateCommitEngine`, `OntologyCommitEngine`, `LawCommitEngine`; use one commit pipeline with typed payloads.
- No `GenesisPackageRegistry`; Genesis is a spec/initialization contract under the existing package system.
- No separate registries for models, simulators, projections, plugins and providers when one typed Runtime Capability Catalog can express them.
- No giant `Manager`, `Service`, `Utils`, `Helpers`, `Engine` God objects.
- No global mutable singleton registry/service locator.
- No ORM session exposure to domain/provider/plugin code.
- No second authoritative UI/client state.
- No duplicated Python/OpenAPI/TypeScript schemas.

## 3. File/function/class quality

- Keep modules cohesive and normally <= ~300 production lines; larger modules require an ADR or clear cohesion argument.
- Prefer pure functions/value objects for deterministic semantic operations.
- Prefer composition over inheritance hierarchies.
- Public contracts and event schemas are typed/versioned.
- Constructors should not hide I/O.
- Errors are explicit domain/application exceptions; no broad silent catch.
- `Any` is exceptional, localized and justified.

## 4. Interface rule

Create a Port/Protocol when the boundary is actually replaceable, external, nondeterministic or independently versioned. Do not create Port→Service→Manager→Adapter chains for internal pure logic with one implementation.

Primary justified ports include persistence, LLM/model provider, Agent Harness, Simulator, Sensor/Reality Connector, Renderer/Projection, Asset Store, external Search/Retrieval and external network APIs.

## 5. Dependency rule

Core/domain semantic code must not import FastAPI, SQLAlchemy/Alembic, React/TS, concrete LLM SDKs, DeepSeek Harness/Cordis, Godot/Babylon, cloud SDKs or concrete simulator SDKs.

Architecture tests must enforce forbidden imports and forbidden direct canonical writes.

## 6. Minimality evidence

Maintain `reports/V5_1_CODE_MINIMALITY_LEDGER.md` with:

- production LOC by top-level package;
- count of public classes/protocols;
- registries/catalogs;
- managers/services/engines;
- duplicate schema definitions;
- dependency cycles;
- unused public interfaces;
- dead-code candidates;
- additions/deletions per Goal;
- justification for every new long-lived abstraction.

Raw LOC reduction is not allowed to destroy readability or correctness. The desired outcome is fewer concepts/duplications and a stable or smaller core surface.

## 7. Consolidation preference

When two old abstractions overlap:

1. identify semantic owner;
2. migrate call sites/tests;
3. preserve compatibility adapter only if externally required;
4. deprecate with explicit sunset;
5. delete old implementation once evidence proves no live path depends on it.

## 8. Schema/migration rule

Every persisted/event/public schema change includes versioning and migration/replay compatibility. Never reinterpret old events silently with new semantics.

## 9. Test quality

Tests must prove behavior, not line coverage. Prefer invariant/property/contract/replay/migration/negative tests around semantic boundaries. Never weaken a requirement to make a test green.
