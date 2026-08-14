# Synthetic Reference World Build (G15B)

## Pack
`reference_worlds/synthetic_full/` — a nontrivial synthetic world authored OUTSIDE Core and built/installed/
instantiated only through public Wanxiang contracts.

## Content (all synthetic, never factual)
- 5 places (2 restricted), 4 people (bodies + positions + resolution strategies).
- 1 organization (guild), 3 roles, 3 memberships, 1 recurring duty.
- 3 objects: coin pouch (custody), sealed letter (info payload), market stall.
- Public + private beliefs (perspective isolation exercised).
- Scenario seeds (autonomous living, human takeover, branching, failure) and worldness eval cases.

## Build/install/instantiate (public path)
| Step | API | Result |
|---|---|---|
| Build manifests | `PackageManifest(...).with_hash()` | PASS |
| Install | `PackageInstaller().install(registry, "sf-scenario")` | PASS (lock hash) |
| Instantiate | `WorldRuntime` + `sf.instantiate` | PASS (all 15 entities present) |
| Upgrade to v2 | register v2 + install | PASS (v1 record + other worlds intact) |

## Worldness evidence
- Persistence independent of session (restart reproduces hash).
- Spatial/material/custody continuity (places + pouch custody).
- Social/organizational continuity (guild + roles + memberships).
- Cognitive continuity + projection isolation (beliefs actor-scoped; no leak).
- Replay/verifiability (clean replay hash == committed hash).

## Tests
`uv run pytest tests/integration/test_g15b_synthetic_world.py -q` -> 4 passed.
Content imports only public SDK (wanxiang_domain / wanxiang_substrate / wanxiang_application); no Core internals.
