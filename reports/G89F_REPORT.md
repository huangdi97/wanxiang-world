# G89F — Character Passport

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

`CharacterPassport.from_character` creates a portable snapshot from the
existing Playable `CharacterRecord`; `to_character_record` is the only identity
round-trip and passport entries never become CharacterEntry or canonical
entities. Each ref-only memory, skill, and item entry declares `portable`,
`conditional`, or `blocked`, plus its origin world, compatibility tags, and
privacy scope.

`DeterministicPassportTranslationPolicy` requires the owner (or explicit
admin), target profile compatibility, supported kinds, exact target refs, and
matching conditional tags. Missing skills/items/memories and blocked entries
produce explicit rejected decisions. The result is a
`PassportTranslationProposal` with no import or commit operation, so impossible
capabilities cannot silently enter a target world. Non-owner projections omit
owner/origin/private-entry data.

## Gates

| Gate | Result |
|---|---|
| Portable identity profile round-trip | PASS |
| Memory / skill / item portability flags | PASS |
| Origin-world refs and target compatibility | PASS |
| Impossible skill/item rejection | PASS |
| Privacy projection | PASS |
| Ruff / format / Pyright | PASS; 0 errors |
| Architecture conformance | PASS |
| Actor-continuity regression | PASS; 12 passed, 1 expected Hypothesis warning |

No new identity authority, canonical state, or persistence schema was created.
v5.5 remains **IN_PROGRESS / NOT_ACCEPTED**; G89G is next.
