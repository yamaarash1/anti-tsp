"""Flask dev server — 全APIを1プロセスで起動"""
from flask import Flask
from flask_cors import CORS
from utils.db import ensure_indexes

app = Flask(__name__)
CORS(app)

# 各モジュールのルートを登録
from solve import solve_route
from geocode import geocode
from cities import list_city_sets_route, create_city_set, delete_city_set_route
from users import create_user_route, get_users_route
from history import get_history_route

app.add_url_rule("/api/solve", view_func=solve_route, methods=["POST"])
app.add_url_rule("/api/geocode", view_func=geocode, methods=["POST"])
app.add_url_rule("/api/cities", view_func=list_city_sets_route, methods=["GET"])
app.add_url_rule("/api/cities", view_func=create_city_set, methods=["POST"])
app.add_url_rule("/api/cities", endpoint="delete_city_set", view_func=delete_city_set_route, methods=["DELETE"])
app.add_url_rule("/api/users", view_func=create_user_route, methods=["POST"])
app.add_url_rule("/api/users", view_func=get_users_route, methods=["GET"])
app.add_url_rule("/api/history", view_func=get_history_route, methods=["GET"])

# 初回リクエスト時にインデックス作成
_indexes_done = False

@app.before_request
def _ensure_indexes():
    global _indexes_done
    if not _indexes_done:
        try:
            ensure_indexes()
            _indexes_done = True
        except Exception as e:
            print(f"[DB] Index creation failed: {e}")

if __name__ == "__main__":
    app.run(port=2001, debug=True)
