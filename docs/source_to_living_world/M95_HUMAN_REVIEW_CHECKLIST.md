# M95 Human Review Checklist / 人工验收清单

Status: **WAITING_HUMAN**. 本文件不是验收通过证明。

Automated evidence (browser E2E, API tests, visual cache tests) can prove that
controls exist and respond, but it **cannot** decide whether the world feels
worth entering, whether the visual stage reads clearly, or whether the
experience is acceptable. Those judgments require a human reviewer.

## What automation already covers

- 上传一本合成书 → 自动生成世界、场景与角色；
- Observer 浏览世界、切换地点视觉，且不改变 canonical location；
- Embodiment 进入角色 → 行动 → Commit Authority → history；
- 离开、继续、历史回放、世界线分支；
- 移动端布局与最低触达尺寸；
- 私有来源的视觉/来源派生上下文对访客隐藏；
- 重启、备份恢复后世界仍可继续，已付费 T1 缓存不重复计费；
- 来源关系冲突会标记为 ⚠，Atlas SVG 用橙色虚线而不是假装一致；
- Atlas 标题与图例随 zh-CN / en-US 本地化；
- T0 场景图内的预览与免责声明为中英双语；
- en-US 页面静态文案无中文，行动建议发送英文命令；
- Chromium E2E 覆盖英文建议 → Commit Authority → 可见状态变化。

## Human checklist

Reviewer: ____________________  Date: ____________  Build SHA: ____________

1. [ ] `uv run python scripts/m95_player_server.py` 启动本地构建。
2. [ ] 首屏 5 秒内出现可读的世界视觉，而不是空白或占位符。
3. [ ] 世界 Atlas / 地点列表让人理解“这是一个世界入口”，而不是后台表格。
4. [ ] 切换观察地点时，明确知道“只是在看预览，角色没有移动”。
5. [ ] 选择一个角色进入后，场景、地点、时间、在场人物与行动输入清楚可辨。
6. [ ] 提交一次行动后，能看到真实状态变化与历史记录，而不是只有 toast。
7. [ ] 离开再继续，世界保留了之前的行动结果；时间推进合理。
8. [ ] 打开历史并回放，能看懂发生了什么；退出回放不丢失已加载历史。
9. [ ] 移动端（约 390px 宽）仍可完成进入、行动、查看历史。
10. [ ] 视觉风格是否愿意继续看下去？是否明显像“同一套通用世界”，而不是一本书的硬编码地图？
11. [ ] 是否发现任何视觉/文案暗示“图片改变了 canonical 世界”？记录原话与复现步骤。
12. [ ] 是否发现来源没有支持、却被呈现为事实的地点/人物/关系？记录原话。
13. [ ] 在 URL 追加 `?locale=en-US`：界面、Atlas 标题/图例、行动建议是否为英文？来源书名/人名保留原文是否可接受？
14. [ ] T0 场景图内的双语标签在桌面与移动端是否清晰、没有裁切？是否仍能读懂“这是示意投影，不是世界真相”？
15. [ ] 若世界出现 ⚠“来源存在不同说法” / “Sources disagree”：是否理解为不确定，而不是被当成既定事实？
16. [ ] 英文页面点击 `Stay awake` 等建议后，输入框、状态变化与历史记录是否一致？是否出现中文残留？
17. [ ] 冲突提示是否不仅靠颜色区分？文字/工具提示是否可读（色盲、低对比度环境）？

## Verdict (human only)

- [ ] ACCEPT
- [ ] REVISE — notes:

## Explicit non-claims

- REAL_T1 / REAL_T3 / T4 remain `EXTERNAL_BLOCKED`; no real external provider
  execution is claimed by this checklist.
- This checklist does not authorize merge, tag, release, Stable, or Gate 80.
- Filling this file does not change `WAITING_HUMAN`; only a human verdict does.
