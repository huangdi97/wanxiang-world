"""Missingness, consistency, and honest completion solving (M64)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.completion.candidates import CompletionCandidate

CompletionLevel = Literal["E0", "E1", "E2", "E3", "E4", "E5"]
GeneratedCompletionLevel = Literal["E1", "E2", "E3", "E4", "E5"]


@dataclass(frozen=True, slots=True)
class MissingnessNode:
    node_id: str
    requirement: str
    blocking: bool
    source_refs: tuple[str, ...] = ()
    category: str = "generic"
    depends_on: tuple[str, ...] = ()
    suggested_class: GeneratedCompletionLevel = "E3"


@dataclass(frozen=True, slots=True)
class MissingnessGraph:
    nodes: tuple[MissingnessNode, ...]
    edges: tuple[tuple[str, str], ...]

    @classmethod
    def from_nodes(cls, nodes: tuple[MissingnessNode, ...]) -> MissingnessGraph:
        known = {node.node_id for node in nodes}
        edges = tuple(
            sorted(
                (node.node_id, dependency)
                for node in nodes
                for dependency in node.depends_on
                if dependency in known
            )
        )
        return cls(nodes, edges)


@dataclass(frozen=True, slots=True)
class ConstraintSet:
    """Inputs for consistency checks; all fields are candidate evidence."""

    temporal: tuple[tuple[str, str], ...] = ()
    identity_keys: tuple[str, ...] = ()
    topology_nodes: tuple[str, ...] = ()
    topology_edges: tuple[tuple[str, str], ...] = ()
    ownership: tuple[tuple[str, str], ...] = ()
    knowledge_edges: tuple[tuple[str, str], ...] = ()
    observed_entities: tuple[str, ...] = ()
    roles: tuple[tuple[str, str], ...] = ()
    scenario_required: tuple[str, ...] = ()
    scenario_present: tuple[str, ...] = ()
    package_dependencies: tuple[str, ...] = ()
    package_lock: tuple[str, ...] = ()
    rights_ok: bool = True


@dataclass(frozen=True, slots=True)
class ConsistencyIssue:
    issue_id: str
    category: str
    detail: str
    blocking: bool = True


@dataclass(frozen=True, slots=True)
class ConsistencyReport:
    issues: tuple[ConsistencyIssue, ...]

    @property
    def ok(self) -> bool:
        return not any(issue.blocking for issue in self.issues)


@dataclass(frozen=True, slots=True)
class CompletionSolveResult:
    candidates: tuple[CompletionCandidate, ...]
    unknown: tuple[MissingnessNode, ...]
    consistency: ConsistencyReport
    graph: MissingnessGraph = MissingnessGraph((), ())
    uncertainty: float = 0.0


class ConsistencySolver:
    """Deterministic checks for temporal, identity, topology and policy gaps."""

    def solve(self, constraints: ConstraintSet) -> ConsistencyReport:
        issues: list[ConsistencyIssue] = []
        dates = [date for _event, date in constraints.temporal if date != "unknown"]
        if dates != sorted(dates):
            issues.append(
                ConsistencyIssue("temporal_order", "temporal", "event order is inconsistent")
            )
        if len(constraints.identity_keys) != len(set(constraints.identity_keys)):
            issues.append(
                ConsistencyIssue("identity_duplicate", "identity", "identity keys collide")
            )
        nodes = set(constraints.topology_nodes)
        if constraints.topology_edges:
            nodes.update(node for edge in constraints.topology_edges for node in edge)
            reachable = {constraints.topology_edges[0][0]}
            changed = True
            while changed:
                changed = False
                for source, target in constraints.topology_edges:
                    if source in reachable and target not in reachable:
                        reachable.add(target)
                        changed = True
            if nodes - reachable:
                issues.append(
                    ConsistencyIssue(
                        "topology_disconnected", "topology", "place graph is not connected"
                    )
                )
        owners: dict[str, str] = {}
        for object_key, owner in constraints.ownership:
            previous = owners.setdefault(object_key, owner)
            if previous != owner:
                issues.append(
                    ConsistencyIssue(
                        f"ownership_{object_key}", "ownership", "object has conflicting owners"
                    )
                )
        observed = set(constraints.observed_entities)
        if any(source not in observed for source, _target in constraints.knowledge_edges):
            issues.append(
                ConsistencyIssue(
                    "knowledge_leak", "knowledge", "knowledge edge lacks an observed source"
                )
            )
        if any(not organization or not role for organization, role in constraints.roles):
            issues.append(
                ConsistencyIssue("role_invalid", "organization", "role lacks organization")
            )
        missing_scenario = set(constraints.scenario_required) - set(constraints.scenario_present)
        if missing_scenario:
            issues.append(
                ConsistencyIssue(
                    "scenario_incomplete", "scenario", "scenario is missing required fields"
                )
            )
        if tuple(sorted(constraints.package_dependencies)) != tuple(
            sorted(constraints.package_lock)
        ):
            issues.append(
                ConsistencyIssue(
                    "package_dependency_mismatch", "package", "package dependency lock differs"
                )
            )
        if not constraints.rights_ok:
            issues.append(ConsistencyIssue("rights_block", "rights", "rights are incompatible"))
        return ConsistencyReport(tuple(issues))


class UncertaintyCalibration:
    """Conservative deterministic uncertainty proxy for completion planning."""

    def calibrate(
        self,
        candidates: tuple[CompletionCandidate, ...],
        unknown: tuple[MissingnessNode, ...],
        issues: tuple[ConsistencyIssue, ...],
    ) -> float:
        average = (
            sum(candidate.confidence for candidate in candidates) / len(candidates)
            if candidates
            else 0.0
        )
        penalty = 0.1 * len(unknown) + 0.1 * len(issues)
        return max(0.0, min(1.0, 1.0 - average + penalty))


class CompletionEngine:
    """Creates E1-E5 candidates and retains unknowns; never forges E0."""

    def solve(
        self,
        missing: tuple[MissingnessNode, ...],
        *,
        source_evidence: tuple[str, ...] = (),
        constraints: ConstraintSet | None = None,
    ) -> CompletionSolveResult:
        candidates: list[CompletionCandidate] = []
        unknown: list[MissingnessNode] = []
        for index, node in enumerate(missing, start=1):
            level: GeneratedCompletionLevel = (
                "E1" if len(node.source_refs) > 1 else node.suggested_class
            )
            refs = node.source_refs or source_evidence
            if level == "E1" and len(refs) < 2:
                unknown.append(node)
                continue
            candidates.append(
                CompletionCandidate(
                    completion_id=f"completion_{index}",
                    description=node.requirement,
                    completion_class=level,
                    support_refs=refs,
                    confidence=0.6 if level == "E1" else 0.3,
                )
            )
            if node.blocking and not refs:
                unknown.append(node)
        missing_issues = tuple(
            ConsistencyIssue(
                issue_id=f"missing_{node.node_id}",
                category=node.category if node.category != "generic" else "missingness",
                detail=node.requirement,
                blocking=node.blocking,
            )
            for node in unknown
        )
        constraint_report = ConsistencySolver().solve(constraints or ConstraintSet())
        issues = missing_issues + constraint_report.issues
        return CompletionSolveResult(
            tuple(candidates),
            tuple(unknown),
            ConsistencyReport(issues),
            MissingnessGraph.from_nodes(missing),
            UncertaintyCalibration().calibrate(tuple(candidates), tuple(unknown), issues),
        )

    def reject_e0_upgrade(self, current: CompletionLevel, requested: CompletionLevel) -> None:
        if current != "E0" and requested == "E0":
            raise ValueError("completion levels E1-E5 cannot be silently upgraded to E0")
