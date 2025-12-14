"""Minimal Flask backend exposing the MajorMatch recommender."""

from __future__ import annotations

from flask import Flask, jsonify, request
from flask_cors import CORS

from major_matcher import normalize_user_data, recommend

app = Flask(__name__)
CORS(app)


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    payload = request.get_json(force=True, silent=True) or {}

    normalized = normalize_user_data(payload)
    try:
        recommendations = recommend(normalized)
    except Exception as exc:  # pragma: no cover - surfaced via JSON
        return jsonify({"error": str(exc)}), 500

    if not recommendations:
        return jsonify({
            "top_recommendation": None,
            "alternatives": [],
            "message": "No recommendation available. Please add more details.",
        })

    top = recommendations[0]
    alternatives = recommendations[1:]
    return jsonify({
        "top_recommendation": top,
        "alternatives": alternatives,
        "message": "success",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
