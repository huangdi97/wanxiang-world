# G98A — v5.5 Stable Baseline & Acceptance Ledger Freeze
Milestone: M95

## Objective
Freeze the exact post-RC baseline before any Stable work and create the new Gates 61–80 ledger without mutating RC evidence.

## Required work
1. Read canonical master + Final Release Report + M79–M84 history + current repository state.
2. Fetch remote/tags and verify current branch ancestry, RC tag identity, v5.4 stable identity, working tree cleanliness and no v5.6/model-training commits.
3. Re-run a small critical baseline: kernel/architecture, replay/branch, Playable smoke and release-manifest check. Do not rerun/rebuild M85–M94 as a project.
4. Create `reports/V55_STABLE_ACCEPTANCE_MATRIX.md` with Gates 61–80 and evidence references.
5. Create `artifacts/v55_stable/baseline.json` with SHAs, tags, migration head, test commands/results and inherited evidence refs.
6. Preserve old matrix/reports byte-for-byte unless an existing policy requires a forward-link; never rewrite historical status.

## Acceptance
- Gate 61 ACCEPTED only if repository baseline is lineage-consistent with Final Closure.
- Any mismatch produces `reports/M95_BASELINE_MISMATCH.md` and blocks release mutation.

## Commit
`g98a: freeze v5.5 stable baseline and acceptance ledger`
