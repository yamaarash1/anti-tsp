from flask import Flask, request, jsonify
from utils.tsp_solver import solve
from utils.db import save_history, find_user

app = Flask(__name__)


@app.route("/api/solve", methods=["POST"])
def solve_route():
    data = request.get_json()
    locations = data.get("locations")
    user_id = data.get("user_id")  # オプション

    if not locations or len(locations) < 3:
        return jsonify({"error": "3件以上の都市が必要です"}), 400
    if len(locations) > 8:
        return jsonify({"error": "8件以下にしてください"}), 400

    try:
        result = solve(locations)

        # user_id が指定されていれば自動的に履歴保存
        if user_id and find_user(user_id):
            save_history(user_id, locations, result)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
