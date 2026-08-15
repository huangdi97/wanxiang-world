# 万相世界 M35–M42 中文全量执行包
本包接续已经完成的 M0–M34。目标不是继续重写底层，而是冻结 v5.2 Kernel v1，把《红楼梦》最小参考实例扩展为 Full Living Red Chamber，再以 Family / Heritage / Campaign 验证同一 Core 的通用性，最后完成 SDK、Package 生态、生产部署和 v5.2 Release Qualification。

使用：
1. 合并到当前万相仓库根目录，不删除现有源码、Git、迁移、tests、reports。
2. 以 `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md` 为设计 Source of Truth。
3. 新开 Codex 对话，复制 `CODEX_COPY_PASTE_M35_M42_CN.txt`。
4. 从 G38A 连续执行到 G45H；每个 Goal PASS 后本地 commit，每个 Milestone PASS 后自动继续。
5. 禁止自动 push / force-push / 生产部署 / 擅自进入 v5.3。
