# G88E — My Characters / Character Entry

Status: **PASS**  
Date: 2026-08-26  
Branch: `feature/v5.5-playable-persistent-evolving`

## Evidence

| Check | Result |
|---|---|
| Character list/create | `CharacterEntryService` creates owner-bound records and returns only the owner's characters |
| Presence vs embodiment | Observer/character presence creates a session without a lease; embodiment uses existing `LeaseService` |
| Double controller | A second embodiment of the same actor raises the existing `LeaseConflict` |
| Leave/resume | Leave releases the existing lease; a subsequent entry acquires a new lease |
| Compatibility | Owner and profile compatibility are checked server-side; unrelated/mismatched records return `NotFound` |
| Observer safety | An observer session cannot acquire embodiment through the existing lease service |
| Tests | `tests/unit/substrate/test_character_entry.py` plus prior M85 tests — 12 passed |
| Architecture/lint/type | architecture guard, ruff, format, and targeted pyright — PASS |

The entry service only creates session/lease metadata through the already
existing session substrate. It does not commit world actions or mutate the
canonical state.

Next: G88F — Free Action Intent Compiler.
