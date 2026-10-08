"""Domain capability manifest (G59A).

A domain declares provides/requires/schema/actions/rules/compat. Domains are
reusable capabilities; specific worlds never modify them. Versioned manifests
are the unit the recommender and dependency resolver operate on.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError


@dataclass(frozen=True, slots=True)
class DomainCapability:
    domain_id: str
    name: str
    version: str
    provides: tuple[str, ...]
    requires: tuple[str, ...] = ()
    schema_refs: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    compat: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.domain_id or not self.name:
            raise ContractError("domain requires id and name")
        if not self.version:
            raise ContractError("domain requires a version")
        if not self.provides:
            raise ContractError("domain must provide at least one capability")
        if self.domain_id in self.requires:
            raise ContractError("domain cannot require itself")


class DomainRegistry:
    """Registry of reusable domain capabilities (single-problem)."""

    def __init__(self) -> None:
        self._domains: dict[str, DomainCapability] = {}

    def register(self, domain: DomainCapability) -> DomainCapability:
        if domain.domain_id in self._domains:
            raise ContractError(f"domain {domain.domain_id!r} already registered")
        self._domains[domain.domain_id] = domain
        return domain

    def get(self, domain_id: str) -> DomainCapability | None:
        return self._domains.get(domain_id)

    def require(self, domain_id: str) -> DomainCapability:
        domain = self.get(domain_id)
        if domain is None:
            raise ContractError(f"unknown domain {domain_id!r}")
        return domain

    def all(self) -> tuple[DomainCapability, ...]:
        return tuple(self._domains.values())
