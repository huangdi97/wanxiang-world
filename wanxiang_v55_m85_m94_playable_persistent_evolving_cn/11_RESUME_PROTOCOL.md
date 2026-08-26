# Resume Protocol

上下文压缩/重启后读取：

1. `STATUS.md`
2. `PLAN.md`
3. `reports/V55_ACCEPTANCE_MATRIX.md`
4. 最近 `Mxx_QUALIFICATION.md`
5. 最近 `Gxx_REPORT.md`
6. `git status`
7. `git log --oneline --decorate -40`
8. 当前 Goal 文件
9. failing tests / CI logs

从最早 ACTIVE / FAIL / BLOCKED Goal 恢复。

不要重跑已有可复现 PASS；不要重新设计 v5.5 总架构；不要因为上下文丢失重做 v5.4。
