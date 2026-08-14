"""Clean-room private/staging deployment helper (G16J).

Brings up a fresh environment from repository artifacts + docs: checks
prerequisites (fails clearly on missing ones), migrates, instantiates the
synthetic reference world, runs a smoke (health + replay), and backs up.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


class PrerequisiteError(RuntimeError):
    pass


def check_prerequisites(database_url: str) -> None:
    if not database_url:
        raise PrerequisiteError("WANXIANG_DATABASE_URL is required for deployment")
    if database_url.startswith("sqlite:///./data/wanxiang.db"):
        raise PrerequisiteError("production deployment must not use the dev sqlite default")
    for tool in ("uv", "node"):
        import shutil

        if shutil.which(tool) is None:
            raise PrerequisiteError(f"missing prerequisite tool: {tool}")


def deploy(database_url: str, *, world_instance: str = "wld_ops") -> dict[str, object]:
    import os

    from alembic import command
    from alembic.config import Config

    check_prerequisites(database_url)
    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old

    # Instantiate the synthetic reference world through the public path.
    sys.path.insert(0, str(ROOT))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "synthetic_full", ROOT / "reference_worlds" / "synthetic_full" / "synthetic_full.py"
    )
    assert spec is not None and spec.loader is not None
    sf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sf)
    runtime = sf.make_runtime(__import__("pathlib").Path(database_url.removeprefix("sqlite:///")))
    w = runtime.create_world(instance_id=sf.INSTANCE)
    runtime.submit_command(sf.instantiate_command(w.root_branch_id, 0))
    final_hash = runtime.current_state(sf.INSTANCE, w.root_branch_id).semantic_hash()

    # Smoke: health + replay.
    from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
    from wanxiang_runtime.replay import ReplayEngine

    events = runtime.persistence.event_store.load(sf.INSTANCE, w.root_branch_id)
    replay_hash = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events).semantic_hash()
    assert replay_hash == final_hash
    return {
        "instance": sf.INSTANCE.value,
        "revision": runtime.current_state(sf.INSTANCE, w.root_branch_id).revision.value,
        "final_hash": final_hash,
        "replay_ok": replay_hash == final_hash,
    }


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        print(deploy(url))
    except PrerequisiteError as exc:
        raise SystemExit(f"PREREQUISITE FAILED: {exc}") from exc
