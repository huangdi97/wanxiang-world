# G88H — M85 Playable E2E Qualification

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Real product-chain evidence

The qualification used the existing v5.4 one-click source pipeline to create a
WorldPackage, then registered that package in the shared `PlayableService`.
The CLI, API, and Studio UI all call that same facade; no test candidate or
manually populated canonical state was used.

| Step | Evidence |
|---|---|
| Source → WorldPackage | `OneClickAuthoring` book flow produced `world:wd_job_cli_playable` with two source-derived entities |
| Plaza / My Worlds | API `/experience/plaza` returned the public profile and owner session cards |
| Character entry | API created `ent_alice`, then entered embodiment through the existing lease service |
| Free action | `set status to awake` produced `ActionProposal(status=proposed)` and one committed event through the runtime |
| StateDiff | Diff was computed from committed before/after state and contained one actor change |
| Replay | `replay_equal=true` from the existing runtime replay path |
| Leave / Continue | Continue returned the same `prv_playable_1` instance and the same post-commit state hash |
| Studio/browser surface | `/studio/ui` contains World Plaza, enter, free-action, leave, and continue controls wired to the API routes |
| Authorization | Another principal received HTTP 404 for the private instance index |
| CLI result | `scripts/playable_e2e.py` emitted sanitized evidence only; `source_path_or_digest_emitted=false` |

## Gates

Focused API and core E2E tests: **2 passed**. Targeted ruff, format, pyright,
architecture guard, and CLI smoke: **PASS**. M85 Gates 2-6 are accepted in
`reports/V55_ACCEPTANCE_MATRIX.md`; the v5.5 release remains **IN_PROGRESS /
NOT_ACCEPTED** because M86-M94 are not complete.

Next: G89A — ActorGoalStack v1.
