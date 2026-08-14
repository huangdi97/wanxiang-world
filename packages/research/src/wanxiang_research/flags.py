"""Feature flags for experimental research (G19A).

ALL experimental features are OFF by default. Stable behavior is preserved with
flags OFF; research code is isolated and never granted Commit Authority.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResearchFlag:
    name: str
    namespace: str
    enabled: bool = False  # experimental is OFF by default
    promote_criteria: str = ""

    def __post_init__(self) -> None:
        if not self.name or not self.namespace:
            raise ValueError("research flag requires name and namespace")
        if not self.promote_criteria:
            raise ValueError("every research flag must declare promote/reject criteria")


class FeatureFlags:
    """Central registry of experimental flags (all OFF by default)."""

    def __init__(self) -> None:
        self._flags: dict[str, ResearchFlag] = {}

    def register(self, flag: ResearchFlag) -> None:
        self._flags[flag.name] = flag

    def is_enabled(self, name: str) -> bool:
        flag = self._flags.get(name)
        return flag.enabled if flag is not None else False

    def enable(self, name: str) -> None:
        if name not in self._flags:
            raise KeyError(f"unknown research flag {name!r}")
        self._flags[name] = ResearchFlag(
            name=self._flags[name].name,
            namespace=self._flags[name].namespace,
            enabled=True,
            promote_criteria=self._flags[name].promote_criteria,
        )

    def all_disabled(self) -> bool:
        return not any(f.enabled for f in self._flags.values())

    def tracks(self) -> tuple[ResearchFlag, ...]:
        return tuple(self._flags.values())


DEFAULT_FLAGS = FeatureFlags()
DEFAULT_FLAGS.register(
    ResearchFlag("ai_compiler", "v5.1", promote_criteria="benchmark parity + clean-room build")
)
DEFAULT_FLAGS.register(
    ResearchFlag("persona_memory", "v5.1", promote_criteria="drift < threshold over 90d run")
)
DEFAULT_FLAGS.register(
    ResearchFlag("distributed_host", "v6", promote_criteria="shard consistency + replay parity")
)
DEFAULT_FLAGS.register(
    ResearchFlag(
        "generative_assets",
        "v5.1",
        promote_criteria="generator parity + rights/provenance audit on real assets",
    )
)
