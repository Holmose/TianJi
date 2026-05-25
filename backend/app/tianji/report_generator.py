from __future__ import annotations

import json
from pathlib import Path

class TianJiReportGenerator:
    def render_markdown(self, state: dict) -> str:
        q = state["query"]
        s = state["symbolic"]
        lines = []
        lines.append(f"# 天机推演报告：{state['report_id']}")
        lines.append("")
        lines.append("## 1. 总断")
        lines.append(f"领域：{q['domain']}。当前主象为 **{s['bagua']['main']} / {s['wuxing']['main']}**，趋势卦参考 **{s['iching']['primary_hexagram']['name']} → {s['iching']['changed_hexagram']['name']}**。")
        lines.append(f"建议：{state['strategy']['best_action']}。")
        lines.append("")
        lines.append("## 2. 现实底盘")
        for f in state["reality"]["facts"]: lines.append(f"- {f}")
        lines.append("")
        lines.append("## 3. 象数建模")
        lines.append(f"- 八卦：{s['bagua']['main']}，关键词：{'、'.join(s['bagua']['keywords'])}")
        lines.append(f"- 五行：{s['wuxing']['main']}，动力：{'、'.join(s['wuxing']['keywords'])}；风险：{s['wuxing']['risk']}")
        iching = s['iching']
        lines.append(f"- 易经：本卦{iching['primary_hexagram']['name']} → 变卦{iching['changed_hexagram']['name']}，变爻{iching['changing_lines']}")
        lines.append(f"  - 趋势：{iching['transition']}")
        lines.append(f"  - 阶段风险：{'；'.join(iching['stage_warning'])}")
        lines.append(f"  - 行动提示：{iching['action_hint']}")
        if s['bazi'].get('status') == 'ok':
            bazi = s['bazi']
            lines.append(f"- 四柱：年柱{bazi['pillars']['year']}、月柱{bazi['pillars']['month']}、日柱{bazi['pillars']['day']}、时柱{bazi['pillars']['hour']}")
            lines.append(f"  - 日主：{bazi['day_master']['stem']}{bazi['day_master']['element']}{bazi['day_master']['yin_yang']}")
            lines.append(f"  - 五行比例：{bazi['five_element_balance']}")
            lines.append(f"  - 人物倾向：{'；'.join(bazi['personality_bias'])}")
            lines.append(f"  - 风险模式：{'；'.join(bazi['risk_pattern'])}")
        else:
            lines.append(f"- 四柱：{s['bazi']['status']}，{s['bazi']['role']}")
        if s['qimen'].get('status') == 'ok':
            qimen = s['qimen']
            lines.append(f"- 奇门：{qimen['bureau']['label']}，主宫{qimen['main_palace']['name']}，主门{qimen['door']['name']}，主星{qimen['star']['name']}，主神{qimen['god']['name']}")
            lines.append(f"  - 局势信号：{'；'.join(qimen['situation_signal'])}")
            lines.append(f"  - 主客关系：{qimen['host_guest']['posture']}；{qimen['host_guest']['relation']}")
            lines.append(f"  - 时机提示：{qimen['timing_hint']}")
            lines.append(f"  - 风险提示：{'；'.join(qimen['risk_hint'])}")
        else:
            lines.append(f"- 奇门：{s['qimen']['status']}，{s['qimen']['role']}")
        lines.append("")
        lines.append("## 4. 多 Agent 推演过程")
        for r in state["simulation"]["rounds"]: lines.append(f"- 第{r['round']}轮｜{r['theme']}：{r['summary']}")
        lines.append("\n共识：")
        for c in state["simulation"]["consensus"]: lines.append(f"- {c}")
        lines.append("\n分歧：")
        for d in state["simulation"]["disagreements"]: lines.append(f"- {d}")
        lines.append("")
        lines.append("## 5. 过去反推")
        for p in state["causal"]["past_turning_points"]: lines.append(f"- {p}")
        lines.append("")
        lines.append("## 6. 未来分支")
        for b in state["future"]["branches"]:
            lines.append(f"### {b['name']}｜概率 {int(b['probability']*100)}%")
            lines.append(f"- 触发条件：{'；'.join(b['trigger_conditions'])}")
            lines.append(f"- 风险：{'；'.join(b['risks'])}")
            lines.append(f"- 结果：{b['outcome']}")
        lines.append("")
        lines.append("## 7. 当前最优策略")
        lines.append(f"- 主动作：{state['strategy']['best_action']}")
        lines.append(f"- 禁忌：{'；'.join(state['strategy']['forbidden_actions'])}")
        lines.append(f"- 观察信号：{'；'.join(state['strategy']['watch_signals'])}")
        lines.append("")
        lines.append("## 8. 置信度与盲区")
        lines.append(f"- 置信度：{state['confidence']['level']}")
        lines.append(f"- 盲区：{'；'.join(state['confidence']['blind_spots'])}")
        lines.append(f"- 原则：{state['confidence']['principle']}")
        return "\n".join(lines) + "\n"

    def save(self, state: dict, out_dir: str | Path) -> dict:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        md = out / f"{state['report_id']}.md"
        js = out / f"{state['report_id']}.json"
        md.write_text(self.render_markdown(state), encoding="utf-8")
        js.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"markdown": str(md), "json": str(js)}
