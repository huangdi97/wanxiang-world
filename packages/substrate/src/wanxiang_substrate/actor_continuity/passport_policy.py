"""Deterministic, privacy-aware interworld passport translation policy."""

from __future__ import annotations

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.actor_continuity.passport_model import (
    CharacterPassport,
    PassportDecision,
    PassportEntry,
    PassportTranslationContext,
    PassportTranslationProposal,
)


class DeterministicPassportTranslationPolicy:
    """Accept only entries the target world explicitly declares possible."""

    def __init__(self, ref: str = "passport-reference-v1") -> None:
        if not ref.strip():
            raise ContractError("passport policy ref cannot be blank")
        self._ref = ref

    def propose(
        self,
        passport: CharacterPassport,
        context: PassportTranslationContext,
    ) -> PassportTranslationProposal:
        if context.requester_id != passport.owner_id and not context.admin:
            raise ContractError("passport translation is owner-restricted")
        entries = passport.visible_entries(context.requester_id, admin=context.admin)
        decisions = tuple(
            self._decide(passport, entry, context)
            for entry in sorted(entries, key=lambda item: item.entry_id)
        )
        return PassportTranslationProposal(
            passport_id=passport.character_id,
            target_world_ref=context.target_world_ref,
            policy_ref=self._ref,
            decisions=decisions,
        )

    def _decide(
        self,
        passport: CharacterPassport,
        entry: PassportEntry,
        context: PassportTranslationContext,
    ) -> PassportDecision:
        if passport.compatible_profile_ids and (
            context.target_profile_id not in passport.compatible_profile_ids
        ):
            return PassportDecision(entry.entry_id, "rejected", "target profile is incompatible")
        if entry.portability == "blocked":
            return PassportDecision(entry.entry_id, "rejected", "entry is blocked by origin policy")
        if entry.kind not in context.supported_kinds:
            return PassportDecision(
                entry.entry_id, "rejected", "target world does not support this kind"
            )
        if entry.ref not in context.available_refs:
            return PassportDecision(entry.entry_id, "rejected", "target world lacks this ref")
        if entry.portability == "conditional":
            if not set(entry.compatibility_tags) & set(context.compatibility_tags):
                return PassportDecision(
                    entry.entry_id, "rejected", "compatibility tags do not match"
                )
            return PassportDecision(
                entry.entry_id, "conditional", "target compatibility is explicit"
            )
        return PassportDecision(entry.entry_id, "accepted", "target capability is explicit")


PassportTranslationPolicy = DeterministicPassportTranslationPolicy
