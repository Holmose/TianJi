"""
RelationshipEngine V5.1 — 人间关系推演引擎
集成松哥撩妹系统：判断能不能做 + 该怎么做
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class RelationshipEngine:
    """人间关系推演引擎 V5.1"""

    HEXAGRAM_MAP = {
        "性格冲突": {"primary": "泽山咸", "secondary": "雷泽归妹"},
        "关系危机": {"primary": "雷泽归妹", "secondary": "水天需"},
        "边界困扰": {"primary": "地天泰", "secondary": "天泽履"},
        "情感困惑": {"primary": "地天泰", "secondary": "天泽履"},
    }

    def __init__(self):
        data_dir = DATA_DIR

        # 卦象元数据
        hex_path = data_dir / "relationship_hexagrams.json"
        with open(hex_path, encoding="utf-8") as f:
            self._hex_data = json.load(f)

        # judgment data — 能不能做 + 该怎么做
        jdg_path = data_dir / "relationship_judgment.json"
        with open(jdg_path, encoding="utf-8") as f:
            self._jdg_data = json.load(f)

        self._std_hex = {}
        std_path = data_dir / "iching_64_hexagrams.json"
        if std_path.exists():
            raw = json.load(open(std_path, encoding="utf-8"))
            # keys are hexagram names (e.g. "地天泰"), values have "gua" field
            self._std_hex = {name: data for name, data in raw.items()}

    # ── helpers ──────────────────────────────────────────────────────────────

    def _match_hexagram_key(self, conflict_type: str, question: str) -> str:
        keywords_map = {
            "性格冲突": ["急", "慢", "不合", "节奏", "性格", "三观", "磨合", "摩擦"],
            "关系危机": ["分手", "危机", "离婚", "冷淡", "冷战", "她说", "他想", "要分", "断了", "挽回", "挽留"],
            "边界困扰": ["边界", "控制", "报备", "查岗", "隐私", "空间", "窒息", "限制", "管"],
            "情感困惑": ["怀疑", "不确定", "猜", "她爱不爱", "是不是", "迷茫", "困惑", "内耗"],
        }
        text = question.lower()
        for key, words in keywords_map.items():
            if any(w in text for w in words):
                return key
        return conflict_type if conflict_type in self.HEXAGRAM_MAP else "性格冲突"

    def _get_hexagram(self, name: str) -> Optional[Dict[str, Any]]:
        if name in self._hex_data:
            return self._hex_data[name]
        for h in self._hex_data.values():
            if h.get("gua") == name:
                return h
        return self._std_hex.get(name) or None

    def _assess_acceptance(self, conflict_type: str, duration: str) -> Dict[str, Any]:
        months = 0
        try:
            d = duration.lower()
            if "年" in d:
                months = int(float(d.replace("年", "").replace("以上", ""))) * 12
            elif "月" in d:
                months = int(float(d.replace("个月", "").replace("月", "").replace("以上", "")))
            elif "天" in d or "周" in d:
                return {"level": "高", "score": 0.85, "compromise_signals": 0, "accept_signals": 1}
        except:
            pass

        if months >= 12:
            score, level = 0.75, "中"
            signals = 2
        elif months >= 6:
            score, level = 0.60, "中"
            signals = 1
        else:
            score, level = 0.30, "低（你在让步，不是在接受）"
            signals = 0

        return {
            "level": level,
            "score": score,
            "compromise_signals": signals,
            "accept_signals": 0,
        }

    def _assess_ying_di(self, conflict_type: str, question: str) -> Dict[str, Any]:
        danger_words = ["分手", "离婚", "要分", "断了", "冷战", "冷战"]
        support_words = ["想清楚", "怎么走", "方向", "该怎么做", "该不该"]
        text = question.lower()

        if any(w in text for w in danger_words):
            return {
                "label": "偏危",
                "description": "关系出现明显裂痕，需要先修复才能谈其他",
            }
        if any(w in text for w in support_words):
            return {
                "label": "待观察",
                "description": "信号不明确，需要更多现实反馈来判断",
            }
        return {
            "label": "待观察",
            "description": "方向暂时一致，但需留意后续动态",
        }

    def _assess_direction(self, conflict_type: str, question: str) -> Dict[str, Any]:
        positive = ["一起", "共同", "愿意", "想", "一起", "磨合", "调整"]
        negative = ["各自", "分开", "分手", "算了", "管她"]
        text = question.lower()
        pos = sum(1 for w in positive if w in text)
        neg = sum(1 for w in negative if w in text)
        if pos > neg:
            return {"status": "一致", "description": "双方有意愿往同一个方向走"}
        if neg > pos:
            return {"status": "分歧", "description": "至少有一方已经在考虑退出"}
        return {"status": "待验证", "description": "方向是否一致需要更多现实反馈"}

    # ── public ───────────────────────────────────────────────────────────────

    def analyze(
        self,
        question: str,
        conflict_type: str,
        party_a_desc: str = "",
        party_b_desc: str = "",
        conflict_event: str = "",
        duration: str = "",
    ) -> Dict[str, Any]:
        # 1. 卦象
        hexagram_key = self._match_hexagram_key(conflict_type, question)
        primary_key = self.HEXAGRAM_MAP.get(hexagram_key, {}).get("primary", "地天泰")
        primary_hex = self._get_hexagram(primary_key) or {}
        secondary_key = self.HEXAGRAM_MAP.get(hexagram_key, {}).get("secondary", "地天泰")
        secondary_hex = self._get_hexagram(secondary_key) or {}

        # 2. 能不能做 — 松哥系统判断
        jdg = self._jdg_data.get(hexagram_key, self._jdg_data["性格冲突"])

        # 判断能不能做：看question里有没有关键词
        text = question.lower()
        can_do_key = "能做"
        if any(w in text for w in ["不行", "不可能", "能挽回吗", "还能救吗"]):
            can_do_key = "难做"
        if any(w in text for w in ["分手", "决心", "她不要", "她不想", "算了"]):
            can_do_key = "不能做"

        can_do_entry = jdg["能做吗"].get(can_do_key, jdg["能做吗"]["难做"])

        # 3. 该怎么做 — 从judgment数据读取每个动作的指引
        action_map = jdg.get("该怎么做", {})
        recommended_action = self._decide_action(
            conflict_type, question, hexagram_key, action_map
        )

        # 4. 接受度 & 应/敌
        acceptance = self._assess_acceptance(conflict_type, duration)
        ying_di = self._assess_ying_di(conflict_type, question)
        direction = self._assess_direction(conflict_type, question)

        # 5. 组装输出
        return {
            # 卦象层
            "primary_hexagram": primary_hex,
            "secondary_hexagram": secondary_hex,
            "hexagram_key": hexagram_key,
            # 松哥系统核心判断
            "can_do": {
                "level": can_do_key,
                "description": can_do_entry,
            },
            "action_guidance": {
                "recommended": recommended_action["action"],
                "description": recommended_action["description"],
                "all_actions": {
                    act: desc
                    for act, desc in action_map.items()
                    if act in ("接住", "起伏", "勾子", "推进", "回收")
                },
            },
            "prohibited": jdg.get("不能做", "无明确禁忌"),
            "philosophy": {
                "core_hexagram": jdg.get("核心卦象", ""),
                "acceptance": jdg.get("接受哲学", ""),
            },
            # 辅助判断
            "acceptance": acceptance,
            "ying_di": ying_di,
            "direction": direction,
            "verdict": self._make_verdict(
                hexagram_key, can_do_key, recommended_action["action"], acceptance, ying_di
            ),
        }

    # ── 动作决策 ─────────────────────────────────────────────────────────────

    def _decide_action(
        self,
        conflict_type: str,
        question: str,
        hexagram_key: str,
        action_map: Dict[str, str],
    ) -> Dict[str, str]:
        text = question.lower()

        # 危机/冷淡 → 回收
        crisis_words = ["分手", "冷战", "冷淡", "她不回", "要分", "断了"]
        if any(w in text for w in crisis_words):
            return {"action": "回收", "description": action_map.get("回收", "先冷静，给彼此空间")}

        # 情绪/试探/示弱 → 接住
        emotion_words = ["委屈", "难过", "伤心", "累了", "她说", "她觉得", "不安", "怕", "担心"]
        if any(w in text for w in emotion_words):
            return {"action": "接住", "description": action_map.get("接住", "先接住她的情绪")}

        # 推进意图 → 看时机
        push_words = ["想升温", "想推进", "想暧昧", "要不要约", "该表白吗"]
        if any(w in text for w in push_words):
            return {"action": "推进", "description": action_map.get("推进", "时机未到，不追进度")}

        # 边界控制
        control_words = ["管太多", "控制", "查岗", "报备"]
        if any(w in text for w in control_words):
            return {"action": "起伏", "description": action_map.get("起伏", "用信任感替代控制感")}

        # 默认按冲突类型给
        defaults = {
            "性格冲突": "起伏",
            "关系危机": "回收",
            "边界困扰": "接住",
            "情感困惑": "接住",
        }
        action = defaults.get(hexagram_key, "接住")
        return {"action": action, "description": action_map.get(action, "按实际情况处理")}

    def _make_verdict(
        self,
        hexagram_key: str,
        can_do_level: str,
        action: str,
        acceptance: Dict[str, Any],
        ying_di: Dict[str, Any],
    ) -> Dict[str, Any]:
        verdict_map = {
            "能做": "关系有改善空间，{action}是当前重点。",
            "难做": "修复难度大，先做{action}观察反应，不要强推。",
            "不能做": "她在拒绝接住你，方向有分歧，先回收。",
        }
        template = verdict_map.get(can_do_level, verdict_map["难做"])
        one_liner = template.format(action=action)
        if acceptance.get("score", 0) < 0.4:
            one_liner += f" 接受度{acceptance['level']}，注意节奏。"
        if ying_di.get("label") == "偏危":
            one_liner += " 关系偏危，优先止损。"
        return {"one_liner": one_liner, "full": one_liner}

    # ── report ────────────────────────────────────────────────────────────────

    def generate_report(self, result: Dict[str, Any]) -> str:
        lines = [
            "# 人间关系推演报告",
            "",
            f"**场景类型**：{result['hexagram_key']}",
            f"**主卦**：{result['primary_hexagram'].get('name', 'N/A')}（{result['primary_hexagram'].get('gua', '')}）",
            f"**副卦**：{result['secondary_hexagram'].get('name', 'N/A')}（{result['secondary_hexagram'].get('gua', '')}）",
            "",
            "## 能不能做",
            f"**结论**：{result['can_do']['level']}",
            f"{result['can_do']['description']}",
            "",
            "## 该怎么做",
            f"**推荐动作**：{result['action_guidance']['recommended']}",
            f"{result['action_guidance']['description']}",
            "",
            "| 动作 | 指引 |",
            "|------|------|",
        ]
        for act, desc in result["action_guidance"]["all_actions"].items():
            lines.append(f"| {act} | {desc} |")

        lines += [
            "",
            "## 禁止动作",
            f"⚠️ {result['prohibited']}",
            "",
            "## 核心卦象",
            f"**{result['philosophy']['core_hexagram']}**",
            "",
            f"_{result['philosophy']['acceptance']}_",
            "",
            "## 接受度",
            f"**等级**：{result['acceptance']['level']}（{result['acceptance']['score']}）",
            "",
            "## 应/敌判断",
            f"**标签**：{result['ying_di']['label']}",
            f"{result['ying_di']['description']}",
            "",
            "## 方向判断",
            f"**状态**：{result['direction']['status']}",
            f"{result['direction']['description']}",
            "",
            "---",
            f"**判词**：{result['verdict']['one_liner']}",
        ]
        return "\n".join(lines)