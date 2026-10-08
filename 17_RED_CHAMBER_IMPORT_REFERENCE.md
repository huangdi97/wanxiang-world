# 《红楼梦》参考验收路径（非硬编码需求）

该实例只用于验证通用架构，不允许红楼梦专名进入 Kernel/通用 Forge。

```text
合法测试底本/用户本地 Source
→ book parsing
→ characters/aliases
→ places/organizations
→ events/timeline
→ relations/knowledge boundaries
→ objects/rules/social norms
→ HistoricalChina + HouseholdSociety + Narrative domain suggestions
→ completion gaps
→ scenario candidates
→ WorldDraft
→ Preview
→ 7-day bounded worldness run
→ publishable package (若 rights permit)
```

验收重点：
- 不把补全冒充原著；
- 秘密不自动泄露；
- 分支不污染 Canon；
- Source locator 可回原文；
- 同一人物多称谓不盲合并；
- 用户本地受限文本默认不进 Git。
