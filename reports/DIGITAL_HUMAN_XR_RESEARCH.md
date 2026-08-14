# Advanced Digital Human / XR Presence Research (G19G)

## Prototype
- `AvatarIdentity` ? synthetic label + identity/voice rights + approved likeness fixture (no real-person
  likeness without explicit approval).
- `PresenceGateway` ? Port/Adapter route for presence: rights checked first; provider outage falls back
  to the deterministic text baseline; interruption returns to baseline; latency recorded; every
  utterance becomes a normal command payload (`action_type=utterance`) ? never a direct world mutation.
- `DeterministicTextAvatar` ? baseline text provider (no paid API). `LatencyProbe` ? measurable latency.

## Results
| Check | Result |
|---|---|
| Provider outage falls back without world corruption | PASS |
| All actions remain normal commands | PASS |
| Real-person likeness rejected without approved fixture | PASS |
| Latency measured; ordering preserved; interruption resets | PASS |
| Flag OFF -> no core regression | PASS |

## Decision
**KEEP_EXPERIMENTAL** ? the presence seam is sound; real speech/avatar and WebXR/Godot/Babylon
integrations are EXTERNAL_BLOCKED. Promotion requires an interruption/latency SLA and an identity
rights audit against a real provider.

## Evidence
- `uv run pytest tests/integration/test_g19g_digital_human.py -q` -> 7 passed.
- ruff/pyright clean; architecture PASS at the M16 gate.
