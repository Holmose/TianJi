# TianJi Roadmap

## Vision

TianJi aims to become an oriental philosophy enhanced multi-agent simulation system for:

- causal reconstruction
- future branching
- strategic decision support
- symbolic state modeling
- retrospective learning

The system should never become a deterministic prophecy machine. Its output must stay probabilistic, evidence-aware, and action-oriented.

## V1: Semantic Simulation Prototype

Status: in progress / initial prototype completed.

### Goals

- Rebuild from MiroFish codebase into TianJi project identity.
- Add independent TianJi backend module.
- Build a semantic symbolic engine.
- Generate structured reports.
- Provide CLI and API entry points.

### Completed

- `backend/app/tianji/state_model.py`
- `backend/app/tianji/engines/reality_parser.py`
- `backend/app/tianji/engines/symbolic_engine.py`
- `backend/app/tianji/engines/simulation_adapter.py`
- `backend/app/tianji/orchestrator.py`
- `backend/app/tianji/report_generator.py`
- `backend/scripts/tianji_cli.py`
- `/api/tianji/run`
- `/api/tianji/health`
- `README_TIANJI.md`
- `docs/TIANJI_ARCHITECTURE.md`
- `docs/API.md`

### Next tasks

- Add frontend TianJi page.
- Add full 64 IChing hexagram semantic dataset.
- Add unit tests.
- Add sample reports.
- Replace inherited MiroFish branding with TianJi branding where appropriate.

## V2: Bazi Natal Pattern Engine

Status: initial implementation completed.

### Goals

Turn Four Pillars / Bazi into a long-term personality and cycle model.

### Implemented modules

```text
backend/app/tianji/engines/bazi_engine.py
backend/app/tianji/data/tiangan_dizhi.json
backend/app/tianji/data/ten_gods.json
```

### Current capabilities

- Birth datetime input: `YYYY-MM-DD HH:MM`.
- Approximate year/month/day/hour pillars.
- Day master.
- Visible stem ten gods.
- Five-element balance.
- Dominant elements.
- Personality bias.
- Risk pattern.
- Agent parameters.
- CLI/API/report integration.

### Limitations

- Month pillar is not solar-term corrected yet.
- Lunar calendar conversion is not implemented yet.
- Luck cycles are not implemented yet.
- Useful god and strength/weakness analysis are not implemented yet.

### Output role

Bazi provides long-cycle parameters for agents, not deterministic fate conclusions.

## V3: Qimen Situation Engine

Status: initial semantic implementation completed.

### Goals

Turn Qimen Dunjia into a concrete event situation and timing model.

### Implemented modules

```text
backend/app/tianji/engines/qimen_engine.py
backend/app/tianji/data/jiugong.json
backend/app/tianji/data/bamen.json
backend/app/tianji/data/jiuxing.json
backend/app/tianji/data/bashen.json
```

### Current capabilities

- Event time input.
- Location input.
- Semantic Yin/Yang Dun and Ju label.
- Nine palaces semantic mapping.
- Eight doors action model.
- Nine stars event-energy model.
- Eight gods hidden-variable model.
- Host/guest posture hint.
- Timing hint.
- Risk hint.
- Action hint.
- Report and simulation adapter integration.

### Limitations

- No precise solar-term Qimen calculation yet.
- No heaven/earth plate layout yet.
- No useful god selection yet.
- No traditional full Sanqi-Liuyi arrangement yet.

### Output role

Qimen models current event situation and action timing, not deterministic prophecy.

## V4: I Ching 64-Hexagram Transition Engine

Status: initial semantic implementation completed.

### Goals

Upgrade the trend layer from seed hexagrams to a full 64-hexagram transition model.

### Implemented modules

```text
backend/app/tianji/engines/iching_engine.py
backend/app/tianji/data/iching_64_hexagrams.json
```

### Current capabilities

- Full 64-hexagram semantic dataset.
- Primary hexagram selection by question/domain.
- Changing-line generation by text/time seed.
- Changed hexagram transition.
- Stage warning by changing-line position.
- Action hint combining primary and changed hexagram strategies.
- Report integration.
- Simulation adapter integration.

### Limitations

- No nuclear hexagram yet.
- No traditional line texts yet.
- No manual coin/yarrow input yet.
- Semantic selection should be replaced or supplemented by explicit divination modes in later versions.

## V5: Full Hermes / MiroFish Integration

### Goals

Replace the V1 deterministic local adapter with the full multi-agent engine.

### Integration points

- Simulation manager.
- Long-term memory.
- Knowledge graph.
- Project artifacts.
- Agent profile generation.
- Report agent.
- Frontend workflow.

### Planned change

```text
LocalSimulationEngine
        ↓
HermesMiroFishSimulationEngine
```

The TianJi state object remains stable. Only the simulation adapter changes.

## V5: Retrospective Learning Loop

### Goals

Make TianJi self-calibrating through outcome feedback.

### Capabilities

- Prediction result tracking.
- Actual outcome feedback.
- Error analysis.
- Agent weight adjustment.
- Symbolic rule evaluation.
- Case library.
- Confidence calibration.

## Quality Principles

1. Reality evidence has priority over symbolic interpretation.
2. All future predictions must be branches, not single deterministic claims.
3. Every report must include blind spots.
4. Skeptic Agent must always be present.
5. Symbolic conclusions must be translated into real-world action language.
6. High-risk domains require explicit disclaimers and no direct decision replacement.
