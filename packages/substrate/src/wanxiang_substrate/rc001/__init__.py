"""RC-001 living-world slice (M33)."""

from wanxiang_substrate.rc001.chaos import (
    ChaosCheck,
    ChaosReport,
    detect_stream_corruption,
    duplicate_command_rejected,
    provider_failure_isolated,
    reconnect_embodiment,
    run_chaos_checks,
    snapshot_restart,
)
from wanxiang_substrate.rc001.experience import ExperienceStudio, ExperienceViews
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
from wanxiang_substrate.rc001.promotion import (
    LongHorizonPromotion,
    accelerate,
    distill_stable,
    promote_long_horizon,
)
from wanxiang_substrate.rc001.seven_day import (
    DAY_TICKS,
    DayEvent,
    SevenDayReferenceRun,
    SevenDayResult,
    optional_llm_run,
)
from wanxiang_substrate.rc001.strategies import (
    BaselineComparison,
    CanonLocks,
    SoftAttractor,
    StrategyConfig,
    compare_to_baseline,
    strategy_for,
)
from wanxiang_substrate.rc001.worldlines import (
    WorldlineComparison,
    WorldlineRun,
    compare_worldlines,
    run_worldlines,
    verify_parent_hash,
)

__all__ = [
    "Activity",
    "ChaosCheck",
    "ChaosReport",
    "detect_stream_corruption",
    "duplicate_command_rejected",
    "provider_failure_isolated",
    "reconnect_embodiment",
    "run_chaos_checks",
    "snapshot_restart",
    "LongHorizonPromotion",
    "accelerate",
    "distill_stable",
    "promote_long_horizon",
    "WorldlineComparison",
    "WorldlineRun",
    "compare_worldlines",
    "run_worldlines",
    "verify_parent_hash",
    "DAY_TICKS",
    "DayEvent",
    "SevenDayReferenceRun",
    "SevenDayResult",
    "optional_llm_run",
    "ExperienceStudio",
    "ExperienceViews",
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
