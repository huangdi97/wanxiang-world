"""RedChamber World Definition + Scenario assembly (G35I).

Assembles a v5.2 WorldPack Definition for a literary-historical world:
- literary_constitution(): a generic realistic/literary constitution (no
  omniscient future leak, character knowledge boundary, source gate before
  canon) with NO Red Chamber proper nouns;
- GenesisSpec + scenario point compiled from an approved source corpus;
- PackageManifest (kind=world) with constitution/genesis/evolution refs,
  dependency pins and content hash;
- WorldDefinition linked to constitution/genesis/package refs;
- HMAC signature over package_id:content_hash.

Real《红楼梦》 canon remains EXTERNAL_BLOCKED (G35A): this assembler compiles
mechanism world packs from an explicitly-labeled synthetic corpus and never
fabricates canon. Core packages contain no Red Chamber hardcoding.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass

from wanxiang_domain.constitution import ConstitutionManifest, ConstitutionVersion
from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import ConstitutionId, WorldDefinitionId
from wanxiang_domain.worldline import WorldDefinition

from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion
from wanxiang_substrate.sources.canon import ScenarioPoint, scenario_at
from wanxiang_substrate.sources.locator import segment_source


@dataclass(frozen=True, slots=True)
class GenesisSpec:
    """Birth content: source corpus + scenario + distilled refs + seed facts."""

    genesis_id: str
    name: str
    source_id: str
    scenario_ref: str
    distilled_refs: tuple[str, ...]
    initial_facts: tuple[str, ...]
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.genesis_id or not self.name or not self.source_id:
            raise ContractError("genesis spec requires id, name and source id")
        if not self.scenario_ref:
            raise ContractError("genesis spec requires a scenario ref")

    def compute_hash(self) -> str:
        payload = json.dumps(
            {
                "genesis_id": self.genesis_id,
                "name": self.name,
                "source_id": self.source_id,
                "scenario_ref": self.scenario_ref,
                "distilled_refs": sorted(self.distilled_refs),
                "initial_facts": sorted(self.initial_facts),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def with_hash(self) -> GenesisSpec:
        return GenesisSpec(
            genesis_id=self.genesis_id,
            name=self.name,
            source_id=self.source_id,
            scenario_ref=self.scenario_ref,
            distilled_refs=self.distilled_refs,
            initial_facts=self.initial_facts,
            content_hash=self.compute_hash(),
        )


@dataclass(frozen=True, slots=True)
class WorldPackSignature:
    """Deterministic HMAC signature over package_id:content_hash."""

    package_id: str
    content_hash: str
    digest: str

    def __post_init__(self) -> None:
        if not self.package_id or not self.content_hash or not self.digest:
            raise ContractError("signature requires package id, content hash and digest")


@dataclass(frozen=True, slots=True)
class AssembledWorldPack:
    """Result of assembly: definition + manifest + genesis + scenario + signature."""

    definition: WorldDefinition
    manifest: PackageManifest
    genesis: GenesisSpec
    scenario: ScenarioPoint
    signature: WorldPackSignature
    dependencies: tuple[str, ...] = ()


def literary_constitution() -> ConstitutionManifest:
    """Generic realistic/literary constitution (no Red Chamber proper nouns)."""
    return ConstitutionManifest(
        constitution_id=ConstitutionId("con_literary_historical"),
        version=ConstitutionVersion(1),
        name="Literary-Historical World Constitution",
        root_constraints=(
            "single_commit_boundary",
            "append_only_history",
            "replayable_history",
            "no_omniscient_future_leak",
            "character_knowledge_boundary",
            "source_gate_before_canon",
            "world_policy_cannot_modify_platform",
        ),
        mutable_law_layers=("ontology", "law", "ritual", "etiquette"),
        rights_ref="worldpack:literary-historical",
        evolution_policy="distillation_review",
    ).with_hash()


def sign_world_pack(manifest: PackageManifest, secret: str) -> WorldPackSignature:
    digest = hmac.new(
        secret.encode(),
        f"{manifest.package_id}:{manifest.content_hash}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return WorldPackSignature(
        package_id=manifest.package_id,
        content_hash=manifest.content_hash,
        digest=digest,
    )


def verify_world_pack(
    signature: WorldPackSignature, manifest: PackageManifest, secret: str
) -> bool:
    if manifest.content_hash != signature.content_hash:
        return False
    expected = sign_world_pack(manifest, secret)
    return hmac.compare_digest(signature.digest, expected.digest)


class WorldPackAssembler:
    """Compile a v5.2 WorldPack Definition + scenario from an approved corpus.

    Pure assembly: no Commit Authority writes, no world instantiation. The
    caller must have passed the SourceGate (G04B) for the corpus before use.
    """

    def __init__(self, *, secret: str = "local-dev-secret") -> None:
        self._secret = secret

    def assemble(
        self,
        *,
        definition_id: WorldDefinitionId,
        name: str,
        source_id: str,
        text: str,
        scenario_chapter: str,
        genesis: GenesisSpec,
        dependencies: tuple[str, ...] = ("narrative_domain",),
        lineage_ref: str | None = None,
    ) -> AssembledWorldPack:
        """Assemble the world pack; re-running on same inputs is identical."""
        scenario = scenario_at(
            segment_source(source_id, text),
            chapter=scenario_chapter,
            scenario_id=genesis.genesis_id,
        )
        constitution = literary_constitution()
        manifest = PackageManifest(
            package_id=definition_id.value,
            kind="world",
            version=SemanticVersion(1, 0, 0),
            name=name,
            dependencies=tuple((dep, ">=1.0.0") for dep in sorted(dependencies)),
            executable_trust="untrusted",
            constitution_ref=constitution.constitution_id.value,
            genesis_ref=genesis.genesis_id,
            evolution_policy_ref=constitution.evolution_policy,
            lineage_ref=lineage_ref,
        ).with_hash()
        definition = WorldDefinition(
            definition_id=definition_id,
            version=1,
            name=name,
            constitution_ref=constitution.constitution_id.value,
            genesis_ref=genesis.genesis_id,
            package_ref=f"pack://{manifest.package_id}@1.0.0",
        ).with_hash()
        return AssembledWorldPack(
            definition=definition,
            manifest=manifest,
            genesis=genesis.with_hash(),
            scenario=scenario,
            signature=sign_world_pack(manifest, self._secret),
            dependencies=dependencies,
        )
