"""Living-world and Worldness transport routes over authoring use cases."""

from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Request
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.state import state_to_primitive
from wanxiang_substrate.authoring.living_world import LivingRuntimePort
from wanxiang_substrate.authoring.service import AuthoringService

router = APIRouter(prefix="/studio")


def _service(request: Request) -> AuthoringService:
    return request.app.state.authoring


def _runtime(request: Request) -> LivingRuntimePort:
    runtime = request.app.state.runtime
    if runtime is None:
        raise ValidationRejected(
            "living runtime is not configured",
            details={"product_state": "RUNTIME_REQUIRED"},
        )
    return runtime


@router.post("/jobs/{job_id}/instantiate")
def instantiate(job_id: str, request: Request) -> dict[str, object]:
    record = _service(request).instantiate_living(job_id, _runtime(request))
    return {"job_id": job_id, "living": record.to_dict()}


@router.post("/jobs/{job_id}/enter")
def enter(job_id: str, request: Request) -> dict[str, object]:
    runtime = _runtime(request)
    record = _service(request).instantiate_living(job_id, runtime)
    state = runtime.current_state(WorldInstanceId(record.instance_id), BranchId(record.branch_id))
    primitive = state_to_primitive(state)
    entities = cast(list[dict[str, object]], primitive["entities"])
    relations = cast(list[dict[str, object]], primitive["relations"])
    perception = {
        "instance_id": record.instance_id,
        "branch_id": record.branch_id,
        "revision": primitive["revision"],
        "entities": [str(item["id"]) for item in entities],
        "relations": [str(item["id"]) for item in relations],
    }
    return {"job_id": job_id, "living": record.to_dict(), "perception": perception}


@router.get("/jobs/{job_id}/living")
def get_living(job_id: str, request: Request) -> dict[str, object]:
    record = _service(request).living(job_id)
    return {"job_id": job_id, "living": record.to_dict() if record else None}


@router.post("/jobs/{job_id}/worldness")
def evaluate_worldness(job_id: str, request: Request) -> dict[str, object]:
    run = _service(request).evaluate_worldness(job_id, _runtime(request))
    return {"job_id": job_id, "worldness": run.to_dict()}


@router.get("/jobs/{job_id}/worldness")
def get_worldness(job_id: str, request: Request) -> dict[str, object]:
    run = _service(request).worldness(job_id)
    return {"job_id": job_id, "worldness": run.to_dict() if run else None}
