from __future__ import annotations

from pathlib import Path
from flask import request, jsonify

from . import tianji_bp
from ..tianji.orchestrator import TianJiOrchestrator
from ..tianji.report_generator import TianJiReportGenerator


@tianji_bp.route('/run', methods=['POST'])
def run_tianji():
    data = request.get_json(silent=True) or {}
    question = data.get('question') or data.get('query') or ''
    if not question.strip():
        return jsonify({"success": False, "error": "question is required"}), 400
    domain = data.get('domain', 'unknown')
    goal = data.get('goal', '')
    event_time = data.get('event_time')
    location = data.get('location')
    birth_datetime = data.get('birth_datetime')
    gender = data.get('gender')
    rounds = int(data.get('rounds', 3))
    save_report = bool(data.get('save_report', True))
    state = TianJiOrchestrator().run(question, domain, goal, event_time, location, rounds, birth_datetime, gender)
    result = {"success": True, "state": state}
    if save_report:
        out_dir = Path(data.get('out_dir', 'reports/tianji'))
        result["files"] = TianJiReportGenerator().save(state, out_dir)
    return jsonify(result)


@tianji_bp.route('/health', methods=['GET'])
def tianji_health():
    return jsonify({"success": True, "service": "TianJi", "version": "0.4.0"})
