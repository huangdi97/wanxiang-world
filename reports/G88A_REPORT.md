# G88A — v5.4 Stable Baseline & v5.5 Branch

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Scope

G88A establishes the v5.5 baseline. It does not re-run or modify the v5.4
source-to-world implementation and does not train a model.

## Evidence

| Check | Result |
|---|---|
| v5.4 stable tag | `v5.4.0` remains annotated at `ef935fc6c24eb47553382d318e1501a795c4da84` |
| v5.4 release evidence | `reports/M84_FIRST_BOOK_REQUALIFICATION.md`, `artifacts/m79_m84/m84_post_release_verification.json` |
| Execution package | 82 goals, 10 milestones, all-in-one 6,870 lines |
| All-in-one SHA-256 | `C5DE84048E8C271B813F71F168EFB7050B27847863F2E10630D5C1B7C4F75DD5` |
| Architecture guard | `uv run python scripts/architecture_check.py` — PASS |
| Full local quality | `uv run python scripts/quality.py` — PASS |
| Python tests | `1219 passed, 1 skipped`; local PostgreSQL skip is `EXTERNAL_BLOCKED` |
| Type/format/lint | ruff, ruff format, pyright — PASS |
| Branch | Created from `c90370d4ff1ce84a9b5d83fe8b76781a0347af87` |
| v5.4 boundary | Kernel/Commit/Ledger/Replay/Branch/Lineage remain frozen; v5.6 and training excluded |

## Keep / Extend / Merge / Delete / Add

| Area | Decision |
|---|---|
| Reality Root, Commit Authority, Event Store, Replay, Branch, Lineage | KEEP/FROZEN |
| Source Registry, Candidate/Evidence/Rights, WorldPackage, Preview, Living | KEEP; consume through existing ports |
| Actor, Epistemic, Session, Host, Scheduler, Evolution, Director, Experiment, Projection | EXTEND/COMPOSE; no second authority or history |
| Existing Studio/API/CLI transports | EXTEND through shared application services |
| Duplicate WorldManager/WorldRuntime/EventStore/PackageRegistry | DELETE/PROHIBIT as new abstractions |
| v5.5 Playable/Long-Horizon/Evolution/Lab/Provider contracts | ADD behind existing boundaries |

## Acceptance

The stable baseline and feature branch are ready. G88B is the next active goal.
