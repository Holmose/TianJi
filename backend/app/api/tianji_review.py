"""TianJi review / feedback storage system."""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from flask import Blueprint, jsonify, request

tianji_review_bp = Blueprint("tianji-review", __name__)

REVIEW_DIR = Path(__file__).resolve().parent.parent.parent.parent / "reports" / "reviews"
REVIEW_DIR.mkdir(parents=True, exist_ok=True)


def _review_path(report_id: str) -> Path:
    return REVIEW_DIR / f"{report_id}.json"


def _list_reviews(limit: int = 50) -> list[dict]:
    reviews = []
    for f in sorted(REVIEW_DIR.glob("*.json"), key=lambda x: -x.stat().st_mtime):
        try:
            with open(f, encoding="utf-8") as fh:
                reviews.append(json.load(fh))
        except Exception:
            pass
        if len(reviews) >= limit:
            break
    return reviews


@tianji_review_bp.route("/reviews", methods=["GET"])
def list_reviews():
    """List recent reviews."""
    limit = int(request.args.get("limit", 50))
    return jsonify({"success": True, "reviews": _list_reviews(limit=limit)})


@tianji_review_bp.route("/reviews/<report_id>", methods=["GET"])
def get_review(report_id: str):
    """Get a specific review."""
    p = _review_path(report_id)
    if not p.exists():
        return jsonify({"success": False, "error": "Review not found"}), 404
    with open(p, encoding="utf-8") as fh:
        return jsonify({"success": True, "review": json.load(fh)})


@tianji_review_bp.route("/reviews/<report_id>", methods=["POST"])
def save_review(report_id: str):
    """Save or update a review for a report."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data"}), 400

    review = {
        "report_id": report_id,
        "timestamp": datetime.now().isoformat(),
        "actual_outcome": data.get("actual_outcome", ""),
        "prediction_accuracy": data.get("prediction_accuracy", ""),
        "deviation_points": data.get("deviation_points", []),
        "what_went_wrong": data.get("what_went_wrong", ""),
        "what_went_right": data.get("what_went_right", ""),
        "correction_note": data.get("correction_note", ""),
        "user_tags": data.get("user_tags", []),
        "will_use_again": data.get("will_use_again", None),
        "metadata": data.get("metadata", {}),
    }

    p = _review_path(report_id)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(review, fh, ensure_ascii=False, indent=2)

    return jsonify({"success": True, "review": review})


@tianji_review_bp.route("/reviews/<report_id>", methods=["DELETE"])
def delete_review(report_id: str):
    """Delete a review."""
    p = _review_path(report_id)
    if not p.exists():
        return jsonify({"success": False, "error": "Review not found"}), 404
    p.unlink()
    return jsonify({"success": True, "deleted": report_id})


@tianji_review_bp.route("/stats", methods=["GET"])
def review_stats():
    """Get review statistics."""
    reviews = _list_reviews(limit=200)
    if not reviews:
        return jsonify({
            "success": True,
            "total": 0,
            "accuracy_breakdown": {},
            "common_deviations": [],
            "recent_trend": []
        })

    total = len(reviews)
    accuracy_counts = {}
    deviation_flat = []
    recent_trend = []

    for r in reviews[:20]:
        acc = r.get("prediction_accuracy", "unknown")
        accuracy_counts[acc] = accuracy_counts.get(acc, 0) + 1

    for r in reviews[:50]:
        for d in r.get("deviation_points", []):
            deviation_flat.append(d)

    deviation_counts = {}
    for d in deviation_flat:
        deviation_counts[d] = deviation_counts.get(d, 0) + 1
    common = sorted(deviation_counts.items(), key=lambda x: -x[1])[:10]

    for r in reviews[:10]:
        recent_trend.append({
            "report_id": r.get("report_id"),
            "timestamp": r.get("timestamp"),
            "accuracy": r.get("prediction_accuracy"),
            "outcome": r.get("actual_outcome", "")[:50]
        })

    return jsonify({
        "success": True,
        "total": total,
        "accuracy_breakdown": accuracy_counts,
        "common_deviations": common,
        "recent_trend": recent_trend
    })
