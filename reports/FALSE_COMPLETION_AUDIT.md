# False-Completion Audit (G13D)

- Production placeholder findings: 0
- Dead production modules (never imported): 0
- Hardcoded-state candidates: 10

## Production placeholders

None (architecture guard enforces this; scanner re-checks independently).

## Dead production modules

None.

## Hardcoded-state candidates

- `packages/domain/src/wanxiang_domain/serialization.py:163` large-dict-literal (11 keys)
- `packages/domain/src/wanxiang_domain/serialization_history.py:50` large-dict-literal (15 keys)
- `packages/domain/src/wanxiang_domain/serialization_history.py:100` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/epistemic/components.py:30` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/epistemic/components.py:58` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/genealogy/gedcom.py:164` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/packages/install.py:160` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/packages/model.py:151` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/sources/model.py:123` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/temporal/components.py:42` large-dict-literal (8 keys)

## Classification

- Test Fakes implement formal Port contracts and are namespaced under tests/;
  they are never selected by production default configuration.
- Any finding above not on the documented allowlist is a P0/P1 gap candidate.
