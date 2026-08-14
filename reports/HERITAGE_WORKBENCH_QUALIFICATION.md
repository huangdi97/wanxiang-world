# Heritage / Museum Workbench Qualification (G18F)

## Service (`wanxiang_api.heritage_workbench_service`)
| Operation | Behavior |
|---|---|
| object_view | physical/digital/semantic-twin/reconstruction identities visibly distinct; timeline labels evidence vs reconstructed |
| export | restricted export requires curator rights (HeritageRightsDenied otherwise) |
| conservation_history | versioned, auditable history |

## Results
| Check | Result |
|---|---|
| Physical/digital/reconstruction states visibly distinct | PASS |
| Rights prevent restricted projection/export | PASS |
| Conservation history remains auditable (versioned) | PASS |
| Reconstructions labeled, never presented as original fact | PASS |

## Evidence
- `uv run pytest tests/integration/test_g18f_heritage_workbench.py -q` -> 3 passed.
- Projection richness does not erase evidence uncertainty (labels preserved).
