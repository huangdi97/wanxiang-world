"""G17D: third-party package conformance & certification harness.

- A reference external package passes certification (static + runtime + versions).
- Known-bad fixtures fail for expected reasons.
- Certification output includes runtime/SDK/package versions.
"""

from __future__ import annotations

import pathlib
import uuid
from collections.abc import Iterator

import pytest
from scripts.wxpack import certify, scaffold

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TMP = ROOT / "tests" / "_arch_tmp"


@pytest.fixture
def workdir() -> Iterator[pathlib.Path]:
    d = TMP / uuid.uuid4().hex
    d.mkdir(parents=True, exist_ok=True)
    yield d
    for p in d.rglob("*"):
        if p.is_file():
            try:  # noqa: SIM105
                p.unlink()
            except OSError:
                pass
    try:  # noqa: SIM105
        d.rmdir()
    except OSError:
        pass


def test_reference_package_passes_certification(workdir: pathlib.Path) -> None:
    scaffold(workdir, "cert-domain", "domain", "Cert Domain")
    report = certify(workdir, "cert-domain")
    assert report["ok"] is True
    assert report["package_id"] == "cert-domain"
    assert report["runtime_version"] == 1
    assert report["schema_version"] == 1
    assert report["platform"]
    names = [c["name"] for c in report["checks"]]
    assert "static_validation" in names
    assert "forbidden_imports" in names
    assert "runtime_install" in names
    assert all(c["ok"] for c in report["checks"])


def test_known_bad_fixture_fails_for_expected_reasons(workdir: pathlib.Path) -> None:
    scaffold(workdir, "bad-domain", "domain", "Bad Domain")
    module = workdir / "bad-domain" / "bad_domain.py"
    text = module.read_text(encoding="utf-8")
    # Insert a syntactically valid forbidden import after the __future__ line.
    module.write_text(
        text.replace(
            "from __future__ import annotations",
            "from __future__ import annotations\nimport wanxiang_persistence",
        ),
        encoding="utf-8",
    )
    report = certify(workdir, "bad-domain")
    assert report["ok"] is False
    by_name = {c["name"]: c for c in report["checks"]}
    assert by_name["forbidden_imports"]["ok"] is False
    assert "wanxiang_persistence" in by_name["forbidden_imports"]["detail"]
