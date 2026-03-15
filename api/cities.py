import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from utils.db import load_city_sets, save_city_set, delete_city_set as db_delete, find_city_set

app = Flask(__name__)


@app.route("/api/cities", methods=["GET"])
def list_city_sets_route():
    set_id = request.args.get("id")
    if set_id:
        found = find_city_set(set_id)
        if not found:
            return jsonify({"error": "見つかりません"}), 404
        return jsonify(found)

    user_id = request.args.get("user_id")
    return jsonify({"city_sets": load_city_sets(user_id=user_id)})


@app.route("/api/cities", methods=["POST"])
def create_city_set():
    data = request.get_json()
    name = data.get("name")
    locations = data.get("locations")
    user_id = data.get("user_id")  # オプション

    if not name or not locations:
        return jsonify({"error": "name と locations が必要です"}), 400

    new_set = {
        "id": str(uuid.uuid4()),
        "name": name,
        "locations": locations,
        "created_at": datetime.utcnow().isoformat(),
    }
    if user_id:
        new_set["user_id"] = user_id

    save_city_set(new_set)
    return jsonify(new_set), 201


@app.route("/api/cities", methods=["DELETE"])
def delete_city_set_route():
    set_id = request.args.get("id")
    if not set_id:
        return jsonify({"error": "id が必要です"}), 400

    if not db_delete(set_id):
        return jsonify({"error": "見つかりません"}), 404

    return jsonify({"ok": True})
