"""Structured capability & learning error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class CapabilityError(WanxiangError):
    """Base error for capability substrate failures."""

    code = "capability_error"


class CapabilityPrerequisiteError(CapabilityError):
    code = "capability_prerequisite_error"


class UnsupportedAssessment(CapabilityError):
    code = "unsupported_assessment"


class EvidenceRequired(CapabilityError):
    code = "capability_evidence_required"
