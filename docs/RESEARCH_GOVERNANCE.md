# Research Governance (G19A)

## Isolation
- Experimental code lives in `wanxiang_research` (v5.1/v6 namespace), OFF by default.
- Feature flags default disabled; stable behavior is preserved with flags OFF.
- Experiments NEVER gain Commit Authority or mutate canonical worlds directly.

## Promote / reject criteria (required per track)
Each research flag declares explicit criteria (e.g., benchmark parity + clean-room build, drift threshold,
shard consistency + replay parity). A track ends with one of:
- **PROMOTE**: evidence meets criteria AND the change is generalized + passes full stable regression + ADR.
- **KEEP_EXPERIMENTAL**: promising but not yet meeting criteria; stays behind its flag.
- **REJECT**: evidence shows a bad tradeoff; the experiment is removed from stable defaults.

## Reproducibility
Every experiment records a manifest: track, seed, decision, evidence, runtime/schema versions; the
manifest hash makes results reproducible.

## Benchmark baseline
M12/M13 baselines (worldness 12/12, 90-day run, 44 commits/s SQLite profile) are the comparison floor;
any research claim must beat or match the baseline at the declared profile.

## ADR
Promotion requires an ADR recording the evidence, criteria, regression results and owner.
