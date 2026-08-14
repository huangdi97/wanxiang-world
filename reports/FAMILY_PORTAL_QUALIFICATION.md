# Family Portal Qualification (G18E)

## Service (`wanxiang_api.family_portal_service`)
| Operation | Behavior |
|---|---|
| person_view | claims + conflicts visible; living-person private views denied to unauthorized |
| export | GEDCOM export preserving source references; private data not exported |

## Results
| Check | Result |
|---|---|
| Conflicting claims remain visible as conflicts (never silently merged) | PASS |
| Unauthorized users cannot see protected living-person fields/media | PASS |
| Export preserves supported source references | PASS |

## Evidence
- `uv run pytest tests/integration/test_g18e_family_portal.py -q` -> 3 passed.
- Privacy and provenance are product behavior (server-enforced, not footnotes).
