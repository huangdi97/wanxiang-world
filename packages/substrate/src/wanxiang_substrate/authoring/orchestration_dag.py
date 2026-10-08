"""Deterministic stage graph for M67 authoring orchestration."""

from __future__ import annotations

AUTHORING_STAGES = (
    "ingest",
    "parse",
    "distill",
    "fuse",
    "domain",
    "complete",
    "scenario",
    "compile",
    "preview",
    "evaluate",
)
STAGE_DEPENDENCIES = {
    "ingest": (),
    "parse": ("ingest",),
    "distill": ("parse",),
    "fuse": ("distill",),
    "domain": ("fuse",),
    "complete": ("domain",),
    "scenario": ("complete",),
    "compile": ("scenario",),
    "preview": ("compile",),
    "evaluate": ("preview",),
}


class AuthoringDAG:
    """The single deterministic order for the source-to-preview stages."""

    def __init__(self, stages: tuple[str, ...] = AUTHORING_STAGES) -> None:
        self._stages = stages

    def order(self) -> tuple[str, ...]:
        remaining = set(self._stages)
        ordered: list[str] = []
        while remaining:
            ready = tuple(
                stage
                for stage in self._stages
                if stage in remaining
                and all(dependency not in remaining for dependency in STAGE_DEPENDENCIES[stage])
            )
            if not ready:
                raise ValueError("authoring stage dependencies contain a cycle")
            ordered.extend(ready)
            remaining.difference_update(ready)
        return tuple(ordered)

    def dependencies(self, stage: str) -> tuple[str, ...]:
        if stage not in STAGE_DEPENDENCIES:
            raise ValueError(f"unknown authoring stage {stage!r}")
        return STAGE_DEPENDENCIES[stage]
