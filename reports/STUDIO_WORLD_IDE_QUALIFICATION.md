# Studio / World IDE Qualification (G18B)

## Service (`wanxiang_api.studio_service.StudioService`)
| Operation | Behavior |
|---|---|
| diagnose_command | command outcome from the event/audit stream (no raw DB access) |
| branch_replay | restore_and_replay through the runtime |
| branch_diff | semantic diff between branches |
| debug_projection | admin-gated debug projection, audited |
| submit | through the command API (Commit Authority); Studio never bypasses it |

## Results
| Check | Result |
|---|---|
| Studio diagnoses a failed command and replay/branch state without direct DB access | PASS |
| Dangerous admin actions require explicit privilege and are audited | PASS |
| No canned world data in the production path (server-truth projections) | PASS |
| Architecture: Studio lives in the transport layer (no application->substrate cycle) | PASS |

## Evidence
- `uv run pytest tests/integration/test_g18b_studio_ide.py -q` -> 3 passed.
