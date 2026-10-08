# Wanxiang v5.5 Stable Certification Report

Date: 2026-08-29  
Candidate: `16f7d89ccf95f405351df6727ddde3184cdd58bc`  
Decision: `NOT_ACCEPTED_FOR_STABLE` / `LOCKED`

## Final gate result

The evidence-derived aggregate completed with ledger consistency `PASS`, but
the Stable predicate is false:

| Gates | Result |
|---|---|
| 61 | `PASS` |
| 62–66 | `USER_INPUT_REQUIRED` |
| 67–77 | `PASS` |
| 78 | `EXTERNAL_BLOCKED` |
| 79 | `LOCKED` |
| 80 | `LOCKED` |

The final machine-readable aggregate is
`artifacts/v55_stable/m100/stable_gate_aggregate.json` with SHA-256
`3881a2923ba6de9962e610f04d20750d31cd7086a52f8f3122ecfd0b0ae3c884`.
The final Stable matrix is
`reports/V55_STABLE_ACCEPTANCE_MATRIX.md` with SHA-256
`f00f37057b33a5630edce647d646815e68c7540d262d0f1dfe5ae6699c13d566`.

## M100 results

- G103A recomputed Gates 61–79 from persisted evidence and passed ledger
  consistency. Gate 79 is derived `LOCKED` because candidate remote/required
  CI identity is not verified.
- G103B completed the 18-command full regression record with no captured
  `FAIL`; PostgreSQL, pnpm/TypeScript, and host-specific browser boundaries
  remain explicit `EXTERNAL_BLOCKED`.
- G103C completed all nine semantic/safety groups with no captured `FAIL`,
  including source/canon immutability, proposal-only providers,
  replay/branch/recovery, rights/privacy/resources, and safety guards.
- G103D verified `git clone --no-local` and detached checkout at an exact
  candidate SHA. All 18 clone commands had no captured `FAIL`; PostgreSQL and
  pnpm/TypeScript remained `EXTERNAL_BLOCKED`. The two earlier bootstrap
  permission failures are preserved as attempt-01/02 records.
- G103E performed read-only Git/GitHub queries. The candidate release branch
  and candidate Actions run were not present; Git `ls-remote` was blocked by
  the host HTTPS helper. No push was attempted.
- G103F prepared release-ready notes with explicit evidence boundaries.
  G103G did not create `v5.5.0`; G103H correctly did not run tag-based
  post-release checks because that tag does not exist.

## Evidence boundaries

Prompt Genesis, bounded long-horizon continuity, World Lab, and emergence
remain `EXPERIMENTAL`/`BOUNDED`. No universal creative, emergence, scientific,
social, true-time/live-world, production-capacity, or 10,000/100,000-NPC claim
is made. Real Godot/physical/visual E2E and live PostgreSQL remain
`EXTERNAL_BLOCKED`; local pnpm/TypeScript and remote candidate CI boundaries
are not relabeled as PASS.

The v5.4.0 tag/release and v5.5.0-rc1 tag/prerelease remain unchanged. The
historical pre-repair real-book `NOT_ACCEPTED` record remains preserved. No
private source, copyright corpus, secret/token, family data, or model cache was
uploaded; no history rewrite, force push, stable tag, GitHub Release, v5.6
branch, or model training was performed.

## Stop decision

Gate 80 remains `LOCKED`. The next permitted action requires genuine human
M95 player evidence and a separately verified remote candidate/required-CI
delivery path. This certification stops here; it does not begin v5.6 or model
training.

Machine-readable final evidence:
`artifacts/v55_stable/m100/stable_certification.json`.
Reproduce the aggregate with:

```text
uv run python scripts/m100_stable_gate_aggregate.py
```
