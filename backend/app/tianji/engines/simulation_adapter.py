from __future__ import annotations

class LocalSimulationEngine:
    """Deterministic V1 fallback simulation.

    Future full simulation integration can replace this adapter. The output shape
    is intentionally compatible with future multi-agent rounds.
    """

    AGENTS = [
        ("Reality Agent", "只看事实与证据"),
        ("Causal Agent", "寻找过去因果链"),
        ("Risk Agent", "专门放大风险与黑天鹅"),
        ("Strategy Agent", "把结论落到行动"),
        ("Bazi Agent", "人物长期结构，V2增强"),
        ("Qimen Agent", "事件时空局势，V3增强"),
        ("IChing Agent", "趋势演化与阶段"),
        ("Wuxing Agent", "动力平衡与生克"),
        ("Skeptic Agent", "反玄学校验，防止过度解释"),
        ("Synthesizer Agent", "收敛共识")
    ]

    def run(self, state: dict, rounds: int = 3) -> dict:
        agents = [{"name": n, "role": r} for n, r in self.AGENTS]
        bagua = state["symbolic"]["bagua"]["main"]
        gua_hint = state["symbolic"]["bagua"]["action_hint"]
        domain = state["query"]["domain"]
        qimen = state["symbolic"].get("qimen", {})
        iching = state["symbolic"].get("iching", {})
        iching_line = ""
        if iching.get("status") == "ok":
            iching_line = f"易经趋势为{iching['primary_hexagram']['name']}转{iching['changed_hexagram']['name']}，提示：{iching['action_hint']}。"
        qimen_line = ""
        if qimen.get("status") == "ok":
            qimen_line = f"奇门显示{qimen['bureau']['label']}，{qimen['door']['name']}主事，时机提示：{qimen['timing_hint']}。"
        sim_rounds = []
        sim_rounds.append({"round": 1, "theme": "事实校验", "summary": "现实信息仍是主约束；象数标签只辅助组织变量。"})
        sim_rounds.append({"round": 2, "theme": "象数争论", "summary": f"主象为{bagua}，提示：{gua_hint}。{iching_line}{qimen_line}反方提醒：不能把象意当必然结果。"})
        sim_rounds.append({"round": 3, "theme": "策略收敛", "summary": "采用三路径输出：顺势路径、受阻路径、反转路径，并设置观察信号。"})
        consensus = [
            "不要输出绝对预言，要输出条件概率与触发条件",
            "过去反推必须绑定事实节点，不能凭空补剧情",
            f"当前主象{bagua}可以作为局势标签，但最终动作仍看现实反馈",
            iching.get("action_hint", "易经未提供趋势参数") if iching.get("status") == "ok" else "易经趋势层缺失",
            qimen.get("action_hint", "奇门未提供事件时机参数") if qimen.get("status") == "ok" else "缺少事件时间，奇门只保留为待补模块"
        ]
        disagreements = [
            "象数派倾向强调趋势感，现实派要求补充更多证据",
            "风险派认为需要保留黑天鹅路径，策略派只允许一个当前主动作"
        ]
        return {"agents": agents, "rounds": sim_rounds[:rounds], "consensus": consensus, "disagreements": disagreements}
