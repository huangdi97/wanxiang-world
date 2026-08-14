# Black-box Final Acceptance (G20D)

Executed as three external personas using only public docs/SDK/API and release artifacts;
no internal imports or DB edits.

| Persona | Result | Evidence |
|---|---|---|
| author | PASS | published+installed=True; custom_action=True; no_core_mod=True |
| operator | PASS | deployed=wld_sf; replay_ok=True; restored_hash_match=True |
| end_user | PASS | session_independent=True; branch_isolated=True; replay_ok=True |
| surfaces | PASS | routes=10; write_api_violations=[]; projection_items=21 |

## Verdict

**PASS** - black-box platform claim proven for author, operator, end user and product surfaces.

## Evidence commands

```
uv run python scripts/blackbox_final_acceptance.py   # writes this report
uv run pytest tests/integration/test_g17g_blackbox_sample.py tests/integration/test_g18a_product_surfaces.py -q
uv run python scripts/quality.py              # full M17 gate
```
