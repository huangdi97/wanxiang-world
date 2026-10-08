"""World Workshop home and shared editor entry point."""

from __future__ import annotations

from wanxiang_substrate.workshop.models import WorkshopHome, WorkshopPanel
from wanxiang_substrate.workshop.store import WorkshopDraftStore


class WorldWorkshop:
    """Information-architecture facade used by API, Studio and tests."""

    def __init__(self, drafts: WorkshopDraftStore | None = None) -> None:
        self.drafts = drafts or WorkshopDraftStore()

    def home(self) -> WorkshopHome:
        return WorkshopHome(
            panels=(
                WorkshopPanel("world_home", "World home", "/workshop"),
                WorkshopPanel("source", "From Source", "/workshop/create/source"),
                WorkshopPanel("prompt", "From Prompt", "/workshop/create/prompt"),
                WorkshopPanel("hybrid", "Hybrid Genesis", "/workshop/create/hybrid"),
                WorkshopPanel("scenario", "Scenario", "/workshop/edit/scenario"),
                WorkshopPanel("experience", "Experience", "/workshop/edit/experience"),
                WorkshopPanel("publishing", "Publishing", "/workshop/publishing"),
                WorkshopPanel("review", "Review", "/workshop/review"),
                WorkshopPanel("registry", "World Registry", "/workshop/registry"),
            )
        )


__all__ = ["WorldWorkshop"]
