from __future__ import annotations

import json
from pathlib import Path

class TianJiReportGenerator:
    def render_markdown(self, state: dict) -> str:
        q = state["query"]
        s = state["symbolic"]
        lines = []
        lines.append(f"# 天玑系统推演报告：{state['report_id']}")
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
        if iching.get('v3_precision'):
            ip = iching['v3_precision']
            lines.append(f"  - 错卦：{ip['错卦_cuo']['name']}（{ip['错卦_cuo']['strategy']}）")
            lines.append(f"  - 互卦：{ip['互卦_nuclear']['name']}（{ip['互卦_nuclear']['trend']}）")
            if ip.get('liu_qin'):
                lq = [f"{l['position']}{l['relation']}" for l in ip['liu_qin']]
                lines.append(f"  - 六亲：{' '.join(lq)}")
            if ip.get('changing_line_detail'):
                chg = [f"{l['position']}{l['label']}" for l in ip['changing_line_detail'] if l.get('label') and l['label'].startswith(('老','少'))]
                if chg: lines.append(f"  - 动爻：{' '.join(chg)}")
        if s['bazi'].get('status') == 'ok':
            bazi = s['bazi']
            lines.append(f"- 四柱：年柱{bazi['pillars']['year']}、月柱{bazi['pillars']['month']}、日柱{bazi['pillars']['day']}、时柱{bazi['pillars']['hour']}")
            lines.append(f"  - 日主：{bazi['day_master']['stem']}{bazi['day_master']['element']}{bazi['day_master']['yin_yang']}")
            lines.append(f"  - 身强：{bazi['strong_weak']} | 主导五行：{bazi['dominant_element']}")
            lines.append(f"  - 五行比例：{bazi['five_element_balance']}")
            lines.append(f"  - 人物倾向：{'；'.join(bazi['personality_bias'])}")
            if bazi.get('v3_precision'):
                vp = bazi['v3_precision']
                lines.append(f"  - 用神：{'、'.join(vp['useful_god']['stems'])} ({vp['useful_god']['note']})")
                lines.append(f"  - 忌神：{'、'.join(vp['forbidden_god']['stems'])} ({vp['forbidden_god']['note']})")
                lines.append(f"  - 藏干：年{','.join(vp['hidden_stems']['年'])}、月{','.join(vp['hidden_stems']['月'])}、日{','.join(vp['hidden_stems']['日'])}、时{','.join(vp['hidden_stems']['时'])}")
                lines.append(f"  - 月令：{vp['month_correction']}")
        else:
            lines.append(f"- 四柱：{s['bazi']['status']}，{s['bazi']['role']}")
        if s['qimen'].get('status') == 'ok':
            qimen = s['qimen']
            lines.append(f"- 奇门：{qimen['bureau']['label']}，时干{qimen['bureau']['stem_branch_hour']}，主宫{qimen['main_palace']['name']}，主门{qimen['door']['name']}，主星{qimen['star']['name']}，主神{qimen['god']['name']}")
            lines.append(f"  - 局势信号：{'；'.join(qimen['situation_signal'])}")
            if qimen.get('v3_precision'):
                qp = qimen['v3_precision']
                lines.append(f"  - 值符宫：{qp['value_fu']['palace']} | 值使宫：{qp['value_shi']['palace']}")
                lines.append(f"  - 天盘干：{dict(list(qp['heaven_plate'].items())[:3])}")
                lines.append(f"  - 地盘干：{dict(list(qp['earth_plate'].items())[:3])}")
                if qp['horse_star'] != '无马星': lines.append(f"  - 马星：{qp['horse_star']}")
                if qp['empty_palaces']: lines.append(f"  - 空亡：{'、'.join(qp['empty_palaces'][:5])}")
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
        lines.append("")
        lines.append("## 9. 通俗解读")
        if state.get("interpretation"):
            itp = state["interpretation"]
            lines.append(f"**{itp.get('plain_title', '')}**")
            lines.append("")
            lines.append(f"### 一句话结论")
            lines.append(f"{itp.get('plain_summary', '')}")
            lines.append("")
            lines.append("### 四柱通俗解读")
            bz = itp.get("bazi", {})
            lines.append(f"- {bz.get('personality', '')}")
            lines.append(f"- 身强：{bz.get('strength', '')}")
            lines.append(f"- 用神：{bz.get('useful', {}).get('what', '')}，{bz.get('useful', {}).get('how', '')}")
            lines.append(f"- 忌神：{bz.get('forbidden', {}).get('what', '')}")
            lines.append("")
            lines.append("### 奇门通俗解读")
            qm = itp.get("qimen", {})
            lines.append(f"- {qm.get('core_signal', '')}")
            lines.append(f"- 局势：{qm.get('summary', '')}")
            lines.append("")
            lines.append("### 易经通俗解读")
            ic = itp.get("iching", {})
            lines.append(f"- 当前主卦：{ic.get('gua', '')}")
            lines.append(f"- 趋势：{ic.get('trend', '')}")
            lines.append(f"- 建议：{ic.get('strategy', '')}")
            lines.append(f"- 风险：{ic.get('risk', '')}")
            lines.append("")
            lines.append("### 综合信号")
            lines.append(f"- 核心主题：{itp.get('integrated', {}).get('core_theme', '')}")
            lines.append(f"- 整体基调：{itp.get('integrated', {}).get('tone', '')}")
            lines.append("")
            lines.append("### 行动建议")
            act = itp.get("action", {})
            lines.append(f"**{act.get('one_liner', '')}**")
            lines.append("")
            if act.get("paths"):
                lines.append("三路径参考：")
                for p in act.get("paths", []):
                    lines.append(f"- {p['name']}（{p['prob']}）：{','.join(p['triggers'])} → {p['action']}")
            if act.get("watch_signals"):
                lines.append(f"- 观察信号：{','.join(act.get('watch_signals', []))}")
        else:
            lines.append("（解读数据未生成）")

        # ── 第10章：神性赋能与天玑判词 ─────────────────────────
        divine = state.get("divine", {})
        if divine:
            lines.append("")
            lines.append("## 10. 天玑判词 · 神性赋能")
            lines.append("")
            # 天机
            timing = divine.get("timing", {})
            lines.append("### 天机·时空同频")
            lines.append(f"- 天时：{timing.get('celestial_time', '')}")
            lines.append(f"- 地利：{timing.get('earthly_location', '')}")
            lines.append(f"- 人和：{timing.get('human_harmony', '')}")
            lines.append(f"- 时代：{timing.get('epoch', '')}")
            lines.append("")
            # 命盘铭文
            verse = divine.get("destiny_verse", {})
            lines.append("### 命盘铭文")
            lines.append(f"**{verse.get('destiny_plate', '')}**")
            lines.append(f"*{verse.get('destiny_poem', '')}*")
            lines.append("")
            lines.append(f"*{verse.get('ten_gods_sigil', '')}*")
            lines.append(f"*{verse.get('useful_god_sigil', '')}*")
            lines.append(f"*{verse.get('forbidden_god_sigil', '')}*")
            lines.append("")
            # 天玑判词
            judgment = divine.get("divine_judgment", {})
            lines.append("### 天玑判词")
            lines.append(f"**{judgment.get('overall_judgment', '')}**")
            lines.append(f"- 奇门：{judgment.get('qimen_judgment', '')}")
            lines.append(f"- 易经：{judgment.get('iching_judgment', '')}")
            lines.append("")
            # 天象
            celestial = divine.get("celestial_sign", {})
            if celestial:
                lines.append("### 奇门天象")
                lines.append(f"- {celestial.get('celestial_map', '')}")
                lines.append(f"- 九宫：{celestial.get('palace_realm', '')}")
                lines.append(f"- 八门：{celestial.get('door_nature', '')}")
                lines.append(f"- 九星：{celestial.get('star_light', '')}")
                lines.append(f"- 八神：{celestial.get('god_command', '')}")
                lines.append("")
            # 三路径神谕
            paths = divine.get("three_paths_divine", [])
            if paths:
                lines.append("### 天机预言·三路径")
                for p in paths:
                    lines.append(f"- **{p['name']}**（{p['celestial_fate']}）：{p['prophecy']}")
                    for s in p.get("divine_signs", []):
                        lines.append(f"  - {s}")
                lines.append("")
            # 核心金句
            golden = divine.get("golden_words", {})
            if golden:
                lines.append("### 核心金句")
                lines.append(f"**{golden.get('golden_sentence', '')}**")
                lines.append(f"- 修：{golden.get('advice', '')}")
                lines.append(f"- 戒：{golden.get('warning', '')}")
                lines.append(f"- 天玑：{golden.get('tianji_motto', '')}")
                lines.append("")
            # 天玑护符
            talisman = divine.get("talisman", {})
            if talisman:
                lines.append("### 天玑护符")
                lines.append(f"**{talisman.get('talisman_text', '')}**")
                lines.append(f"- 符印：{talisman.get('talisman_id', '')}")
                lines.append(f"- 天机：{talisman.get('celestial_elements', '')}")
                lines.append(f"- 命要：{talisman.get('destiny_key', '')}")
                lines.append(f"- 易象：{talisman.get('iching_key', '')}")
                lines.append(f"- 神力：{talisman.get('power_level', '')}")
        return "\n".join(lines) + "\n"

    def save(self, state: dict, out_dir: str | Path) -> dict:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        md = out / f"{state['report_id']}.md"
        js = out / f"{state['report_id']}.json"
        md.write_text(self.render_markdown(state), encoding="utf-8")
        js.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"markdown": str(md), "json": str(js)}
