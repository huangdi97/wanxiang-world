# Wanxiang Engineering Program — README FIRST

This package is the engineering-control layer for starting formal implementation of Wanxiang v5.0-R1.

## What to run tonight

Copy the whole package into the repository root (merge deliberately with existing docs rather than blindly overwriting project history), ensure the master specification is available as `docs/spec/WANXIANG_v5_MASTER_SPEC.md`, then give Codex Desktop the contents/instruction in:

`01_CODEX_TONIGHT_MASTER_PROMPT.md`

The tonight batch intentionally stops after **M1 Authoritative World Exists**. It is a large batch, but it does not proceed into living substrate/UI/domain reference worlds before the canonical/event/replay/branch foundation has proven itself.

## Documents

- `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md` — complete program decomposition and dependency architecture.
- `01_CODEX_TONIGHT_MASTER_PROMPT.md` — controller prompt for continuous P0+P1 execution.
- `02_ENGINEERING_STANDARDS.md` — readability, modularity, upgradeability and code rules.
- `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md` — testing/gates/evidence standard.
- `goals/*.md` — executable Goal contracts for the first batch.

## Goal order

1. 00A Repository Foundation
2. 00B Architecture Guards
3. 01A Core Contracts
4. 01B Commit Authority
5. 01C Event Store
6. 01D Replay/Branch
7. 01E Persistence/Migration
8. 01F Minimal Vertical Slice + M1 Qualification

Do not skip directly to 01F and do not start G02A until M1 PASS.
