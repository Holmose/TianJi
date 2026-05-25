from __future__ import annotations

from pathlib import Path
from .state_model import new_state
from .engines.reality_parser import RealityParser
from .engines.symbolic_engine import SymbolicEngine
from .engines.simulation_adapter import LocalSimulationEngine
from .engines.bazi_engine import BaziEngine
from .engines.qimen_engine import QimenEngine
from .engines.qimen_precision import QimenPrecisionEngine
from .engines.iching_engine import IChingEngine
from .engines.bazi_precision import BaziPrecisionEngine

class TianJiOrchestrator:
    def __init__(self) -> None:
        self.reality = RealityParser()
        self.symbolic = SymbolicEngine()
        self.bazi = BaziEngine()
        self.qimen = QimenEngine()
        self.iching = IChingEngine()
        self.bazi_precision = BaziPrecisionEngine()
        self.qimen_precision = QimenPrecisionEngine()
        self.sim = LocalSimulationEngine()

    def run(self, question: str, domain: str = "unknown", goal: str = "", event_time: str | None = None, location: str | None = None, rounds: int = 3, birth_datetime: str | None = None, gender: str | None = None) -> dict:
        parsed = self.reality.parse(question, domain, goal)
        state = new_state(question, parsed["domain"], goal, event_time, location)
        state.reality.facts = parsed["facts"]
        state.reality.timeline = parsed["timeline"]
        state.reality.people = parsed["people"]
        state.reality.known_variables = parsed["known_variables"]
        state.reality.unknown_variables = parsed["unknown_variables"]
        state.reality.constraints = parsed["constraints"]
        sym = self.symbolic.analyze(question, state.query.domain)
        state.symbolic.bagua = sym["bagua"]
        state.symbolic.wuxing = sym["wuxing"]
        state.symbolic.iching = self.iching.analyze(question, state.query.domain, event_time)
        bazi = self.bazi.analyze(birth_datetime=birth_datetime, gender=gender, location=location)
        state.symbolic.bazi = bazi
        if bazi.get("status") == "ok":
            precision = self.bazi_precision.analyze(
                bazi["pillars"], bazi["day_master"],
                bazi["strong_weak"], bazi["dominant_element"],
                bazi["five_element_balance"]
            )
            bazi["v3_precision"] = precision
        qimen = self.qimen.analyze(event_time=event_time, location=location, question=question, domain=state.query.domain)
        state.symbolic.qimen = qimen
        if qimen.get("status") == "ok":
            qp = self.qimen_precision.analyze(qimen["bureau"], qimen["board"], state.query.domain, question)
            qimen["v3_precision"] = qp
        d = state.to_dict()
        d["simulation"] = self.sim.run(d, rounds)
        d["causal"] = self._causal(d)
        d["future"] = self._future(d)
        d["strategy"] = self._strategy(d)
        d["confidence"] = self._confidence(d)
        return d

    def _causal(self, d: dict) -> dict:
        timeline = d["reality"]["timeline"]
        return {
            "past_turning_points": timeline[:3] or ["当前资料未提供明确时间线，需补充过去关键节点"],
            "causal_chain": ["输入事实 → 象数状态标签 → 多Agent争论 → 条件概率路径"],
            "missed_signals": ["缺少对方/环境连续反馈时，不判断为必然趋势"]
        }

    def _future(self, d: dict) -> dict:
        hint = d["symbolic"]["bagua"]["action_hint"]
        return {"branches": [
            {"name": "A 顺势发展", "probability": 0.45, "trigger_conditions": ["现实反馈持续增强", "关键风险未触发", hint], "risks": ["过早下定论"], "outcome": "局势按当前方向推进"},
            {"name": "B 中途受阻", "probability": 0.35, "trigger_conditions": ["信息不足继续扩大", "外部变量介入", "执行动作过急或过慢"], "risks": ["误把短期信号当长期趋势"], "outcome": "进入停滞、冷却或反复"},
            {"name": "C 突发反转", "probability": 0.20, "trigger_conditions": ["隐藏变量暴露", "时间窗口变化", "关键人物态度突变"], "risks": ["黑天鹅不可控"], "outcome": "出现和主路径相反的结果"}
        ]}

    def _strategy(self, d: dict) -> dict:
        return {
            "best_action": d["symbolic"]["bagua"]["action_hint"],
            "forbidden_actions": ["把推演当绝对预言", "在证据不足时做高风险承诺", "跳过现实反馈只看象数"],
            "watch_signals": ["对方/市场/环境是否持续反馈", "关键时间节点是否出现新变量", "风险信号是否从隐性变显性"],
            "change_conditions": ["新增事实推翻当前假设", "主路径连续两次不成立", "黑天鹅变量出现"]
        }

    def _confidence(self, d: dict) -> dict:
        missing = len(d["reality"]["unknown_variables"])
        level = "中" if missing <= 1 else "中低"
        return {"level": level, "blind_spots": d["reality"]["unknown_variables"], "principle": "现实证据 > 多Agent共识 > 象数解释"}
