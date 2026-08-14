# M10 Independent Requalification (G13I)

## Method
Independently re-run the release-critical evidence from a clean shell, without trusting prior PASS claims, at the M10 checkpoint.

## Requalification evidence
| Check | Command | Result |
|---|---|---|
| Clean bootstrap (migrations from scratch) | `alembic upgrade head` on a fresh SQLite DB | PASS (head 0002; tables created) |
| M1 acceptance | `pytest tests/integration/test_m1_acceptance.py` | PASS |
| M2 living-world qualification | `pytest tests/integration/test_m2_qualification.py` | PASS |
| M3 agency qualification | `pytest tests/integration/test_m3_qualification.py` | PASS |
| M4 world-authoring qualification | `pytest tests/integration/test_m4_qualification.py` | PASS |
| M5 host/embodiment + G06 proofs | `pytest test_m5_qualification.py test_m5_g06_proofs.py` | PASS |
| M6 reality/experiments qualification | `pytest test_m6_qualification.py` | PASS |
| M7 domain-generality qualification | `pytest test_m7_qualification.py` | PASS |
| M8 co-simulation qualification | `pytest test_m8_qualification.py` | PASS |
| M9 stability (30-day/1000+ tick) | `pytest test_g12a_stability.py` | PASS |
| Replay golden corpus | `python scripts/history_forensics.py` | PASS (golden + synthetic hashes stable) |
| Source-gate/security probes | `python scripts/security_forensics.py` | PASS (0 secrets; all probes as expected) |
| Architecture/dependency forensics | `python scripts/architecture_forensics.py` | PASS (0 forbidden/leakage/writes/cycles) |
| False-completion + schema drift | `python scripts/false_completion_scan.py` | PASS (0 placeholders/dead; drift aligned 10/10) |
| M1-M9 milestone set | 21 tests | PASS |
| Full quality gate | `python scripts/quality.py` | PASS (428 pytest, ruff, pyright, architecture) |

## Verdict
M10 = **PASS** (P0=0, required P1=0, traceability complete, M1-M9 critical regressions independently reproduced).
Baseline SHA frozen at the M10 checkpoint commit (recorded in M10_ACCEPTANCE.md).
