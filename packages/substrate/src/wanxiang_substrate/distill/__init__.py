"""Distillation substrate (G57B)."""

from wanxiang_substrate.distill.passes import (
    EventTimeSpacePass,
    IdentityPass,
    RelationOrganizationPass,
)
from wanxiang_substrate.distill.passes_knowledge import (
    CharacterKnowledgePass,
    ObjectRuleSkillPass,
)
from wanxiang_substrate.distill.protocol import Distiller, DistillerDAG, DistillerRegistry

__all__ = [
    "CharacterKnowledgePass",
    "Distiller",
    "DistillerDAG",
    "DistillerRegistry",
    "EventTimeSpacePass",
    "IdentityPass",
    "ObjectRuleSkillPass",
    "RelationOrganizationPass",
]
