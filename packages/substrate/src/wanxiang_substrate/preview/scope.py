"""Preview scope isolation (G60E)."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.compile.assembler import WorldPackageDraft

PREVIEW_SCHEME = "preview://"


@dataclass(frozen=True, slots=True)
class PreviewInstall:
    preview_id: str
    package_id: str
    draft_id: str
    package_hash: str

    @property
    def scoped_ref(self) -> str:
        return f"{PREVIEW_SCHEME}{self.preview_id}"


class PreviewRegistry:
    """Isolated preview registry; published catalog untouched."""

    def __init__(self) -> None:
        self._installs: dict[str, PreviewInstall] = {}
        self._by_package: dict[str, str] = {}

    def install(self, package: WorldPackageDraft) -> PreviewInstall:
        if package.package_id in self._by_package:
            return self._installs[self._by_package[package.package_id]]
        preview_id = f"preview_{len(self._installs) + 1}"
        install = PreviewInstall(
            preview_id=preview_id,
            package_id=package.package_id,
            draft_id=package.draft_id,
            package_hash=package.manifest.content_hash,
        )
        self._installs[preview_id] = install
        self._by_package[package.package_id] = preview_id
        return install

    def get(self, preview_id: str) -> PreviewInstall | None:
        return self._installs.get(preview_id)

    def for_package(self, package_id: str) -> PreviewInstall | None:
        preview_id = self._by_package.get(package_id)
        return self._installs.get(preview_id) if preview_id else None

    def all(self) -> tuple[PreviewInstall, ...]:
        return tuple(self._installs.values())

    def uninstall(self, preview_id: str) -> None:
        install = self._installs.pop(preview_id, None)
        if install is None:
            raise ContractError(f"preview {preview_id!r} not installed")
        self._by_package.pop(install.package_id, None)
