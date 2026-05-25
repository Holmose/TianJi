"""Divine Engine: 天玑神性赋能层

为推演结果注入东方神性赋能与仪式感。
不是玄学包装，而是将象数宇宙观美学化呈现。

神性三层：
L1 天机：解读这一刻天时、地利、人和的宇宙同频信号
L2 命盘铭文：将四柱写成有力量感的命盘诗句
L3 天玑判词：将奇门+易经结论升华为一句话判词
"""

from __future__ import annotations
from datetime import datetime
import json
from pathlib import Path

# 十二长生宫（阳干）
CHANG_SHENG = {
    "甲": ["长生","沐浴","冠带","临官","帝旺","衰","病","死","墓","绝","胎","养"],
    "丙": ["长生","沐浴","冠带","临官","帝旺","衰","病","死","墓","绝","胎","养"],
    "庚": ["长生","沐浴","冠带","临官","帝旺","衰","病","死","墓","绝","胎","养"],
    "壬": ["长生","沐浴","冠带","临官","帝旺","衰","病","死","墓","绝","胎","养"],
}
# 阴干长生位（丙戊己乙丁辛癸随用）
CHANG_SHENG_YIN = {
    "乙": ["病","死","墓","绝","胎","养","长生","沐浴","冠带","临官","帝旺","衰"],
    "丁": ["死","墓","绝","胎","养","长生","沐浴","冠带","临官","帝旺","衰"],
    "己": ["临官","帝旺","衰","病","死","墓","绝","胎","养","长生","沐浴","冠带"],
    "辛": ["死","墓","绝","胎","养","长生","沐浴","冠带","临官","帝旺","衰"],
    "癸": ["死","墓","绝","胎","养","长生","沐浴","冠带","临官","帝旺","衰"],
}

ELEM_NAMES = {"木":"青","火":"赤","金":"白","水":"玄","土":"黄"}
YY_NAMES = {"阳":"乾","阴":"坤"}

DM_POETRY = {
    "甲": "日出东方，破甲而出，天地壮阔，此命非凡",
    "乙": "春风化雨，柔中藏锋，花开向阳，暗香自来",
    "丙": "烈焰腾空，光照万物，朱明耀眼，气势如虹",
    "丁": "星火微芒，暗夜明灯，温润如玉，静待时机",
    "戊": "厚土载物，稳固如山，大地承载，根基深沉",
    "己": "坤柔合德，包容万物，大地生化，灵动而有节",
    "庚": "白虎金气，刚健斩断，秋收肃杀，一刀两断",
    "辛": "太阴金商，精致细腻，珠玉光华，锋芒内敛",
    "壬": "北海深潜，变动不居，江河浩荡，一泻千里",
    "癸": "幽泉暗流，静深而至，癸水润下，智慧藏渊",
}

DOOR_POETRY = {
    "开门": "九天之上，洞开金门，机遇临门，当乘势而出",
    "休门": "玄武休囚，安养静守，修身养息，待时而动",
    "生门": "生门大吉，生机盎然，厚德载物，财富自来",
    "伤门": "白虎伤门，动则有伤，冲突显现，谨慎行事",
    "杜门": "青天龙遁，杜塞不通，隐蔽潜行，另辟蹊径",
    "景门": "朱雀景门，繁华似锦，声势喧哗，谨防虚火",
    "死门": "黑瘟死地，凶祸已成，不可妄动，静待生机",
    "惊门": "白虎惊门，惊恐不安，讼事兴起，以静制动",
}

