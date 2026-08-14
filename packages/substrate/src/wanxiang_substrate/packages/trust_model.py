"""Plugin trust, signing & capability permissions (G17E).

Trust model: data-only packages never execute code; executable plugins in the
protected profile must be signed and declare capabilities. A CapabilityGate
enforces declared capabilities at the application boundary, and every plugin
action is audited. OS-level sandboxing is NOT claimed; this is an application-
boundary policy (stated honestly).
"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass
from typing import Any

CAPABILITIES = ("filesystem", "network", "database", "commit")


@dataclass(frozen=True, slots=True)
class PluginSignature:
    """Deterministic HMAC signature over plugin metadata."""

    plugin_id: str
    version: str
    digest: str


def sign_manifest(plugin_id: str, version: str, secret: str) -> PluginSignature:
    digest = hmac.new(
        secret.encode(), f"{plugin_id}:{version}".encode(), hashlib.sha256
    ).hexdigest()
    return PluginSignature(plugin_id=plugin_id, version=version, digest=digest)


def verify_signature(signature: PluginSignature, secret: str) -> bool:
    expected = sign_manifest(signature.plugin_id, signature.version, secret)
    return hmac.compare_digest(signature.digest, expected.digest)


@dataclass(frozen=True, slots=True)
class PluginPermissions:
    """Declared capabilities for a plugin."""

    plugin_id: str
    version: str
    capabilities: tuple[str, ...] = ()
    trusted: bool = False

    def __post_init__(self) -> None:
        for cap in self.capabilities:
            if cap not in CAPABILITIES:
                raise ValueError(f"unknown capability {cap!r}")


class CapabilityGate:
    """Enforces declared capabilities at the adapter boundary."""

    def __init__(self, secret: str = "test-secret") -> None:
        self._secret = secret
        self._audit: list[dict[str, Any]] = []
        self._signed: dict[tuple[str, str], PluginSignature] = {}

    def authorize(
        self, permissions: PluginPermissions, signature: PluginSignature | None, *, capability: str
    ) -> bool:
        if capability not in CAPABILITIES:
            raise ValueError(f"unknown capability {capability!r}")
        if capability == "commit":
            # Commit capability is never granted to plugins: only Commit
            # Authority may mutate canonical state.
            self._audit.append(
                {
                    "plugin": permissions.plugin_id,
                    "version": permissions.version,
                    "action": capability,
                    "allowed": False,
                }
            )
            return False
        if capability not in permissions.capabilities:
            self._audit.append(
                {
                    "plugin": permissions.plugin_id,
                    "version": permissions.version,
                    "action": capability,
                    "allowed": False,
                }
            )
            return False
        if permissions.trusted:  # noqa: SIM102
            if signature is None or not verify_signature(signature, self._secret):
                self._audit.append(
                    {
                        "plugin": permissions.plugin_id,
                        "version": permissions.version,
                        "action": capability,
                        "allowed": False,
                    }
                )
                return False
        self._audit.append(
            {
                "plugin": permissions.plugin_id,
                "version": permissions.version,
                "action": capability,
                "allowed": True,
            }
        )
        return True

    def audit(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._audit)
