from flask import Flask, request, jsonify
from utils.tsp_solver import solve

app = Flask(__name__)


@app.route("/api/solve", methods=["POST"])
def solve_route():
    data = request.get_json()
    locations = data.get("locations")
    if not locations or len(locations) < 3:
        return jsonify({"error": "3件以上の都市が必要です"}), 400
    if len(locations) > 8:
        return jsonify({"error": "8件以下にしてください"}), 400

    try:
        result = solve(locations)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
