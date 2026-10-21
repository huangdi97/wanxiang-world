"""Simplified Chinese Player copy for explicit T2 panorama upgrades."""

from __future__ import annotations

_PANORAMA_STRINGS: dict[str, str] = {
    "panorama_stage_enter": "进入全景",
    "panorama_stage_exit": "返回视觉场景",
    "panorama_stage_error": "全景渲染器加载失败；已保留当前视觉场景。",
    "panorama_upgrade_eyebrow": "全景升级",
    "panorama_upgrade_heading": "把这个地点升级为可环视全景",
    "panorama_upgrade_submit": "生成全景场景",
    "panorama_upgrade_ready": "{place} 已有可交互全景；进入世界后可以环视。",
    "panorama_upgrade_available": ("{place} 可升级全景 · 预计 {cost}；世界预算余 {remaining}/{budget}"),
    "panorama_upgrade_unavailable_provider": (
        "当前未配置可用的全景生成器；现有视觉场景仍可正常使用。"
    ),
    "panorama_upgrade_unavailable_network": ("全景生成器当前未获准联网；现有视觉场景不受影响。"),
    "panorama_upgrade_unavailable_rights": ("来源未授权外部全景生成；继续使用本地/已有视觉。"),
    "panorama_upgrade_unavailable_privacy": "当前全景生成器不满足此来源的隐私要求。",
    "panorama_upgrade_unavailable_budget": "当前世界剩余预算不足以生成新的全景。",
    "status_panorama_generated": "{place} 的全景场景已生成并缓存。",
}
