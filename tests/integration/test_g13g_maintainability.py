"""G13G: maintainability, complexity, test-quality and upgradeability checks.

- No exception swallowing remains in production (after the scheduler fix).
- No production file exceeds the size threshold; no import cycles.
- No cross-package private-name imports (refactor-survival invariant).
- Quality gate tooling is documented and runnable.
- Scheduler rejections are observable and deterministic (regression for the fix).
"""

from __future__ import annotations

import ast
import pathlib

from scripts.architecture_forensics import detect_cycles, import_edges
from scripts.maintainability_audit import MAX_LINES, any_and_swallow_scan, file_stats, iter_prod_py

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def _prod_files() -> list[pathlib.Path]:
    return iter_prod_py(ROOT)


def test_no_exception_swallowing_in_production() -> None:
    findings = any_and_swallow_scan(ROOT)["exception_swallows"]
    assert findings == [], f"exception swallows found: {findings}"


def test_no_files_over_size_threshold() -> None:
    over = [s for s in (file_stats(p) for p in _prod_files()) if s["lines"] > MAX_LINES]
    assert over == [], f"files over {MAX_LINES} lines: {over}"


def test_no_import_cycles() -> None:
    assert detect_cycles(import_edges(ROOT)) == []


def test_no_cross_package_private_imports() -> None:
    """Internals of one package must not be imported by another (refactor seam)."""
    from scripts.architecture_forensics import module_to_pkg, package_of

    mod_to_pkg = module_to_pkg(ROOT)
    violations: list[str] = []
    for py in _prod_files():
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        importer = package_of(py, ROOT)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                target_pkg = mod_to_pkg.get(node.module.split(".")[0])
                if target_pkg is not None and target_pkg != importer:
                    for alias in node.names:
                        if alias.name.startswith("_"):
                            violations.append(
                                f"{py.relative_to(ROOT)}:{node.lineno}: {node.module}.{alias.name}"
                            )
    assert violations == [], f"cross-package private imports: {violations}"


def test_quality_gate_documented() -> None:
    quality = ROOT / "scripts" / "quality.py"
    assert quality.exists()
    text = quality.read_text(encoding="utf-8")
    for tool in ("ruff", "pyright", "pytest", "architecture_check"):
        assert tool in text, f"quality.py must include {tool}"
    # Architecture guard runs as part of the gate.
    assert (ROOT / "scripts" / "architecture_check.py").exists()


def test_scheduler_rejections_are_observable_and_deterministic() -> None:
    from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
    from wanxiang_runtime.resolver import ResolverRegistry
    from wanxiang_substrate.body.resolver import register_body_resolvers
    from wanxiang_substrate.institution.resolver import register_institution_resolvers
    from wanxiang_substrate.population.fixture import DAY, INSTANCE, build_town_fixture_commands
    from wanxiang_substrate.population.model import SchedulerRunResult
    from wanxiang_substrate.population.resolver import register_population_resolvers
    from wanxiang_substrate.population.scheduler import AutonomousScheduler
    from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

    def register(registry: ResolverRegistry) -> None:
        register_temporal_resolvers(registry)
        register_body_resolvers(registry)
        register_institution_resolvers(registry)
        register_population_resolvers(registry)

    results: list[SchedulerRunResult] = []
    paths = [fresh_db_path(), fresh_db_path()]
    try:
        for path in paths:
            runtime = make_world_runtime(path, extra_resolvers=register)
            w = runtime.create_world(instance_id=INSTANCE)
            for command in build_town_fixture_commands(w.root_branch_id):
                runtime.submit_command(command)
            scheduler = AutonomousScheduler(runtime, seed=7)
            results.append(scheduler.run(w.instance_id, w.root_branch_id, horizon_ticks=2 * DAY))
    finally:
        for path in paths:
            cleanup_db_file(path)
    a, b = results[0], results[1]
    assert isinstance(a.rejected_events, int) and a.rejected_events >= 0
    assert a.rejected_events == b.rejected_events, "rejection count must be deterministic"
    assert a.events_submitted == b.events_submitted
