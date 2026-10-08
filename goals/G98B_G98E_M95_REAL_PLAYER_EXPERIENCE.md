# G98B–G98E — M95 Real Player Experience Acceptance

## G98B — Player Experience Evidence Instrumentation
Add/reuse sanitized session evidence that can link player input → Proposal → Validate/Resolve → Commit → StateDiff → Projection, plus leave/continue identity/replay refs. Instrumentation must not become a second ledger.

Acceptance: deterministic/product E2E proves evidence linkage and privacy filtering; no authority bypass.
Commit: `g98b: add player experience acceptance instrumentation`

## G98C — Real Player Test Route & Readiness
Ensure the real Studio/Experience route supports:
World Plaza → world/scenario → character → enter → observe/free action → response → StateDiff → leave → continue.
Fix only concrete P0/P1/P2 blockers required to make the current v5.5 experience usable; do not redesign the product or add v5.6 features.
Generate `reports/M95_PLAYER_TEST_READINESS.md` and a filled-build version of `M95_PLAYER_TEST_PACKET.md`.
Commit: `g98c: prepare real player acceptance route`

## G98D — Genuine Human Session
A genuine human must execute the route. Playwright, scripted policy, LLM, Codex or synthetic feedback cannot count.
If no human is available, mark `USER_INPUT_REQUIRED`, preserve the packet, and continue independent later goals.

Required evidence:
- sanitized session metadata;
- >=3 free-form actions;
- committed consequence + StateDiff evidence;
- leave/continue continuity evidence;
- human ratings and free-text notes;
- defects with severity.

No code commit required for feedback-only evidence unless repository policy stores sanitized evidence; never store sensitive/private content.

## G98E — M95 Qualification
Resolve discovered P0/P1 issues, rerun the same human route if necessary, and write:
- `reports/M95_REAL_PLAYER_EXPERIENCE_ACCEPTANCE.md`
- `artifacts/v55_stable/m95/player_acceptance.json`

Gates 62–66 may be ACCEPTED only with genuine human evidence and no unresolved P0/P1 issue. Minimum ratings follow `01_STABLE_ACCEPTANCE_MATRIX.md`.

Do not claim population-level UX validation from one/few sessions.
Commit: `g98e: qualify m95 real player experience`
