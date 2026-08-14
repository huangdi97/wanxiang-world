# Worldness Certification (G15J)

## Criterion-by-criterion evidence matrix (synthetic reference world, black-box public API)
| Criterion | Evidence | Status |
|---|---|---|
| Persistence independent of session | restart (fresh runtime) reproduces the semantic hash | PASS |
| Spatiotemporal continuity | places + clock + positions persist across runs | PASS |
| Material/container/custody continuity | exclusive containers; custody chain; custody != knowledge | PASS |
| Life/body continuity | body condition survives 90-day run; no actor starvation | PASS |
| Social/organizational continuity | guild roles/memberships persist; duties scheduled | PASS |
| Cognitive/knowledge continuity | beliefs actor-scoped; no leak; public/private distinction | PASS |
| Causal continuity | worldlines diverge causally; branch outcomes differ | PASS |
| Character/persona continuity | embodiment takeover/release/re-entry coherent | PASS |
| Control-handoff continuity | human exit -> autonomous advance -> rejoin | PASS |
| Canon/source continuity | source-gate + ledger provenance retained | PASS (synthetic; real EXTERNAL_BLOCKED) |
| Replay/verifiability | full replay + sampled checkpoints reproduce hashes | PASS |
| Projection independence | projection read-only; rebuild from events identical | PASS |

## Black-box scenario (build -> install -> instantiate -> operate -> leave -> advance -> rejoin -> fork -> replay -> compare)
PASS (tests/integration/test_g15j_worldness_certification.py).

## Real data blocks
Red Chamber, family, heritage, campaign real slices: EXTERNAL_BLOCKED (isolated; generic capability complete).
