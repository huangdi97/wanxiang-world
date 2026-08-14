# 《红楼梦》Source Gate 与最小活世界验收标准

## 1. Source Gate

真实《红楼梦》实例必须：
- 明确选定版本/底本/电子文本来源；
- 保存来源 URI/文件、checksum、版本/版次说明、rights/licence/public-domain 依据；
- 章节/段落/人物/事件 Claim 可回链到来源位置；
- 不允许模型记忆补写 Canon；
- 无来源内容只能进入 Completion，且标 E1–E5；
- FutureCanon 不进入角色当前 Perception。

如果执行环境无法取得可合法使用且可追溯的文本：
- 真实 Source Goal 标 `EXTERNAL_BLOCKED`；
- 不得把 synthetic fixture 改名为《红楼梦》；
- 仍完成所有通用 Domain、Compiler、Runtime、UI、测试能力；
- 最终 M34 不得宣称真实红楼梦实例 PASS。

## 2. 第一版实例范围

空间：潇湘馆、怡红院、公共路径、一个公共/过渡空间，具备 access/visibility/acoustic/privacy。

人物：林黛玉、贾宝玉、紫鹃、2 名经来源确认的主要人物、10–20 名职责型 NPC。

物品：信/诗稿、礼物、药物、服饰/首饰、陈设、容器/钥匙/保管关系。

动作：移动、观察、等待、交谈、试探、隐瞒、传话、请安、访友、探病、写/读/藏/交付信件、赠礼/拒礼/转交、赴约/回避/邀请、休息、服药、用饭、写诗/领域活动。

## 3. 正典分层

- PastCanon：当前时点已发生。
- CharacterCanon：身份/经历/关系/人格边界。
- FutureCanon：只供正典控制，不注入当前人物观察。
- Completion：必须有类别、支持来源、置信度、review_status、can_enter_canon=false 默认。

## 4. 三种 Evolution Policy

- Canonical Replay：关键节点锁定。
- Soft Canon：未来事件为吸引子/条件图，可被强因果链改变。
- Living/Open：未来 Canon 仅比较基线，允许开放演化。

三个模式共享同一 Runtime，仅 Policy 不同。

## 5. 七日验收

1. 固定快照启动。
2. Day1 用户接管林黛玉。
3. 委托紫鹃传话。
4. 紫鹃可接受/改变方式/拒绝。
5. 消息按实际可达/可听/转交链传播，无全知泄漏。
6. 信件位置、保管、密封/阅读状态持续。
7. 人物按日程生活并受身体/职责/邀请约束。
8. Day3 用户退出，AI 按授权恢复控制。
9. Day3 Fork；Parent 不变化。
10. Day7 全事件可 replay 重建。
11. 比较 Canon / 用户 / 无人干预三条世界线。
12. 每条 Canon/Completion/Generated 内容可识别来源级别。
13. 运行中 WorldPack 母本不被修改。
14. 可从一条长期/加速 Worldline 生成 Promotion Candidate，但不得自动覆盖原著世界定义。
