"""G20C: final independent security, reliability & chaos re-run.

- The curated high-risk suite (G13F, G14A-I, G16A/F/G/I) is re-run by
  scripts/security_reliability_certify.py (65 passed at certification time).
- Enabling ALL research flags never changes replay determinism (subprocess
  isolation so the global DEFAULT_FLAGS registry is not mutated in-process).
- The curated file list and the pytest summary parser stay valid.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

from scripts.security_reliability_certify import CURATED, match_count

ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_curated_suite_files_exist() -> None:
    for relative in CURATED:
        assert (ROOT / relative).exists(), f"missing curated suite file {relative}"


def testmatch_count_parser() -> None:
    assert match_count("65 passed, 0 failed, 0 skipped in 70s", r"(\d+) passed") == 65
    assert match_count("1 failed, 64 passed", r"(\d+) failed") == 1
    assert match_count("no summary", r"(\d+) passed") == 0


def test_flags_on_do_not_change_replay_determinism() -> None:
    code = (
        "from scripts.security_reliability_certify import flags_on_stable_check; "
        "import sys; sys.exit(0 if flags_on_stable_check()['ok'] else 1)"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, result.stdout + result.stderr
