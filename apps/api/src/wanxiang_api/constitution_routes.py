"""Constitution API routes (G34E): read-only constitution manifest access."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from wanxiang_domain.constitution import ROOT_CONSTITUTION, legacy_default_constitution

router = APIRouter(prefix="/constitutions", tags=["constitution"])


def _registry(request: Request) -> dict[str, dict[str, object]]:
    registry = getattr(request.app.state, "constitutions", None)
    if registry is None:
        legacy = legacy_default_constitution()
        registry = {
            ROOT_CONSTITUTION.constitution_id.value: ROOT_CONSTITUTION.to_primitive(),
            legacy.constitution_id.value: legacy.to_primitive(),
        }
        request.app.state.constitutions = registry
    return registry


@router.get("/{constitution_id}")
def get_constitution(constitution_id: str, request: Request) -> dict[str, object]:
    manifest = _registry(request).get(constitution_id)
    if manifest is None:
        raise HTTPException(status_code=404, detail=f"constitution {constitution_id!r} not found")
    return manifest
