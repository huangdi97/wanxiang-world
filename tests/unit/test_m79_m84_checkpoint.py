from __future__ import annotations

import os
from pathlib import Path

from scripts.m79_m84_checkpoint import ROOT, checkpoint


def test_checkpoint_requires_real_external_files() -> None:
    system_root = Path(os.environ.get("SYSTEMROOT", "C:/Windows"))
    book = system_root / "System32" / "kernel32.dll"
    gedcom = system_root / "System32" / "ntdll.dll"

    result = checkpoint(book, gedcom)

    assert result["status"] == "READY_TO_RESUME"
    assert result["missing_inputs"] == []
    assert result["invalid_inputs"] == []
    assert result["private_local_sources"] == {
        "second_book": True,
        "gedcom": True,
        "copied_to_git": False,
        "modified": False,
    }


def test_checkpoint_rejects_missing_directories_and_repo_paths() -> None:
    external_root = Path.cwd().parent
    missing_book = external_root / "__wanxiang_missing_second_book__.epub"
    directory = external_root

    result = checkpoint(missing_book, directory)
    assert result["status"] == "USER_INPUT_REQUIRED"
    assert result["missing_inputs"] == []
    assert result["invalid_inputs"] == ["second_real_book_path", "gedcom_path"]
    assert result["resume"] == {
        "M79": "G82A_SOURCE_GATE_INVALID",
        "M82": "G85A_SOURCE_GATE_INVALID",
        "completed_independent_work": ("M80", "M81", "M83"),
    }

    repo_file = ROOT / "scripts" / "m79_m84_checkpoint.py"
    repo_result = checkpoint(repo_file, None)
    assert repo_result["private_local_sources"] == {
        "second_book": False,
        "gedcom": False,
        "copied_to_git": False,
        "modified": False,
    }
    assert repo_result["source_validation"] == {
        "second_book": {"status": "invalid", "reason": "inside_repository"},
        "gedcom": {"status": "missing", "reason": "path_not_provided"},
    }
