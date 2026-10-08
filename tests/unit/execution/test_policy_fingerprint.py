"""ExecutionPolicy fingerprint binds every routing/security field."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_execution import ExecutionPolicy, policy_fingerprint, policy_projection


def test_policy_fingerprint_is_deterministic_and_complete() -> None:
    policy = ExecutionPolicy.default_untrusted()

    assert policy_fingerprint(policy) == policy_fingerprint(policy)
    projection = policy_projection(policy)
    assert set(projection) == {
        "trust",
        "execution_class",
        "filesystem",
        "network",
        "secrets",
        "cpu_seconds_limit",
        "memory_mb_limit",
        "wall_seconds_limit",
        "reproducibility",
        "cost_class",
        "side_effects",
    }


def test_every_resource_or_security_change_changes_policy_fingerprint() -> None:
    base = ExecutionPolicy.default_untrusted()
    changed = replace(base, memory_mb_limit=base.memory_mb_limit + 1)

    assert policy_fingerprint(base) != policy_fingerprint(changed)
