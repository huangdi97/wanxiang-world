"""Missingness, consistency, and honest completion solving (M64)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.completion.candidates import CompletionCandidate

CompletionLevel = Literal["E0", "E1", "E2", "E3", "E4", "E5"]


@dataclass(frozen=True, slots=True)
class MissingnessNode:
    node_id: str
    requirement: str
    blocking: bool
    source_refs: tuple[str, ...] = ()


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


class CompletionEngine:
    """Creates E1-E5 candidates and retains unknowns; never forges E0."""

    def solve(
        self,
        missing: tuple[MissingnessNode, ...],
        *,
        source_evidence: tuple[str, ...] = (),
    ) -> CompletionSolveResult:
        candidates: list[CompletionCandidate] = []
        unknown: list[MissingnessNode] = []
        for index, node in enumerate(missing, start=1):
            level: CompletionLevel = (
                "E1" if node.source_refs and len(node.source_refs) > 1 else "E3"
            )
            refs = node.source_refs or source_evidence
            if level == "E1" and not refs:
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
        issues = tuple(
            ConsistencyIssue(
                issue_id=f"missing_{node.node_id}",
                category="missingness",
                detail=node.requirement,
                blocking=node.blocking,
            )
            for node in unknown
        )
        return CompletionSolveResult(tuple(candidates), tuple(unknown), ConsistencyReport(issues))

    def reject_e0_upgrade(self, current: CompletionLevel, requested: CompletionLevel) -> None:
        if current != "E0" and requested == "E0":
            raise ValueError("completion levels E1-E5 cannot be silently upgraded to E0")
