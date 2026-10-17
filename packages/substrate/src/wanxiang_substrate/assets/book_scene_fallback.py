"""Product-tier visual provider failure accounting and fallback provenance."""

# pyright: reportPrivateUsage=false, reportUnusedClass=false, reportUnusedFunction=false

from __future__ import annotations

from wanxiang_substrate.assets.book_scene_types import SceneImageProvider


class _VisualProviderIneligible(ValueError):
    """Generation is disallowed, but already-cached provider assets may still be reused."""

    def __init__(self, message: str, *, reason: str) -> None:
        super().__init__(message)
        self.reason = reason


class _VisualProviderFailure(ValueError):
    """Provider failure plus conservative attempt/cost accounting for fallback."""

    def __init__(
        self,
        message: str,
        *,
        provider_calls: int,
        cache_hits: int,
        cost_units: int,
    ) -> None:
        super().__init__(message)
        self.provider_calls = provider_calls
        self.cache_hits = cache_hits
        self.cost_units = cost_units


def _provider_failure(
    message: str,
    *,
    attempted_calls: int,
    cache_hits: int,
    provider: SceneImageProvider,
) -> _VisualProviderFailure:
    return _VisualProviderFailure(
        message,
        provider_calls=attempted_calls,
        cache_hits=cache_hits,
        cost_units=provider.cost_units_per_asset * attempted_calls,
    )


def _provider_identity(provider: SceneImageProvider) -> str:
    provider_id = provider.provider_id or "configured-provider"
    provider_version = provider.provider_version or "unknown"
    return f"{provider_id}@{provider_version}"
