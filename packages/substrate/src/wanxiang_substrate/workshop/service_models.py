"""Transport-neutral Workshop build evidence."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.preview import PreviewInstall
from wanxiang_substrate.workshop.genesis_provider import PromptGenesisRun
from wanxiang_substrate.workshop.hybrid_genesis import HybridGenesisResult
from wanxiang_substrate.workshop.models import WorkshopDraft
from wanxiang_substrate.workshop.publishing import PublishingDecision


@dataclass(frozen=True, slots=True)
class WorkshopBuild:
    workshop: WorkshopDraft
    package: WorldPackageDraft
    preview: PreviewInstall
    publishing: PublishingDecision
    prompt_run: PromptGenesisRun | None = None
    hybrid: HybridGenesisResult | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "workshop": self.workshop.to_dict(),
            "package_id": self.package.package_id,
            "package_hash": self.package.manifest.content_hash,
            "preview": {
                "preview_id": self.preview.preview_id,
                "scoped_ref": self.preview.scoped_ref,
                "package_id": self.preview.package_id,
            },
            "publishing": {
                "publishable": self.publishing.publishable,
                "visible_in_plaza": self.publishing.visible_in_plaza,
                "reasons": list(self.publishing.reasons),
            },
            "prompt": self.prompt_run.contract.to_dict() if self.prompt_run else None,
            "hybrid": self.hybrid.to_dict() if self.hybrid else None,
        }


__all__ = ["WorkshopBuild"]
