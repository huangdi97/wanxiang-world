# Codex Post-M9 Continuous Master Prompt — M10 → M17

> Mission: continue Wanxiang after a claimed M9 completion and execute the entire Post-M9 Program through final M17 certification.
> Do not redesign the product.
> Do not trust conversational completion claims. Verify repository evidence first.

## 0. Start condition

The user states M0–M9/G00A–G12H are complete. Before changing code:

1. read `docs/spec/WANXIANG_v5_MASTER_SPEC.md`;
2. read existing engineering program/standards/acceptance docs;
3. read M9 and final reports, `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
4. inspect Git status/history, source, tests, migrations, deployment and generated SDK/API artifacts;
5. run the narrow critical M9 regression suite.

If M9 is materially regressed, repair the regression as part of the baseline before G13A and record it. Do not redo M0–M9 from scratch when healthy.

## 1. Normative new files

Read in this order:

- `10_POST_M9_PROGRAM_ARCHITECTURE.md`
- `11_CODEX_POST_M9_MASTER_PROMPT.md`
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- `14_AUDIT_TRACEABILITY_PROTOCOL.md`
- `15_ADVERSARIAL_CHAOS_PROTOCOL.md`
- `16_REFERENCE_WORLD_QUALIFICATION_STANDARD.md`
- `17_PRODUCTION_OPERATIONS_STANDARD.md`
- `18_SDK_ECOSYSTEM_STANDARD.md`
- `19_PRODUCT_SURFACE_COMPLETION_STANDARD.md`
- `20_RESEARCH_EXPANSION_V5_1_V6.md`
- `21_FINAL_CERTIFICATION_STANDARD.md`
- current Goal file

Product authority remains `docs/spec/WANXIANG_v5_MASTER_SPEC.md`. Existing M0–M9 standards remain in force unless a later ADR explicitly strengthens them without contradicting the mother spec.

## 2. Execution mode

Execute every Goal in `12_POST_M9_GOALS_INDEX.md` in order. At the end of each milestone execute the corresponding `milestones/Mxx_QUALIFICATION.md`.

A milestone PASS automatically continues to the next milestone. Do not stop for routine user confirmation. If context compresses/restarts, recover from Git + ledgers + latest Goal/milestone report, never chat memory.

Stop only when:

- M17 is completed; or
- a genuinely unrecoverable repository/environment blocker prevents **all** further independent work.

A narrow real-data/provider/hardware blocker does not stop unrelated work.

## 3. Never trust previous PASS blindly

M10 explicitly performs an independent audit. Existing reports are evidence candidates, not authority. Every important requirement must map to:

`spec requirement → implementation owner → test → reproducible runtime/build evidence`.

A class/interface/route/file name by itself is not evidence of completion.

## 4. Core mutation rule

All world-changing input continues through the single authority pipeline:

```text
Command / Intent / Observation / External Proposal
→ normalize
→ validate
→ resolve/adjudicate
→ ProposedWorldDelta
→ expected-revision / invariant checks
→ Commit Authority
→ ordered committed Event
→ canonical state projection
→ audit/trace
```

No UI, LLM, Actor policy, Director, Reality Bridge, plugin, simulator, SDK client, research model, Godot/Babylon/XR/digital-human integration or package compiler may directly mutate Canonical World State.

## 5. Continuous regression rule

After any change touching stable Core, persistence, package contracts, rights, host, SDK or product surfaces, run the smallest affected suite plus the relevant global regression before closing the Goal. At milestone gates run the broad suite defined in the milestone file.

Never make tests green by:

- deleting a failing test;
- reducing an assertion that represented the requirement;
- adding broad skips/xfails;
- disabling type/architecture checks;
- catching and ignoring errors;
- replacing real integration with static fake data.

## 6. Gap closure priority

- P0: correctness, authority, data loss, replay/branch, critical security/rights, fake completion of mandatory path. Must close before M11.
- P1: required maintainability/integration/compatibility/observability/security/release defect. Must close before relevant later gate.
- P2: useful but non-blocking debt/optimization. Track explicitly; do not smuggle into DONE.

## 7. Real-data Source Gate

Red Chamber, Liaoshen, real family records, real heritage collections, real sensors and real-person digital human assets remain source/rights gated.

If missing, complete generic contracts, synthetic fixtures, source-gate tests, rights checks and external-blocker report. Never fabricate canonical real content from model memory.

## 8. M16 research rule

M16 is allowed to experiment, but:

- experimental features are OFF by default;
- they live behind explicit Port/feature flags/experimental namespaces;
- stable data schemas are not silently repurposed;
- research model output remains proposal/candidate/observation;
- stable regression with flags OFF must pass;
- each track ends with `PROMOTE`, `KEEP_EXPERIMENTAL` or `REJECT` and evidence.

## 9. Per-goal reporting and Git

For each Goal:

1. read Goal completely;
2. inspect current relevant code/tests;
3. update `PLAN.md` and `STATUS.md`;
4. implement in small cohesive changes;
5. run requested tests + quality gates;
6. update traceability/acceptance artifacts where applicable;
7. write `reports/<goal_id>_REPORT.md` (or the Goal-specific report names);
8. update `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
9. create a local Git checkpoint only when Goal acceptance passes.

Do not push or deploy externally unless the user separately authorizes it.

## 10. Final stop condition

Do not claim completion until M17 generated at least:

- `reports/FINAL_DESIGN_TRACEABILITY.md`
- `reports/CLEAN_ROOM_CERTIFICATION.md`
- `reports/FINAL_SECURITY_RELIABILITY_CERTIFICATION.md`
- `reports/BLACKBOX_FINAL_ACCEPTANCE.md`
- `reports/M17_FINAL_CERTIFICATION.md`
- `reports/FINAL_PROGRAM_COMPLETION_REPORT.md`
- `docs/RELEASE_READINESS.md`
- `docs/POST_V5_ROADMAP.md`

Stable P0/P1 gaps must be zero. `EXTERNAL_BLOCKED` and M16 experimental/rejected items must be explicit and must not be described as complete stable functionality.

Then stop after a local checkpoint and report to the user.
