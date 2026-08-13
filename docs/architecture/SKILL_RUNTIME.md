# Skill Runtime (G03F)

Ownership: `wanxiang_substrate.skills` (reusable, resumable structured skills).

## Model

- `SkillDefinition`: versioned skill (id + version + name + steps +
  required_permission). Version must be positive; a skill requires a name and
  at least one step (`ContractError` otherwise).
- `SkillStep`: one validated action with payload, optional required
  capability, duration ticks and cost.
- `SkillInstance`: observable execution state (idle/running/paused/completed/
  failed/cancelled) with current step index and completed step ids.

## Registry

`SkillRegistry` maps `(skill_id, version)` to a `SkillDefinition`;
`register_reference_skills` provides `deliver_letter` (3 steps) and
`inspect_object` (1 step) reference skills.

## Runtime

`SkillRuntime.execute/pause/resume/cancel` drives the state machine. Every step
is expanded to a command submitted through `WorldRuntime` (validate -> resolve
-> commit); the runtime never mutates canonical state directly. After each step
the instance component is updated via `skill.set_state`, so progress is
observable and replayable.

- Permission gate: `skill.start` checks the actor's permission through
  `InstitutionQuery` before any step runs; insufficient permission raises
  `SkillPrerequisiteError`.
- Failure: a step that fails to commit marks the instance `failed` and raises
  `InvalidSkillStep` with the underlying cause.
- Determinism: step payloads are flat `FieldValue` maps; nested data is
  JSON-encoded by the caller. Command ids derive from action type + revision,
  so retries are idempotent within a revision.

## Resolvers

`register_skill_resolvers` registers `skill.start` (creates the versioned
`skill.instance` component) and `skill.set_state` (validates the instance
exists and updates state/step index/completed steps). Both produce
`ProposedWorldDelta` only; commit happens through Commit Authority.

## Compatibility

- `skill.instance` component is schema-versioned (`SKILL_SCHEMA_VERSION = 1`).
- No new table or migration: skill state lives on versioned components in the
  existing canonical store.
- Replay: completed steps and state are stored in the canonical component, so
  a replay reproduces the exact same skill execution.