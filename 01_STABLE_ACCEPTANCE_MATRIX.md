# Wanxiang v5.5 Stable Acceptance Matrix — Proposed Gates 61–80

This is the **new** Stable gate generation. It inherits RC evidence but does not mutate Gates 1–60.

| Gate | Requirement | Required for Stable? | Initial status |
|---|---|---:|---|
| 61 | Stable baseline / lineage / scope freeze | YES | PENDING |
| 62 | Real player full product-chain session | YES | PENDING |
| 63 | Player comprehension / no critical usability blocker | YES | PENDING |
| 64 | Meaningful agency and valid rejection behavior | YES | PENDING |
| 65 | Consequence visibility from committed StateDiff | YES | PENDING |
| 66 | Leave → Continue continuity on same worldline/actor | YES | PENDING |
| 67 | New original Prompt Genesis provenance/E5 boundary | YES | PENDING |
| 68 | Prompt → WorldDraft → Review → WorldPackage → Publish → Play | YES | PENDING |
| 69 | Original Prompt World 7d bounded run | YES | PENDING |
| 70 | Versioned Experience Quality benchmark schema | YES | PENDING |
| 71 | Quality baseline on source-driven + prompt-created worlds | YES | PENDING |
| 72 | Worldness / Experience Quality / Scientific Validity separation | YES | PENDING |
| 73 | 30d multi-seed/policy/pressure regression | YES | PENDING |
| 74 | 90d multi-run regression + replay/checkpoint/recovery | YES | PENDING |
| 75 | Bounded emergence repeatability / false-positive evidence | YES | PENDING |
| 76 | Scale ladder 10→50→100→500→1000 actors | YES | PENDING |
| 77 | CPU/RAM/DB/Event/Provider/Latency/Cost/Storage degradation curve | YES | PENDING |
| 78 | Real Godot projection/physics E2E | NO (Optional) | OPTIONAL_PENDING |
| 79 | Stable preflight: full regression, immutability, rights/security, clean clone, remote CI, evidence lineage | YES | PENDING |
| 80 | `v5.5.0` Stable release gate | YES | LOCKED |

## Gate 80 predicate

Gate 80 may become `ACCEPTED_FOR_STABLE` only if:
- every required Gate 61–77 and 79 is `ACCEPTED`;
- Gate 78 is either `ACCEPTED`, `EXTERNAL_BLOCKED`, or `NOT_IN_STABLE_SCOPE` with explicit evidence;
- no P0/P1 unresolved regression exists;
- stable release evidence still preserves all RC/v5.4 historical evidence;
- annotated tag `v5.5.0` and non-prerelease GitHub Release are created only after the predicate is true.

## Human acceptance threshold for M95

Minimum release-qualifying human evidence:
- at least one genuine human session; automated/LLM/Playwright sessions do not count as the human session;
- completes World Plaza → Select World/Scenario → Character → Enter → Observe/Free Action → Response → StateDiff → Leave → Continue;
- at least 3 free-form actions, including at least 1 action that commits a visible state consequence and at least 1 valid rejection or constrained outcome if naturally reachable;
- no P0/P1 blocker, privacy leak, authority bypass, or state/narrative contradiction caused by projection bypass;
- human ratings for comprehension, agency, consequence visibility and continuation continuity are each >= 3/5, with overall >= 3.5/5.

These thresholds are an engineering Stable criterion for this release, not a scientific/user-population validity claim.
