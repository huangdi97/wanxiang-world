# Product Surface Contract Audit (G18A)

## Results
| Check | Result |
|---|---|
| Branch/session context switch updates surfaces from server truth | PASS |
| No surface writes world state outside the command API (only sanctioned `submit` path) | PASS |
| Shared types do not drift from OpenAPI/SDK baseline | PASS |
| Route ownership map produced (all surfaces consume the same API) | PASS |

## Server-truth contract
- All product faces (Studio, Experience, Strategy, Heritage, Family, Learn, Operator) consume the same
  authoritative server world; no per-surface backend truth store.
- Projections own no exclusive state; surfaces rebuild from server projections.
- Renderers remain EXTERNAL_BLOCKED; server-composed projections + typed view models are the qualified contract.

## Evidence
- `uv run pytest tests/integration/test_g18a_product_surfaces.py -q` -> 3 passed.
- Architecture: docs/PRODUCT_SURFACE_ARCHITECTURE.md.
