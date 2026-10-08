# Surface Integration Map (G13D)

API route -> handler -> authoritative application use-case -> canonical state.

| Method | Path | Handler | Runtime use case |
|---|---|---|---|
| ? | ? | reset_action_rate_limiter | static response |
| ? | ? | _runtime | static response |
| GET | /healthz | healthz | static response |
| POST | /worlds | create_world | create_world |
| GET | /worlds/{instance_id} | get_world | static response |
| GET | /worlds/{instance_id}/state | get_state | current_state |
| GET | /worlds/{instance_id}/events | get_events | events |
| POST | /worlds/{instance_id}/actions | submit_action | submit_command |
| POST | /worlds/{instance_id}/checkpoint | checkpoint | create_checkpoint |
| POST | /worlds/{instance_id}/replay | replay | restore_and_replay |
| POST | /worlds/{instance_id}/branches | create_branch | create_branch |
| POST | /worlds/{instance_id}/branches/compare | compare | diff |
| ? | ? | _resolve_branch | static response |

Every stateful route resolves through `request.app.state.runtime` (WorldRuntime);
no route returns canned world state.
