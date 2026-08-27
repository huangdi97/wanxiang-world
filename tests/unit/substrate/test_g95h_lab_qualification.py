"""G95H: cross-artifact M92 qualification model semantics."""

from __future__ import annotations

from wanxiang_substrate.world_lab import (
    LabQualification,
    QualificationCheck,
    QualificationStatus,
)


def _qualification(status: QualificationStatus = "pass") -> LabQualification:
    checks = tuple(
        QualificationCheck(
            name=name,
            status=status,
            reason=f"explicit {name} evidence",
            evidence_refs=(f"evidence:g95h:{name}",),
        )
        for name in ("batch_4plus", "intervention", "comparison", "run_artifacts")
    )
    return LabQualification(
        qualification_id="qualification:g95h",
        experiment_ref="experiment:g95h",
        source_profile="literary",
        validation_profile_ref="validation:g95g",
        batch_ref="batch:g95h",
        worldline_refs=("worldline:g95h:1", "worldline:g95h:2"),
        artifact_refs=("artifact:g95h:1", "artifact:g95h:2"),
        intervention_refs=("intervention-run:g95h",),
        comparison_ref="comparison:g95h",
        checks=checks,
    )


def test_qualification_round_trip_is_sanitized_and_qualified() -> None:
    qualification = _qualification()

    restored = LabQualification.from_dict(qualification.to_dict())

    assert qualification.qualified is True
    assert qualification.overall_status == "pass"
    assert restored == qualification
    assert "source_text" not in repr(qualification.to_dict())


def test_unknown_or_empty_qualification_is_not_qualified() -> None:
    unknown = _qualification("unknown")
    empty = LabQualification(
        qualification_id="qualification:g95h:empty",
        experiment_ref="experiment:g95h",
        source_profile="literary",
        validation_profile_ref="validation:g95g",
        batch_ref="batch:g95h",
        worldline_refs=("worldline:g95h:1",),
        artifact_refs=("artifact:g95h:1",),
        intervention_refs=("intervention-run:g95h",),
        comparison_ref="comparison:g95h",
        checks=(),
    )

    assert unknown.overall_status == "unknown"
    assert unknown.qualified is False
    assert empty.overall_status == "unknown"
    assert empty.qualified is False
