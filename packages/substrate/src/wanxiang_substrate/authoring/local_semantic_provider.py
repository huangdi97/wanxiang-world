# pyright: reportPrivateUsage=false

import hashlib
import json
import re
from typing import cast

from wanxiang_substrate.authoring.local_semantic_gedcom import extract_gedcom
from wanxiang_substrate.authoring.local_semantic_rules import (
    _CHINESE,
    _COMMON_FALSE_NAMES,
    _CUE,
    _ENGLISH_FALSE_NAMES,
    _EVENT_CUES,
    _PLACE_SUFFIX,
    _RELATION_WORDS,
    _TITLE,
    _clean,
    _identity_key,
)
from wanxiang_substrate.authoring.providers import (
    ProviderCapability,
    ProviderProposal,
)
from wanxiang_substrate.sources.errors import SemanticProviderSchemaError


class LocalSemanticProvider:
    """Deterministic private-safe provider registered in the normal router."""

    def __init__(self, provider_id: str = "local_semantic_v1") -> None:
        self.capability = ProviderCapability(
            provider_id=provider_id,
            kind="semantic",
            version="1.0.0",
            available=True,
            cost_units=1,
            deterministic=True,
            private_safe=True,
        )

    def propose(self, source_refs: tuple[str, ...], payload: str) -> tuple[ProviderProposal, ...]:
        entries = self._decode(payload)
        allowed_refs = set(source_refs)
        proposals: list[ProviderProposal] = []
        for entry in entries:
            locator = entry["locator"]
            if locator not in allowed_refs:
                raise SemanticProviderSchemaError(
                    "semantic provider returned a locator outside the requested batch"
                )
            proposals.extend(self._extract(locator, entry["text"]))
        return tuple(proposals)

    @staticmethod
    def _decode(payload: str) -> tuple[dict[str, str], ...]:
        try:
            raw: object = json.loads(payload)
        except (TypeError, ValueError) as exc:
            raise SemanticProviderSchemaError("semantic provider input is not valid JSON") from exc
        if not isinstance(raw, list):
            raise SemanticProviderSchemaError("semantic provider input schema is invalid")
        entries: list[dict[str, str]] = []
        for item in cast(list[object], raw):
            values = cast(dict[str, object], item) if isinstance(item, dict) else {}
            locator, text = values.get("locator"), values.get("text")
            if not isinstance(locator, str) or not isinstance(text, str):
                raise SemanticProviderSchemaError("semantic provider input schema is invalid")
            entries.append({"locator": locator, "text": text})
        return tuple(entries)

    def _extract(self, locator: str, text: str) -> tuple[ProviderProposal, ...]:
        gedcom = extract_gedcom(locator, text, self.capability.provider_id)
        if gedcom:
            return gedcom
        places = self._places(text)
        place_keys = {place.casefold() for place in places}
        names = tuple(name for name in self._names(text) if name.casefold() not in place_keys)
        proposals: list[ProviderProposal] = []
        for name in names:
            key = _identity_key(name)
            proposals.append(
                self._proposal("identity", {"key": key, "display_name": name}, locator, 0.72)
            )
            proposals.append(
                self._proposal(
                    "character", {"subject_key": key, "display_name": name}, locator, 0.68
                )
            )
        for place in places:
            proposals.append(self._proposal("place", {"name": place}, locator, 0.66))
        for source_place, target_place, relation_type in self._place_relations(text):
            proposals.append(
                self._proposal(
                    "place_relation",
                    {
                        "source_place": source_place,
                        "target_place": target_place,
                        "relation_type": relation_type,
                    },
                    locator,
                    0.72,
                )
            )
        for organization in self._organizations(text):
            proposals.append(self._proposal("organization", {"name": organization}, locator, 0.64))
        event_date = self._date(text)
        if event_date or any(cue in text for cue in _EVENT_CUES):
            fields = {
                "event_type": self._event_type(text),
                "date": event_date or "unknown",
                "participants": ",".join(_identity_key(name) for name in names[:4]),
            }
            proposals.append(self._proposal("event", fields, locator, 0.61 if event_date else 0.55))
        if event_date:
            proposals.append(
                self._proposal("time", {"date": event_date, "uncertain": "true"}, locator, 0.58)
            )
        if len(names) >= 2:
            relation = self._relation_type(text)
            proposals.append(
                self._proposal(
                    "relation",
                    {
                        "source_key": _identity_key(names[0]),
                        "target_key": _identity_key(names[1]),
                        "relation_type": relation,
                    },
                    locator,
                    0.56 if relation == "co_occurrence" else 0.64,
                )
            )
        for rule in self._rules(text):
            proposals.append(self._proposal("rule", {"name": rule}, locator, 0.63))
        for obj in self._objects(text):
            proposals.append(self._proposal("object", {"name": obj}, locator, 0.57))
        return tuple(proposals)

    def _names(self, text: str) -> tuple[str, ...]:
        found: list[str] = []
        for pattern in (
            rf"([{_CHINESE}]{{2,4}})(?=(?:{_CUE}))",
            rf"([{_CHINESE}]{{2,4}})(?=(?:{_TITLE}))",
            rf"(?:人物|角色|主人公|姓名|名叫|称为)\s*[:：]?\s*([{_CHINESE}]{{2,4}})",
        ):
            found.extend(match.group(1) for match in re.finditer(pattern, text))
        found.extend(
            match.group(0)
            for match in re.finditer(r"\b[A-Z][A-Za-z]{1,24}(?:\s+[A-Z][A-Za-z]{1,24})?\b", text)
            if match.group(0) not in _ENGLISH_FALSE_NAMES
        )
        return tuple(dict.fromkeys(name for name in found if self._valid_name(name)))

    def _valid_name(self, name: str) -> bool:
        return (
            name not in _COMMON_FALSE_NAMES
            and not any(char in name for char in "的了着在是有和与及")
            and not name.isdigit()
        )

    def _places(self, text: str) -> tuple[str, ...]:
        found: list[str] = []
        pattern = (
            rf"(?:在|到|从|去|位于|来到|返回|进入|离开|赶到)\s*"
            rf"([{_CHINESE}]{{2,20}}?(?:{_PLACE_SUFFIX}))"
        )
        found.extend(match.group(1) for match in re.finditer(pattern, text))
        found.extend(
            match.group(1)
            for match in re.finditer(
                r"(?:Place|地点)\s*[:：]\s*([^,，。;；]+)", text, re.IGNORECASE
            )
        )
        found.extend(
            match.group(1)
            for match in re.finditer(
                (
                    r"\b(?:arrived|visited|went|returned|entered|left|travelled|traveled)"
                    r"\s+(?:(?:in|to|from|at)\s+)?"
                    r"([A-Z][A-Za-z]{1,24}(?:\s+[A-Z][A-Za-z]{1,24})?)\b"
                ),
                text,
            )
        )
        return tuple(dict.fromkeys(_clean(place, 48) for place in found if _clean(place, 48)))

    def _place_relations(self, text: str) -> tuple[tuple[str, str, str], ...]:
        place = rf"([{_CHINESE}]{{2,20}}?(?:{_PLACE_SUFFIX}))"
        found: list[tuple[str, str, str]] = []
        patterns = (
            (rf"从\s*{place}\s*(?:到|至|前往)\s*{place}", "route"),
            (rf"{place}\s*(?:通往|通向|连接)\s*{place}", "connected"),
            (rf"{place}\s*(?:毗邻|邻近)\s*{place}", "adjacent"),
            (rf"{place}\s*位于\s*{place}", "located_in"),
        )
        for pattern, relation_type in patterns:
            for match in re.finditer(pattern, text):
                source_place = _clean(match.group(1), 48)
                target_place = _clean(match.group(2), 48)
                if source_place and target_place and source_place != target_place:
                    found.append((source_place, target_place, relation_type))
        for match in re.finditer(
            (
                r"\bfrom\s+([A-Z][A-Za-z ]{1,32}?)\s+to\s+"
                r"([A-Z][A-Za-z ]{1,32}?)(?=[,.;]|\s+(?:and|then)\b|$)"
            ),
            text,
        ):
            source_place = _clean(match.group(1), 48)
            target_place = _clean(match.group(2), 48)
            if source_place and target_place and source_place != target_place:
                found.append((source_place, target_place, "route"))
        return tuple(dict.fromkeys(found))

    def _organizations(self, text: str) -> tuple[str, ...]:
        pattern = rf"([{_CHINESE}]{{2,20}}?(?:公司|集团|委员会|政府|法院|公安局|银行|部门|机关))"
        return tuple(
            dict.fromkeys(_clean(match.group(1), 48) for match in re.finditer(pattern, text))
        )

    def _date(self, text: str) -> str:
        match = re.search(
            r"(?:18|19|20|21)\d{2}(?:年|[-/.])?(?:\d{1,2}(?:月|[-/.])?\d{0,2}(?:日)?)?", text
        )
        return match.group(0) if match else ""

    def _event_type(self, text: str) -> str:
        for cue in _EVENT_CUES:
            if cue in text:
                return cue
        return "narrative_observation"

    def _relation_type(self, text: str) -> str:
        for marker, relation in _RELATION_WORDS.items():
            if marker in text:
                return relation
        if any(marker in text for marker in ("关系", "之间", "与", "和", "同")):
            return "related"
        return "co_occurrence"

    def _rules(self, text: str) -> tuple[str, ...]:
        found: list[str] = []
        for match in re.finditer(
            r"(?:规则|规定|制度|原则|政策|必须|不得|禁止)\s*[:：]?\s*([^。！？\n]{2,64})", text
        ):
            found.append(_clean(match.group(0), 72))
        for match in re.finditer(r"(?:rule|norm|policy)\s*[:：]\s*([^\n]+)", text, re.IGNORECASE):
            found.append(_clean(match.group(1), 72))
        return tuple(dict.fromkeys(item for item in found if item))

    def _objects(self, text: str) -> tuple[str, ...]:
        found: list[str] = []
        for match in re.finditer(
            r"(?:物品|对象|object)\s*[:：]\s*([^,，。;；\n]+)", text, re.IGNORECASE
        ):
            found.append(_clean(match.group(1), 48))
        return tuple(dict.fromkeys(item for item in found if item))

    def _proposal(
        self, kind: str, fields: dict[str, str], locator: str, confidence: float
    ) -> ProviderProposal:
        normalized = tuple(sorted((key, _clean(value)) for key, value in fields.items() if value))
        digest = hashlib.sha256(
            json.dumps(
                [kind, normalized, locator], ensure_ascii=False, separators=(",", ":")
            ).encode()
        ).hexdigest()[:20]
        payload = (
            ("candidate_kind", kind),
            ("schema_version", "semantic-candidate-v1"),
            *normalized,
        )
        return ProviderProposal(
            proposal_id=f"semantic_{digest}",
            kind="candidate",
            provider_id=self.capability.provider_id,
            source_refs=(locator,),
            payload=payload,
            confidence=confidence,
        )
