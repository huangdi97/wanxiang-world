"""IIIF ingest adapter (G10A).

Parses IIIF Manifests (Canvas/AnnotationPage/Annotation bodies, image/audio/
video service refs, rights/attribution) into a local metadata cache with
provenance. Real IIIF endpoints are EXTERNAL_BLOCKED; synthetic manifests are
fixtures.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import cast

from wanxiang_substrate.heritage.errors import IiifParseError


@dataclass(frozen=True, slots=True)
class IiifCanvas:
    canvas_id: str
    label: str
    service_refs: tuple[str, ...] = ()
    annotation_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IiifManifest:
    manifest_id: str
    label: str
    rights: str = ""
    attribution: str = ""
    canvases: tuple[IiifCanvas, ...] = ()
    external_ids: tuple[str, ...] = ()


class IiifIngester:
    """Parses IIIF manifest JSON into a local metadata cache."""

    def __init__(self) -> None:
        self._cache: dict[str, IiifManifest] = {}

    def ingest(self, manifest_json: str) -> IiifManifest:
        try:
            decoded = json.loads(manifest_json)
        except ValueError as exc:
            raise IiifParseError("manifest is not valid JSON") from exc
        if not isinstance(decoded, dict):
            raise IiifParseError("manifest must be an object")
        data: dict[str, object] = cast(dict[str, object], decoded)
        if not data.get("id") or not data.get("label"):
            raise IiifParseError("manifest requires id and label")
        canvases: list[IiifCanvas] = []
        for canvas_data in _list_value(_first(data, "items", "sequences")):
            if not isinstance(canvas_data, dict):
                continue
            canvas_map: dict[str, object] = cast(dict[str, object], canvas_data)
            canvas_id = str(canvas_map.get("id") or "")
            if not canvas_id:
                continue
            label = _label(canvas_map.get("label"))
            service_refs: list[str] = []
            annotation_refs: list[str] = []
            for item in _list_value(canvas_map.get("items")):
                if not isinstance(item, dict):
                    continue
                item_map: dict[str, object] = cast(dict[str, object], item)
                body = item_map.get("body")
                if isinstance(body, dict):
                    body_map: dict[str, object] = cast(dict[str, object], body)
                    body_id = body_map.get("id")
                    if isinstance(body_id, str):
                        service_refs.append(body_id)
                item_id = item_map.get("id")
                if isinstance(item_id, str):
                    annotation_refs.append(item_id)
            canvases.append(
                IiifCanvas(
                    canvas_id=canvas_id,
                    label=label,
                    service_refs=tuple(service_refs),
                    annotation_refs=tuple(annotation_refs),
                )
            )
        external: list[str] = []
        for ext in _list_value(data.get("seeAlso")):
            if isinstance(ext, str):
                external.append(ext)
        manifest = IiifManifest(
            manifest_id=str(data["id"]),
            label=_label(data.get("label")),
            rights=str(data.get("rights") or ""),
            attribution=str(data.get("attribution") or ""),
            canvases=tuple(canvases),
            external_ids=tuple(external),
        )
        self._cache[manifest.manifest_id] = manifest
        return manifest

    def get(self, manifest_id: str) -> IiifManifest | None:
        return self._cache.get(manifest_id)


def _first(data: dict[str, object], *keys: str) -> object:
    """Return the first present key value (deterministic)."""
    for key in keys:
        value = data.get(key)
        if value is not None:
            return value
    return {}


def _list_value(value: object) -> list[object]:
    if isinstance(value, list):
        items = cast(list[object], value)
        return list(items)
    return [value]


def _label(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        label_map: dict[str, object] = cast(dict[str, object], value)
        for key in ("en", "none"):
            values = label_map.get(key)
            if isinstance(values, list) and values and isinstance(values[0], str):
                return values[0]
            if isinstance(values, str):
                return values
    return ""
