# G102A–G102D — M99 Optional Real Godot Projection Integration

M99 is OPTIONAL for v5.5 Stable unless Stable scope is explicitly changed before Gate freeze.

## G102A — Environment probe
Detect an actual supported Godot executable/runtime and record version/platform. Do not download/install a large external engine silently. If unavailable, write `reports/M99_GODOT_REAL_INTEGRATION.md` = `EXTERNAL_BLOCKED`, set Gate 78 accordingly, and continue G103.
Commit only if evidence files are repository-tracked by policy.

## G102B — Minimal real projection
If Godot exists, implement/reuse a minimal external project that reads Wanxiang projection state and renders at least actor + navigable obstacle/target. No duplicate canonical truth in Godot.
Commit: `g102b: add real godot projection integration`

## G102C — Physical action round trip
Prove:
Canonical State → Godot Scene → Player Physical Action → Physics/Navigation Result → ProposedDelta → Wanxiang Validate/Commit → StateDiff → Projection Refresh.
Godot cannot write database/canonical state directly. Include stale snapshot/revision rejection and replay evidence.
Commit: `g102c: qualify godot physical action round trip`

## G102D — M99 qualification
Write `reports/M99_GODOT_REAL_INTEGRATION.md` and machine-readable artifact.
Gate 78 = ACCEPTED only for a real engine E2E; otherwise EXTERNAL_BLOCKED/NOT_IN_STABLE_SCOPE. Never call ABI/reference-provider tests “real Godot”.
Commit: `g102d: record m99 godot qualification`
