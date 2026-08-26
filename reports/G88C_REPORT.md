# G88C — ExperiencePackage v1

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

| Check | Result |
|---|---|
| Experience configuration | Controls, UI capabilities, entry modes, allowed actions, projection ref, and StateDiff fields are versioned value objects |
| Embodiment boundary | `EmbodimentPolicy` enforces one primary controller and a required lease for embodiment |
| Rights | Private and family-private packages require owner/audience metadata; server-side `can_view`/`can_enter` deny an unrelated principal |
| Compatibility | `experience_from_profile()` composes the package from the G88B shell without creating a second registry or state store |
| Round trip | JSON-shaped `to_dict`/`from_dict` preserves the package contract |
| Tests | `tests/unit/substrate/test_experience_package.py` plus G88B tests — 7 passed |
| Architecture/lint/type | architecture guard, ruff, format, and targeted pyright — PASS |

ExperiencePackage is configuration and policy only. It has no runtime state,
resolver, event append, or Commit Authority capability.

Next: G88D — World Plaza / My Worlds / Continue.
