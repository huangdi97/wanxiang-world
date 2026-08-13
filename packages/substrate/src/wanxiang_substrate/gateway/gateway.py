"""Digital Human / XR gateway contracts (G12G).

The gateway exposes speech/emotion/intent contracts and TTS/lipsync/expression/
action outputs as non-authoritative proposals. Rights gate: unauthorized
asset/voice/face generation calls are rejected.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import WanxiangError


class GatewayError(WanxiangError):
    code = "gateway_error"


class GatewayRightsDenied(GatewayError):
    code = "gateway_rights_denied"


@dataclass(frozen=True, slots=True)
class SpeechInput:
    speech_id: str
    speaker: str
    text: str
    emotion: str = "neutral"
    action_intent: str = ""


@dataclass(frozen=True, slots=True)
class MediaOutput:
    """TTS/lipsync/expression/action outputs + stream metadata."""

    output_id: str
    kind: str
    text: str = ""
    emotion: str = "neutral"
    stream_ref: str = ""
    metadata: tuple[tuple[str, str], ...] = ()


class DigitalHumanGateway:
    """Non-authoritative gateway; outputs are proposals, never world truth."""

    def __init__(self) -> None:
        self._permissions: dict[str, tuple[str, ...]] = {}
        self._outputs: dict[str, MediaOutput] = {}

    def grant(self, speaker: str, permissions: tuple[str, ...]) -> None:
        self._permissions[speaker] = permissions

    def require_permission(self, speaker: str, permission: str) -> None:
        if permission not in self._permissions.get(speaker, ()):
            raise GatewayRightsDenied(f"speaker {speaker!r} lacks {permission!r} for generation")

    def generate(
        self,
        speech: SpeechInput,
        *,
        outputs: tuple[str, ...] = ("tts", "lipsync", "expression"),
    ) -> tuple[MediaOutput, ...]:
        for output_kind in outputs:
            self.require_permission(speech.speaker, output_kind)
        result: list[MediaOutput] = []
        for kind in outputs:
            output = MediaOutput(
                output_id=f"{kind}_{speech.speech_id}",
                kind=kind,
                text=speech.text if kind == "tts" else "",
                emotion=speech.emotion,
                stream_ref=f"ref://stream/{speech.speech_id}/{kind}",
                metadata=(("speaker", speech.speaker), ("intent", speech.action_intent)),
            )
            self._outputs[output.output_id] = output
            result.append(output)
        return tuple(result)

    def get(self, output_id: str) -> MediaOutput | None:
        return self._outputs.get(output_id)
