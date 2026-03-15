from flask import Flask, request, jsonify
from utils.db import load_graph_points, load_graph_edges, save_history, find_user
from utils.graph_solver import solve_graph

app = Flask(__name__)


@app.route("/api/graph/points", methods=["GET"])
def get_graph_points():
    return jsonify(load_graph_points())


@app.route("/api/graph/edges", methods=["GET"])
def get_graph_edges():
    return jsonify(load_graph_edges())


@app.route("/api/graph/solve", methods=["POST"])
def solve_graph_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "リクエストボディが必要です"}), 400

    start = data.get("start")
    end = data.get("end")
    user_id = data.get("user_id")

    if not start or not end:
        return jsonify({"error": "start と end が必要です"}), 400
    if start == end:
        return jsonify({"error": "始点と終点は異なる必要があります"}), 400

    points = load_graph_points()
    edges = load_graph_edges()

    point_names = {p["name"] for p in points}
    if start not in point_names or end not in point_names:
        return jsonify({"error": "指定されたポイントが見つかりません"}), 400

    result = solve_graph(start, end, edges)

    # ユーザー指定時は履歴保存
    if user_id and find_user(user_id):
        save_history(user_id, points, result)

    return jsonify({
        "shortest": result["shortest"],
        "longest": result["longest"],
        "points": points,
        "edges": edges,
    })
