"""Domain capability substrate (G59A-C)."""

from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry
from wanxiang_substrate.domains.recommender import DomainRecommender, Recommendation
from wanxiang_substrate.domains.resolver import (
    DependencyResolution,
    DomainDependencyResolver,
)

__all__ = [
    "DependencyResolution",
    "DomainCapability",
    "DomainDependencyResolver",
    "DomainRecommender",
    "DomainRegistry",
    "Recommendation",
]
