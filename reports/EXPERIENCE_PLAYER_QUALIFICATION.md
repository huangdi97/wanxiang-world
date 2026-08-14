# Experience Player Qualification (G18C)

## Service (`wanxiang_api.experience_player_service.ExperiencePlayerService`)
| Operation | Behavior |
|---|---|
| start_session | selects the world root branch |
| project | server-composed text projection (labels + redaction) |
| act | revision-aware submission through the server command pipeline; stale -> PlayerResyncRequired |
| resync | re-project from server truth and retry |

## Results
| Check | Result |
|---|---|
| User returns to the authoritative advanced world (background advance while disconnected) | PASS |
| Client resync works after a dropped connection (stale revision -> resync -> retry) | PASS |
| All actions route through the server command pipeline (Commit Authority) | PASS |
| Basic accessibility: text projections carry labels + redaction flags | PASS |

## Evidence
- `uv run pytest tests/integration/test_g18c_experience_player.py -q` -> 4 passed.
- No client-side game-state simulation; no fake data in the production path.
