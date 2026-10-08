"""Actor Trajectory Ledger with privacy, retention and at-rest codec seams.

Trajectory records explain why an actor made a decision. They store references
and hashes, not full prompts/private memory by default, and are explicitly
non-authoritative: deleting/redacting trajectory data never alters World history.
"""

from __future__ import annotations

import base64
import json
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

_BytesTransform = Callable[[bytes], bytes]


def _identity_bytes(value: bytes) -> bytes:
    return value


def _tuple_of_strings(value: object, name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be a list/tuple of strings")
    raw_values = cast(list[object] | tuple[object, ...], value)
    values: list[str] = []
    for item in raw_values:
        if not isinstance(item, str):
            raise ValueError(f"{name} must contain only strings")
        values.append(item)
    return tuple(values)


def _string(value: object, name: str, *, required: bool = False) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if required and not value.strip():
        raise ValueError(f"{name} must be non-empty")
    return value


def _record_from_payload(payload: Mapping[str, object]) -> ActorTrajectoryRecord:
    allowed = set(ActorTrajectoryRecord.__dataclass_fields__)
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ValueError(f"unknown trajectory payload fields: {unknown}")
    redacted = payload.get("redacted", False)
    if not isinstance(redacted, bool):
        raise ValueError("redacted must be bool")
    return ActorTrajectoryRecord(
        trajectory_id=_string(payload.get("trajectory_id"), "trajectory_id", required=True),
        actor_id=_string(payload.get("actor_id"), "actor_id", required=True),
        world_id=_string(payload.get("world_id"), "world_id", required=True),
        worldline_id=_string(payload.get("worldline_id"), "worldline_id", required=True),
        decision_id=_string(payload.get("decision_id"), "decision_id", required=True),
        created_at=_string(payload.get("created_at"), "created_at", required=True),
        observation_refs=_tuple_of_strings(payload.get("observation_refs"), "observation_refs"),
        memory_refs=_tuple_of_strings(payload.get("memory_refs"), "memory_refs"),
        memory_hashes=_tuple_of_strings(payload.get("memory_hashes"), "memory_hashes"),
        belief_refs=_tuple_of_strings(payload.get("belief_refs"), "belief_refs"),
        goal_refs=_tuple_of_strings(payload.get("goal_refs"), "goal_refs"),
        context_hash=_string(payload.get("context_hash"), "context_hash"),
        provider_id=_string(payload.get("provider_id"), "provider_id"),
        model_id=_string(payload.get("model_id"), "model_id"),
        tool_refs=_tuple_of_strings(payload.get("tool_refs"), "tool_refs"),
        plan_ref=_string(payload.get("plan_ref"), "plan_ref"),
        intent_ref=_string(payload.get("intent_ref"), "intent_ref"),
        adjudication_ref=_string(payload.get("adjudication_ref"), "adjudication_ref"),
        outcome_ref=_string(payload.get("outcome_ref"), "outcome_ref"),
        world_event_refs=_tuple_of_strings(payload.get("world_event_refs"), "world_event_refs"),
        rights_scope=_tuple_of_strings(payload.get("rights_scope"), "rights_scope")
        or ("trajectory.read",),
        retention_until=_string(payload.get("retention_until"), "retention_until"),
        redacted=redacted,
    )


@dataclass(frozen=True, slots=True)
class ActorTrajectoryRecord:
    trajectory_id: str
    actor_id: str
    world_id: str
    worldline_id: str
    decision_id: str
    created_at: str
    observation_refs: tuple[str, ...] = ()
    memory_refs: tuple[str, ...] = ()
    memory_hashes: tuple[str, ...] = ()
    belief_refs: tuple[str, ...] = ()
    goal_refs: tuple[str, ...] = ()
    context_hash: str = ""
    provider_id: str = ""
    model_id: str = ""
    tool_refs: tuple[str, ...] = ()
    plan_ref: str = ""
    intent_ref: str = ""
    adjudication_ref: str = ""
    outcome_ref: str = ""
    world_event_refs: tuple[str, ...] = ()
    rights_scope: tuple[str, ...] = ("trajectory.read",)
    retention_until: str = ""
    redacted: bool = False

    def __post_init__(self) -> None:
        for name in (
            "trajectory_id",
            "actor_id",
            "world_id",
            "worldline_id",
            "decision_id",
            "created_at",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        if not self.rights_scope:
            raise ValueError("rights_scope must not be empty")
        if len(set(self.rights_scope)) != len(self.rights_scope):
            raise ValueError("rights_scope must not contain duplicates")
        _parse_time(self.created_at)
        if self.retention_until:
            _parse_time(self.retention_until)


def _parse_time(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("trajectory timestamps must include timezone")
    return parsed.astimezone(UTC)


class ActorTrajectoryLedger:
    """Privacy-scoped trajectory records with optional encoded JSONL persistence."""

    def __init__(
        self,
        path: Path | None = None,
        *,
        encode: _BytesTransform | None = None,
        decode: _BytesTransform | None = None,
    ) -> None:
        if (encode is None) != (decode is None):
            raise ValueError("encode/decode transforms must be supplied together")
        self._path = path
        self._encode: _BytesTransform = encode or _identity_bytes
        self._decode: _BytesTransform = decode or _identity_bytes
        self._entries: list[ActorTrajectoryRecord] = []
        if path is not None and path.exists():
            self._load(path)

    def record_payload(self, payload: Mapping[str, object]) -> ActorTrajectoryRecord:
        """Record a bounded bridge payload; unknown/private-content keys fail closed."""
        return self.record(_record_from_payload(payload))

    def record(self, item: ActorTrajectoryRecord) -> ActorTrajectoryRecord:
        if any(entry.trajectory_id == item.trajectory_id for entry in self._entries):
            raise ValueError(f"duplicate trajectory id {item.trajectory_id!r}")
        self._entries.append(item)
        self._persist()
        return item

    def read(
        self,
        actor_id: str,
        *,
        requester_scopes: tuple[str, ...],
    ) -> tuple[ActorTrajectoryRecord, ...]:
        matching = tuple(item for item in self._entries if item.actor_id == actor_id)
        visible = tuple(
            item for item in matching if set(item.rights_scope).issubset(requester_scopes)
        )
        if matching and not visible:
            raise PermissionError("trajectory read denied by rights scope")
        return visible

    def redact(
        self,
        trajectory_id: str,
        *,
        requester_scopes: tuple[str, ...],
    ) -> ActorTrajectoryRecord:
        if "trajectory.admin" not in requester_scopes:
            raise PermissionError("trajectory.admin scope required for redaction")
        index = self._index(trajectory_id)
        item = self._entries[index]
        redacted = replace(
            item,
            observation_refs=(),
            memory_refs=(),
            belief_refs=(),
            goal_refs=(),
            context_hash="",
            tool_refs=(),
            plan_ref="",
            intent_ref="",
            adjudication_ref="",
            outcome_ref="",
            provider_id="",
            model_id="",
            redacted=True,
        )
        self._entries[index] = redacted
        self._persist()
        return redacted

    def prune_expired(
        self,
        now: datetime,
        *,
        requester_scopes: tuple[str, ...],
    ) -> tuple[str, ...]:
        if "trajectory.admin" not in requester_scopes:
            raise PermissionError("trajectory.admin scope required for retention pruning")
        current = now.astimezone(UTC)
        expired = tuple(
            item.trajectory_id
            for item in self._entries
            if item.retention_until and _parse_time(item.retention_until) <= current
        )
        if expired:
            expired_set = set(expired)
            self._entries = [
                item for item in self._entries if item.trajectory_id not in expired_set
            ]
            self._persist()
        return expired

    def entries(self) -> tuple[ActorTrajectoryRecord, ...]:
        return tuple(self._entries)

    def _index(self, trajectory_id: str) -> int:
        for index, item in enumerate(self._entries):
            if item.trajectory_id == trajectory_id:
                return index
        raise KeyError(trajectory_id)

    def _persist(self) -> None:
        if self._path is None:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        lines: list[str] = []
        for item in self._entries:
            raw = json.dumps(asdict(item), sort_keys=True, separators=(",", ":")).encode()
            lines.append(base64.b64encode(self._encode(raw)).decode("ascii"))
        self._path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="ascii")

    def _load(self, path: Path) -> None:
        for raw in path.read_text(encoding="ascii").splitlines():
            if not raw:
                continue
            decoded = self._decode(base64.b64decode(raw))
            loaded: object = json.loads(decoded.decode("utf-8"))
            if not isinstance(loaded, dict):
                raise ValueError("trajectory JSONL row must be an object")
            payload = cast(dict[str, object], loaded)
            self._entries.append(_record_from_payload(payload))


__all__ = ["ActorTrajectoryLedger", "ActorTrajectoryRecord"]
