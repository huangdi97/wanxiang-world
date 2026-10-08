# G60G Report — Preview World Smoke

## Status

**PASS** — The preview smoke creates entities and a relation, exposes a legal
  action, records committed events, and produces a different replay hash after
  a committed action.

## Evidence

`test_m57_compiles_pins_and_instantiates_through_host` passed with:

- 2 entities;
- 1 relation;
- 3 genesis events;
- post-genesis status action through Host/Runtime/Commit Authority;
- replay hash changed after the action.

