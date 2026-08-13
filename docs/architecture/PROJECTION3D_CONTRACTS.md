# Godot / Babylon Projection Contracts (G12E)

`packages/sdk_ts/src/projection3d.ts` defines scene/entity transform
projections, asset refs, animation/state cues, command input validation and an
update protocol diff over server projections. Renderers remain
non-authoritative; scenes are view-model contracts only.