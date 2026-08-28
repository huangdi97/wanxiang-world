# Wanxiang / 万相 v5.5 M95–M100 Stable Certification Goal Pack

Date: 2026-08-28
Scope: v5.5 Stable Certification only. **Do not enter v5.6. Do not train a Wanxiang-owned model.**

## Canonical inputs

1. `万相世界_v5.5-RC1-R3_Playable_Persistent_Evolving_Living_World_OS_完整母版_截至2026-08-28.md` — sole design master.
2. `V55_FINAL_RELEASE_REPORT.md` — current v5.5.0-rc1 release/closure evidence.
3. `M79_M84_STATUS.md` — historical v5.4 Stable delivery evidence.
4. Current repository, Git history, tags, remote branch, CI, reports, tests, migrations and release metadata — engineering reality to be verified before changing code.

## Frozen current truth

- `v5.4.0` is already Stable and must not be rebuilt or rewritten.
- `v5.5.0-rc1` is already a GitHub prerelease.
- M85–M94 are closed for RC scope.
- Gates 1–59 = ACCEPTED; Gate 60 = ACCEPTED_FOR_RC.
- Final Closure uses latest authoritative qualification while preserving historical failures.
- Prompt Genesis, reference/deterministic providers, bounded long-horizon / World Lab / emergence remain EXPERIMENTAL/BOUNDED.
- Heavy physical/visual provider E2E and live PostgreSQL profile remain unverified / EXTERNAL_BLOCKED unless newly proven by real evidence.

## New work only

M95 Real Player Experience Acceptance
→ M96 Original Prompt World Acceptance
→ M97 Experience Quality Benchmark
→ M98 Emergence / Multi-run / Scale Burn-in
→ M99 Optional Real Godot Projection Integration
→ M100 v5.5 Stable Certification
→ `v5.5.0` Stable
→ STOP

## Release-governance rule

Do **not** append Stable work into the RC Gates 1–60 as if they were the same gate generation. Create a new stable-certification ledger: Gates 61–80. Old reports remain immutable evidence. New qualification may reference old accepted evidence but may not rewrite it.

## Execution rule

For every Goal:
1. inspect current code and existing tests first;
2. reuse architecture and contracts; do not create a second truth/state/event/branch system;
3. implement only the missing delta;
4. run focused tests, then applicable regression/quality gates;
5. write machine-readable and human-readable evidence;
6. commit after PASS;
7. push without force only when allowed by repository policy;
8. if a human/external environment is missing, record `USER_INPUT_REQUIRED` or `EXTERNAL_BLOCKED`, then continue every independent Goal;
9. never convert mock/reference/synthetic evidence into a real-product or real-human claim.

Start with `goals/G98A_STABLE_BASELINE_AND_LEDGER.md`.
