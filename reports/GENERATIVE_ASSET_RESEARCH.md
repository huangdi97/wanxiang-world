# Generative Asset / Scene Pipeline & Semantic Binding Research (G19F)

## Prototype
- `AssetManifest` ? generated-asset metadata bound to canonical entity/package/revision, with rights,
  provenance, version and explicit fallback marker (assets are projections/artifacts, never authority).
- `AssetFoundryPipeline` ? deterministic local foundry; regeneration creates a NEW version and retains
  the old manifest in history (no silent overwrite); discard removes only the active projection binding.
- `SceneProjector` ? rebuilds `SceneLayout` from semantic anchors; missing assets become explicit
  fallback markers, never silent blanks.

## Results
| Check | Result |
|---|---|
| Regeneration versions instead of overwriting; world truth untouched | PASS |
| Rights/provenance travel with the asset into projections | PASS |
| Projection rebuildable from semantic state (deterministic rebuild hash) | PASS |
| Missing asset -> explicit fallback marker | PASS |
| Flag OFF -> no core regression (stable compiler path unchanged) | PASS |

## Decision
**KEEP_EXPERIMENTAL** ? the binding/versioning seam is sound; real renderers and 3D/visual/audio
generation providers are EXTERNAL_BLOCKED. Promotion requires generator parity and a
rights/provenance audit over real generated assets (ADR + full stable regression).

## Evidence
- `uv run pytest tests/integration/test_g19f_generative_assets.py -q` -> 5 passed.
- ruff/pyright clean; architecture PASS at the M16 gate.
