from app.tianji.engines.qimen_engine import QimenEngine


def test_qimen_engine_missing_event_time():
    result = QimenEngine().analyze()
    assert result["status"] == "missing_event_time"


def test_qimen_engine_basic_output():
    result = QimenEngine().analyze("2026-05-26 21:30", location="Guangzhou", question="是否适合发布", domain="strategy")
    assert result["status"] == "ok"
    assert result["bureau"]["label"]
    assert result["main_palace"]["name"]
    assert result["door"]["name"]
    assert result["star"]["name"]
    assert result["god"]["name"]
    assert result["timing_hint"]
    assert result["risk_hint"]
    assert result["useful_god"]["useful_palace"]
    assert len(result["board"]) == 9


def test_qimen_engine_nine_palace_board():
    result = QimenEngine().analyze("2026-05-26 22:30", domain="strategy")
    assert len(result["board"]) == 9
    assert all(p in result["board"] for p in ["坎一宫", "坤二宫", "震三宫", "巽四宫", "中五宫", "乾六宫", "兑七宫", "艮八宫", "离九宫"])
