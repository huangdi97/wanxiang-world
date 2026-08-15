"""RC-001 living-world slice (M33)."""

from wanxiang_substrate.rc001.instantiate import (
    InitialSnapshot,
    RC001Instance,
    RC001Profile,
    genesis_delta,
    instantiate_rc001,
    record_lineage_root,
    resolve_rc001_profile,
)
from wanxiang_substrate.rc001.npc import (
    Activity,
    ActivityKind,
    NPCProfile,
    daily_schedule,
    resolve_population,
    resolve_population_result,
)
from wanxiang_substrate.rc001.strategies import (
    BaselineComparison,
    CanonLocks,
    SoftAttractor,
    StrategyConfig,
    compare_to_baseline,
    strategy_for,
)

__all__ = [
    "Activity",
    "BaselineComparison",
    "CanonLocks",
    "SoftAttractor",
    "StrategyConfig",
    "compare_to_baseline",
    "strategy_for",
    "ActivityKind",
    "InitialSnapshot",
    "NPCProfile",
    "daily_schedule",
    "resolve_population",
    "resolve_population_result",
    "RC001Instance",
    "RC001Profile",
    "genesis_delta",
    "instantiate_rc001",
    "record_lineage_root",
    "resolve_rc001_profile",
]