GUA_POETRY = {
    "乾为天": "天行刚健，君子以自强不息；纯阳至刚，时至则龙跃于渊",
    "坤为地": "地势宽厚，君子以厚德载物；纯阴至柔，静中有大机遇",
    "乾上坤下": "天地否卦，闭塞不通，宜静守不宜妄动，否极则泰来",
    "坤上乾下": "地天泰卦，通泰祥和，上下交通，阴阳和合",
    "天火同人": "天火同人，同心协力；火助天势，贵人相助",
    "火天大有": "火天大有，如日中天；文明以健，德照天下",
    "雷水解": "雷水解卦，困境得释；冬雷震震，束缚渐开",
    "风雷益": "风雷益卦，乘风而起；雷厉风行，获益匪浅",
    "泽山咸": "泽山咸卦，感应之道；山泽通气，心意相投",
    "天山遁": "天山遁卦，隐退之时；君子远遁，不宜强求",
    "天泽履": "天泽履卦，循礼而行；脚踏实地，谨慎趋吉",
    "地山谦": "地山谦卦，山藏地下；谦逊有德，退守有吉",
    "雷山小过": "雷山小过，过犹不及；小过当前，守成为上",
    "水山蹇": "水山蹇卦，前路艰难；知难而退，另寻他途",
}

FIVE_ELEM_CYCLE = {
    "木": {"生":"火","克":"金","被":"水生","防":"金克"},
    "火": {"生":"土","克":"木","被":"木生","防":"木克"},
    "土": {"生":"金","克":"水","被":"火生","防":"水克"},
    "金": {"生":"水","克":"火","被":"土生","防":"火克"},
    "水": {"生":"木","克":"土","被":"金生","防":"土克"},
}

SEASONAL_DOOR = {
    "春":"生门 伤门","夏":"景门 惊门","秋":"开门 惊门","冬":"休门 生门"
}

JIU_XING_DIVINE = {
    "天蓬": "北冥之兽，主智慧与隐藏，谋略深远如渊",
    "天任": "厚德之牛，任重道远，稳中求进，大器晚成",
    "天冲": "雷霆之将，冲动果断，速战速决，切忌冒进",
    "天辅": "文曲之曜，辅弼之才，学识渊博，宜文教",
    "天英": "朱明之火，声名显赫，才华外露，宜声张",
    "天芮": "幽暗之结，问题显现，修炼自身，宜内省",
    "天柱": "白虎之肃，支柱中流，刚正不阿，宜坚守",
    "天心": "天心之医，仁心济世，变革创新，宜决策",
    "天禽": "中宫凤凰，统御四方，大吉之位，宜总领",
}

BA_SHEN_DIVINE = {
    "值符": "诸神之首，九天应命，权力核心，执牛耳者",
    "螣蛇": "火之精魂，缠绕缠绵，变动虚耗，疑心生暗",
    "太阴": "金之精英，阴佑相助，荫蔽深厚，贵人暗中",
    "六合": "木之合和，调解之力，众缘和合，人际畅通",
    "白虎": "金之煞神，凶煞横逆，灾祸显现，伤灾血光",
    "玄武": "水之暗神，暗昧失守，私欲作祟，偷盗阴谋",
    "九地": "地之厚德，潜藏坚固，蛰伏待机，以守为攻",
    "九天": "天之威灵，威震四方，行动张扬，飞扬跋扈",
}


def _load_data(name: str) -> dict:
    p = Path(__file__).parent.parent / "data" / f"{name}.json"
    if p.exists():
        return json.loads(p.read_text())
    return {}


