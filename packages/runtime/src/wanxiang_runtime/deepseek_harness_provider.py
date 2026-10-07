"""Optional adapter for the official DeepSeek Harness Python SDK.

The official SDK is an external dependency and is intentionally imported lazily.
Wanxiang can therefore ship and test this adapter without pretending that an SDK
binary, model credential, or network route exists on every host.

The adapter preserves the R7 boundary: DeepSeek Harness receives a read-only
WorldObservation and may return only an AgentDecision. Consequences are sent back
into the same durable DSH session. It never imports Commit Authority, persistence,
or a canonical-state writer.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from wanxiang_runtime.r7_agent_harness_contract import (
    AgentDecision,
    HarnessConsequence,
    HarnessInfo,
    HarnessProtocolError,
    HarnessUnavailable,
    WorldObservation,
    parse_decision,
)

_HarnessFactory = Callable[..., object]


def _run_sdk(harness: object, prompt: str, *, session_id: str) -> object:
    run = getattr(harness, "run", None)
    if not callable(run):
        raise HarnessUnavailable("official DeepSeek Harness SDK has no callable run method")
    invoke = cast("Callable[..., object]", run)
    return invoke(prompt, session_id=session_id)


def _close_sdk(harness: object) -> None:
    close = getattr(harness, "close", None)
    if close is None:
        return
    if not callable(close):
        raise HarnessUnavailable("official DeepSeek Harness SDK has a non-callable close member")
    invoke = cast("Callable[[], object]", close)
    invoke()


@dataclass(frozen=True, slots=True)
class OfficialDshSettings:
    """Non-secret launch settings for the official DSH SDK."""

    dsh_home: Path
    cwd: Path
    provider: str
    model: str
    reasoning_effort: str | None = None
    max_tokens: int | None = None
    request_timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        if not self.provider.strip() or not self.model.strip():
            raise HarnessUnavailable("official DSH provider/model must be non-empty")
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise HarnessUnavailable("official DSH max_tokens must be positive")
        if self.request_timeout_seconds is not None and self.request_timeout_seconds <= 0:
            raise HarnessUnavailable("official DSH request timeout must be positive")


def _load_factory() -> _HarnessFactory:
    try:
        module = importlib.import_module("deepseek_harness")
    except ModuleNotFoundError as exc:
        raise HarnessUnavailable(
            "official DeepSeek Harness SDK is not installed; install deepseek-harness-sdk"
        ) from exc
    factory = getattr(module, "DeepSeekHarness", None)
    if factory is None or not callable(factory):
        raise HarnessUnavailable("deepseek_harness.DeepSeekHarness is unavailable")
    return cast(_HarnessFactory, factory)


def _sdk_version() -> str:
    try:
        return importlib.metadata.version("deepseek-harness-sdk")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _final_response(result: object, what: str) -> str:
    value = getattr(result, "final_response", None)
    if not isinstance(value, str):
        raise HarnessProtocolError(f"official DSH {what} has no string final_response")
    return value


def _parse_json_response(text: str, what: str) -> dict[str, object]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise HarnessProtocolError(f"official DSH {what} was not exact JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise HarnessProtocolError(f"official DSH {what} must be a JSON object")
    return {str(key): item for key, item in cast(Mapping[object, object], value).items()}


class OfficialDeepSeekHarnessProvider:
    """AgentHarnessProvider backed by DeepSeek's official subprocess SDK."""

    provider_id = "agent-harness-deepseek-official"

    def __init__(
        self,
        settings: OfficialDshSettings,
        *,
        harness_factory: _HarnessFactory | None = None,
        sdk_version: str | None = None,
    ) -> None:
        self._settings = settings
        self._factory = harness_factory
        self._version = sdk_version
        self._harness: object | None = None

    def _ensure_harness(self) -> object:
        if self._harness is not None:
            return self._harness
        factory = self._factory or _load_factory()
        kwargs: dict[str, object] = {
            "dsh_home": str(self._settings.dsh_home.resolve()),
            "cwd": str(self._settings.cwd.resolve()),
            "provider": self._settings.provider,
            "model": self._settings.model,
        }
        if self._settings.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self._settings.reasoning_effort
        if self._settings.max_tokens is not None:
            kwargs["max_tokens"] = self._settings.max_tokens
        if self._settings.request_timeout_seconds is not None:
            kwargs["request_timeout_seconds"] = self._settings.request_timeout_seconds
        try:
            self._harness = factory(**kwargs)
        except Exception as exc:
            raise HarnessUnavailable(
                f"cannot initialize official DeepSeek Harness SDK: {exc}"
            ) from exc
        return self._harness

    def info(self) -> HarnessInfo:
        self._ensure_harness()
        return HarnessInfo(
            harness_id="deepseek-harness-python-sdk",
            harness_version=self._version or _sdk_version(),
            kind="official-deepseek-harness-sdk",
            official_dsh=True,
        )

    def decide(self, observation: WorldObservation) -> AgentDecision:
        payload = observation.payload()
        prompt = (
            "You are an external proposal-only actor connected to Wanxiang. "
            "You have no commit authority. Based only on the observation JSON below, "
            "return EXACTLY one JSON object and no markdown. Either return "
            '{"status":"abstained","proposal":null,"reason":"..."} or '
            '{"status":"proposed","proposal":{"proposalId":"...","action":"...",'
            '"rationaleRef":"...","payloadDigest":"<sha256-or-stable-digest>"},'
            '"reason":"..."}. Do not claim that the world changed. Observation: '
            + json.dumps(payload, sort_keys=True, ensure_ascii=False)
        )
        try:
            result = _run_sdk(
                self._ensure_harness(),
                prompt,
                session_id=self._session_id(observation.worldline_id),
            )
        except Exception as exc:
            raise HarnessUnavailable(f"official DeepSeek Harness decision failed: {exc}") from exc
        return parse_decision(_parse_json_response(_final_response(result, "decision"), "decision"))

    def deliver_consequence(self, consequence: HarnessConsequence) -> bool:
        prompt = (
            "Wanxiang has resolved your previous proposal. This is authoritative "
            "consequence data; do not reinterpret it as a new world mutation. "
            'Acknowledge by returning EXACTLY {"acknowledged":true}. Consequence: '
            + json.dumps(consequence.payload(), sort_keys=True, ensure_ascii=False)
        )
        try:
            result = _run_sdk(
                self._ensure_harness(),
                prompt,
                session_id=self._session_id(consequence.worldline_id),
            )
        except Exception as exc:
            raise HarnessUnavailable(
                f"official DeepSeek Harness consequence failed: {exc}"
            ) from exc
        fields = _parse_json_response(
            _final_response(result, "consequence acknowledgement"),
            "consequence acknowledgement",
        )
        if fields.get("acknowledged") is not True:
            raise HarnessProtocolError("official DSH did not acknowledge the consequence")
        return True

    def close(self) -> None:
        harness = self._harness
        self._harness = None
        if harness is not None:
            _close_sdk(harness)

    @staticmethod
    def _session_id(worldline_id: str) -> str:
        if not worldline_id.strip():
            raise HarnessProtocolError("worldline_id must be non-empty")
        return f"wanxiang-{worldline_id}"


__all__ = ["OfficialDeepSeekHarnessProvider", "OfficialDshSettings"]
