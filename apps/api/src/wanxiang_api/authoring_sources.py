"""Transport models for text and private binary authoring sources."""

from __future__ import annotations

import base64
import binascii
import hashlib

from pydantic import BaseModel, Field, model_validator
from wanxiang_substrate.authoring.service import AuthoringService
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


class SourceInput(BaseModel):
    source_id: str
    kind: str
    content: str = ""
    content_base64: str | None = None
    version: str = "1"
    stage: str = "E0"
    owner: str = "user"
    usage: str = "reference"
    rights_approved: bool = False
    access: str = "private"
    reliability: float = Field(default=1.0, ge=0.0, le=1.0)
    provenance: str = "studio"
    ingest_allowed: bool = True
    private_analysis_allowed: bool = True
    external_model_processing_allowed: bool = False
    package_inclusion_allowed: bool | None = None
    public_export_allowed: bool = False
    training_allowed: bool = False

    @model_validator(mode="after")
    def validate_payload_encoding(self) -> SourceInput:
        self.raw_blob()
        return self

    def raw_blob(self) -> bytes | None:
        if self.content_base64 is None:
            return None
        if self.content:
            raise ValueError("source input must use content or content_base64, not both")
        try:
            return base64.b64decode(self.content_base64, validate=True)
        except (ValueError, binascii.Error):
            raise ValueError("content_base64 is not valid base64") from None

    def record(self) -> SourceRecord:
        raw = self.raw_blob()
        content_hash = (
            hashlib.sha256(raw).hexdigest() if raw is not None else payload_hash(self.content)
        )
        return SourceRecord(
            source_id=self.source_id,
            kind=self.kind,
            content_hash=content_hash,
            content_ref=f"memory://{self.source_id}",
            stage=self.stage,  # type: ignore[arg-type]
            rights=RightsEnvelope(
                owner=self.owner,
                usage=self.usage,
                approved=self.rights_approved,
                ingest_allowed=self.ingest_allowed,
                private_analysis_allowed=self.private_analysis_allowed,
                external_model_processing_allowed=self.external_model_processing_allowed,
                package_inclusion_allowed=self.package_inclusion_allowed,
                public_export_allowed=self.public_export_allowed,
                training_allowed=self.training_allowed,
            ),
            payload=self.content if raw is None else "",
            provenance=self.provenance,
            version=self.version,
            access=self.access,  # type: ignore[arg-type]
            reliability=self.reliability,
        )


def source_records(
    service: AuthoringService, sources: list[SourceInput]
) -> tuple[SourceRecord, ...]:
    records: list[SourceRecord] = []
    for source in sources:
        raw = source.raw_blob()
        if raw is not None:
            service.attach_source_blob(source.source_id, raw)
        records.append(source.record())
    return tuple(records)
