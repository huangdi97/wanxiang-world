# Goal G37A Acceptance Report — 红楼梦七日场景自动化执行

## Status
PASS (mechanism) — deterministic no-LLM reference run; optional LLM run
separate and EXTERNAL_BLOCKED; real canon EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/seven_day.py` (new):
   - `SevenDayReferenceRun` — fixed snapshot -> Day1 embody Daiyu + commission
     Zijuan relay -> Day3 release + fork -> run to Day7; deterministic hash.
   - `optional_llm_run()` — separated; EXTERNAL_BLOCKED without LLM key.
2. `tests/unit/substrate/test_rc001_seven_day.py` (4 tests): determinism;
   Day1 embody/relay; Day3 release+fork; LLM run separated.

## Reuse
- G36A instantiation + G36F embodiment; fork via runtime branch model.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_seven_day.py -q` | 4 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g37a: 红楼梦七日场景自动化执行`
