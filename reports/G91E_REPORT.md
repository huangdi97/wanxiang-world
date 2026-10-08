# G91E — Experiment Intervention

Date: 2026-08-26  
Status: PASS

## Result

`InterventionTrigger` makes time and committed-event triggers explicit.
`Intervention` is a schema-versioned, artifact-linked proposal with a typed
intervention kind, parent branch ref, payload refs, and reversible setup. A
reversal is another proposal record; it is not a mutation of the original
worldline.

`ExperimentSetup` is immutable and carries the interventions that will later
be included in a `WorldRunArtifact`. `ExperimentInterventionRunner` delegates
only child branch creation to the existing runtime branch boundary. It never
applies an intervention or writes an event, and the parent event history/hash
remain unchanged in the real reference-runtime qualification.

## Evidence

- `tests/integration/test_g91e_experiment_intervention.py`: 2 passed.
- `uv run ruff check`, format check, and `uv run pyright` on changed files:
  PASS; 0 errors and 0 warnings.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.

G91E is complete and committed. Gate 20 remains pending until the M88
qualification records the branch/artifact isolation through the full playable
path; G91F is next and v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No model
training or v5.6 work was performed.
