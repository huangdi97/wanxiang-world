# Wanxiang M51–M70：Source → Living World 全量连续工程执行包

本包**取代**此前单独的 M51–M59 包。不要把两套 Goal 叠加执行；从本包开始，以本包为唯一工程执行 Source of Truth。

## 最终目标

不是只做到“能导入一本书”，而是一次把后续阶段接上：

```text
Book / GEDCOM / JSON / CSV / DOCX / text-PDF / Assets / Multi-source Bundle
→ Source Registry
→ Parse / Segment / Stable Locator
→ Multi-pass Distillation
→ Candidate / Claim / Evidence / Rights
→ Cross-source Fusion / Conflict Preservation
→ Domain Inference / Composition
→ WorldDraft
→ Constraint-backed Completion
→ Scenario / Genesis Authoring
→ WorldPackageDraft
→ Preview Instance
→ Worldness Validation
→ Repair / Completion Loop
→ Publishable World Package
→ Living World Instance
```

## M51–M59：World Creation Foundation

把统一的 Source→WorldDraft→Preview 底层做实。

## M60–M70：Autonomous World Authoring & Genesis

继续把 Preview 初稿推进到：
- 长文本世界理解；
- 多版本/多来源融合；
- 多模态/外部 Source 能力；
- Domain 自动推断与组合；
- 约束驱动的世界补全；
- Scenario/Genesis 自动生成；
- Worldness 自动验证；
- 自动修补循环；
- 最小人工审核；
- 一键 Source→Living World；
- GitHub CI + RC 发布。

## 关键边界

- **不训练 Wanxiang 自有基础模型。**
- LLM / embedding / OCR / ASR / vision / world model 都是可替换 Provider。
- 没有 API Key 时，核心 deterministic/reference E2E 仍必须通过。
- 模型输出永远是 Candidate / Proposal，不拥有 Commit Authority。
- 不为《红楼梦》、家谱或任何单一领域修改 Kernel。
- “任意一本书自动得到 100% 正确完整世界”不是可诚实承诺的验收标准；本包要求的是**有证据、有不确定性、有补全等级、有验证闭环的自动世界创作系统**。
