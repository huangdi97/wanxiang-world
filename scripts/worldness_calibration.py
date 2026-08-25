"""Run and persist the M81 adversarial Worldness calibration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from wanxiang_substrate.quality.worldness_calibration import run_worldness_calibration

ROOT = Path(__file__).resolve().parent.parent


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    report = run_worldness_calibration().to_dict()
    target = ROOT / "artifacts" / "m79_m84" / "worldness_calibration.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
