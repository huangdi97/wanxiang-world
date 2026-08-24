"""G73D: public Source -> Living World documentation contracts."""

from __future__ import annotations

import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOC_ROOT = ROOT / "docs" / "source_to_living_world"


@pytest.mark.integration
def test_public_guides_exist_and_preserve_boundaries() -> None:
    names = (
        "QUICKSTART.md",
        "PROVIDER_SDK.md",
        "DOMAIN_EXTENSION.md",
        "SOURCE_RIGHTS_GUIDE.md",
    )
    text = "\n".join((DOC_ROOT / name).read_text(encoding="utf-8") for name in names)
    assert "scripts/wxworld.py reference" in text
    assert "/studio/one-click" in text
    assert "ProviderProposal" in text
    assert "DomainRegistry" in text
    assert "RightsGate" in text
    assert "OCR_REQUIRED" in text
    assert "Canonical World State" in text
    assert "Commit Authority" in text


@pytest.mark.integration
def test_provider_and_rights_examples_use_existing_ports() -> None:
    from wanxiang_substrate.authoring.providers import (
        ProviderCapability,
        ProviderRouter,
        ReferenceProvider,
    )
    from wanxiang_substrate.sources.errors import OcrRequired

    provider = ReferenceProvider(
        ProviderCapability("docs-reference", "linking", "1", deterministic=True)
    )
    proposals = ProviderRouter((provider,)).propose("linking", ("source://docs",), "data")
    assert proposals and proposals[0].kind == "candidate"
    assert not hasattr(proposals[0], "commit")
    with pytest.raises(OcrRequired, match="OCR_REQUIRED"):
        ProviderRouter().require("ocr", ("source://scan",))


@pytest.mark.integration
def test_domain_extension_registers_with_single_registry() -> None:
    from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry

    registry = DomainRegistry()
    domain = DomainCapability("docs-domain", "Docs Domain", "1.0.0", ("demo",))
    assert registry.register(domain) is domain
    assert registry.require("docs-domain") is domain
