"""M79 binary EPUB entrypoints share the production authoring chain."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.authoring.local_semantic_provider import LocalSemanticProvider
from wanxiang_substrate.authoring.pipeline import SourceToDraftPipeline
from wanxiang_substrate.authoring.providers import ProviderRouter
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord


def _epub() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?><container '
            'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="OPS/book.opf" '
            'media-type="application/oebps-package+xml"/></rootfiles></container>',
        )
        archive.writestr(
            "OPS/book.opf",
            '<?xml version="1.0"?><package '
            'xmlns="http://www.idpf.org/2007/opf" version="3.0">'
            '<manifest><item id="c1" href="text/chapter-1.xhtml" '
            'media-type="application/xhtml+xml"/><item id="c2" '
            'href="text/chapter-2.xhtml" media-type="application/xhtml+xml"/></manifest>'
            '<spine><itemref idref="c1"/><itemref idref="c2"/></spine></package>',
        )
        archive.writestr(
            "OPS/text/chapter-1.xhtml",
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>第一章</title></head>'
            "<body><h1>第一章 起因</h1><p>张三来到北京市，李四说。</p>"
            "<p>规则：重要记录不得外传。</p></body></html>",
        )
        archive.writestr(
            "OPS/text/chapter-2.xhtml",
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>第二章</title></head>'
            "<body><h1>第二章 关系</h1><p>张三和李四在北京市见面。</p>"
            "<p>张三说，李四说。</p><p>张三决定调查。</p></body></html>",
        )
    return buffer.getvalue()


def _record(blob: bytes, source_id: str) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        kind="epub",
        content_hash=hashlib.sha256(blob).hexdigest(),
        content_ref=f"memory://{source_id}",
        stage="E3",
        rights=RightsEnvelope(
            owner="m79-fixture",
            usage="private-analysis",
            approved=True,
            package_inclusion_allowed=True,
        ),
        payload="",
        provenance="synthetic:m79-epub-entrypoints",
        access="private",
    )


@pytest.mark.integration
def test_binary_epub_preserves_spine_href_locators_and_candidates() -> None:
    blob = _epub()
    record = _record(blob, "m79_epub_pipeline")
    pipeline = SourceToDraftPipeline(
        blob_loader=lambda source: blob if source.source_id == record.source_id else None,
        providers=ProviderRouter((LocalSemanticProvider(),)),
    )
    build = pipeline.run(
        (record,),
        draft_id="wd_m79_epub_pipeline",
        use_semantic_provider=True,
    )
    assert build.candidates
    assert any("spine=1;href=OPS/text/chapter-1.xhtml" in s.locator.ref for s in build.segments)
    assert any("spine=2;href=OPS/text/chapter-2.xhtml" in s.locator.ref for s in build.segments)
    assert all(candidate.source_refs for candidate in build.candidates)
    assert all(
        "href=OPS/text/" in ref
        for candidate in build.candidates
        for ref in candidate.source_refs
        if ref.startswith("epub://")
    )


@pytest.mark.integration
def test_api_base64_epub_reaches_package_and_preview() -> None:
    blob = _epub()
    client: Any = TestClient(create_app(build_reference_runtime()))
    response = client.post(
        "/studio/one-click",
        json={
            "job_id": "job_m79_epub_api",
            "profile": "book",
            "semantic_provider": "local",
            "sources": [
                {
                    "source_id": "m79_epub_api",
                    "kind": "epub",
                    "content": "",
                    "content_base64": base64.b64encode(blob).decode("ascii"),
                    "stage": "E3",
                    "rights_approved": True,
                    "package_inclusion_allowed": True,
                    "access": "private",
                }
            ],
        },
    )
    assert response.status_code == 201
    draft = client.get("/studio/jobs/job_m79_epub_api/draft").json()
    assert draft["candidates"]
    assert any(
        "href=OPS/text/" in ref for item in draft["candidates"] for ref in item["source_refs"]
    )
    package = client.post("/studio/jobs/job_m79_epub_api/build")
    preview = client.post("/studio/jobs/job_m79_epub_api/preview")
    assert package.status_code == 200
    assert preview.status_code == 200
    assert client.get("/studio/ui").status_code == 200
    assert "content_base64" in client.get("/studio/ui").text


@pytest.mark.integration
def test_cli_binary_epub_reaches_living_world() -> None:
    source = Path.cwd() / f".m79-epub-{os.getpid()}.epub"
    source.write_bytes(_epub())
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(Path("scripts/wxworld.py")),
                "reference",
                "--profile",
                "book",
                "--kind",
                "epub",
                "--file",
                str(source),
                "--job-id",
                "job_m79_epub_cli",
                "--semantic-provider",
                "local",
                "--publish",
                "--instantiate",
                "--worldness",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        source.unlink(missing_ok=True)
    result = json.loads(completed.stdout)
    assert result["published"] is True
    assert result["living"]["instance_id"]
    assert result["worldness"]["passed"] is True
