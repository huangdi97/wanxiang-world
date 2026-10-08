# M81 / G84 Worldness Calibration

Date: 2026-08-25
Scope: adversarial Worldness calibration; no model training.

## Decision

`PASS` for the synthetic adversarial calibration and threshold policy.

## Evidence

Artifact: `artifacts/m79_m84/worldness_calibration.json`

The intact baseline scores 0.98 and passes the independent preview, publish,
and living-ready gates. Seven deliberately broken cases were evaluated:

- teleportation
- secret leakage
- duplicate object
- temporal reversal
- unsupported fact
- replay mismatch
- identity corruption

Every broken case fails the publish and living-ready gates, and every repair
restores the baseline score and all gates. The minimum adversarial score drop
is 0.092. The calibration reports both `anti_gaming_passed: true` and
`threshold_policy_passed: true`.

The scoring path measures identity, time, space, causality, epistemic
isolation, object consistency, uncertainty, replay, evidence coverage, and
action evidence. A successful endpoint without action evidence references
cannot satisfy the living-ready gate.

## Boundary

This is a synthetic calibration of the gate behavior, not a claim that the
missing second real book or GEDCOM source has passed Worldness or family
validation. Those real-source gates remain pending user input.
