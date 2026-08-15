# Goal G38C Acceptance Report — Kernel Change Guard

## Status
PASS — import/path/AST guard for Kernel v1 freeze.

## Delivered
1. `scripts/kernel_guard.py` (new):
   - `scan_domain_names()` — forbids domain proper nouns (Red Chamber etc.) in
     Kernel packages (domain/runtime).
   - `scan_direct_mutation()` — flags canonical-state mutation calls in
     substrate production code outside the authority (with a vetted pure
     dry-run allowlist: resolution/service.py, capability/resolver.py).
   - `scan_abi_drift()` — kernel v1 ABI golden must match the committed golden.
   - Exit 0 when clean.
2. `tests/architecture/test_kernel_guard.py` (3 tests): guard passes on the
   current tree; catches a planted domain name in Kernel; catches a planted
   direct mutation path.

## Verification
| Command | Result |
|---|---|
| `uv run python scripts/kernel_guard.py` | kernel guard: 0 violation(s), exit 0 |
| `uv run pytest tests/architecture/test_kernel_guard.py -q` | 3 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g38c: Kernel Change Guard`
