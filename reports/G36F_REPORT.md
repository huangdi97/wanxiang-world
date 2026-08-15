# Goal G36F Acceptance Report — 林黛玉 Embodiment ShadowPolicy Handoff

## Status
PASS (mechanism) — embodiment of an actor key with control modes; no
fabricated canon; real《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/session/embodiment.py` (new):
   - `ControlMode` (intent/co_drive/full_control).
   - `EmbodimentState` + `ControlHandoffEvent` (append-only audit).
   - `EmbodimentController` — acquire lease under a mode, set_mode, release;
     composes LeaseService + ShadowPolicy.
   - `major_decision()` — ShadowPolicy NEVER makes major decisions (raises
     ShadowCannotCommit); advice-only channel preserved.
2. `tests/unit/substrate/test_rc001_embodiment.py` (5 tests): acquire under
   full_control + event; mode change intent->co_drive; release hands back;
   shadow never commits/makes major decisions; observer session cannot embody.

## Reuse
- G05C ShadowPolicy/ControlHandoff; G05B LeaseService; only modes + events new.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_embodiment.py -q` | 5 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36f: 林黛玉 Embodiment ShadowPolicy Handoff`
