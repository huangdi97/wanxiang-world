# M12 Qualification — Reference World & Worldness Certification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G15A, G15B, G15C, G15D, G15E, G15F, G15G, G15H, G15I, G15J.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M12_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

Comprehensive synthetic world passes worldness criteria and long-run/replay/branch/human-control tests; real reference slices are PASS or narrow EXTERNAL_BLOCKED.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M12 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.
