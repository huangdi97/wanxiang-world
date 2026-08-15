# 连续执行与恢复协议
中断/压缩/重启后按顺序读取：
1. STATUS.md
2. PLAN.md
3. reports/M35_M42_ACCEPTANCE_MATRIX.md
4. 最近 Milestone qualification
5. 最近 Goal report
6. git status
7. git log --oneline --decorate -30
8. 当前 Goal 文件
9. 当前 failing tests / blockers

从最早 ACTIVE/FAIL Goal 恢复。先跑最窄 regression，再继续。不得凭聊天记忆重新规划，不重做已有可复现 PASS。
