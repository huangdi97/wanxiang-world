# G68G Report — Reproducible Seed

**PASS** — the seed is derived from draft id, revision, scenario id, and
source versions with canonical JSON and SHA-256. Rebuilding the same draft
produces byte-equivalent plans; changing the scenario id changes the seed.

Evidence: reproducibility and seed-difference assertions in the M65 test.
