from __future__ import annotations

STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
STEM_ELE = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
BRANCH_ELE = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土",
              "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金",
              "戌": "土", "亥": "水"}
BRANCH_YINYANG = {"子": "阳", "丑": "阴", "寅": "阳", "卯": "阴",
                  "辰": "阳", "巳": "阴", "午": "阳", "未": "阴",
                  "申": "阳", "酉": "阴", "戌": "阳", "亥": "阴"}

# 奇门九宫顺序（排盘飞布用）
PALACE_POSITIONS = [
    ("坎一宫", 1), ("坤二宫", 2), ("震三宫", 3), ("巽四宫", 4),
    ("中五宫", 5), ("乾六宫", 6), ("兑七宫", 7), ("艮八宫", 8), ("离九宫", 9)
]
# 八门顺序（值使起）
DOOR_ORDER = ["休", "生", "伤", "杜", "景", "死", "惊", "开"]
# 九星顺序（值符起）
STAR_ORDER = ["蓬", "任", "冲", "辅", "英", "芮", "柱", "心", "禽"]


class QimenPrecisionEngine:
    """V3 Qimen precision engine.

    Computes: value-fu (值符) / value-shi (值使) palace position,
    heaven-plate / earth-plate stem/branch for each palace,
    empty palace detection, horse star position.
    """

    def analyze(self, bureau: dict, board: dict, domain: str, question: str) -> dict:
        dun = bureau.get("dun", "阳遁")
        ju = bureau.get("ju_number", 4)
        stem_branch = bureau.get("stem_branch_hour", "甲戌")
        hour_stem = stem_branch[0]
        hour_branch = stem_branch[1] if len(stem_branch) >= 2 else "戌"

        # 值符宫 = 时干所在宫
        val_fu_palace = self._stem_to_palace(hour_stem, board)
        # 值使宫 = 八门顺排到时支位置
        val_shi_palace = self._branch_to_palace(hour_branch, board)

        # 天盘干：值符在本宫，其余按洛书顺序飞布
        heaven_plate = self._heaven_plate(val_fu_palace, board)
        # 地盘干：本宫地盘固定
        earth_plate = self._earth_plate()
        # 马星：寅申亥巳
        horse_palace = self._horse_star(hour_branch, board)
        # 空亡宫（时干不在的宫）
        empty_palaces = self._empty_palaces(hour_stem, board)

        return {
            "value_fu": {"palace": val_fu_palace, "note": "时干所在宫"},
            "value_shi": {"palace": val_shi_palace, "note": "时支对应宫"},
            "heaven_plate": heaven_plate,
            "earth_plate": earth_plate,
            "horse_star": horse_palace,
            "empty_palaces": empty_palaces,
            "agent_hint": self._agent_hint(val_fu_palace, val_shi_palace, domain)
        }

    def _stem_to_palace(self, stem: str, board: dict) -> str:
        for name, data in board.items():
            if data.get("stem") == stem:
                return name
        # fallback: 壬甲落中宫
        return "中五宫"

    def _branch_to_palace(self, branch: str, board: dict) -> str:
        for name, data in board.items():
            if data.get("branch") == branch:
                return name
        return "中五宫"

    def _heaven_plate(self, val_fu_palace: str, board: dict) -> dict:
        result = {}
        pos_order = ["坎一宫", "坤二宫", "震三宫", "巽四宫", "中五宫", "乾六宫", "兑七宫", "艮八宫", "离九宫"]
        val_idx = next((i for i, p in enumerate(pos_order) if p == val_fu_palace), 4)
        val_stem = board.get(val_fu_palace, {}).get("stem", "甲")
        val_stem_idx = STEMS.index(val_stem) if val_stem in STEMS else 0
        for i, pal in enumerate(pos_order):
            stem_idx = (val_stem_idx + i - val_idx) % 10
            result[pal] = STEMS[stem_idx]
        return result

    def _earth_plate(self) -> dict:
        return {
            "坎一宫": "子", "坤二宫": "未", "震三宫": "卯", "巽四宫": "辰",
            "中五宫": "中", "乾六宫": "戌", "兑七宫": "酉", "艮八宫": "丑", "离九宫": "午"
        }

    def _horse_star(self, hour_branch: str, board: dict) -> str:
        if hour_branch not in ["寅", "申", "亥", "巳"]:
            return "无马星"
        horse_map = {"寅": "申", "申": "寅", "亥": "巳", "巳": "亥"}
        target_branch = horse_map.get(hour_branch, "")
        for name, data in board.items():
            if data.get("branch") == target_branch:
                return name
        return "无马星"

    def _empty_palaces(self, hour_stem: str, board: dict) -> list[str]:
        used_stems = {data.get("stem", "") for data in board.values() if data.get("stem")}
        missing = [stem for stem in STEMS if stem not in used_stems]
        return missing

    def _agent_hint(self, val_fu: str, val_shi: str, domain: str) -> str:
        hints = {
            "relationship": f"值符{val_fu}、值使{val_shi}，主客关系清晰，适合关系推进",
            "business": f"值符{val_fu}主资源，值使{val_shi}主执行，适合商业决策",
            "content": f"值符{val_fu}主声量，值使{val_shi}主节奏，适合内容发布",
            "strategy": f"值符{val_fu}主战略，值使{val_shi}主落地，适合系统布局",
        }
        return hints.get(domain, f"值符{val_fu}、值使{val_shi}")