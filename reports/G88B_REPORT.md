# G88B — PlayableWorldProfile v1

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

| Check | Result |
|---|---|
| Versioned shell | `PlayableWorldProfile`, `ScenarioProfile`, `RuntimeProfile`, and `ProjectionProfile` are immutable value objects with schema `1` |
| v5.4 compatibility | `profile_from_world_package()` consumes the existing package id/manifest only; no canonical state is copied |
| Backward compatibility | v0 aliases (`package_id`, `scenario_id`, `runtime_id`) read and normalize to schema 1 |
| Validation | Empty refs, duplicate tags, invalid LOD/visibility and invalid provider refs reject with `ContractError` |
| Visibility | `public` is discoverable; `private`, `unlisted`, and `family-private` require the owning principal |
| Storage boundary | `PlayableStore` stores descriptors only and refuses a conflicting immutable replacement |
| Tests | `tests/unit/substrate/test_playable_profile.py` — 4 passed |
| Architecture/lint/format | architecture guard, ruff check and ruff format check — PASS |

The shell contains references and experience metadata only. Commit Authority,
Event Store, Branch, Lineage, and WorldPackage ownership remain in their v5.4
ports.

Next: G88C — ExperiencePackage v1.
