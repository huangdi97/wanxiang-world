"""Structured skill error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class SkillError(WanxiangError):
    """Base error for skill substrate failures."""

    code = "skill_error"


class SkillPrerequisiteError(SkillError):
    code = "skill_prerequisite_error"


class InvalidSkillStep(SkillError):
    code = "invalid_skill_step"
