# API Documentation

## TianJi API

Base prefix:

```text
/api/tianji
```

## Health Check

```http
GET /api/tianji/health
```

Response:

```json
{
  "success": true,
  "service": "TianJi",
  "version": "0.4.0"
}
```

## Run TianJi Simulation

```http
POST /api/tianji/run
Content-Type: application/json
```

### Request Body

```json
{
  "question": "我现在想做一个东方哲学增强型推演系统，未来这个项目能不能做大？",
  "domain": "strategy",
  "goal": "判断项目路线",
  "event_time": "2026-05-26 02:00:00",
  "location": "Guangzhou, China",
  "birth_datetime": "1998-06-15 14:30",
  "gender": "male",
  "rounds": 3,
  "save_report": true,
  "out_dir": "reports/tianji"
}
```

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `question` | string | yes | The raw question or event background to simulate. |
| `domain` | string | no | `relationship`, `business`, `content`, `personal`, `strategy`, or `unknown`. Defaults to `unknown`. |
| `goal` | string | no | User objective. |
| `event_time` | string | no | Event/start time. Used by V3 Qimen situation engine and V4 I Ching changing-line seed. |
| `location` | string | no | Event location. Used by V3 Qimen output context. |
| `birth_datetime` | string | no | Birth datetime for V2 Bazi engine. Format: `YYYY-MM-DD HH:MM`. |
| `gender` | string | no | Gender marker for future luck-cycle direction extensions. |
| `rounds` | integer | no | Simulation rounds. V1 local adapter defaults to `3`. |
| `save_report` | boolean | no | Whether to save Markdown/JSON report files. Defaults to `true`. |
| `out_dir` | string | no | Output report directory. Defaults to `reports/tianji`. |

### Response

```json
{
  "success": true,
  "state": {
    "report_id": "tianji_YYYYMMDD_HHMMSS",
    "timestamp": "2026-05-26T02:00:00",
    "query": {},
    "reality": {},
    "symbolic": {},
    "simulation": {},
    "causal": {},
    "future": {},
    "strategy": {},
    "confidence": {}
  },
  "files": {
    "markdown": "reports/tianji/tianji_YYYYMMDD_HHMMSS.md",
    "json": "reports/tianji/tianji_YYYYMMDD_HHMMSS.json"
  }
}
```

## Core Output Sections

### `reality`

Parsed real-world context:

- facts
- timeline
- people
- known variables
- unknown variables
- constraints

### `symbolic`

Oriental symbolic state:

- bagua: 八卦状态象意
- wuxing: 五行动力结构
- iching: V4 64卦趋势演化，本卦/变卦/变爻/阶段风险
- bazi: V2 四柱人物长期结构，出生时间缺失时返回 `missing_birth_datetime`
- qimen: V3 奇门事件局势，事件时间缺失时返回 `missing_event_time`

### `simulation`

Multi-agent simulation output:

- agents
- rounds
- consensus
- disagreements

### `causal`

Past reconstruction:

- past turning points
- causal chain
- missed signals

### `future`

Future branching:

- A 顺势发展
- B 中途受阻
- C 突发反转

### `strategy`

Decision strategy:

- best action
- forbidden actions
- watch signals
- change conditions

### `confidence`

Confidence and blind spots:

- level
- blind spots
- principle

## CLI Equivalent

```bash
cd backend
PYTHONPATH=. python scripts/tianji_cli.py "你的问题" --domain strategy --goal "你的目标" --out reports/tianji
```
