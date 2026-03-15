from flask import Flask, request, jsonify
from utils.db import get_user_history_with_lookup

app = Flask(__name__)


@app.route("/api/history", methods=["GET"])
def get_history_route():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id が必要です"}), 400

    limit = request.args.get("limit", 50, type=int)
    limit = min(max(limit, 1), 200)

    history = get_user_history_with_lookup(user_id, limit)
    return jsonify({"history": history})
