# Final Independent Security, Reliability & Chaos Re-run (G20C)

Re-run of the highest-risk M11/M13 suites against final M17 code, with all experimental
research flags enabled to prove they cannot affect the stable default.

## Curated security/chaos suite

- Files: 14 (G13F, G14A-I, G16A, G16F, G16G, G16I).
- Result: **65 passed, 0 failed, 0 skipped** (pytest exit 0).

## Experimental flags ON (stable-path check)

- Enabled flags: 7 tracks (all ON).
- Golden replay with ALL research flags enabled reproduces the committed
  expected semantic hash exactly; research code never touches canonical state
- Expected `7d17aba7b9b7` vs actual `7d17aba7b9b7` - identical.

## Verdict

**PASS** - no high/critical unresolved security/reliability issue; experimental failures cannot affect the stable default.

## Evidence commands

```
uv run python scripts/security_reliability_certify.py   # writes this report
uv run pytest tests/integration/test_g14a_concurrency.py -q  # curated
uv run python scripts/quality.py               # full M17 gate
```

## Notes

- Live PostgreSQL remains EXTERNAL_BLOCKED (test_g16b skip); the SQLite profile is
  the certified deterministic path.
- M11 baseline: G14A-I = 45 passed; final totals add G13F/G16A/G16F/G16G/G16I.
