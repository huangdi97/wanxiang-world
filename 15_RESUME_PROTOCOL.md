# Resume Protocol

会话压缩/重启后：

1. 读取 STATUS.md / PLAN.md / 当前 branch。
2. 读取 reports/SOURCE_TO_LIVING_WORLD_ACCEPTANCE_MATRIX.md。
3. 读取最近 milestone qualification。
4. 读取最近 Goal report。
5. `git status`、`git log --oneline --decorate -40`。
6. 定位最早 ACTIVE / FAIL Goal。
7. 从该 Goal 恢复；不要重做已可复现 PASS。
8. 若当前 job 有 checkpoint，从 checkpoint 恢复，不重新 ingest。
9. 不因上下文丢失重新设计 Kernel。
