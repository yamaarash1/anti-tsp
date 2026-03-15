from flask import Flask, request, jsonify
from utils.db import create_user, find_user, list_users, get_user_profile_with_stats

app = Flask(__name__)


@app.route("/api/users", methods=["POST"])
def create_user_route():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify({"error": "username が必要です"}), 400

    display_name = data.get("display_name")
    try:
        user = create_user(username, display_name)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route("/api/users", methods=["GET"])
def get_users_route():
    username = request.args.get("username")
    if username:
        user = get_user_profile_with_stats(username)
        if not user:
            return jsonify({"error": "ユーザーが見つかりません"}), 404
        return jsonify(user)
    return jsonify({"users": list_users()})
