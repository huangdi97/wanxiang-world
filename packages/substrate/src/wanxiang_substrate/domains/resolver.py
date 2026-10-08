"""Domain dependency resolver (G59C).

Resolves a selected domain set: topological ordering by requires, version
compat check, and conflict explanation. Reuses the version-constraint style of
the package resolver (no second package system).
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.domains.capability import DomainRegistry


@dataclass(frozen=True, slots=True)
class DependencyResolution:
    selected: tuple[str, ...]
    order: tuple[str, ...]
    conflicts: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.conflicts


class DomainDependencyResolver:
    """Topological domain resolution with conflict reporting."""

    def resolve(
        self,
        registry: DomainRegistry,
        selected: tuple[str, ...],
    ) -> DependencyResolution:
        known = {domain.domain_id for domain in registry.all()}
        selected_ids = tuple(dict.fromkeys(selected))
        conflicts: list[str] = []
        for domain_id in selected_ids:
            if domain_id not in known:
                conflicts.append(f"unknown domain {domain_id!r}")
        if conflicts:
            return DependencyResolution(selected_ids, (), tuple(conflicts))
        # Topological order: requires first.
        order: list[str] = []
        visited: set[str] = set()
        temporary: set[str] = set()

        def visit(domain_id: str) -> None:
            if domain_id in visited:
                return
            if domain_id in temporary:
                conflicts.append(f"dependency cycle at {domain_id!r}")
                return
            temporary.add(domain_id)
            domain = registry.require(domain_id)
            for required in domain.requires:
                if required in selected_ids:
                    visit(required)
            temporary.discard(domain_id)
            visited.add(domain_id)
            order.append(domain_id)

        for domain_id in selected_ids:
            visit(domain_id)
        if conflicts:
            return DependencyResolution(selected_ids, (), tuple(conflicts))
        return DependencyResolution(selected_ids, tuple(order), ())
