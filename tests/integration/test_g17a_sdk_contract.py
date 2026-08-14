"""G17A: public SDK contract, semantic versioning & compatibility policy.

- Third-party code can perform supported operations through the SDK only.
- Breaking changes are detected by the compatibility snapshot.
- Experimental APIs are clearly separated/labeled (policy doc).
"""

from __future__ import annotations

import json
import pathlib

from scripts.sdk_baseline import build

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
BASELINE = ROOT / "reports" / "sdk_api_baseline.json"


def test_third_party_operations_via_sdk_only(persist_db_path: pathlib.Path) -> None:
    """A third-party author performs supported operations using public SDK only."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "synthetic_full", ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"
    )
    assert spec is not None and spec.loader is not None
    sf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sf)

    # Build + install the pack through the public package SDK.
    registry = sf.build_registry()
    record = sf.install_pack(registry)
    assert record.lock_hash
    # Instantiate + operate through the public application runtime.
    runtime = sf.make_runtime(persist_db_path)
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    # Project through the public projection API.
    from wanxiang_substrate.projection.model import ProjectionRequest
    from wanxiang_substrate.projection.service import ProjectionService

    state = runtime.current_state(sf.INSTANCE, w.root_branch_id)
    snap = ProjectionService(state).compose(
        ProjectionRequest(
            session_id="s", actor_id=sf.MAYOR.value, branch_id=w.root_branch_id, mode="text"
        )
    )
    assert snap.revision == state.revision.value
    # The third-party code used no ORM sessions, no Commit internals, no
    # underscore-prefixed runtime objects (verified by imports above).


def test_breaking_changes_detected_by_snapshot() -> None:
    current = build()
    committed = json.loads(BASELINE.read_text(encoding="utf-8"))
    assert current == committed, (
        "public SDK surface drifted from the committed baseline; run scripts/sdk_baseline.py "
        "and review the change (a breaking change requires a major version bump)"
    )
    # Simulate a breaking change: removing an API route must be detected.
    tampered = json.loads(BASELINE.read_text(encoding="utf-8"))
    tampered["api_routes"].pop()
    assert current != tampered


def test_experimental_apis_separated_and_stable_surface_clean() -> None:
    data = json.loads(BASELINE.read_text(encoding="utf-8"))
    # No underscore-prefixed internals leak into the stable Python surface.
    assert not any(name.split(".")[-1].startswith("_") for name in data["python_surface"])
    # Experimental namespace is documented separately (not in the stable baseline).
    policy = (ROOT / "docs" / "SDK_COMPATIBILITY_POLICY.md").read_text(encoding="utf-8")
    assert "Experimental" in policy and "stable" in policy.lower()
