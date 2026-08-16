# Resume Protocol

上下文压缩/重启后依次读取：STATUS.md → PLAN.md → reports/V5_3_FINAL_ACCEPTANCE_MATRIX.md → 最近 milestone → 最近 goal report → git status → git log -30 → 当前 Goal → failing tests。

从最早 ACTIVE/FAIL Goal 恢复，先跑最窄 regression，不重做已有可复现 PASS。
