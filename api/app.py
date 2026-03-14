"""Flask dev server — 全APIを1プロセスで起動"""
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 各モジュールのルートを登録
from solve import solve_route
from geocode import geocode
from cities import list_city_sets, create_city_set, delete_city_set

app.add_url_rule("/api/solve", view_func=solve_route, methods=["POST"])
app.add_url_rule("/api/geocode", view_func=geocode, methods=["POST"])
app.add_url_rule("/api/cities", view_func=list_city_sets, methods=["GET"])
app.add_url_rule("/api/cities", view_func=create_city_set, methods=["POST"])
app.add_url_rule("/api/cities", endpoint="delete_city_set", view_func=delete_city_set, methods=["DELETE"])

if __name__ == "__main__":
    app.run(port=2001, debug=True)
