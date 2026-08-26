"""Validation helpers shared by the experiment registry contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import isfinite
from typing import cast

from wanxiang_domain.errors import ContractError


def ref(value: object, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ContractError(f"{name} must be a non-empty reference")
    if any(char.isspace() for char in value):
        raise ContractError(f"{name} must not contain whitespace")
    return value


def integer(value: object, name: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ContractError(f"{name} must be an integer >= {minimum}")
    return value


def sequence(value: object, name: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise ContractError(f"{name} must be a list")
    return tuple(cast(list[object] | tuple[object, ...], value))


def names(values: Sequence[object], name: str) -> tuple[str, ...]:
    result = tuple(ref(value, f"{name} item") for value in values)
    if len(result) != len(set(result)):
        raise ContractError(f"{name} must not contain duplicates")
    return tuple(sorted(result))


def pairs(values: Sequence[object], name: str) -> tuple[tuple[str, str], ...]:
    result: list[tuple[str, str]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError(f"{name} items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError(f"{name} items must be pairs")
        result.append((ref(pair[0], f"{name} key"), ref(pair[1], f"{name} value")))
    if len({key for key, _value in result}) != len(result):
        raise ContractError(f"{name} keys must be unique")
    return tuple(sorted(result))


def json_value(value: object, name: str) -> object:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not isfinite(value):
            raise ContractError(f"{name} contains a non-finite number")
        return value
    if isinstance(value, (list, tuple)):
        values = cast(list[object] | tuple[object, ...], value)
        return tuple(json_value(item, name) for item in values)
    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, object], value)
        items = sorted(mapping.items(), key=lambda pair: str(pair[0]))
        return tuple((ref(key, f"{name} key"), json_value(item, name)) for key, item in items)
    raise ContractError(f"{name} contains a non-serializable value")


def parameters(values: Sequence[object], name: str) -> tuple[tuple[str, object], ...]:
    result: list[tuple[str, object]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError(f"{name} items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError(f"{name} items must be pairs")
        result.append((ref(pair[0], f"{name} key"), json_value(pair[1], f"{name} value")))
    if len({key for key, _value in result}) != len(result):
        raise ContractError(f"{name} keys must be unique")
    return tuple(sorted(result))


def variants(values: Sequence[object], name: str) -> tuple[tuple[str, object], ...]:
    result: list[tuple[str, object]] = []
    for item in values:
        if not isinstance(item, (list, tuple)):
            raise ContractError(f"{name} items must be pairs")
        pair = cast(list[object] | tuple[object, ...], item)
        if len(pair) != 2:
            raise ContractError(f"{name} items must be pairs")
        result.append((ref(pair[0], f"{name} key"), json_value(pair[1], f"{name} value")))
    if len(set(result)) != len(result):
        raise ContractError(f"{name} must not contain duplicate variants")
    return tuple(sorted(result))


def variant_options(
    values: tuple[tuple[str, object], ...],
) -> tuple[tuple[tuple[str, object], ...], ...]:
    return tuple(parameters((item,), "parameter variant") for item in values)


__all__ = [
    "integer",
    "names",
    "pairs",
    "parameters",
    "ref",
    "sequence",
    "variants",
    "variant_options",
]
