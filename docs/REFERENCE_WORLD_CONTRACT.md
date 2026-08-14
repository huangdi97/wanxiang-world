# Reference World Contract (G15A)

## Purpose
A serious reference World Pack is a black-box client of Wanxiang Core. It proves platform generality
without hard-coding world content into Core, and is accepted through public package/runtime contracts only.

## Black-box boundary
- A World Pack is definition: `Domain Pack -> World Pack -> Scenario -> World Instance -> Branch -> Session -> Projection`.
- Core never imports reference content; reference content never imports Core internals.
- Acceptance is measured through the public SDK/API: package registry/install, world instantiation,
  command submission through Commit Authority, projection/query, replay/branch, and rights/source gates.

## Required pack composition (validated by the conformance harness)
| Field | Requirement |
|---|---|
| package_id / kind / version | present, versioned (SemanticVersion), kind in domain/world/scenario |
| dependencies | exact pins; deterministic resolution; no cycles/conflicts |
| content_hash | matches manifest content (tamper-proof) |
| executable_trust | explicit (default untrusted); executable extensions default-deny |
| rights_refs | references to approved RightsEnvelopes for any real/private content |
| evidence_refs | source/evidence links for claims |
| asset_refs | media/asset references with rights provenance |
| sources | gated through SourceGate (E3 canonical-eligible, rights approved) |

## Required worldness scenarios
Persistence-independent-of-session; spatiotemporal continuity; material/container/custody continuity;
life/body continuity; social/organizational continuity; cognitive/knowledge continuity; causal continuity;
character/persona continuity; control-handoff continuity; canon/source continuity; replay/verifiability;
projection independence. (Detailed in 16_REFERENCE_WORLD_QUALIFICATION_STANDARD.md.)

## Version pinning & reproducible build
- Installs record exact pins + lock hash; exporting the same install reproduces the same hash.
- A world pack build is reproducible when the same manifests/versions produce the same lock and install hash.

## Conformance harness
`scripts/reference_world_conformance.py` validates any World Pack against this contract:
- required manifest metadata (id/kind/version/dependencies/content_hash/executable_trust);
- rights/evidence/eval metadata presence (catches missing rights/source/eval metadata);
- install through the public PackageInstaller (no Core modification).
