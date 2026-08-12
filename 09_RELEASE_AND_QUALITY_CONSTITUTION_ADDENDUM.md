# Release and Quality Constitution Addendum — M2 to M9

This addendum strengthens the existing `02_ENGINEERING_STANDARDS.md` for the much larger continuation phase.

## 1. Maintainability is an acceptance property

A Goal that technically passes behavior tests but materially worsens architecture may not be marked PASS until the issue is fixed or explicitly justified.

Inspect:
- module cohesion;
- dependency direction;
- import cycles;
- file/function/class growth;
- duplicated schemas and rules;
- semantic ownership;
- error handling;
- observability;
- migration/version seams;
- test readability;
- adapter isolation.

## 2. Small modules, not artificial fragmentation

The approximate 300-line source-file target is a trigger for review, not an instruction to create meaningless one-function files. Split around stable responsibilities:
- domain type/invariant;
- application use-case;
- port;
- adapter;
- repository;
- serializer/schema;
- policy/resolver;
- projection;
- test fixture.

Avoid both God files and excessive wrapper layers.

## 3. Naming

Use names from the master ontology. Do not create synonyms such as `Universe`, `GameSave`, `StoryState` or `MasterState` for existing formal concepts unless an ADR explicitly defines a different local role.

Prefer:
- `WorldInstance`, `Branch`, `Session`, `Projection`;
- `Observation`, `Belief`, `Memory`;
- `Intent`, `Action`, `Adjudication`, `WorldDelta`;
- `Source`, `Claim`, `Evidence`, `RightsEnvelope`;
- `Run`, `ExperimentSpec`, `ValidityEnvelope`.

## 4. Public API stability

Freeze one canonical API vocabulary through ADR. Avoid parallel aliases such as both `/world-pack/import` and `/world-packages/import`.

Breaking public API changes require:
- version/deprecation decision;
- generated client update;
- compatibility test;
- changelog entry.

## 5. Database ownership

Only persistence adapters know ORM implementation details. Domain/application/runtime objects must not become SQLAlchemy models by inheritance or accidental import.

Migrations must:
- be deterministic;
- be tested from retained old fixtures;
- never silently destroy event provenance;
- update schema version metadata;
- include recovery guidance for destructive operations.

## 6. Event compatibility

Events are long-lived contracts.

Do not:
- rename fields and reinterpret old data silently;
- derive old meaning from current defaults;
- drop event versions;
- let a renderer/model version affect replay without recording it.

Use explicit versioned readers/upcasters/migrations where necessary.

## 7. Frontend quality

React/Phaser work must include:
- TypeScript strict;
- generated API types;
- accessible labels/keyboard behavior for core Studio controls;
- explicit loading/error/empty/conflict states;
- no duplicated business rule implementation;
- no secrets/privacy filtering that exists only client-side;
- Playwright vertical tests for authoritative command flows.

## 8. Domain plugin discipline

Family, Heritage, Narrative, Campaign and future domains:
- register schemas/rules/resolvers through declared extension points;
- may not import persistence internals;
- may not call Commit Authority directly except through normal application contracts;
- may not patch Core conditionals based on package name;
- must carry their own eval fixtures.

If Core must be changed for a domain, prove the capability is truly domain-general and add a generic contract/test.

## 9. External adapter discipline

Every sensor/simulator/model/renderer/digital-human/asset adapter needs:
- port contract;
- version/identity;
- timeout/failure model;
- deterministic fake;
- contract tests;
- input validation;
- rights/security where relevant;
- no canonical mutation authority.

## 10. Test readability

Prefer test names that state invariant/behavior. Use fixtures/builders with semantic names rather than opaque blobs. Large golden files require a documented update procedure.

No snapshot test should become a replacement for semantic assertions on critical authority, rights or epistemic behavior.

## 11. Performance work

Profile before optimizing. Any cache must define:
- key;
- invalidation;
- authority status;
- memory bound;
- replay/restart behavior.

A cache never becomes truth.

## 12. Security

At minimum:
- no secrets in repo/logs;
- source content treated as untrusted data;
- upload validation;
- least-privilege admin/debug/export;
- private memory and living-person data access tests;
- audit history protected from ordinary deletion;
- generated/reconstructed content labeled;
- dependency/license/security reports at M9.

## 13. Release evidence

M9 is an engineering release-qualification claim, not a legal/compliance certification. Reports must state exactly what has been verified in the current environment and what remains external or unaccredited.