class DivineEngine:
    """天玑神性赋能引擎"""

    def __init__(self) -> None:
        self.tiangan_dizhi = _load_data("tiangan_dizhi")
        self.ten_gods = _load_data("ten_gods")

    def divine(self, report: dict) -> dict:
        """对推演报告进行神性赋能"""
        sym = report.get("symbolic", {})
        bazi = sym.get("bazi", {})
        qimen = sym.get("qimen", {})
        iching = sym.get("iching", {})
        future = report.get("future", {})

        divine = {
            "timing": self._timing(report),
            "destiny_verse": self._destiny_verse(bazi),
            "divine_judgment": self._divine_judgment(qimen, iching),
            "celestial_sign": self._celestial_sign(qimen),
            "three_paths_divine": self._three_paths_divine(future),
            "golden_words": self._golden_words(bazi, qimen),
            "talisman": self._talisman(bazi, qimen, iching),
        }
        return divine

    # ── L1 天机：这一刻的宇宙同频信号 ────────────────────────────

    def _timing(self, report: dict) -> dict:
        """解读这一刻天时、地利、人和的宇宙同频"""
        event_time = report.get("query", {}).get("event_time", "")
        try:
            dt = datetime.strptime(event_time[:16], "%Y-%m-%d %H:%M")
        except Exception:
            dt = datetime.now()

        hour = dt.hour
        month = dt.month
        day = dt.day

        # 天时
        if 5 <= hour < 9:
            tian_shi = "卯时·日出破晓，万物初醒，灵气充沛，宜行动"
        elif 9 <= hour < 13:
            tian_shi = "午时·日上中天，阳气最盛，宜决断"
        elif 13 <= hour < 17:
            tian_shi = "未时·日偏西斜，余晖犹在，宜收敛"
        elif 17 <= hour < 21:
            tian_shi = "酉时·日落西山，金气收敛，宜静守"
        else:
            tian_shi = "子时·夜深沉寂，一阳初生，宜潜藏"

        # 节气感
        if month in [3, 4]:
            tian_shi += "，春木生发"
        elif month in [5, 6]:
            tian_shi += "，夏火炽盛"
        elif month in [7, 8]:
            tian_shi += "，秋金肃杀"
        elif month in [9, 10]:
            tian_shi += "，金水交界"
        elif month in [11, 12]:
            tian_shi += "，冬水封藏"
        else:
            tian_shi += "，土气转换"

        # 地利（奇门宫位解读）
        sym = report.get("symbolic", {})
        qimen = sym.get("qimen", {})
        palace = qimen.get("palace", "")
        di_li = f"主宫{palace}宫" if palace else ""

        # 人和（现实变量数）
        unknown = len(report.get("reality", {}).get("unknown_variables", []))
        ren_he = f"未知变量{unknown}个，判断置信度中等" if unknown else "变量清晰，判断置信度高"

        return {
            "celestial_time": tian_shi,
            "earthly_location": di_li,
            "human_harmony": ren_he,
            "epoch": f"今日{month}月{day}日，天地同频，时空交汇"
        }

    # ── L2 命盘铭文：四柱写成诗句 ────────────────────────────────

    def _destiny_verse(self, bazi: dict) -> dict:
        """将四柱写成有力量感的命盘诗句"""
        dm_stem = bazi.get("day_master", {}).get("stem", "")
        dm_elem = bazi.get("day_master", {}).get("element", "")
        dm_yy = bazi.get("day_master", {}).get("yin_yang", "")
        pillars = bazi.get("pillars", {})
        v3 = bazi.get("v3_precision", {})

        pillars_text = []
        for p, key in [("年","year"),("月","month"),("日","day"),("时","hour")]:
            vals = pillars.get(key, ["?","?"])
            stem = vals[0] if vals else "?"
            branch = vals[1] if len(vals) > 1 else "?"
            pillars_text.append(f"{stem}{branch}")

        pillars_str = " · ".join(pillars_text)

        # 日主诗句
        dm_poem = DM_POETRY.get(dm_stem, f"{dm_stem}命，灵动深沉")

        # 命格判断诗
        label = v3.get("balance_analysis", {}).get("label", "")
        elem_strength = v3.get("element_strength", {})

        # 求最大、最小五行
        if elem_strength:
            counts = {k: v["count"] for k, v in elem_strength.items()}
            max_elem = max(counts, key=counts.get) if counts else ""
            max_cnt = counts.get(max_elem, 0)
            min_elem = min(counts, key=counts.get)
            min_cnt = counts.get(min_elem, 0)
        else:
            max_elem, max_cnt, min_elem, min_cnt = "", 0, "", 0

        # 生成命格诗
        if label == "身强":
            power_poem = "五行偏旺，" + max_elem + "盛，命格强势，" + min_elem + "为短板，宜修" + min_elem + "之功"
        elif label == "身弱":
            power_poem = dm_elem + "日主，身弱而灵，" + max_elem + "偏旺，宜借" + max_elem + "之势补身"
        elif label == "中和":
            power_poem = f"五行均衡，阴阳调和，大运平稳，持盈保泰"
        else:
            power_poem = f"命格{label}，动态平衡，进退有度，顺势而为"

        # 十神铭文
        ten_gods_detail = v3.get("ten_gods_detail", {})
        god_poems = []
        for pos in ten_gods_detail:
            tg = ten_gods_detail[pos].get("ten_god", "")
            tg_elem = ten_gods_detail[pos].get("ten_god_element", "")
            if tg:
                god_poems.append(f"{pos}柱{self._ten_god_sigil(tg)}")
        gods_str = " · ".join(god_poems[:4])

        # 用神忌神铭文
        useful = v3.get("useful_god", {})
        forbidden = v3.get("forbidden_god", {})
        useful_stems = useful.get("stems", [])
        useful_note = useful.get("note", "")
        forbidden_stems = forbidden.get("stems", [])
        forbidden_note = forbidden.get("note", "")

        useful_str = ",".join(useful_stems) if useful_stems else "待定"
        forbidden_str = ",".join(forbidden_stems) if forbidden_stems else "待定"

        return {
            "destiny_plate": f"{dm_stem} · {pillars_str}",
            "destiny_poem": f"{dm_poem}。{power_poem}",
            "ten_gods_sigil": f"十神同参：{gods_str}",
            "useful_god_sigil": f"用神天机：{useful_str}，{useful_note}",
            "forbidden_god_sigil": f"忌神天机：{forbidden_str}，{forbidden_note}",
        }

    def _ten_god_sigil(self, tg: str) -> str:
        s = {
            "比肩":"同气连枝","劫财":"争竞锋芒","食神":"吐纳生津",
            "伤官":"才华横溢","偏财":"逐利四方","正财":"正业稳守",
            "偏官":"杀伐果断","正官":"正印加身","偏印":"暗中生扶",
            "正印":"慈恩庇护"
        }.get(tg, tg)
        return s

    # ── L3 天玑判词：奇门+易经升华为判词 ────────────────────────

    def _divine_judgment(self, qimen: dict, iching: dict) -> dict:
        """将奇门+易经结论升华为一句话判词"""
        door = qimen.get("door", {}).get("name", "")
        star = qimen.get("star", {}).get("name", "")
        god = qimen.get("god", {}).get("name", "")
        palace = qimen.get("palace", "")
        dun_type = qimen.get("dun_type", "")
        bureau = qimen.get("bureau", "")

        door_p = DOOR_POETRY.get(door, f"{door}门，局势待定")
        star_p = JIU_XING_DIVINE.get(star, f"{star}星，星辰待照")
        god_p = BA_SHEN_DIVINE.get(god, f"{god}，诸神待命")

        # 奇门判词
        qimen_judgment = f"{bureau}局{dun_type}，主{door_p}。{star_p}。{god_p}"

        # 易经判词
        iching_gua = iching.get("hexagram", "")
        iching_transtype = iching.get("transition_type", "")
        iching_trend = iching.get("trend", "")

        gua_p = GUA_POETRY.get(iching_gua, f"当前{iching_gua}，天地运行中")
        iching_judgment = f"易象：{gua_p}"

        # 综合判词
        overall = self._merge_judgment(qimen, iching)

        return {
            "qimen_judgment": qimen_judgment,
            "iching_judgment": iching_judgment,
            "overall_judgment": overall,
        }

    def _merge_judgment(self, qimen: dict, iching: dict) -> str:
        """将奇门与易经判词合并为一个核心判词"""
        door = qimen.get("door", {}).get("name", "")
        iching_gua = iching.get("hexagram", "")

        patterns = {
            ("开门", "乾为天"): "天门洞开，纯阳至健，时至龙飞，不可抑藏",
            ("开门", "坤为地"): "地广开门，宽厚待人，厚德载物，吉无不利",
            ("生门", "乾为天"): "天德生门，富贵自来，君子乘天，正当其时",
            ("生门", "地天泰"): "泰来生门，阴阳交泰，万物生发，大有可期",
            ("休门", "地山谦"): "休养谦德，静待天时，退守有吉，蓄势待发",
            ("伤门", "天火同人"): "同人见伤，同心受创，谨慎小人，避其锋芒",
            ("景门", "天火同人"): "朱雀逞威，繁华似锦，虚火上炎，宜静不宜躁",
            ("死门", "天地否"): "否卦死门，天地闭塞，守成为上，静待转机",
            ("惊门", "雷水解"): "解卦惊门，困境初解，惊恐渐消，渐入佳境",
            ("开门", "雷天大壮"): "大壮开门，雷天震震，行动张扬，把握时机",
            ("杜门", "天山遁"): "遁卦杜门，隐退潜行，不宜强求，知难而退",
        }

        key = (door, iching_gua)
        if key in patterns:
            return patterns[key]

        # 动态组合
        if door in ["开门","生门"]:
            base = "吉"
        elif door in ["死门","惊门","伤门"]:
            base = "凶"
        else:
            base = "平"

        return f"当前{base}，{door}配{iching_gua}，天机已动，静观其变"

    def _celestial_sign(self, qimen: dict) -> dict:
        """奇门天象：九宫八门的宇宙符号解读"""
        bureau = qimen.get("bureau", {})
        bureau_label = bureau.get("label", "")
        dun_type = bureau.get("dun", "")
        bureau_palace = bureau.get("main_palace", {}) or qimen.get("main_palace", {})
        palace_name = bureau_palace.get("name", "") if isinstance(bureau_palace, dict) else str(bureau_palace or "")
        bureau = bureau_label
        door = qimen.get("door", {}).get("name", "")
        star = qimen.get("star", {}).get("name", "")
        god = qimen.get("god", {}).get("name", "")

        palace_meanings = {
            "1":"坎一宫·暗流涌动","2":"坤二宫·厚德载物","3":"震三宫·雷动惊醒",
            "4":"巽四宫·风入无形","5":"中五宫·统御四方","6":"乾六宫·天行刚健",
            "7":"兑七宫·泽润金气","8":"艮八宫·山静止步","9":"离九宫·火明虚华"
        }
        palace_text = palace_meanings.get(palace_name, f"{palace_name}宫")

        door_elem = {
            "开门":"金","休门":"水","生门":"土","伤门":"木",
            "杜门":"木","景门":"火","死门":"土","惊门":"金"
        }.get(door, "")
        star_elem = {
            "天蓬":"水","天任":"土","天冲":"木","天辅":"木",
            "天英":"火","天芮":"土","天柱":"金","天心":"金","天禽":"土"
        }.get(star, "")

        return {
            "palace_realm": palace_text,
            "bureau_dun": f"{bureau}局，{dun_type}，主{bureau_palace.get('name', bureau_palace) if isinstance(bureau_palace, dict) else bureau_palace}宫",
            "door_nature": f"{door}，{door_elem}性主导",
            "star_light": f"{star}，{star_elem}星照耀",
            "god_command": f"{god}，诸神令行",
            "celestial_map": f"九宫巡天：{palace_text} · 八门定地：{door} · 九星照天：{star}"
        }

    def _three_paths_divine(self, future: dict) -> list[dict]:
        """将三路径升华为天机预言"""
        branches = future.get("branches", [])
        divine_paths = []
        for b in branches:
            name = b.get("name", "")
            prob = b.get("probability", 0)
            triggers = b.get("trigger_conditions", [])
            prob_pct = f"{prob*100:.0f}%"
            # 天机预言
            if "A" in name or "顺" in name:
                prophecy = "天恩浩荡，吉象显化，顺势而动，不可懈怠"
            elif "B" in name or "阻" in name:
                prophecy = "风云突变，阻碍显现，隐忍待机，静观其变"
            else:
                prophecy = "天机逆转，祸福相依，谨慎行事，以退为进"
            divine_paths.append({
                "name": name,
                "celestial_fate": f"{prob_pct}天意",
                "prophecy": prophecy,
                "divine_signs": [self._divine_sign(t) for t in triggers[:2]]
            })
        return divine_paths

    def _divine_sign(self, trigger: str) -> str:
        """将触发条件翻译为天机符号"""
        trigger_map = {
            "反馈":"回响","持续":"连绵","新变量":"天机",
            "关键节点":"时机","时间窗口":"天时","信号":"瑞兆",
            "扩大":"蔓延","介入":"波澜","暴露":"显化",
            "变化":"转机","隐性":"暗涌","显性":"明镜",
        }
        for k, v in trigger_map.items():
            if k in trigger:
                return trigger.replace(k, v)
        return trigger

    def _golden_words(self, bazi: dict, qimen: dict) -> dict:
        """核心金句：四柱+奇门的最强一句话"""
        dm_stem = bazi.get("day_master", {}).get("stem", "")
        dm_elem = bazi.get("day_master", {}).get("element", "")
        label = bazi.get("v3_precision", {}).get("balance_analysis", {}).get("label", "")
        door = qimen.get("door", {}).get("name", "")
        palace = qimen.get("palace", "")
        star = qimen.get("star", {}).get("name", "")

        elem_god = {"木":"仁","火":"礼","土":"信","金":"义","水":"智"}.get(dm_elem, "智")

        word = f"{dm_stem}命{dm_elem}性，{label}，{door}当令，{star}照命"
        advice = f"修{elem_god}道，顺{self._season_hint(dm_elem)}势，借{self._elem_ally(dm_elem)}气"
        warning = f"戒{self._elem_enemy(dm_elem)}之过，防{door}之偏"

        return {
            "golden_sentence": word,
            "advice": advice,
            "warning": warning,
            "tianji_motto": "天玑一动，破晓黎明；象数同参，命自我立"
        }

    def _season_hint(self, elem: str) -> str:
        return {"木":"春生","火":"夏长","土":"长夏","金":"秋收","水":"冬藏"}.get(elem, "天地")

    def _elem_ally(self, elem: str) -> str:
        return {"木":"水生","火":"木生","土":"火生","金":"土生","水":"金生"}.get(elem, "水生")

    def _elem_enemy(self, elem: str) -> str:
        return {"木":"金克","火":"水克","土":"木克","金":"火克","水":"土克"}.get(elem, "金克")

    def _talisman(self, bazi: dict, qimen: dict, iching: dict) -> dict:
        """天玑护符：命盘的最浓缩符号"""
        dm_stem = bazi.get("day_master", {}).get("stem", "")
        dm_elem = bazi.get("day_master", {}).get("element", "")
        label = bazi.get("v3_precision", {}).get("balance_analysis", {}).get("label", "")
        door = qimen.get("door", {}).get("name", "")
        star = qimen.get("star", {}).get("name", "")
        iching_gua = iching.get("hexagram", "")
        bureau = qimen.get("bureau", {})
        bureau_label = bureau.get("label", "") if isinstance(bureau, dict) else str(bureau or "")

        elem_sigil = ELEM_NAMES.get(dm_elem, "")
        yy = YY_NAMES.get(bazi.get("day_master", {}).get("yin_yang", ""), "")

        talisman_id = f"TJ-{dm_stem}{elem_sigil}{bureau_label}-{door[:1]}{star[:1]}-{iching_gua[:2]}"
        talisman_power = self._calc_talisman_power(label, door)

        return {
            "talisman_id": talisman_id,
            "celestial_elements": f"{yy}{dm_stem}·{elem_sigil}·{bureau_label}局",
            "destiny_key": f"{dm_stem}{label}命，{door}门，{star}星",
            "iching_key": iching_gua,
            "power_level": talisman_power,
            "talisman_text": self._talisman_text(dm_stem, door, star, label),
        }

    def _calc_talisman_power(self, label: str, door: str) -> str:
        if label == "身强" and door in ["开门","生门"]:
            return "大吉·天赐"
        elif label == "身弱" and door in ["休门","杜门"]:
            return "小吉·潜修"
        elif door in ["死门","惊门"]:
            return "凶中藏吉"
        elif door in ["开门","生门"]:
            return "吉"
        else:
            return "平"

    def _talisman_text(self, dm: str, door: str, star: str, label: str) -> str:
        power = {
            "甲":"甲","乙":"乙","丙":"丙","丁":"丁","戊":"戊",
            "己":"己","庚":"庚","辛":"辛","壬":"壬","癸":"癸"
        }.get(dm, "癸")
        return f"天玑符·{power}·{door[:1]}·{star[:1]}·{label[:1]} — 天机不可泄露"