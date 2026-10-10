"""A durable local visual index serializes independent Python worker processes."""

import json
import pathlib
import subprocess
import sys
import time


_WORKER = """
import json
import pathlib
import sys
import time

from wanxiang_substrate.assets.book_scene_cache import LocalJsonVisualCacheIndex, VisualAssetCache
from wanxiang_substrate.assets.book_scene_materialize import _materialize_visual_plan
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest, _SourceVisualPlan
from wanxiang_substrate.assets.book_scene_render import _ProceduralSvgSceneProvider
from wanxiang_substrate.assets.foundry import SemanticSceneSpec
from wanxiang_substrate.assets.storage import LocalObjectStore


class SlowScene(_ProceduralSvgSceneProvider):
    def produce(self, request):
        time.sleep(0.6)
        return super().produce(request)


root = pathlib.Path(sys.argv[1])
(root / f"ready-{sys.argv[2]}").touch()
while not (root / "go").exists():
    time.sleep(0.01)

request = _SourceSceneRequest(
    place_name="旧城",
    stable_key="shared-process-scene",
    spec=SemanticSceneSpec(
        spec_id="test-scene",
        semantic_id="place:shared-process-scene",
        kind="illustrated-environment",
        requirements=("source_place_name:旧城",),
    ),
    cache_key="one-source-scene-cache",
)
plan = _SourceVisualPlan(
    package_id="world:shared-process",
    source_digest="f" * 64,
    status="READY_FOR_ASSET_PROVIDER",
    scene_requests=(request,),
    deferred_scene_count=0,
)
cache = VisualAssetCache(
    LocalObjectStore(root / "blobs"), LocalJsonVisualCacheIndex(root / "index.json")
)
result = _materialize_visual_plan(plan, provider=SlowScene(), cache=cache)
print(json.dumps({"calls": result.provider_calls, "hits": result.cache_hits}))
"""


def test_two_processes_share_one_local_scene_generation(tmp_path: pathlib.Path) -> None:
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
            assert time.monotonic() < deadline, "visual cache worker startup timed out"
            assert all(p.poll() is None for p in processes), "visual worker exited early"
            time.sleep(0.02)
        (tmp_path / "go").write_text("go", encoding="utf-8")
        results: list[dict[str, int]] = []
        for process in processes:
            out, err = process.communicate(timeout=30)
            assert process.returncode == 0, err
            decoded: object = json.loads(out)
            assert isinstance(decoded, dict)
            results.append({"calls": int(decoded["calls"]), "hits": int(decoded["hits"])})
        assert sorted(row["calls"] for row in results) == [0, 1]
        assert sorted(row["hits"] for row in results) == [0, 1]
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)
