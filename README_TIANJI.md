# TianJi 天机推演系统

> 东方象数增强型多智能体推演系统。基于 MiroFish / Hermes 思路重建，目标是把现实信息、东方哲学建模、多 Agent 沙盘推演、因果回溯、未来分支预测整合成一个可持续升级的开源系统。

## 1. 项目定位

TianJi 不是单纯的算命工具，也不是只服务情感领域的聊天分析器。

它的定位是：

```text
现实数据 + 东方象数 + 多 Agent 推演 + 因果回溯 + 概率未来 + 行动策略
```

东方象数体系在本项目中不是“绝对预言”，而是作为一种世界状态建模语言：

- 八卦：状态象意标签
- 五行：动力关系与风险结构
- 易经：趋势演化模型
- 四柱八字：人物长期结构模型（V2）
- 奇门遁甲：事件局势与行动时机模型（V3）

## 2. 当前版本

当前为 **TianJi V1 原型版**：

- 已从 MiroFish 源码复制并建立独立项目骨架
- 新增 `backend/app/tianji/` 天机模块
- 新增八卦、五行、易经语义种子库
- 新增 Reality Parser 现实解析器
- 新增 Symbolic Engine 东方象数语义引擎
- 新增 Local Simulation Adapter 本地多 Agent 推演适配器
- 新增 TianJi Orchestrator 总调度器
- 新增 Markdown / JSON 报告生成器
- 新增 CLI 入口

V1 先保证能跑通完整链路，后续再接入完整版 Hermes / MiroFish 的真实多 Agent、记忆、图谱与 Web UI。

## 3. 架构

```text
用户问题/事件资料
        ↓
Reality Parser 现实解析器
        ↓
Symbolic Engine 东方象数引擎
  - Bagua 八卦
  - Wuxing 五行
  - IChing 易经语义
  - Bazi 四柱接口占位
  - Qimen 奇门接口占位
        ↓
TianJi Orchestrator 总调度
        ↓
Simulation Adapter 多 Agent 推演适配
        ↓
Causal Engine 因果回溯
        ↓
Future Branch Engine 未来分支
        ↓
Strategy Engine 行动策略
        ↓
Report Generator 报告输出
```

## 4. 快速开始

### 4.1 后端 CLI 原型运行

```bash
cd backend
python scripts/tianji_cli.py "我现在想做一个东方哲学增强型推演系统，未来这个项目能不能做大？" --domain strategy --goal "判断项目路线" --out reports/tianji
```

输出：

```text
reports/tianji/tianji_YYYYMMDD_HHMMSS.md
reports/tianji/tianji_YYYYMMDD_HHMMSS.json
```

### 4.2 输出报告包含

- 总断
- 现实底盘
- 象数建模
- 多 Agent 推演过程
- 过去反推
- 未来三路径
- 当前最优策略
- 置信度与盲区

## 5. 目录说明

```text
backend/app/tianji/
  __init__.py
  state_model.py              # TianJiState 数据结构
  orchestrator.py             # 总调度器
  report_generator.py         # Markdown/JSON报告生成
  data/
    bagua.json                # 八卦象意库
    wuxing.json               # 五行动力库
    iching_64_hexagrams.json  # 易经64卦语义库
    tiangan_dizhi.json        # 天干地支数据
    ten_gods.json             # 十神映射数据
    jiugong.json              # 九宫语义数据
    bamen.json                # 八门语义数据
    jiuxing.json              # 九星语义数据
    bashen.json               # 八神语义数据
  engines/
    reality_parser.py         # 现实解析器
    symbolic_engine.py        # 八卦/五行象意引擎
    iching_engine.py          # V4 易经64卦趋势引擎
    bazi_engine.py            # V2 四柱人物结构引擎
    qimen_engine.py           # V3 奇门事件局势引擎
    simulation_adapter.py     # 本地多Agent适配器
backend/scripts/
  tianji_cli.py               # CLI入口
```

## 6. Agent 角色设计

V1 内置 10 类 Agent 角色，后续会接入真实 Hermes / MiroFish Agent：

1. Reality Agent：现实事实派
2. Causal Agent：因果链派
3. Risk Agent：风险派
4. Strategy Agent：策略派
5. Bazi Agent：四柱结构派
6. Qimen Agent：奇门局势派
7. IChing Agent：易经趋势派
8. Wuxing Agent：五行平衡派
9. Skeptic Agent：反玄学校验派
10. Synthesizer Agent：总结收敛派

其中 Skeptic Agent 是强制角色，用于防止系统把象数解释包装成绝对预言。

## 7. 路线图

### V1：语义推演版

- 八卦象意映射
- 五行动力模型
- 易经语义趋势库
- 本地多 Agent 推演适配
- 因果回溯
- 未来三路径
- 报告生成

### V2：四柱人物模型版

- 干支历法
- 日主/十神/五行强弱
- 大运/流年/流月基础
- 人物长期结构参数
- 与 Agent 人物画像融合

### V3：奇门事件局势版

- 起局时间/地点
- 阴阳遁
- 九宫/八门/九星/八神
- 三奇六仪
- 用神定位
- 主客关系与行动时机

### V4：易经 64 卦趋势演化引擎

- 完整 64 卦语义数据
- 本卦/变卦
- 变爻阶段提示
- 趋势转化
- 阶段风险
- 行动提示

### V5：Hermes / MiroFish 深度集成

- 接入完整版多 Agent 调度
- 接入长期记忆
- 接入图谱系统
- 接入 Web UI
- 预测结果回填与误差分析
- Agent 权重动态校准

## 8. 使用原则

1. 现实优先，象数辅助。
2. 多路径输出，不做绝对断言。
3. 每个判断尽量标注来源：现实证据 / 象数标签 / Agent 共识。
4. 必须保留反方质疑。
5. 结果必须可复盘、可回填、可迭代。
6. 高风险领域如投资、医疗、法律，只做辅助推演，不替用户决策。

## 9. 开源说明

本项目当前基于 MiroFish 源码原型重建，保留原项目许可证信息。后续上传到你的仓库前，需要根据目标开源策略补充：

- LICENSE 继承与说明
- 原项目 Attribution
- 项目 Logo / 名称替换
- 安装部署文档
- API 文档
- 贡献指南

## 10. 当前状态

当前版本为 **V0.4.0 / V1-V4 Prototype Completed**，已在本地 CLI 与 `/api/tianji/run` 跑通完整链路：

1. V1 语义推演底座：现实解析、八卦、五行、多 Agent、因果回溯、未来三路径。
2. V2 四柱人物长期结构：出生时间、近似四柱、日主、十神、五行比例、人物倾向、风险模式。
3. V3 奇门事件局势：事件时间/地点、九宫、八门、九星、八神、主客关系、时机和风险提示。
4. V4 易经64卦趋势：本卦、变卦、变爻阶段提示、趋势转化和行动建议。

下一步建议：

1. 做 V5 示例库与测试体系。
2. 替换前端遗留 MiroFish 品牌为 TianJi。
3. 接入真实 Hermes / MiroFish simulation manager。
4. 增加预测结果回填与误差分析。
