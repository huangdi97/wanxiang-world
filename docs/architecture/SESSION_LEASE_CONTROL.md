# Session, Embodiment Lease & Control Handoff (G05B, G05C)

Ownership: `wanxiang_substrate.session`.

## Session & lease

`Session` binds a client to a world instance with a mode (observe/embody/admin).
`LeaseService` enforces exactly one primary embodiment controller per actor:
acquiring a lease while another is active raises `LeaseConflict`; leases renew,
release and expire with explicit state transitions.

## Control handoff

`ControlHandoff` is a per-actor state machine:
autonomous -> human_control -> handing_back -> resuming_autonomous ->
autonomous. Acquiring human control pauses the autonomous controller and
records a resume ref; release restores the deterministic controller from the
current world + memory state.

## Shadow policy

`ShadowPolicy` is strictly advice-only. Its `commit` raises
`ShadowCannotCommit`; shadow outputs exist only in the advice channel and can
never compete for authoritative body control. Committed human actions are
normal world history.