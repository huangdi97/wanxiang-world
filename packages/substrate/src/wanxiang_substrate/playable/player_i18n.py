"""Immutable locale catalogue shared by Player projections and UI adapters."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from wanxiang_substrate.playable.player_i18n_en import STRINGS as _EN_STRINGS
from wanxiang_substrate.playable.player_i18n_history_en import STRINGS as _EN_HISTORY
from wanxiang_substrate.playable.player_i18n_history_zh import STRINGS as _ZH_HISTORY
from wanxiang_substrate.playable.player_i18n_visual_generation_en import (
    STRINGS as _EN_VISUAL_GENERATION,
)
from wanxiang_substrate.playable.player_i18n_visual_generation_zh import (
    STRINGS as _ZH_VISUAL_GENERATION,
)
from wanxiang_substrate.playable.player_i18n_zh import STRINGS as _ZH_STRINGS

_Locale = Literal["zh-CN", "en-US"]


@dataclass(frozen=True, slots=True)
class _PlayerCopy:
    """One complete Player vocabulary; content data is translated elsewhere."""

    locale: _Locale
    strings: Mapping[str, str]

    def text(self, key: str) -> str:
        return self.strings.get(key, key)

    def render(self, key: str, **values: object) -> str:
        return self.text(key).format(**values)


def _copy(locale: _Locale, strings: dict[str, str]) -> _PlayerCopy:
    return _PlayerCopy(locale, MappingProxyType(strings))


_ZH_CN = _copy("zh-CN", {**_ZH_STRINGS, **_ZH_HISTORY, **_ZH_VISUAL_GENERATION})
_EN_US = _copy("en-US", {**_EN_STRINGS, **_EN_HISTORY, **_EN_VISUAL_GENERATION})
_CATALOG: Mapping[_Locale, _PlayerCopy] = MappingProxyType({"zh-CN": _ZH_CN, "en-US": _EN_US})


def _normalize_locale(value: str | None) -> _Locale:
    normalized = (value or "").strip().replace("_", "-").casefold()
    return "en-US" if normalized == "en" or normalized.startswith("en-") else "zh-CN"


def _copy_for(value: str | None = None) -> _PlayerCopy:
    return _CATALOG[_normalize_locale(value)]


def _serialize_copy(value: _PlayerCopy) -> str:
    payload = {"locale": value.locale, "strings": dict(value.strings)}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
