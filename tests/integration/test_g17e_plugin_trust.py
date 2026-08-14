"""G17E: plugin trust, signing, capability permissions & isolation policy.

- Protected profile rejects unauthorized executable plugins.
- Capability escalation fails (including commit, which is never granted).
- Data-only packages cannot execute code.
- Audit identifies plugin/version/action.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages.errors import UntrustedExecutable
from wanxiang_substrate.packages.model import UNTRUSTED
from wanxiang_substrate.packages.trust import ExecutableExtensionPolicy
from wanxiang_substrate.packages.trust_model import (
    CapabilityGate,
    PluginPermissions,
    PluginSignature,
    sign_manifest,
    verify_signature,
)


def test_protected_profile_rejects_unauthorized_executable_plugin() -> None:
    # An untrusted (data-only) package cannot execute code.
    with pytest.raises(UntrustedExecutable):
        ExecutableExtensionPolicy.require_executable(UNTRUSTED, ".py")
    # A trusted package without a valid signature is rejected by the gate.
    gate = CapabilityGate(secret="s3cret")
    permissions = PluginPermissions("p1", "1.0.0", capabilities=("filesystem",), trusted=True)
    assert gate.authorize(permissions, None, capability="filesystem") is False
    forged = PluginSignature("p1", "1.0.0", "0" * 64)
    assert gate.authorize(permissions, forged, capability="filesystem") is False


def test_signed_trusted_plugin_allowed_and_capability_escalation_fails() -> None:
    gate = CapabilityGate(secret="s3cret")
    sig = sign_manifest("p1", "1.0.0", "s3cret")
    assert verify_signature(sig, "s3cret") is True
    permissions = PluginPermissions("p1", "1.0.0", capabilities=("filesystem",), trusted=True)
    assert gate.authorize(permissions, sig, capability="filesystem") is True
    # Escalation: an undeclared capability is denied.
    assert gate.authorize(permissions, sig, capability="network") is False
    assert gate.authorize(permissions, sig, capability="database") is False
    # Commit is never granted to any plugin.
    assert gate.authorize(permissions, sig, capability="commit") is False


def test_data_only_package_cannot_execute_code() -> None:
    assert ExecutableExtensionPolicy.allows(UNTRUSTED, ".py") is False
    assert ExecutableExtensionPolicy.allows(UNTRUSTED, ".wasm") is False
    # Data-only packages declare no capabilities.
    permissions = PluginPermissions("data-pack", "1.0.0", capabilities=(), trusted=False)
    gate = CapabilityGate()
    assert gate.authorize(permissions, None, capability="filesystem") is False


def test_audit_identifies_plugin_version_action() -> None:
    gate = CapabilityGate(secret="s3cret")
    sig = sign_manifest("p2", "2.1.0", "s3cret")
    permissions = PluginPermissions("p2", "2.1.0", capabilities=("filesystem",), trusted=True)
    gate.authorize(permissions, sig, capability="filesystem")
    gate.authorize(permissions, sig, capability="network")  # denied
    audit = gate.audit()
    assert len(audit) == 2
    assert all(e["plugin"] == "p2" and e["version"] == "2.1.0" for e in audit)
    assert audit[0]["allowed"] is True and audit[1]["allowed"] is False
