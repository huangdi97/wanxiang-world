"""Simplified Chinese Player copy for optional T3 spatial-scene upgrades."""

from __future__ import annotations

_SPATIAL_STRINGS: dict[str, str] = {
    "spatial_stage_enter": "进入空间场景",
    "spatial_stage_exit": "返回视觉场景",
    "spatial_stage_error": "空间渲染器加载失败；已保留当前视觉场景。",
    "spatial_stage_reset": "复位视角",
    "spatial_stage_controls_hint": "拖动旋转 · 滚轮缩放 · 方向键/WASD 调整视角",
    "spatial_stage_point_count": "{place} · {count} 个空间点",
    "spatial_upgrade_eyebrow": "空间升级",
    "spatial_upgrade_heading": "把这个地点升级为空间场景",
    "spatial_upgrade_submit": "生成空间场景",
    "spatial_upgrade_retry": "重新生成空间场景",
    "spatial_upgrade_refresh": "刷新生成状态",
    "spatial_upgrade_available": (
        "{place} 可生成空间场景 · 本次预计 {cost}；世界剩余 {remaining} 个预算单位"
    ),
    "spatial_upgrade_pending": "{place} 的空间场景正在生成 · {state}",
    "spatial_upgrade_ambiguous": (
        "{place} 的远端提交结果未确认。为避免重复付费，万相不会自动重提；"
        "当前视觉场景仍可使用，请先核对 Provider 任务或账单后再恢复。"
    ),
    "spatial_upgrade_ready": "{place} 的空间场景已就绪 · {count} 个空间资产",
    "spatial_upgrade_terminal": "{place} 的空间任务状态：{state}。现有场景仍可继续使用。",
    "spatial_upgrade_unavailable_provider": "当前未配置空间生成器；现有插画场景仍可正常使用。",
    "spatial_upgrade_unavailable_network": "空间生成器当前未获准联网；现有场景不受影响。",
    "spatial_upgrade_unavailable_rights": "来源未授权外部空间生成；继续使用本地/已有视觉。",
    "spatial_upgrade_unavailable_privacy": "当前空间生成器不满足此来源的隐私要求。",
    "spatial_upgrade_unavailable_budget": "当前空间生成预算不足。",
    "spatial_upgrade_state_submission_ambiguous": "提交结果未确认",
    "spatial_upgrade_state_submitted": "已提交",
    "spatial_upgrade_state_queued": "排队中",
    "spatial_upgrade_state_running": "生成中",
    "spatial_upgrade_state_verified": "已验证",
    "spatial_upgrade_state_attached": "已就绪",
    "spatial_upgrade_state_failed": "生成失败",
    "spatial_upgrade_state_cancelled": "已取消",
    "spatial_upgrade_state_expired": "已过期",
    "status_spatial_submitted": "{place} 的空间场景任务已提交；你可以继续使用当前世界。",
    "status_spatial_refreshed": "空间场景状态已刷新。",
}
