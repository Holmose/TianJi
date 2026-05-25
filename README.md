# TianJi 天机推演系统

> 东方象数增强型多智能体推演系统：融合现实数据、易经八卦、五行、四柱八字、奇门遁甲与 Multi-Agent Simulation，用于过去反推、未来分支预测与决策推演。

TianJi is an oriental philosophy enhanced multi-agent simulation system for causal reconstruction, future branching, and decision strategy.

## 当前状态

当前版本为 **V1 Prototype**，基于 MiroFish 源码骨架重建，新增 `backend/app/tianji` 天机推演模块，已支持：

- 现实解析 Reality Parser
- 八卦象意 Bagua semantic mapping
- 五行动力 Wuxing dynamics
- 易经趋势 IChing transition seeds
- 本地多 Agent 推演适配器
- 因果回溯
- 未来三路径预测
- Markdown / JSON 报告生成
- CLI 入口
- HTTP API：`/api/tianji/run`

## 快速体验

```bash
cd backend
PYTHONPATH=. python scripts/tianji_cli.py "我现在想做一个东方哲学增强型推演系统，未来这个项目能不能做大？" --domain strategy --goal "判断项目路线" --out reports/tianji
```

输出：

```text
reports/tianji/tianji_YYYYMMDD_HHMMSS.md
reports/tianji/tianji_YYYYMMDD_HHMMSS.json
```

## API

```http
POST /api/tianji/run
```

请求示例：

```json
{
  "question": "我现在想做一个东方哲学增强型推演系统，未来这个项目能不能做大？",
  "domain": "strategy",
  "goal": "判断项目路线",
  "rounds": 3,
  "save_report": true
}
```

## 文档

- [TianJi 详细说明](./README_TIANJI.md)
- [系统架构文档](./docs/TIANJI_ARCHITECTURE.md)
- [API 文档](./docs/API.md)
- [Roadmap](./docs/ROADMAP.md)
- [Contributing](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

## 路线图

### V1：语义推演版

- 八卦象意映射
- 五行动力模型
- 易经语义趋势库
- 本地多 Agent 推演适配
- 因果回溯
- 未来三路径
- 报告生成

### V2：四柱人物模型版

- 干支基础数据
- 十神映射数据
- 出生时间输入
- 近似年/月/日/时柱计算
- 日主识别
- 可见天干十神分析
- 五行比例计算
- 人物长期倾向、风险模式、Agent 参数
- 与 TianJi 报告集成

注意：V2 当前采用公历近似计算，月柱尚未按节气修正，大运/流年/用神分析将在后续版本增强。

### V3：奇门事件局势版

- 事件时间/地点输入
- 语义阳遁/阴遁与局数
- 九宫语义模型
- 八门行动模型
- 九星事件能量模型
- 八神隐性变量模型
- 主客关系判断
- 时机提示、风险提示、行动提示

注意：V3 当前是“语义奇门局势引擎”，尚不是完整传统奇门排盘；节气、阴阳遁精确起局、天地盘、用神定位将在后续版本增强。

### V4：完整 64 卦易经趋势引擎

- 完整 64 卦语义数据集
- 本卦/变卦趋势模型
- 变爻阶段提示
- 趋势转化说明
- 阶段风险与行动提示
- 与多 Agent 推演报告集成

### V5：Hermes / MiroFish 深度集成

- 接入完整版多 Agent 调度
- 接入长期记忆
- 接入图谱系统
- 接入 Web UI
- 预测结果回填与误差分析
- Agent 权重动态校准

## 原则

1. 现实优先，象数辅助。
2. 多路径输出，不做绝对断言。
3. 每个判断尽量标注来源：现实证据 / 象数标签 / Agent 共识。
4. 必须保留反方质疑。
5. 结果必须可复盘、可回填、可迭代。
6. 高风险领域如投资、医疗、法律，只做辅助推演，不替用户决策。

## License & Attribution

This prototype is rebuilt on top of the MiroFish codebase and follows the original AGPL-3.0 license. See [LICENSE](./LICENSE).
