# ADR-0023: Skill Runtime Design (G03F)

- Status: accepted
- Date: 2026-08-13

## Context

G03F needs reusable, resumable structured skills that expand intents into
validated actions with explicit prerequisites, cost, duration and failure
handling, without creating a second mutation path.

## Decision

1. Skills are versioned definitions (`SkillDefinition` + steps) stored in a
   `SkillRegistry` keyed by `(skill_id, version)`.
2. `SkillRuntime` expands steps one at a time and submits every generated
   action through `WorldRuntime` (validate -> resolve -> commit); it never
   mutates canonical state directly.
3. Skill execution state is persisted as a versioned `skill.instance`
   component (state, current step index, completed step ids), so progress is
   observable, resumable and replayable.
4. Permission prerequisites are enforced at `skill.start` via
   `InstitutionQuery`; insufficient permission blocks start with
   `SkillPrerequisiteError`.
5. Step failure marks the instance `failed` and raises `InvalidSkillStep`
   carrying the underlying cause; no silent failure.

## Consequences

- All skill side effects remain auditable events behind Commit Authority.
- Replay reproduces identical skill executions; no new table/migration.
- Skills are reusable across actors/worlds via the registry.