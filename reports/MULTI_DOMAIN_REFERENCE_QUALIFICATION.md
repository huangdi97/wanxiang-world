# Multi-domain Reference Qualification (G15I)

## Four domain families (all via public domain-package interfaces)
| Domain | Synthetic conformance | Real slice |
|---|---|---|
| Literature (Red Chamber) | source-gate + ledger labels + provenance | EXTERNAL_BLOCKED (G15H) |
| Family (genealogy) | GEDCOM roundtrip, conflicting claims, privacy consent/revocation, persona modes | EXTERNAL_BLOCKED (real family records) |
| Heritage (museum) | IIIF parse, Linked Art provenance, semantic twin distinctness, conservation history, biography labels | EXTERNAL_BLOCKED (real museum data) |
| Campaign (co-sim) | fog-of-war, region logistics, validity envelope, checkpoint round-trip | EXTERNAL_BLOCKED (real campaign history) |

## Results
| Check | Result |
|---|---|
| Synthetic suites PASS for all four domains | PASS |
| No domain requires Core special-casing (architecture forensics clean) | PASS |
| Real slices precisely EXTERNAL_BLOCKED (never fabricated) | PASS |
| Branch/replay on domains covered by shared Core (G15E/F) | PASS |

## Evidence
- `uv run pytest tests/integration/test_g15i_multidomain.py -q` -> 4 passed.
- Four distinct domain families prove package generality; blocked real content does not invalidate it.
