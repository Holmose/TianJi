"""V3 Enhanced Qimen Situation Engine with structural layout."""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _load_json(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)

JIU_GONG = _load_json("jiugong.json")
BA_MEN = _load_json("bamen.json")
JIU_XING = _load_json("jiuxing.json")
BA_SHEN = _load_json("bashen.json")
SANQI = _load_json("qimen_sanqi.json")

BRANCH_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"
}
BRANCH_ZODIAC = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GUA_ZHANG = {"子": "甲子", "丑": "甲丑", "寅": "甲寅", "卯": "甲卯", "辰": "甲辰",
             "巳": "甲巳", "午": "甲午", "未": "甲未", "申": "甲申", "酉": "甲酉",
             "戌": "甲戌", "亥": "甲亥"}

SHUN_DUN_RULES = {
    "子": "冬", "丑": "冬", "寅": "春", "卯": "春", "辰": "春",
    "巳": "夏", "午": "夏", "未": "夏",
    "申": "秋", "酉": "秋", "戌": "秋", "亥": "冬"
}

# 阳遁顺行序（数字对应九宫位置：1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离）
YANG_DUN_POSITIONS = {1: 1, 2: 8, 3: 3, 4: 4, 5: 9, 6: 2, 7: 7, 8: 6, 9: 5}
# 阴遁逆行序
YIN_DUN_POSITIONS = {1: 9, 2: 6, 3: 4, 4: 7, 5: 5, 6: 3, 7: 8, 8: 2, 9: 1}

DOOR_SORT_ORDER = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门"]
STAR_SORT_ORDER = ["蓬", "任", "冲", "辅", "英", "芮", "柱", "心", "禽"]
GOD_SORT_ORDER = ["符", "蛇", "阴", "合", "虎", "武", "地", "天"]

PALACE_ORDER = ["坎一宫", "坤二宫", "震三宫", "巽四宫", "中五宫",
                "乾六宫", "兑七宫", "艮八宫", "离九宫"]

def _parse_dt(value: str) -> datetime:
    for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError("event_time must be YYYY-MM-DD or YYYY-MM-DD HH:MM")

def _get_yin_yang(dt: datetime) -> str:
    month = dt.month
    if month in [11, 12, 1]:
        return "阴遁"
    return "阳遁"

def _calc_ju_number(dt: datetime, dun: str) -> int:
    branch_idx = (dt.month + dt.day) % 9
    if branch_idx == 0:
        branch_idx = 9
    if dun == "阴遁":
        branch_idx = 10 - branch_idx if branch_idx > 5 else branch_idx + 4
    return branch_idx

def _build_board(ju: int, dun: str) -> dict:
    positions = YANG_DUN_POSITIONS if dun == "阳遁" else YIN_DUN_POSITIONS
    ju_mod = ju if ju <= 9 else ju - 9
    palace_map = {}
    stem_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    branch_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 阳遁：地盘干按乾1→9顺布，阴遁逆布
    for palace_idx, palace_name in enumerate(PALACE_ORDER):
        numeric_pos = palace_idx + 1
        board_pos = (positions.get(ju_mod, ju_mod) + numeric_pos - 1) % 9 + 1
        star_idx = (board_pos - 1) % 9
        door_idx = (board_pos + 2) % 8
        door_name = DOOR_SORT_ORDER[door_idx]
        god_idx = (board_pos + 4) % 8
        # 地盘天干：阳遁从甲开始顺飞
        stem_idx = (numeric_pos - 1) % 10
        branch_idx = (numeric_pos - 1) % 12
        palace_map[palace_name] = {
            "star": STAR_SORT_ORDER[star_idx],
            "door": DOOR_SORT_ORDER[door_idx],
            "god": GOD_SORT_ORDER[god_idx],
            "stem": stem_list[stem_idx],
            "branch": branch_list[branch_idx],
            "board_position": board_pos
        }
    return palace_map

def _select_useful_god(question: str, domain: str, board: dict) -> dict:
    hints = {
        "relationship": ["六合", "太阴", "值符"],
        "business": ["生门", "开门", "值符"],
        "content": ["景门", "天英", "九天"],
        "personal": ["太阴", "九地", "天辅"],
        "strategy": ["值符", "九天", "生门"]
    }
    candidates = hints.get(domain, hints["strategy"])
    for palace_name, data in board.items():
        if data["god"] in candidates or data["door"] in candidates:
            return {
                "useful_palace": palace_name,
                "useful_god": data["god"],
                "useful_door": data["door"],
                "useful_star": data["star"],
                "reason": f"{data['door']}{data['god']}在{palace_name}，适合{domain}方向"
            }
    default_palace = list(board.keys())[0]
    return {
        "useful_palace": default_palace,
        "useful_god": board[default_palace]["god"],
        "useful_door": board[default_palace]["door"],
        "useful_star": board[default_palace]["star"],
        "reason": f"默认参考{palace_name}局势"
    }

