"""Round-trippable JSON Pointer and CSV cell evidence (M83/G86B)."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from typing import cast

from wanxiang_substrate.parsing.segment import StableLocator

type JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


@dataclass(frozen=True, slots=True)
class StructuredEvidence:
    locator: StableLocator
    value: str


def json_pointer_locator(source_id: str, pointer: str) -> StableLocator:
    """Create a standard JSON Pointer locator without copying source content."""
    if not pointer.startswith("/") and pointer != "":
        raise ValueError("JSON Pointer must be empty or start with '/'")
    return StableLocator(source_id, "json", "record", pointer or "/")


def csv_cell_locator(source_id: str, row: int, column: int) -> StableLocator:
    """Create a one-based CSV row/column locator."""
    if row < 1 or column < 1:
        raise ValueError("CSV row and column are one-based positive integers")
    return StableLocator(source_id, "csv", "column", f"row_{row}/column_{column}")


def resolve_json_pointer(payload: str, pointer: str) -> str:
    """Resolve a JSON Pointer and return a canonical scalar/object value."""
    value: JsonValue = cast(JsonValue, json.loads(payload))
    if pointer not in ("", "/"):
        for token in pointer[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(value, list):
                value = value[int(token)]
            elif isinstance(value, dict):
                value = value[token]
            else:
                raise KeyError(pointer)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def resolve_csv_cell(payload: str, row: int, column: int) -> str:
    """Resolve one one-based CSV cell, preserving the source row/column."""
    rows = list(csv.reader(io.StringIO(payload)))
    try:
        return rows[row - 1][column - 1]
    except (IndexError, ValueError) as exc:
        raise KeyError(f"row={row},column={column}") from exc


def json_leaf_evidence(source_id: str, payload: str) -> tuple[StructuredEvidence, ...]:
    """Enumerate JSON leaf values as anonymized evidence handles."""
    root: JsonValue = cast(JsonValue, json.loads(payload))
    found: list[StructuredEvidence] = []

    def visit(value: JsonValue, pointer: str) -> None:
        if isinstance(value, dict):
            for key in sorted(value):
                escaped = str(key).replace("~", "~0").replace("/", "~1")
                visit(value[key], f"{pointer}/{escaped}")
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{pointer}/{index}")
            return
        found.append(StructuredEvidence(json_pointer_locator(source_id, pointer), str(value)))

    visit(root, "")
    return tuple(found)


__all__ = [
    "StructuredEvidence",
    "csv_cell_locator",
    "json_leaf_evidence",
    "json_pointer_locator",
    "resolve_csv_cell",
    "resolve_json_pointer",
]
