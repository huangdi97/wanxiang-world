"""World compiler boundary (G60A).

The compiler consumes ONLY reviewed WorldDrafts (status READY_TO_COMPILE or
later) and pins every input revision/version in the output. Drafts with
unresolved conflicts/rights or a blocked coverage gap are refused. The
compiler proposes a compiled package; it never writes Canon.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.draft.model import WorldDraft

COMPILABLE_STATUSES = ("READY_TO_COMPILE", "PREVIEWABLE", "PUBLISHABLE")


@dataclass(frozen=True, slots=True)
class CompilerInput:
    """Pinned inputs the compiler accepts."""

    draft: WorldDraft
    draft_revision: int
    source_versions: tuple[tuple[str, str], ...]
    domain_versions: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if self.draft.revision != self.draft_revision:
            raise ContractError(
                f"draft revision mismatch: {self.draft.revision} != {self.draft_revision}"
            )
        if not self.source_versions:
            raise ContractError("compiler requires at least one pinned source")
        if len(dict(self.source_versions)) != len(self.source_versions):
            raise ContractError("compiler source pins must not contain duplicates")
        if len(dict(self.domain_versions)) != len(self.domain_versions):
            raise ContractError("compiler domain pins must not contain duplicates")


@dataclass(frozen=True, slots=True)
class CompileOutcome:
    draft_id: str
    pinned_revision: int
    ok: bool
    reasons: tuple[str, ...]


class CompilerBoundary:
    """Gate: only reviewed, pinned drafts may be compiled."""

    def can_compile(self, draft: WorldDraft) -> tuple[bool, str]:
        if draft.status not in COMPILABLE_STATUSES:
            return False, f"draft status {draft.status} is not compilable"
        if draft.unresolved_conflicts:
            return False, "draft has unresolved conflicts"
        if draft.unresolved_rights:
            return False, "draft has unresolved rights"
        if draft.coverage <= 0.0:
            return False, "draft has zero coverage"
        return True, ""

    def check(self, inputs: CompilerInput) -> CompileOutcome:
        ok, reason = self.can_compile(inputs.draft)
        reasons: list[str] = []
        if not ok:
            reasons.append(reason)
        # Pin everything: source versions must match the draft record, and each
        # selected domain must carry an explicit version on the compile input.
        pinned_sources = dict(inputs.draft.source_versions)
        requested_sources = dict(inputs.source_versions)
        if requested_sources != pinned_sources:
            missing = sorted(set(pinned_sources) - set(requested_sources))
            extra = sorted(set(requested_sources) - set(pinned_sources))
            if missing:
                reasons.append(f"missing source pins: {','.join(missing)}")
            if extra:
                reasons.append(f"unexpected source pins: {','.join(extra)}")
            for source_id in sorted(set(pinned_sources) & set(requested_sources)):
                if pinned_sources[source_id] != requested_sources[source_id]:
                    reasons.append(f"source {source_id} version changed")
        domain_versions = dict(inputs.domain_versions)
        for domain_id in inputs.draft.selected_domains:
            if domain_id not in domain_versions:
                reasons.append(f"domain {domain_id} has no pinned version")
        if tuple(sorted(inputs.draft.source_refs)) != tuple(sorted(requested_sources)):
            reasons.append("source pins do not match draft source references")
        return CompileOutcome(
            draft_id=inputs.draft.draft_id,
            pinned_revision=inputs.draft_revision,
            ok=not reasons,
            reasons=tuple(reasons),
        )
