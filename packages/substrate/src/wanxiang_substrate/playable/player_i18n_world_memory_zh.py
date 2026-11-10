"""World-memory, consequence and world-card copy for the Player surface."""

# ruff: noqa: E501

from __future__ import annotations

STRINGS: dict[str, str] = {
    "visual_tier_t0": "T0 · 离线场景",
    "visual_tier_t1": "T1 · 高质量场景",
    "visual_tier_t3": "T3 · 3D 空间",
    "change_status_from": "{subject}的状态：{before} → {after}",
    "delta_absent": "未记录",
    "delta_removed": "已移除",
    "delta_yes": "是",
    "delta_no": "否",
    "chronicle_details": "记录说明",
    "atlas_relation_route": "\u8def\u7ebf",
    "atlas_relation_default": "\u6765\u6e90\u5173\u7cfb",
    "visual_proof_heading": "视觉说明",
    "list_separator": "\u3001",
    "label_separator": "\uff1a",
    "panorama_stage_aria": "360 \u5ea6\u5168\u666f",
    "observer_gate_copy": "你正在观察这个世界：角色没有移动，世界也没有因为你改变。",
    "observer_gate_action": "选择角色进入",
    "visual_tier_short_t0": "离线场景",
    "visual_tier_short_t1": "高清场景",
    "visual_tier_short_t2": "全景场景",
    "visual_tier_short_t3": "可探索空间",
    "world_card_visual_alt": "{world}的世界视觉",
    "world_card_place": "最近地点：{place}",
    "world_card_time": "世界时刻 {time}",
    "world_card_happening": "最近事件：{event}",
    "world_card_continue": "可以继续",
    "world_card_enter": "可以进入",
    "world_card_no_facts": "进入后会读取此刻的世界状态",
    "world_card_no_visual": "尚未生成世界视觉",
    "chronicle_who_you": "你",
}
