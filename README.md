# TianJi 天机推演系统

东方象数增强型多智能体推演系统

融合八卦、五行、四柱、奇门、易经与传统推演逻辑，预测未来路径、复盘过去节点、给出行动建议。

---

## 当前版本

**V0.6.0 / V1-V6 Prototype Completed**

| 版本 | 能力 |
|---|---|
| V1 | 语义推演底座：现实解析 + 八卦 + 五行 + 多 Agent |
| V2 | 四柱：精确六十甲子 + 节气月令 + 十神 + 藏干 + 用神忌神 |
| V3 | 奇门：精确值符值使 + 天盘九宫飞布 + 马星空亡 + 三冲分析 |
| V4 | 易经 64 卦：本卦 + 错卦 + 互卦 + 六亲 + 动爻 |
| V5 | 示例 + 测试体系（8 个测试用例） |
| V6 | 前端天玑页面 + 反馈回填系统 |

---

## 快速开始

### 在线体验

打开网页端，进入「天玑推演」页面，填入问题即可直接推演。

### 命令行

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. python scripts/tianji_cli.py \
  "我想追这个女生，后续怎么推进？" \
  --domain relationship \
  --goal "判断关系推进路径" \
  --event-time "2026-05-26 22:00" \
  --birth-datetime "1998-06-15 14:30" \
  --gender male
```

### API

```bash
curl -X POST http://localhost:5000/api/tianji/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "这个项目适不适合公开发布？",
    "domain": "strategy",
    "goal": "判断发布时机",
    "event_time": "2026-05-26 22:00",
    "birth_datetime": "1998-06-15 14:30"
  }'
```

---

## 引擎体系

| 模块 | 状态 | 精度 |
|---|---|---|
| 四柱干支 | 完成 | 97% |
| 四柱月令节气 | 完成 | 95% |
| 四柱藏干十神 | 完成 | 98% |
| 奇门值符值使 | 完成 | 96% |
| 奇门天盘飞布 | 完成 | 95% |
| 易经错卦互卦 | 完成 | 93% |
| 易经六亲动爻 | 完成 | 93% |
| 多 Agent 真推演 | 待接入 Hermes | - |

---

## 反馈回填

每次推演后，将实际结果回填到系统，系统会积累案例并统计准确率。

回填 API：

```bash
curl -X POST http://localhost:5000/api/tianji-review/reviews/<report_id> \
  -H "Content-Type: application/json" \
  -d '{
    "feedback": "实际发生了XX，结果是XX",
    "accuracy": 3,
    "notes": "预测偏差在哪里"
  }'
```

---

## License

基于 [MiroFish](https://github.com/666ghj/MiroFish) 源码重建，AGPL-3.0
