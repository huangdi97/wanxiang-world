# M41 Qualification — Cross-Domain Generality

## Status
**M41 Milestone Gate PASS (mechanism)**

Real external data (family/heritage/campaign) remains EXTERNAL_BLOCKED; the
cross-domain generality MECHANISM is certified, honestly labeled.

## Goal status (M41)
| Goal | Status |
|---|---|
| G44A Generality Harness + Kernel Lock | PASS |
| G44B Family World Qualification | PASS (mechanism; external data EXTERNAL_BLOCKED) |
| G44C Heritage World Qualification | PASS (mechanism; external data EXTERNAL_BLOCKED) |
| G44D Campaign World Qualification | PASS (mechanism; external data EXTERNAL_BLOCKED) |
| G44E 四领域同 Core 对照 | PASS |
| G44F 第三方黑盒 World Pack | PASS |
| G44G M41 Generality Qualification | PASS (this report) |

## Quality gate (2026-08-15)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | 978 passed + 1 skipped (live PostgreSQL EXTERNAL_BLOCKED); architecture PASS |
| SDK baseline | routes=17 ts=5 py=1169; contract PASS |
| ruff / format / pyright | PASS (0 errors) |

## Key invariants verified (M41)
- Shared acceptance harness across four domains; kernel diff guard.
- Core commit/replay/branch/snapshot/scheduler reused; no per-domain Core.
- Black-box world pack trust + hash gate.

## Honest boundary
- Real external data acquisition remains EXTERNAL_BLOCKED (BLOCKERS.md).

## Local checkpoint
- G44 mechanism committed; M41 gate certified; tag `m41-generality`.
