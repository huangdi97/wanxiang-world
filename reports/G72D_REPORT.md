# G72D Report — Mixed-source world

**PASS (2026-08-25)** — Book + image + structured supplement is accepted by
the shared one-click service. Image bytes are handled by the explicit asset
adapter and in-memory object-store reference path; they do not become fake
semantic Canon. The mixed package passes deterministic validation and publish
checkpointing.

Evidence: `tests/integration/test_m69_one_click.py` mixed flow and the M62
multimodal/asset-port regression.
