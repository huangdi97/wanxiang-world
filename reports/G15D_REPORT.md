# Goal G15D Acceptance Report — Human Embodiment, Exit, Re-entry & Control Continuity Qualification

## Status
PASS

## Objective
Prove a human can take over a character/body, leave, and later return while the world and shadow/autonomous policy continue coherently.

## Delivered
- `tests/integration/test_g15d_embodiment.py` — full embodiment/exit/re-entry scenario.
- `reports/EMBODIMENT_CONTINUITY_QUALIFICATION.md`, `reports/G15D_REPORT.md`.

## Findings
- Human takeover via embodiment lease (one primary controller; conflicting takeover rejected).
- Human commands are normal committed actions through Commit Authority.
- Shadow advice recorded; handoff resumes autonomous control after exit.
- World advances after user exit (no freeze).
- Re-entry receives the authoritative current perspective (not a stale snapshot).

## Evidence
- 1 test passed; ruff/pyright clean.

## Remaining limitations
- Real human clients/transport remain EXTERNAL_BLOCKED; deterministic session/lease semantics qualified.

## Final checkpoint
- commit: `g15d: human embodiment, exit, re-entry & control continuity qualification`
