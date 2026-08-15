# Goals G42A-G42G Acceptance Report — Studio & Experience (M39)

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/studio_experience/` (new):
   - G42A `SourceBrowserEntry` + `CandidateReview` — source browser/locator,
     candidate approve/reject, conflict/evidence view.
   - G42B/C `StudioWorkspace` — character graph/timeline, evidence drawer,
     future-canon permission, map topology, schedules, norm/duty (propose-only).
   - G42D `ExperienceEntry` + catalog — world/scenario/role + scenario/canon
     modes + embodiment entry.
   - G42E `LivingWorldView` — map/actors/items/actions/dialogue/perception/time.
   - G42F `EmbodimentReturnSummary` — leave/return + timeline/lineage/canon
     distance + background policy.
   - G42G `run_fresh_user_flow` — fresh-user flow + basic accessibility.
2. `tests/unit/substrate/test_studio_experience.py` (5 tests).

## Reuse
- G36H ExperienceStudio patterns; propose-only; no write path/UI authority.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_studio_experience.py -q` | 5 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |
| architecture_check.py | PASS |

## Local commit
- `g42: Studio & Experience (M39 mechanism)`
