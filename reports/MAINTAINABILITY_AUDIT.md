# Maintainability Audit (G13G)

- Production files: 239; total lines: 19369; functions: 1030
- Mean max-function complexity: 3.3
- Files over 300 lines: 0
- High-complexity hotspots (>=15): 5
- Long-function hotspots (>=120 lines): 0
- Import cycles: 0
- Public `Any`-typed parameters: 9
- Exception swallows (except: pass): 0

## Files over the 300-line threshold

None (architecture guard enforces the target; exceptions must be documented).

## High-complexity hotspots

- `packages/substrate/src/wanxiang_substrate/genealogy/gedcom.py` max_complexity=25 functions=13
- `packages/substrate/src/wanxiang_substrate/spatial/resolver.py` max_complexity=21 functions=5
- `packages/substrate/src/wanxiang_substrate/heritage/iiif.py` max_complexity=19 functions=6
- `packages/substrate/src/wanxiang_substrate/material/query.py` max_complexity=19 functions=14
- `packages/substrate/src/wanxiang_substrate/institution/query.py` max_complexity=16 functions=15

## Long-function hotspots

None >= 120 lines.

## Typing / exception-swallowing signals

- Any param: `packages/domain/src/wanxiang_domain/serialization.py:42:expect_version`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:70:_decode_components`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:123:delta_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:178:command_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:71:event_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:113:snapshot_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:139:run_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:162:ancestry_from_primitive`
- Any param: `packages/persistence/src/wanxiang_persistence/database.py:20:_enable_sqlite_foreign_keys`
- No `except: pass` swallowing in production.

## Import cycles

None.

Hotspots are candidates for G13H/G13I closure tasks with owner and rationale;
no 'rewrite later' hotspot is left untracked.
