# Material, Information & Social Continuity Qualification (G15E)

## Scenarios
| Criterion | Behavior | Result |
|---|---|---|
| Object never in two exclusive containers | move into box A then box B -> in B only; A no longer contains it | PASS |
| Custody != knowledge | sealed payload unread; non-custodian read rejected (NotCustodian) | PASS |
| Knowledge requires a causal path | receive custody, then read; readers recorded; double-read rejected | PASS |
| Branch divergence | fork; child delivers the letter; parent custody unchanged; distinct hashes; both replay stably | PASS |

## Worldness criteria
Material/custody continuity, information propagation via explicit world mechanisms (transfer + read),
social consequence (custody chain), cognitive boundary (unread actors cannot act on hidden content),
replay/verifiability.

## Evidence
- `uv run pytest tests/integration/test_g15e_material_info.py -q` -> 3 passed.
