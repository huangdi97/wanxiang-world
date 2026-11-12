"""Local durable T3 jobs coalesce concurrent provider submissions across processes."""

import json
import pathlib
import subprocess
import sys
import time
from typing import cast

_WORKER = r"""
import json
import pathlib
import sys
import time

from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_jobs import (
    _LocalJsonSpatialJobStore,
    _SpatialGenerationCoordinator,
)
from wanxiang_substrate.assets.book_spatial_types import _SpatialGenerationProvider
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.assets.storage import LocalObjectStore


class SlowProvider(_SpatialGenerationProvider):
    provider_id = "spatial:process-test"
    provider_version = "1"
    requires_network = False
    private_safe = True
    cost_units_per_job = 1
    allowed_media_types = frozenset({"model/gltf-binary"})

    def submit(self, request, *, idempotency_key):
        _ = request
        count_path = root / "provider-calls.log"
        with count_path.open("a", encoding="utf-8") as handle:
            handle.write(idempotency_key + "\\n")
            handle.flush()
        time.sleep(0.5)
        return "shared-task"

    def poll(self, task_ref):
        raise AssertionError(task_ref)


root = pathlib.Path(sys.argv[1])
(root / f"ready-{sys.argv[2]}").touch()
while not (root / "go").exists():
    time.sleep(0.01)

request = _SourceSceneRequest(
    place_name="机关桥",
    stable_key="bridge",
    spec=SemanticSceneSpec(
        spec_id="scene-bridge",
        semantic_id="place:bridge",
        kind="illustrated-environment",
    ),
    cache_key="shared-cache-key",
    style_key="shared-style",
)
coordinator = _SpatialGenerationCoordinator(
    SlowProvider(),
    jobs=_LocalJsonSpatialJobStore(root / "spatial-jobs.json"),
    objects=LocalObjectStore(root / "objects"),
)
ticket = coordinator.submit(
    request,
    allow_network=False,
    external_processing_allowed=False,
    private_source=False,
    max_cost_units=1,
    delivery_rights="source-gated",
    scope_key="world:shared",
)
print(json.dumps({"submission_id": ticket.submission_id, "task": ticket.provider_task_ref}))
"""


def test_two_processes_submit_one_durable_t3_provider_job(tmp_path: pathlib.Path) -> None:
    processes: list[subprocess.Popen[str]] = []
    try:
        for worker_id in range(2):
            processes.append(
                subprocess.Popen(
                    [sys.executable, "-c", _WORKER, str(tmp_path), str(worker_id)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            )
        deadline = time.monotonic() + 30
        while not all((tmp_path / f"ready-{i}").exists() for i in range(2)):
            assert time.monotonic() < deadline, "T3 worker startup timed out"
            assert all(p.poll() is None for p in processes), "T3 worker exited early"
            time.sleep(0.02)

        (tmp_path / "go").write_text("go", encoding="utf-8")
        rows: list[dict[str, str]] = []
        for process in processes:
            out, err = process.communicate(timeout=30)
            assert process.returncode == 0, err
            decoded: object = json.loads(out)
            assert isinstance(decoded, dict)
            row = cast(dict[str, object], decoded)
            submission_id, task = row.get("submission_id"), row.get("task")
            assert isinstance(submission_id, str) and isinstance(task, str)
            rows.append({"submission_id": submission_id, "task": task})

        calls = (tmp_path / "provider-calls.log").read_text(encoding="utf-8").splitlines()
        assert len(calls) == 1
        assert len({row["submission_id"] for row in rows}) == 1
        assert {row["task"] for row in rows} == {"shared-task"}
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)
