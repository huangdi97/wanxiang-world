# Goal G36A Acceptance Report — 实例化 RC-001 与固定世界快照

## Status
PASS (mechanism) — real《红楼梦》text remains EXTERNAL_BLOCKED (G35A);
instantiation uses synthetic anonymized content only.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/instantiate.py`:
   - `RC001Profile` + `resolve_rc001_profile()` — domains/runtime profile
     (narrative_domain + deterministic runtime).
   - `genesis_delta()` — initial synthetic entities (places/actors/objects).
   - `InitialSnapshot` — immutable snapshot (revision, entity_count, hash,
     primitive).
   - `instantiate_rc001()` — Genesis through the single Commit Authority
     (1 commit, no bypass), builds InstanceIdentity, snapshot.
   - `record_lineage_root()` — lineage root node for the instance.
2. `tests/unit/substrate/test_rc001_instantiate.py` (4 tests): single-commit
   instantiation; fixed reproducible snapshot hash; lineage root recorded;
   deterministic profile.

## Reuse
- G35I WorldPackAssembler/GenesisSpec; G31A InstanceIdentity; CommitAuthority;
  state_to_primitive/semantic_sha256; LineageGraph.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_instantiate.py -q` | 4 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36a: 实例化 RC-001 与固定世界快照`
