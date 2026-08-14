# Learn / Challenge Qualification (G18G)

## Service (`wanxiang_api.learn_service`)
| Operation | Behavior |
|---|---|
| discover | Opportunity/Challenge runtime detection from world state |
| practice | evidence-backed practice delta applied to capability |
| assess | evidence-backed assessment delta applied to capability |
| biography | longitudinal learning worldline (capability levels) |

## Results
| Check | Result |
|---|---|
| Learning artifact/assessment evidence is traceable (evidence_refs provenance) | PASS |
| Capability changes are separated from persona changes (no persona mutation) | PASS |
| Challenge affects the world through the normal action/commit path | PASS |

## Evidence
- `uv run pytest tests/integration/test_g18g_learn_challenge.py -q` -> 3 passed.
- Reward points are never equated with capability evidence; capability deltas are evidence-backed and clamped.
