from __future__ import annotations

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class IChingEngine:
    """V4 I Ching trend transition engine.

    V4 scope:
    - full 64 hexagram semantic dataset
    - deterministic semantic hexagram selection from question/domain/context
    - changed hexagram placeholder based on text/time seed
    - trend stage and action strategy output

    This engine is for trend modeling, not deterministic divination.
    """

    def __init__(self) -> None:
        self.hexagrams = json.loads((DATA_DIR / "iching_64_hexagrams.json").read_text(encoding="utf-8"))
        self.names = list(self.hexagrams.keys())

    def analyze(self, text: str, domain: str = "unknown", event_time: str | None = None) -> dict:
        primary_name = self._pick_primary(text, domain)
        primary = dict(self.hexagrams[primary_name])
        primary["name"] = primary_name
        changing_lines = self._changing_lines(text, event_time)
        changed_name = self._changed_hexagram(primary_name, changing_lines)
        changed = dict(self.hexagrams[changed_name])
        changed["name"] = changed_name
        return {
            "status": "ok",
            "primary_hexagram": primary,
            "changing_lines": changing_lines,
            "changed_hexagram": changed,
            "transition": self._transition(primary, changed, changing_lines),
            "stage_warning": self._stage_warning(changing_lines, primary, changed),
            "action_hint": self._action_hint(primary, changed),
            "principle": "易经层用于趋势演化建模，必须受现实证据和多路径推演约束"
        }

    def _pick_primary(self, text: str, domain: str) -> str:
        rules = [
            (["开始", "启动", "新项目", "开局"], "水雷屯"),
            (["信息不足", "不懂", "学习", "迷茫"], "山水蒙"),
            (["等待", "时机", "什么时候"], "水天需"),
            (["争议", "冲突", "官司", "吵"], "天水讼"),
            (["团队", "组织", "带人"], "地水师"),
            (["合作", "连接", "关系"], "水地比"),
            (["发布", "曝光", "展示", "内容"], "火天大有" if domain == "content" else "天火同人"),
            (["卡", "阻碍", "困难"], "水山蹇"),
            (["解除", "化解", "松动"], "雷水解"),
            (["止损", "减少", "收缩"], "山泽损"),
            (["增长", "加码", "扩张"], "风雷益"),
            (["决断", "切割", "摊牌"], "泽天夬"),
            (["变革", "重做", "升级"], "泽火革"),
            (["稳定", "长期", "持续"], "雷风恒"),
            (["完成", "已经成", "落地"], "水火既济"),
            (["未完成", "还没", "未来"], "火水未济"),
        ]
        for words, name in rules:
            if any(w in text for w in words):
                return name
        if domain == "strategy": return "乾为天"
        if domain == "business": return "地天泰"
        if domain == "relationship": return "泽山咸"
        if domain == "content": return "风火家人"
        return "火水未济"

    def _changing_lines(self, text: str, event_time: str | None) -> list[int]:
        seed = len(text) + (sum(ord(c) for c in event_time) if event_time else 0)
        first = seed % 6 + 1
        if seed % 3 == 0:
            second = (first + 2) % 6 + 1
            return sorted(set([first, second]))
        return [first]

    def _changed_hexagram(self, primary_name: str, changing_lines: list[int]) -> str:
        idx = self.names.index(primary_name)
        shift = sum(changing_lines)
        return self.names[(idx + shift) % len(self.names)]

    def _transition(self, primary: dict, changed: dict, lines: list[int]) -> str:
        return f"本卦{primary['name']}：{primary['trend']}；变爻{lines}后趋向{changed['name']}：{changed['trend']}。"

    def _stage_warning(self, lines: list[int], primary: dict, changed: dict) -> list[str]:
        warns = []
        if any(i in [1, 2] for i in lines): warns.append("变化发生在早期，先稳基础，不要急于放大投入")
        if any(i in [3, 4] for i in lines): warns.append("变化发生在中段，重点看执行过程与外部反馈")
        if any(i in [5, 6] for i in lines): warns.append("变化发生在后段，注意结果收口、名实匹配和过度消耗")
        warns.append(f"本卦风险：{primary['risk']}")
        warns.append(f"变卦风险：{changed['risk']}")
        return warns

    def _action_hint(self, primary: dict, changed: dict) -> str:
        return f"先按本卦策略：{primary['strategy']}；同时预留变卦方向：{changed['strategy']}。"
