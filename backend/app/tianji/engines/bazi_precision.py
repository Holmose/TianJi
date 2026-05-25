from __future__ import annotations

STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
STEM_ELE = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
BRANCH_ELE = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土",
              "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金",
              "戌": "土", "亥": "水"}

GOD_TABLE = {
    "甲": {"甲": "比", "乙": "劫", "丙": "食", "丁": "伤", "戊": "财",
           "己": "才", "庚": "杀", "辛": "官", "壬": "枭", "癸": "印"},
    "乙": {"甲": "劫", "乙": "比", "丙": "伤", "丁": "食", "戊": "才",
           "己": "财", "庚": "官", "辛": "杀", "壬": "印", "癸": "枭"},
    "丙": {"甲": "枭", "乙": "印", "丙": "比", "丁": "劫", "戊": "食",
           "己": "伤", "庚": "财", "辛": "才", "壬": "杀", "癸": "官"},
    "丁": {"甲": "印", "乙": "枭", "丙": "劫", "丁": "比", "戊": "伤",
           "己": "食", "庚": "才", "辛": "财", "壬": "官", "癸": "杀"},
    "戊": {"甲": "杀", "乙": "官", "丙": "枭", "丁": "印", "戊": "比",
           "己": "劫", "庚": "食", "辛": "伤", "壬": "财", "癸": "才"},
    "己": {"甲": "官", "乙": "杀", "丙": "印", "丁": "枭", "戊": "劫",
           "己": "比", "庚": "伤", "辛": "食", "壬": "才", "癸": "财"},
    "庚": {"甲": "财", "乙": "才", "丙": "杀", "丁": "官", "戊": "枭",
           "己": "印", "庚": "比", "辛": "劫", "壬": "食", "癸": "伤"},
    "辛": {"甲": "才", "乙": "财", "丙": "官", "丁": "杀", "戊": "印",
           "己": "枭", "庚": "劫", "辛": "比", "壬": "伤", "癸": "食"},
    "壬": {"甲": "食", "乙": "伤", "丙": "财", "丁": "才", "戊": "杀",
           "己": "官", "庚": "枭", "辛": "印", "壬": "比", "癸": "劫"},
    "癸": {"甲": "伤", "乙": "食", "丙": "才", "丁": "财", "戊": "官",
           "己": "杀", "庚": "印", "辛": "枭", "壬": "劫", "癸": "比"},
}


class BaziPrecisionEngine:
    """V3 Precision Bazi engine.

    Adds: useful god / forbidden god, hidden stems analysis,
    lunar month correction, day stem-cycle index for 60-cycle mapping.
    """

    def analyze(self, pillars: dict, day_master: dict, strong_weak: str,
                dominant: str, balance: dict) -> dict:
        dm_stem = day_master["stem"]
        dm_ele = day_master["element"]
        month_stem = pillars["month"][0]
        month_branch = pillars["month"][1]
        month_ele = BRANCH_ELE[month_branch]

        useful = self._calc_useful(dm_stem, strong_weak)
        avoid = self._calc_avoid(dm_stem, strong_weak)
        hidden = self._hidden_stems(pillars)
        month_correction = self._month_correction(month_branch)
        day_idx = STEMS.index(dm_stem)

        agent_params = self._agent_params(dm_stem, dm_ele, strong_weak, useful, avoid)

        return {
            "useful_god": useful,
            "forbidden_god": avoid,
            "hidden_stems": hidden,
            "month_correction": month_correction,
            "agent_params": agent_params
        }

    def _calc_useful(self, dm_stem: str, strong_weak: str) -> dict:
        if "强" in strong_weak:
            targets = ["财", "才", "官", "杀"]
        else:
            targets = ["印", "枭", "比", "劫"]
        stars = self._find_stems(dm_stem, targets)
        note = "身强宜财官抑身" if "强" in strong_weak else "身弱宜印比生扶"
        return {"stems": stars, "note": note}

    def _calc_avoid(self, dm_stem: str, strong_weak: str) -> dict:
        if "强" in strong_weak:
            targets = ["比", "劫", "印", "枭"]
        else:
            targets = ["财", "才", "官", "杀"]
        stars = self._find_stems(dm_stem, targets)
        note = "比劫过旺则争宜收敛" if "强" in strong_weak else "财官过重则压身"
        return {"stems": stars, "note": note}

    def _find_stems(self, dm_stem: str, targets: list[str]) -> list[str]:
        table = GOD_TABLE.get(dm_stem, {})
        return [stem for stem, god in table.items() if stem != dm_stem and god in targets]

    def _hidden_stems(self, pillars: dict) -> dict:
        BRANCH_HIDDEN = {
            "子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"],
            "卯": ["乙"], "辰": ["戊", "乙", "癸"], "巳": ["丙", "戊", "庚"],
            "午": ["丁", "己"], "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"],
            "酉": ["辛"], "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]
        }
        return {key: BRANCH_HIDDEN.get(pillars[key][1], [pillars[key][1]]) for key in ["year", "month", "day", "hour"]}

    def _month_correction(self, month_branch: str) -> str:
        return {
            "寅": "立春", "卯": "惊蛰", "辰": "清明", "巳": "立夏",
            "午": "芒种", "未": "小暑", "申": "立秋", "酉": "白露",
            "戌": "寒露", "亥": "立冬", "子": "大雪", "丑": "小寒"
        }.get(month_branch, month_branch)

    def _agent_params(self, dm_stem: str, dm_ele: str, strong_weak: str,
                      useful: dict, avoid: dict) -> dict:
        risk_map = {
            "偏强": "高压下容易走极端，过度扩张后失控",
            "身强": "刚毅果断但易刚愎自用，不听劝告",
            "偏弱": "韧性好但犹豫，外部压力下容易放弃",
            "身弱": "依赖心强但敏感，需要外部认可维持动力",
            "中和": "适应力强但缺乏主心骨，容易随波逐流"
        }
        return {
            "emotional_pattern": risk_map.get(strong_weak, "需结合具体局面判断"),
            "useful_action": f"宜用{useful['stems']}引导方向",
            "forbidden_action": f"忌用{avoid['stems']}硬推",
            "growth_direction": self._growth_hint(dm_stem, strong_weak)
        }

    def _growth_hint(self, dm_stem: str, strong_weak: str) -> str:
        hints = {
            "偏强": "学习柔性和合作，补水、金属性短板",
            "身强": "练格局感和战略眼光，不过刚",
            "偏弱": "建立稳定能量源，补土、火属性基础",
            "身弱": "培养内核和独立性，减少依赖外部评价",
            "中和": "专注单点突破，避免分散精力"
        }
        return hints.get(strong_weak, "持续观察和修正")