# M17 Qualification — Final Independent Certification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G20A, G20B, G20C, G20D, G20E.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M17_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

Stable P0/P1=0; clean-room, security/reliability, black-box author/user/operator and final traceability all PASS; release readiness bundle complete.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M17 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.
