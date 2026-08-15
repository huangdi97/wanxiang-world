# Cross-Domain Generality Matrix

## Status
PASS (mechanism) — four domains qualified against the shared Core harness.

| Domain | Core reused | Acceptance | External data |
|---|---|---|---|
| Family | commit/replay/branch/snapshot, GEDCOM fixture | PASS (mechanism) | EXTERNAL_BLOCKED |
| Heritage | commit/snapshot, IIIF/Linked Art mappings | PASS (mechanism) | EXTERNAL_BLOCKED |
| Campaign | scheduler/commit, SimulationAdapter, ValidityEnvelope | PASS (mechanism) | EXTERNAL_BLOCKED |
| Narrative / RedChamber | commit/resolver/narrative_domain, canon graph | PASS (mechanism) | EXTERNAL_BLOCKED (G35A) |

## Kernel purity
- Kernel diff guard: `kernel_diff_guard` PASS; kernel_guard.py 0 violations.
- Black-box world pack gate: `black_box_world_pack_gate` (trust + sha256).
- No RedChamber proper nouns in Kernel (scan empty); no second
  Commit/Event/Branch/Worldline/Registry/Engine.
