# Synthetic Full Reference World (G15B)

Explicitly synthetic content — all people, places and organizations are invented
and presented as synthetic, never as factual. This pack is the mandatory
regression world for future releases: it exercises space, time, material
custody, bodies, institutions, cognition, action, host, evidence, challenges
and projections together through the public path only.

## Contents
- 5 places (town square, market, temple, guild hall, mayor house; two restricted).
- 4 people with bodies, positions, resolution strategies; guild memberships/roles.
- 1 organization (guild), 3 roles, 1 recurring duty (guild rounds).
- 3 objects: coin pouch (custody), sealed letter (info payload), market stall.
- Public belief + private belief (perspective isolation).
- Scenario seeds: autonomous living, human takeover, branching, failure.
- Worldness eval cases (12 continuities).

## Build/install/instantiate
- `synthetic_full.build_registry()` -> public package registry.
- `synthetic_full.install_pack()` -> public PackageInstaller (lock hash, no Core changes).
- `synthetic_full.make_runtime(path)` + `sf.instantiate` -> authoritative instantiation.
