# Goal G14F Acceptance Report — Hostile Package, Plugin & Source Input Qualification

## Status
PASS

## Objective
Treat packages, compiler inputs and optional plugin code as hostile/untrusted according to the chosen trust model and verify parsing, review and execution boundaries.

## Delivered
- `tests/integration/test_g14f_hostile_input.py` — 6 hostile-input tests.
- `reports/HOSTILE_PACKAGE_SOURCE_QUALIFICATION.md` — trust model + scenarios + limitation.
- `reports/G14F_REPORT.md`.

## Findings
- No critical hostile-input bypass: opaque identifiers, content-hash rejection, default-deny executable
  policy, dependency-conflict rollback (registry unchanged), prompt-injection-as-data, size/format limits.
- Trust model matches implementation: package code is never executed; strong sandboxing is not claimed.

## Evidence
- `uv run pytest tests/integration/test_g14f_hostile_input.py -q` -> 6 passed.

## Remaining limitations
- No OS-level sandboxing; executable plugins are not executed by the platform (trusted-code boundary is
  "trusted or none"), documented explicitly.

## Final checkpoint
- commit: `g14f: hostile package, plugin & source input qualification`
