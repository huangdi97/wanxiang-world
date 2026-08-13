"""Reality bridge error taxonomy (G07A-G07E)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class RealityError(WanxiangError):
    """Base error for reality bridge failures."""

    code = "reality_error"


class InvalidObservation(RealityError):
    code = "invalid_physical_observation"


class FusionPolicyError(RealityError):
    code = "fusion_policy_error"


class ChallengeValidationError(RealityError):
    code = "challenge_validation_error"


class DirectorError(RealityError):
    code = "director_error"


class ExperimentError(RealityError):
    code = "experiment_error"
