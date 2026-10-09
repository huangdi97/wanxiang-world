"""Language cues used by the deterministic local semantic provider."""

from __future__ import annotations

import re

_CHINESE = r"\u4e00-\u9fff"
_CUE = r"说|道|问|答|称|表示|指出|认为|告诉|回忆|喊|叫道|开口"
_TITLE = r"同志|先生|女士|书记|局长|主任|市长|县长|部长|厅长|科长|处长|校长|老师"
_PLACE_SUFFIX = (
    r"省|市|县|区|镇|乡|村|路|街|巷|院|厂|公司|学校|大学|医院|站|馆|楼|"
    r"山|河|桥|城|宫|府|寺|塔|谷|岛|港|湖|园|殿|门|亭|洞|关|寨|庄|阁|堂"
)
_EVENT_CUES = (
    "到达",
    "离开",
    "返回",
    "进入",
    "发生",
    "召开",
    "决定",
    "见面",
    "谈话",
    "签署",
    "任命",
    "调查",
    "逮捕",
    "死亡",
    "出生",
    "结婚",
    "冲突",
    "转移",
    "来到",
    "赶到",
    "访问",
    "拜访",
    "开始",
    "结束",
    "发现",
    "接受",
    "拒绝",
    "同意",
    "要求",
    "宣布",
    "成立",
    "参加",
    "离职",
)
_RELATION_WORDS = {
    "夫妻": "spouse",
    "父亲": "parent",
    "母亲": "parent",
    "兄弟": "sibling",
    "姐妹": "sibling",
    "朋友": "friend",
    "同事": "colleague",
    "领导": "authority",
    "下属": "subordinate",
    "同学": "classmate",
}
_COMMON_FALSE_NAMES = {
    "我们",
    "他们",
    "她们",
    "这个",
    "那个",
    "事情",
    "时候",
    "因为",
    "所以",
    "已经",
    "可以",
    "没有",
    "自己",
    "什么",
    "这里",
    "那里",
    "现在",
    "后来",
    "一天",
    "第二",
}
_ENGLISH_FALSE_NAMES = {"The", "This", "That", "Alice", "Bob", "Chapter"}


def _identity_key(name: str) -> str:
    if all("\u4e00" <= char <= "\u9fff" for char in name):
        return f"zh:{name}"
    return re.sub(r"[^a-z0-9]+", "|", name.lower()).strip("|")


def _clean(value: str, limit: int = 96) -> str:
    return re.sub(r"\s+", " ", value).strip(" \t\r\n,，。；;:：()（）[]【】\"'")[:limit]
