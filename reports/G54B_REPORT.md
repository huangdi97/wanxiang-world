# G54B Report — Kernel Freeze Goldens (M51)

## Status
**PASS** — Kernel freeze goldens frozen for the M51-M70 program and guards
verified active on the CURRENT tree.

## Delivered
1. `scripts/generate_kernel_freeze_golden.py` — deterministic generator that
   freezes semantic goldens for the frozen Kernel surface:
   - Commit event hashes (5-event reference fixture, `tests/helpers/replay_fixture`);
   - Replay final state hash;
   - Branch fork isolation (child branch-local seq + parent unchanged hash);
   - Worldline (WorldDefinition) content hash;
   - Package manifest content hash (official `PackageManifest` schema);
   - Kernel v1 ABI golden hash cross-check.
2. `reports/kernel_freeze_golden.json` — committed golden (regeneration is
   byte-stable).
3. `tests/architecture/test_kernel_freeze_goldens.py` — 5 architecture tests
   (stability, reproducibility, branch isolation, ABI golden match, guard
   pass).

## Reuse
- Existing `kernel_v1_abi_golden.json` + `scripts/kernel_guard.py` (G38B/G38C)
  and `tests/fixtures/v5_2_baseline/` (G29A) are KEEP; this Goal adds the
  program-level freeze golden without replacing them.

## Verification
| Command | Result |
|---|---|
| `python scripts/generate_kernel_freeze_golden.py` (twice) | byte-stable |
| `pytest tests/architecture/test_kernel_freeze_goldens.py -q` | 5 passed |
| `scripts/kernel_guard.py` | 0 violations |
| ABI golden `1ec5768b...` | matches committed `reports/kernel_v1_abi_golden.json` |

## Kernel freeze invariants (M51-M70)
- Reality Root / Commit / Ledger / Snapshot / Replay / Branch / Worldline /
  Lineage semantics are frozen; any Kernel change requires the G54B-style
  freeze golden update + Kernel Change Proposal + regression gate.
- No domain content / LLM / provider coupling in the goldens.

## Local commit
- `goal g54b: Kernel freeze goldens (M51)`