def _host_guest(posture: str, door: str, god: str) -> dict:
    active_doors = ["开", "生", "景"]
    passive_doors = ["死", "惊", "伤"]
    neutral_doors = ["休", "杜"]
    if door in active_doors:
        posture_text = "主动方占优，适宜积极推进"
    elif door in passive_doors:
        posture_text = "被动方/环境约束较强，适宜防守等待"
    else:
        posture_text = "中性局势，适宜试探验证"
    relation_gods = ["合", "阴", "地"]
    risk_gods = ["虎", "武", "蛇"]
    if any(g in god for g in relation_gods):
        rel_text = "关系方向有利，适合协商整合"
    elif any(g in god for g in risk_gods):
        rel_text = "需注意风险变量，防暗箭和欺骗"
    else:
        rel_text = "方向中性，注意主客关系处理"
    return {"posture": posture_text, "relation": rel_text}

class QimenEngine:
    def __init__(self) -> None:
        self.jiugong = JIU_GONG
        self.bamen = BA_MEN
        self.jiuxing = JIU_XING
        self.bashen = BA_SHEN

    def analyze(self, event_time: str | None = None, location: str | None = None,
                question: str = "", domain: str = "unknown") -> dict:
        if not event_time:
            return {"status": "missing_event_time", "role": "具体事件局势与行动时机，需要 event_time 才能起结构局"}
        dt = _parse_dt(event_time)
        dun = _get_yin_yang(dt)
        ju = _calc_ju_number(dt, dun)
        board = _build_board(ju, dun)
        main_palace_name = list(board.keys())[0]
        main_data = board[main_palace_name]
        useful = _select_useful_god(question, domain, board)
        hg = _host_guest(useful["reason"], main_data["door"], main_data["god"])
        stem_branch = GUA_ZHANG.get(BRANCH_ZODIAC[dt.hour % 12], "甲子")
        return {
            "status": "ok",
            "event_time": event_time,
            "location": location,
            "domain": domain,
            "question": question,
            "bureau": {
                "dun": dun,
                "ju_number": ju,
                "label": f"{dun}{ju}局",
                "stem_branch_hour": stem_branch
            },
            "main_palace": {"name": main_palace_name, **self.jiugong.get(main_palace_name, {})},
            "door": {"name": main_data["door"], **self.bamen.get(main_data["door"], {})},
            "star": {"name": main_data["star"], **self.jiuxing.get(main_data["star"], {})},
            "god": {"name": main_data["god"], **self.bashen.get(main_data["god"], {})},
            "useful_god": useful,
            "host_guest": hg,
            "board": {k: {"star": v["star"], "door": v["door"], "god": v["god"], "stem": v.get("stem", ""), "branch": v.get("branch", "")} for k, v in board.items()},
            "situation_signal": self._signals(main_palace_name, main_data),
            "timing_hint": self._timing_hint(main_data, useful, hg),
            "risk_hint": self._risk_hint(main_data, hg),
            "action_hint": self._action_hint(main_data, useful, hg),
            "v4_needed": ["值符值使精确飞布", "天地盘", "马星", "空亡"]
        }

    def _signals(self, main_palace_name: str, main_data: dict) -> list[str]:
        return [
            f"主宫{main_palace_name}：{self.jiugong.get(main_palace_name, {}).get('keywords', [])}",
            f"主门{main_data['door']}：{self.bamen.get(main_data['door'], {}).get('keywords', [])}",
            f"主星{main_data['star']}：{self.jiuxing.get(main_data['star'], {}).get('keywords', [])}",
            f"主神{main_data['god']}：{self.bashen.get(main_data['god'], {}).get('keywords', [])}"
        ]

    def _timing_hint(self, main: dict, useful: dict, hg: dict) -> str:
        quality = self.bamen.get(main["door"], {}).get("quality", "")
        if "吉" in quality:
            return f"时机偏开，主门{main['door']}为吉，{useful['reason']}，可小步推进并观察反馈"
        elif "凶" in quality:
            return f"时机不稳，主门{main['door']}为凶，{hg['posture']}，先控风险或等待新信号"
        return f"时机中性，主门{main['door']}，{hg['posture']}，适合试探验证、低成本行动"

    def _risk_hint(self, main: dict, hg: dict) -> list[str]:
        risks = [self.bamen.get(main["door"], {}).get("action_hint", "")]
        risks.append(self.jiuxing.get(main["star"], {}).get("risk", ""))
        risks.append(self.bashen.get(main["god"], {}).get("hint", ""))
        risks.append(hg["relation"])
        return [r for r in risks if r]

    def _action_hint(self, main: dict, useful: dict, hg: dict) -> str:
        return f"{self.bamen.get(main['door'], {}).get('action_hint', '')}；{self.bashen.get(main['god'], {}).get('hint', '')}；参考有用神：{useful['useful_palace']}{useful['useful_door']}{useful['useful_god']}"