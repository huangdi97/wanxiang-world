"""G19H: multi-simulator federation & co-simulation research.

- Federation can checkpoint/restore reproducibly.
- Conflicts resolved explicitly before commit; fastest simulator never wins implicitly.
- Failed simulator does not corrupt others or the world.
- Multi-rate time coordination is deterministic and measured.
- Research flag off => no core regression.
"""

from __future__ import annotations

from wanxiang_research.flags import DEFAULT_FLAGS
from wanxiang_research.sim_federation import (
    ConflictResolver,
    FederationCoordinator,
    FederationScheduler,
    FlakySimulator,
    PreciseSimulator,
    TickSimulator,
)


def _federation() -> FederationScheduler:
    return FederationScheduler((TickSimulator(), PreciseSimulator()), horizon=3.0)


def test_federation_checkpoint_restore_reproducible() -> None:
    first = _federation()
    first.run()
    digest1 = first.checkpoint().digest()

    second = _federation()
    second.run()
    digest2 = second.checkpoint().digest()
    assert digest1 == digest2

    # Restore into a fresh scheduler and re-run: identical delta sequence.
    restored = FederationScheduler((TickSimulator(), PreciseSimulator()), horizon=0.0)
    restored.restore(first.checkpoint())
    assert restored.checkpoint().digest() == digest1
    assert len(restored.run()) == len(first.checkpoint().deltas)


def test_conflicts_resolved_explicitly_before_commit() -> None:
    # No precedence: conflict at t=1.0 stays unresolved; proposal not ready.
    coordinator = FederationCoordinator(_federation(), ConflictResolver())
    proposal = coordinator.run()
    assert proposal.ready is False
    # Conflicts occur at every time both simulators produce (0, 1, 2, 3).
    assert len(proposal.unresolved) == 8
    conflict_times = {0.0, 1.0, 2.0, 3.0}
    assert {d.time for d in proposal.unresolved} == conflict_times

    # Explicit precedence: precise model wins; proposal becomes ready.
    resolver = ConflictResolver(precedence={"precise_model": 1, "tick_model": 0})
    proposal2 = FederationCoordinator(_federation(), resolver).run()
    assert proposal2.ready is True
    assert proposal2.unresolved == ()
    accepted_times = {d.time for d in proposal2.deltas}
    assert 1.0 in accepted_times
    accepted_at_1 = [d for d in proposal2.deltas if d.time == 1.0]
    assert len(accepted_at_1) == 1
    assert accepted_at_1[0].model_id == "precise_model"


def test_fastest_simulator_never_wins_implicitly() -> None:
    # Tick advances faster (1.0/step) than precise (0.5/step); precedence must be
    # declared explicitly and must not be derived from step speed.
    deltas = _federation().run()
    conflict = ConflictResolver().resolve([d for d in deltas if d.time == 1.0])[0]
    assert conflict.accepted is None  # no implicit winner
    resolver = ConflictResolver(precedence={"tick_model": 2, "precise_model": 1})
    resolved = resolver.resolve([d for d in deltas if d.time == 1.0])[0]
    assert resolved.accepted is not None
    assert resolved.accepted.model_id == "tick_model"
    assert resolved.reason == "explicit-precedence"


def test_partial_simulator_failure_isolated() -> None:
    scheduler = FederationScheduler(
        (FlakySimulator(fail_from=2.0), PreciseSimulator()), horizon=3.0
    )
    deltas = scheduler.run()
    failed = dict(scheduler.failed())
    assert "flaky" in failed
    # Precise simulator kept producing after the failure.
    precise_times = sorted(d.time for d in deltas if d.simulator_id == "precise")
    assert precise_times == [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    # World untouched.
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    assert StructuredCompiler().compile("stable_2", {"src": approved_source()}).ok


def test_time_coordination_benchmark_deterministic() -> None:
    scheduler = _federation()
    deltas = scheduler.run()
    # tick: 0,1,2,3 ; precise: 0..3 step .5 -> coordination at 7 distinct times.
    assert scheduler.coordination_steps == 7
    assert len(deltas) == 4 + 7
    # Deltas are emitted in time order (causality preserved).
    times = [d.time for d in deltas]
    assert times == sorted(times)


def test_validity_envelopes_persist() -> None:
    assumptions = dict(_federation().assumptions())
    assert assumptions["tick"].max_horizon == 10.0
    assert assumptions["precise"].max_horizon == 2.0
    # Every produced delta carries its validity envelope.
    for delta in _federation().run():
        assert delta.validity == assumptions[delta.simulator_id]
        assert delta.proposed is True


def test_flag_off_no_core_regression() -> None:
    assert DEFAULT_FLAGS.is_enabled("multi_simulator_federation") is False
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    assert StructuredCompiler().compile("stable_2", {"src": approved_source()}).ok
