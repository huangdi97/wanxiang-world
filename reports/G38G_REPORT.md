# Goal G38G Acceptance Report — API/DB/Package 性能基线冻结

## Status
PASS — baselines frozen.

## Delivered
1. OpenAPI snapshot: routes=17 (regenerated baseline; contract 3/3 PASS).
2. Migration head: `0004_add_world_metadata` (revises 0003; downgrade-safe).
3. Package goldens: kernel v1 ABI golden (reports/kernel_v1_abi_golden.json),
   SDK baseline (reports/sdk_api_baseline.json, py=1101, ts=5), v5.2 worldpack
   assembly goldens.
4. Performance benchmark (`uv run python scripts/benchmarks.py`):
   - commits: 200 events, ~4.97s, ~40.2 events/s (SQLite-bound)
   - replay: 1200 events ~24ms
   - lineage: 400 nodes query ~13ms

## Local commit
- `g38g: API/DB/Package 性能基线冻结`
