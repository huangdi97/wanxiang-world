"""G35I: RedChamber World Definition + Scenario assembly (mechanism; synthetic).

Synthetic corpus ONLY - never real《红楼梦》canon. Real text remains
EXTERNAL_BLOCKED (G35A); the assembler compiles a mechanism world pack and
never fabricates canon.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from wanxiang_domain.ids import WorldDefinitionId, WorldInstanceId, WorldlineId
from wanxiang_domain.worldline import InstanceIdentity
from wanxiang_substrate.packages.install import PackageInstaller, export_install
from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry
from wanxiang_substrate.worldpack import (
    AssembledWorldPack,
    GenesisSpec,
    WorldPackAssembler,
    literary_constitution,
    verify_world_pack,
)

# Synthetic corpus ONLY - never real《红楼梦》canon text.
SYNTHETIC = "第一回\nc1 进府。c2 居园。\n第二回\nc3 探望 c2。\n"

FORBIDDEN_RED_CHAMBER_NAMES = ("林黛玉", "贾宝玉", "潇湘馆", "怡红院", "红楼梦", "贾府")


def _genesis() -> GenesisSpec:
    return GenesisSpec(
        genesis_id="gen_rc001",
        name="RedChamber RC-001 Synthetic Genesis",
        source_id="src_rc_synth",
        scenario_ref="第二回",
        distilled_refs=("identity:c1", "identity:c2", "place:garden"),
        initial_facts=("c1 进府", "c2 居园"),
    ).with_hash()


def _assemble() -> AssembledWorldPack:
    return WorldPackAssembler(secret="test-secret").assemble(
        definition_id=WorldDefinitionId("wd_rc001"),
        name="RedChamber RC-001 (synthetic mechanism world)",
        source_id="src_rc_synth",
        text=SYNTHETIC,
        scenario_chapter="第二回",
        genesis=_genesis(),
        dependencies=("narrative_domain",),
        lineage_ref="lineage://rc001",
    )


@pytest.mark.unit
def test_assemble_world_pack_with_refs_hash_and_signature() -> None:
    packed = _assemble()
    assert packed.manifest.kind == "world"
    assert packed.manifest.constitution_ref == "con_literary_historical"
    assert packed.manifest.genesis_ref == "gen_rc001"
    assert packed.manifest.evolution_policy_ref == "distillation_review"
    assert packed.manifest.lineage_ref == "lineage://rc001"
    assert packed.manifest.content_hash
    assert packed.definition.constitution_ref == packed.manifest.constitution_ref
    assert packed.definition.genesis_ref == packed.manifest.genesis_ref
    assert packed.definition.content_hash
    assert packed.genesis.content_hash
    assert verify_world_pack(packed.signature, packed.manifest, "test-secret") is True


@pytest.mark.unit
def test_validate_install_export_import() -> None:
    packed = _assemble()
    registry = InMemoryPackageRegistry()
    registry.register(packed.manifest)
    registry.register(
        PackageManifest(
            package_id="narrative_domain",
            kind="domain",
            version=SemanticVersion(1, 0, 0),
            name="narrative domain",
            executable_trust="untrusted",
        ).with_hash()
    )
    record = PackageInstaller().install(
        registry,
        packed.manifest.package_id,
        packed.manifest.version,
        install_id="install_rc001",
        rights_refs=("worldpack:literary-historical",),
        evidence_refs=packed.genesis.distilled_refs,
    )
    assert record.package_id == "wd_rc001"
    exported = export_install(record)
    assert exported["lock_hash"] == record.lock_hash
    # Import = re-register + resolve round-trip keeps the same lock hash.
    imported = InMemoryPackageRegistry()
    imported.register(packed.manifest)
    imported.register(
        PackageManifest(
            package_id="narrative_domain",
            kind="domain",
            version=SemanticVersion(1, 0, 0),
            name="narrative domain",
            executable_trust="untrusted",
        ).with_hash()
    )
    reimported = PackageInstaller().install(
        imported,
        packed.manifest.package_id,
        packed.manifest.version,
        install_id="install_rc001_import",
    )
    assert reimported.lock_hash == record.lock_hash


@pytest.mark.unit
def test_instantiation_dry_run() -> None:
    packed = _assemble()
    # Dry-run instance identity: refs resolve; NO events committed, no
    # Commit Authority touched, no world loop started.
    identity = InstanceIdentity(
        instance_id=WorldInstanceId("wld_rc001_dryrun"),
        worldline_id=WorldlineId("wl_rc001"),
        definition_ref=packed.definition.definition_id.value,
        genesis_ref=packed.genesis.genesis_id,
        constitution_ref=packed.definition.constitution_ref,
        runtime_ref="runtime:deterministic",
    )
    assert identity.definition_ref == "wd_rc001"
    assert identity.genesis_ref == "gen_rc001"
    assert identity.constitution_ref == "con_literary_historical"


@pytest.mark.unit
def test_no_core_hardcode() -> None:
    root = Path(__file__).resolve().parents[2]
    core_roots = (
        root / "packages/runtime",
        root / "packages/domain",
        root / "packages/application",
        root / "packages/persistence",
    )
    haystack = "".join(
        p.read_text(encoding="utf-8") for base in core_roots for p in base.rglob("*.py")
    )
    forbidden = [name for name in FORBIDDEN_RED_CHAMBER_NAMES if name in haystack]
    assert "red_chamber" not in haystack
    assert forbidden == [], f"core packages must not hardcode Red Chamber content: {forbidden}"


@pytest.mark.unit
def test_literary_constitution_is_generic() -> None:
    constitution = literary_constitution()
    assert "no_omniscient_future_leak" in constitution.root_constraints
    assert "character_knowledge_boundary" in constitution.root_constraints
    assert "source_gate_before_canon" in constitution.root_constraints
    assert "ritual" in constitution.mutable_law_layers
    text = str(constitution.to_primitive())
    assert not any(name in text for name in FORBIDDEN_RED_CHAMBER_NAMES)


@pytest.mark.unit
def test_scenario_compiled_from_source() -> None:
    packed = _assemble()
    assert packed.scenario.time_ref == "第二回"
    assert packed.scenario.source_id == "src_rc_synth"


@pytest.mark.unit
def test_tampered_manifest_fails_verification() -> None:
    packed = _assemble()
    tampered = PackageManifest(
        package_id=packed.manifest.package_id,
        kind=packed.manifest.kind,
        version=packed.manifest.version,
        name="tampered name",
        dependencies=packed.manifest.dependencies,
        executable_trust=packed.manifest.executable_trust,
        constitution_ref=packed.manifest.constitution_ref,
        genesis_ref=packed.manifest.genesis_ref,
        evolution_policy_ref=packed.manifest.evolution_policy_ref,
        lineage_ref=packed.manifest.lineage_ref,
    ).with_hash()
    assert verify_world_pack(packed.signature, tampered, "test-secret") is False


@pytest.mark.unit
def test_assembly_is_deterministic() -> None:
    first = _assemble()
    second = _assemble()
    assert first.manifest == second.manifest
    assert first.definition == second.definition
    assert first.signature == second.signature
