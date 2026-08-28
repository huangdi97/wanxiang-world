"""Collect ExperienceQuality from observable traces without copying canon."""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.quality.experience_models import (
    QUALITY_DIMENSIONS,
    ExperienceDimension,
    ExperienceMeasurement,
    ExperienceQualityRun,
)
from wanxiang_substrate.quality.experience_scenarios import ExperienceBenchmarkScenario


@dataclass(frozen=True, slots=True)
class ExperienceTraceEvidence:
    """Small trace summary passed by a runner; canonical state stays behind refs."""

    run_id: str
    build_sha: str
    seed: int
    trace_ref: str
    worldness_ref: str
    event_refs: tuple[str, ...]
    state_refs: tuple[str, ...]
    replay_refs: tuple[str, ...]
    action_committed: bool
    rejection_observed: bool
    replay_equal: bool
    character_identity_stable: bool
    leave_continue_equal: bool
    revision_aligned: bool
    goal_visible: bool
    state_diff_count: int
    after_state_hashes: tuple[str, ...]
    memory_revision_count: int = 0
    belief_revision_count: int = 0
    relationship_revision_count: int = 0
    human_ratings: tuple[tuple[str, float], ...] = ()

    def __post_init__(self) -> None:
        for name in ("run_id", "build_sha", "trace_ref", "worldness_ref"):
            value = getattr(self, name)
            if (
                not isinstance(value, str)
                or not value.strip()
                or any(char.isspace() for char in value)
            ):
                raise ContractError(f"{name} must be a non-empty opaque reference")
        if self.state_diff_count < 0 or any(
            value < 0
            for value in (
                self.memory_revision_count,
                self.belief_revision_count,
                self.relationship_revision_count,
            )
        ):
            raise ContractError("experience trace counts cannot be negative")
        for name in ("event_refs", "state_refs", "replay_refs", "after_state_hashes"):
            values = tuple(getattr(self, name))
            if (
                not values
                or len(set(values)) != len(values)
                or any(not item.strip() for item in values)
            ):
                raise ContractError(f"{name} must contain unique non-empty refs")
        ratings = dict(self.human_ratings)
        if len(ratings) != len(self.human_ratings):
            raise ContractError("human rating dimensions must be unique")
        if any(
            name not in QUALITY_DIMENSIONS or not 1.0 <= value <= 5.0
            for name, value in ratings.items()
        ):
            raise ContractError("human ratings must use required dimensions and a 1..5 scale")


def _boolean_value(value: bool) -> float:
    return 1.0 if value else 0.0


def _bounded_ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return min(1.0, max(0.0, numerator / denominator))


def collect_experience_quality(
    scenario: ExperienceBenchmarkScenario,
    trace: ExperienceTraceEvidence,
) -> ExperienceQualityRun:
    """Create one run record from trace facts and optional real human ratings."""
    if scenario.scenario_id not in trace.run_id:
        raise ContractError("run id must identify its frozen benchmark scenario")
    unique_after = len(set(trace.after_state_hashes))
    automated: dict[str, tuple[float | None, str, str, tuple[str, ...]]] = {
        "Agency": (
            (float(trace.action_committed) + float(trace.rejection_observed)) / 2.0,
            "behavioral_trace",
            "committed action and observed invalid-action rejection",
            (trace.trace_ref, trace.event_refs[0]),
        ),
        "Coherence": (
            _boolean_value(trace.replay_equal),
            "invariant_metric",
            "replay hash equality",
            tuple(trace.replay_refs),
        ),
        "CharacterConsistency": (
            _boolean_value(trace.character_identity_stable),
            "behavioral_trace",
            "entry and continuation actor identity equality",
            (trace.trace_ref, trace.state_refs[-1]),
        ),
        "ConsequenceVisibility": (
            _bounded_ratio(trace.state_diff_count, len(trace.event_refs)),
            "behavioral_trace",
            "observable StateDiff count over committed trace events",
            (trace.trace_ref, trace.state_refs[-1]),
        ),
        "NarrativeStateAlignment": (
            _boolean_value(trace.revision_aligned),
            "invariant_metric",
            "event revision and state projection alignment",
            (trace.event_refs[-1], trace.state_refs[-1]),
        ),
        "GoalClarity": (
            _boolean_value(trace.goal_visible),
            "behavioral_trace",
            "frozen action script and allowed action visible",
            (trace.trace_ref,),
        ),
        "WorldReactivity": (
            _bounded_ratio(unique_after, len(trace.after_state_hashes)),
            "behavioral_trace",
            "unique post-action state hashes over action trace",
            tuple(trace.state_refs),
        ),
        "MemoryQuality": (
            1.0 if trace.memory_revision_count > 0 else None,
            "behavioral_trace",
            "bounded continuity memory revisions",
            (trace.trace_ref,),
        ),
        "ContinuationQuality": (
            _boolean_value(trace.leave_continue_equal),
            "behavioral_trace",
            "leave and continue state identity",
            (trace.trace_ref, trace.state_refs[-1]),
        ),
        "NoveltyRepetition": (
            _bounded_ratio(unique_after, len(trace.after_state_hashes)),
            "invariant_metric",
            "post-action state variation ratio; no universal threshold",
            tuple(trace.state_refs),
        ),
    }
    ratings = dict(trace.human_ratings)
    dimensions: list[ExperienceDimension] = []
    for name in QUALITY_DIMENSIONS:
        value, method, note, refs = automated[name]
        measurements = [
            ExperienceMeasurement(
                method,  # type: ignore[arg-type]
                "measured" if value is not None else "not_applicable",
                value,
                refs,
                sample_size=1 if value is not None else 0,
                note=note,
            )
        ]
        if name in ratings:
            measurements.append(
                ExperienceMeasurement(
                    "human_rating",
                    "measured",
                    (ratings[name] - 1.0) / 4.0,
                    (f"human:{trace.run_id}",),
                    sample_size=1,
                    scale="1_to_5_normalized_to_0_1",
                )
            )
        else:
            measurements.append(
                ExperienceMeasurement(
                    "human_rating",
                    "missing",
                    note="genuine human session or rating not available",
                )
            )
        dimensions.append(ExperienceDimension(name, tuple(measurements)))
    missing_data = (
        ()
        if len(ratings) == len(QUALITY_DIMENSIONS)
        else (
            "human_session",
            "human_ratings",
        )
    )
    return ExperienceQualityRun(
        run_id=trace.run_id,
        scenario_id=scenario.scenario_id,
        world_family=scenario.family,
        world_ref=scenario.world_ref,
        package_ref=scenario.package_ref,
        scenario_version=scenario.version,
        build_sha=trace.build_sha,
        seed=trace.seed,
        action_script=scenario.action_script,
        event_refs=trace.event_refs,
        state_refs=trace.state_refs,
        replay_refs=trace.replay_refs,
        dimensions=tuple(dimensions),
        worldness_ref=trace.worldness_ref,
        human_status="provided" if not missing_data else "missing",
        missing_data=missing_data,
    ).with_hash()


__all__ = ["ExperienceTraceEvidence", "collect_experience_quality"]
