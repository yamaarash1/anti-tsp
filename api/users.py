from flask import Flask, request, jsonify
from utils.db import (
    create_user, authenticate_user, find_user, list_users,
    get_user_profile_with_stats, update_user, verify_password,
)

app = Flask(__name__)


@app.route("/api/auth/register", methods=["POST"])
def register_route():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    display_name = data.get("display_name")

    if not username or not email or not password:
        return jsonify({"error": "username, email, password は必須です"}), 400
    if len(password) < 6:
        return jsonify({"error": "パスワードは6文字以上にしてください"}), 400

    try:
        user = create_user(username, email, password, display_name)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route("/api/auth/login", methods=["POST"])
def login_route():
    data = request.get_json()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email と password は必須です"}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"error": "メールアドレスまたはパスワードが正しくありません"}), 401

    return jsonify(user)


@app.route("/api/users/me", methods=["GET"])
def get_me_route():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username が必要です"}), 400

    user = get_user_profile_with_stats(username)
    if not user:
        return jsonify({"error": "ユーザーが見つかりません"}), 404
    return jsonify(user)


@app.route("/api/users/me", methods=["PUT"])
def update_me_route():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"error": "username が必要です"}), 400

    updates = {}
    if "display_name" in data:
        updates["display_name"] = data["display_name"]

    if "new_password" in data:
        current_password = data.get("current_password") or ""
        if not verify_password(username, current_password):
            return jsonify({"error": "現在のパスワードが正しくありません"}), 400
        if len(data["new_password"]) < 6:
            return jsonify({"error": "新しいパスワードは6文字以上にしてください"}), 400
        updates["password"] = data["new_password"]

    user = update_user(username, updates)
    if not user:
        return jsonify({"error": "ユーザーが見つかりません"}), 404
    return jsonify(user)


@app.route("/api/users", methods=["GET"])
def get_users_route():
    username = request.args.get("username")
    if username:
        user = get_user_profile_with_stats(username)
        if not user:
            return jsonify({"error": "ユーザーが見つかりません"}), 404
        return jsonify(user)
    return jsonify({"users": list_users()})
