# Action, Affordance & Validator (G03D)

Ownership: `wanxiang_substrate.actions` (structured action definitions,
affordances, side-effect-free validation before resolution).

## Model

- `ActionDefinition`: action type + version + parameter schema (+ optional
  permission/resource cost); versioned registry.
- `ValidationIssue` / `ValidationResult`: structured rejection reasons.
- `Affordance`: whether an actor can perform an action now, with reasons.

## Validator

`ActionValidator.validate(command, state)` is pure (no mutation) and rejects
before resolution:
- unknown action/version (explicit `unknown_action`);
- parameter schema (missing/wrong type);
- actor existence/aliveness/activation;
- permission (institution);
- reachability (spatial path for `spatial.move`);
- epistemic validity (`material.read_payload` requires knowledge of the item);
- resources (`body.rest` requires a body condition).

Reference actions: move, read_payload, deliver_message, rest, inspect.

## Affordances

`compute_affordances(actor, state, registry, validator)` returns the currently
available actions with reasons for unavailable ones.

## Compatibility

- Action definitions are code-level contracts (versioned); no new persisted
  table; validator is deterministic and replay-agnostic.
