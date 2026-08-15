# Goal G36D Acceptance Report — 信件诗稿礼物药物的物质与信息连续性

## Status
PASS (mechanism) — synthetic objects only; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/material/reading.py` (new):
   - `ACTION_READ_AND_REMEMBER` resolver: reading a sealed payload performs the
     existing material read transition AND forms an observation memory for the
     reader (epistemic memory entity). Reuses `resolve_read` (no duplicate).
2. `tests/unit/substrate/test_rc001_material_continuity.py` (3 tests):
   - instantiate/deliver/seal/read: reading forms an observation memory;
   - hide in container preserves containment chain;
   - gift ownership+custody transfer and medicine consume continuity.

## Reuse
- G04E material resolvers (create/transfer/move/consume/seal/read/give_ownership);
  G35F letter domain; epistemic memory components. Reading is the only new
  behavior (read -> observation memory).

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_material_continuity.py tests/unit/substrate/test_rc001_npc.py -q` | 8 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36d: 信件诗稿礼物药物的物质与信息连续性`
