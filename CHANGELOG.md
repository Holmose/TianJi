# Changelog

All notable changes to TianJi will be documented in this file.

## [0.4.0] - 2026-05-26

### Added

- Added V4 I Ching Transition Engine.
- Added full 64-hexagram semantic dataset: `iching_64_hexagrams.json`.
- Added `backend/app/tianji/engines/iching_engine.py`.
- Added primary hexagram and changed hexagram trend modeling.
- Added changing-line based stage warnings.
- Integrated I Ching transition output into reports.
- Integrated I Ching action hints into local simulation adapter.

### Notes

- V4 is a semantic trend engine, not deterministic divination.
- Nuclear hexagram and line-by-line traditional texts are planned for future versions.

## [0.3.0] - 2026-05-26

### Added

- Added V3 Qimen Situation Engine.
- Added `backend/app/tianji/engines/qimen_engine.py`.
- Added Qimen semantic datasets:
  - `jiugong.json`
  - `bamen.json`
  - `jiuxing.json`
  - `bashen.json`
- Integrated event-time based Qimen semantic situation analysis into Orchestrator.
- Integrated Qimen layout rendering into Markdown reports.
- Enhanced local simulation adapter with Qimen timing hints.

### Notes

- V3 uses semantic Qimen layout, not yet full traditional solar-term Qimen calculation.
- Solar terms, Yin/Yang Dun precision, Ju number, heaven/earth plates, and useful god selection are planned for future versions.

## [0.2.0] - 2026-05-26

### Added

- Added V2 Bazi Natal Pattern Engine.
- Added `backend/app/tianji/engines/bazi_engine.py`.
- Added Heavenly Stems and Earthly Branches data: `tiangan_dizhi.json`.
- Added Ten Gods mapping data: `ten_gods.json`.
- Added birth datetime support in CLI.
- Added birth datetime and gender support in API.
- Integrated Bazi output into TianJi Orchestrator.
- Integrated Bazi result rendering into Markdown reports.
- Updated API docs and roadmap for V2.

### Notes

- V2 uses approximate solar-calendar pillar calculation.
- Month pillar is not yet corrected by solar terms.
- Luck cycles, useful god, and strength analysis are planned for future versions.

## [0.1.0] - 2026-05-26

### Added

- Initial TianJi V1 prototype based on MiroFish codebase.
- Added independent `backend/app/tianji` module.
- Added TianJi state model.
- Added Reality Parser.
- Added Bagua semantic dataset.
- Added Wuxing dynamics dataset.
- Added IChing semantic seed dataset.
- Added Symbolic Engine.
- Added Local Simulation Adapter with 10 agent roles:
  - Reality Agent
  - Causal Agent
  - Risk Agent
  - Strategy Agent
  - Bazi Agent
  - Qimen Agent
  - IChing Agent
  - Wuxing Agent
  - Skeptic Agent
  - Synthesizer Agent
- Added TianJi Orchestrator.
- Added Markdown/JSON Report Generator.
- Added CLI entry: `backend/scripts/tianji_cli.py`.
- Added HTTP API:
  - `GET /api/tianji/health`
  - `POST /api/tianji/run`
- Added `README_TIANJI.md`.
- Added `docs/TIANJI_ARCHITECTURE.md`.
- Added `docs/API.md`.
- Added `docs/ROADMAP.md`.
- Added `CONTRIBUTING.md`.
- Added `NOTICE.md` attribution file.

### Changed

- Updated root `README.md` for TianJi project identity.
- Updated root `package.json` name and description.
- Registered TianJi Flask blueprint.

### Removed

- Removed inherited GitHub workflow from original codebase to avoid token workflow-scope push issue.
