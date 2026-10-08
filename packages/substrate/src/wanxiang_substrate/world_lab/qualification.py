"""M92 cross-artifact qualification over existing World Lab evidence (G95H)."""

from __future__ import annotations

from collections.abc import Sequence

from wanxiang_substrate.world_lab.artifact import WorldRunArtifact
from wanxiang_substrate.world_lab.batch_aggregate import BatchExecution
from wanxiang_substrate.world_lab.comparison_models import (
    METRIC_CATEGORIES,
    LabWorldlineComparison,
)
from wanxiang_substrate.world_lab.fork_models import ForkedInterventionRun
from wanxiang_substrate.world_lab.qualification_models import (
    LabQualification,
    QualificationCheck,
)
from wanxiang_substrate.world_lab.registry_support import ref


class WorldLabQualifier:
    """Qualify references from G95A-G95G without owning any runtime state."""

    def qualify(
        self,
        *,
        qualification_id: str,
        experiment_ref: str,
        source_profile: str,
        validation_profile_ref: str,
        batch: BatchExecution,
        intervention_runs: Sequence[ForkedInterventionRun],
        comparison: LabWorldlineComparison,
        artifacts: Sequence[WorldRunArtifact],
    ) -> LabQualification:
        ref(qualification_id, "qualification_id")
        ref(experiment_ref, "experiment_ref")
        ref(source_profile, "source_profile")
        ref(validation_profile_ref, "validation_profile_ref")
        completed = tuple(result for result in batch.results if result.status == "completed")
        artifact_by_ref = {artifact.artifact_id: artifact for artifact in artifacts}
        expected_artifacts = {result.artifact_ref for result in completed}
        observed_worldlines = tuple(result.worldline_ref for result in completed)
        checks = (
            QualificationCheck(
                "batch_4plus",
                "pass"
                if len(completed) >= 4 and len(set(observed_worldlines)) == len(completed)
                else "fail",
                "batch contains at least four completed, uniquely referenced worldlines",
                (batch.plan.batch_id, *observed_worldlines),
            ),
            QualificationCheck(
                "intervention",
                "pass"
                if intervention_runs
                and all(run.status in {"forked", "resumed"} for run in intervention_runs)
                else "fail",
                "at least one intervention run carries typed fork provenance",
                tuple(run.provenance.provenance_id for run in intervention_runs),
            ),
            QualificationCheck(
                "comparison",
                "pass"
                if comparison.qualified
                and {item.category for item in comparison.categories} == set(METRIC_CATEGORIES)
                else "fail",
                "comparison is aligned and covers all five World Lab metric planes",
                (f"comparison:{comparison.alignment_ref}",),
            ),
            QualificationCheck(
                "run_artifacts",
                "pass"
                if expected_artifacts
                and expected_artifacts.issubset(artifact_by_ref)
                and len(artifact_by_ref) >= len(expected_artifacts)
                else "fail",
                "each completed worldline has a corresponding RunArtifact reference",
                tuple(sorted(expected_artifacts)),
            ),
            QualificationCheck(
                "artifact_integrity",
                "pass"
                if expected_artifacts
                and all(
                    artifact_by_ref[artifact_ref].sanitized
                    and artifact_by_ref[artifact_ref].verify_hash()
                    for artifact_ref in expected_artifacts
                )
                else "fail",
                "all referenced RunArtifacts are sanitized and hash-verifiable",
                tuple(sorted(expected_artifacts)),
            ),
        )
        return LabQualification(
            qualification_id=qualification_id,
            experiment_ref=experiment_ref,
            source_profile=source_profile,
            validation_profile_ref=validation_profile_ref,
            batch_ref=batch.plan.batch_id,
            worldline_refs=observed_worldlines,
            artifact_refs=tuple(artifact.artifact_id for artifact in artifacts),
            intervention_refs=tuple(run.run_id for run in intervention_runs),
            comparison_ref=f"comparison:{comparison.alignment_ref}",
            checks=checks,
        )


__all__ = ["WorldLabQualifier"]
