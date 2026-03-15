"""
シードデータ投入スクリプト
使い方: cd api && python scripts/seed.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.db import get_db, ensure_indexes
from utils.tsp_solver import solve
from werkzeug.security import generate_password_hash

db = get_db()

# === 既存データをクリア ===
print("Clearing existing data...")
db.users.delete_many({})
db.city_sets.delete_many({})
db.calculation_history.delete_many({})

# === インデックス作成 ===
ensure_indexes()

# === ユーザー (全員パスワード: password123) ===
DEFAULT_PW = generate_password_hash("password123")
USERS = [
    {"username": "taro", "email": "taro@example.com", "password_hash": DEFAULT_PW, "display_name": "太郎", "created_at": "2026-01-10T09:00:00+00:00", "updated_at": "2026-01-10T09:00:00+00:00"},
    {"username": "hanako", "email": "hanako@example.com", "password_hash": DEFAULT_PW, "display_name": "花子", "created_at": "2026-02-15T10:00:00+00:00", "updated_at": "2026-02-15T10:00:00+00:00"},
    {"username": "jiro", "email": "jiro@example.com", "password_hash": DEFAULT_PW, "display_name": "次郎", "created_at": "2026-03-01T11:00:00+00:00", "updated_at": "2026-03-01T11:00:00+00:00"},
]
db.users.insert_many(USERS)
print(f"  users: {len(USERS)} 件挿入")

# === 都市セット ===
CITY_SETS = [
    {
        "id": "set-kanto",
        "name": "関東エリア",
        "user_id": "taro",
        "locations": [
            {"name": "東京駅", "lat": 35.6812, "lng": 139.7671},
            {"name": "横浜駅", "lat": 35.4658, "lng": 139.6223},
            {"name": "大宮駅", "lat": 35.9064, "lng": 139.6239},
            {"name": "千葉駅", "lat": 35.6131, "lng": 140.1135},
        ],
        "created_at": "2026-01-15T12:00:00+00:00",
    },
    {
        "id": "set-kansai",
        "name": "関西エリア",
        "user_id": "taro",
        "locations": [
            {"name": "大阪駅", "lat": 34.7024, "lng": 135.4959},
            {"name": "京都駅", "lat": 34.9858, "lng": 135.7588},
            {"name": "神戸駅", "lat": 34.6797, "lng": 135.1783},
            {"name": "奈良駅", "lat": 34.6802, "lng": 135.8190},
        ],
        "created_at": "2026-01-20T14:00:00+00:00",
    },
    {
        "id": "set-tohoku",
        "name": "東北エリア",
        "user_id": "hanako",
        "locations": [
            {"name": "仙台駅", "lat": 38.2602, "lng": 140.8824},
            {"name": "盛岡駅", "lat": 39.7014, "lng": 141.1369},
            {"name": "秋田駅", "lat": 39.7171, "lng": 140.1029},
            {"name": "山形駅", "lat": 38.2488, "lng": 140.3279},
        ],
        "created_at": "2026-02-20T09:00:00+00:00",
    },
    {
        "id": "set-kyushu",
        "name": "九州エリア",
        "user_id": "hanako",
        "locations": [
            {"name": "福岡駅", "lat": 33.5902, "lng": 130.4207},
            {"name": "熊本駅", "lat": 32.7899, "lng": 130.6879},
            {"name": "鹿児島中央駅", "lat": 31.5842, "lng": 130.5416},
            {"name": "長崎駅", "lat": 32.7519, "lng": 129.8694},
        ],
        "created_at": "2026-02-25T10:00:00+00:00",
    },
    {
        "id": "set-tokaido",
        "name": "東海道エリア",
        "user_id": "jiro",
        "locations": [
            {"name": "東京駅", "lat": 35.6812, "lng": 139.7671},
            {"name": "名古屋駅", "lat": 35.1709, "lng": 136.8815},
            {"name": "大阪駅", "lat": 34.7024, "lng": 135.4959},
        ],
        "created_at": "2026-03-05T08:00:00+00:00",
    },
    {
        "id": "set-hokkaido",
        "name": "北海道エリア",
        "user_id": "jiro",
        "locations": [
            {"name": "札幌駅", "lat": 43.0687, "lng": 141.3508},
            {"name": "旭川駅", "lat": 43.7631, "lng": 142.3580},
            {"name": "函館駅", "lat": 41.7738, "lng": 140.7268},
            {"name": "帯広駅", "lat": 42.9224, "lng": 143.2046},
        ],
        "created_at": "2026-03-08T11:00:00+00:00",
    },
]
db.city_sets.insert_many(CITY_SETS)
print(f"  city_sets: {len(CITY_SETS)} 件挿入")

# === 計算履歴（実際にソルバーを実行して結果を生成）===
HISTORY_INPUTS = [
    {
        "user_id": "taro",
        "locations": CITY_SETS[0]["locations"],  # 関東
        "calculated_at": "2026-01-16T10:00:00+00:00",
    },
    {
        "user_id": "taro",
        "locations": CITY_SETS[1]["locations"],  # 関西
        "calculated_at": "2026-01-21T15:00:00+00:00",
    },
    {
        "user_id": "taro",
        "locations": [
            {"name": "東京駅", "lat": 35.6812, "lng": 139.7671},
            {"name": "大阪駅", "lat": 34.7024, "lng": 135.4959},
            {"name": "福岡駅", "lat": 33.5902, "lng": 130.4207},
            {"name": "名古屋駅", "lat": 35.1709, "lng": 136.8815},
            {"name": "仙台駅", "lat": 38.2602, "lng": 140.8824},
        ],
        "calculated_at": "2026-02-05T09:30:00+00:00",
    },
    {
        "user_id": "hanako",
        "locations": CITY_SETS[2]["locations"],  # 東北
        "calculated_at": "2026-02-21T11:00:00+00:00",
    },
    {
        "user_id": "hanako",
        "locations": CITY_SETS[3]["locations"],  # 九州
        "calculated_at": "2026-02-26T14:00:00+00:00",
    },
    {
        "user_id": "hanako",
        "locations": [
            {"name": "東京駅", "lat": 35.6812, "lng": 139.7671},
            {"name": "大阪駅", "lat": 34.7024, "lng": 135.4959},
            {"name": "福岡駅", "lat": 33.5902, "lng": 130.4207},
        ],
        "calculated_at": "2026-03-01T16:00:00+00:00",
    },
    {
        "user_id": "jiro",
        "locations": CITY_SETS[4]["locations"],  # 東海道
        "calculated_at": "2026-03-06T09:00:00+00:00",
    },
    {
        "user_id": "jiro",
        "locations": CITY_SETS[5]["locations"],  # 北海道
        "calculated_at": "2026-03-09T13:00:00+00:00",
    },
]

history_docs = []
for h in HISTORY_INPUTS:
    result = solve(h["locations"])
    history_docs.append({
        "user_id": h["user_id"],
        "locations": h["locations"],
        "result": result,
        "city_count": len(h["locations"]),
        "calculated_at": h["calculated_at"],
    })

db.calculation_history.insert_many(history_docs)
print(f"  calculation_history: {len(history_docs)} 件挿入")

# === 結果サマリー ===
print("\n=== Seed完了 ===")
print(f"  users: {db.users.count_documents({})} 件")
print(f"  city_sets: {db.city_sets.count_documents({})} 件")
print(f"  calculation_history: {db.calculation_history.count_documents({})} 件")

print("\n=== ユーザー一覧 ===")
for u in db.users.find():
    hist_count = db.calculation_history.count_documents({"user_id": u["username"]})
    sets_count = db.city_sets.count_documents({"user_id": u["username"]})
    print(f"  {u['username']} ({u['display_name']}) — 履歴: {hist_count}件, セット: {sets_count}件")

print("\n=== 計算履歴 ===")
for h in db.calculation_history.find().sort("calculated_at", -1):
    print(f"  [{h['user_id']}] {h['city_count']}都市 | "
          f"最長: {h['result']['longest']['distance_km']}km / "
          f"最短: {h['result']['shortest']['distance_km']}km | "
          f"{h['calculated_at']}")

# === グラフデータ ===
print("\nSeeding graph data...")
db.graph_points.delete_many({})
db.graph_edges.delete_many({})

GRAPH_POINTS = [
    # 上段 (y=10)
    {"name": "A", "label": "Alpha",   "x": 0,  "y": 10},
    {"name": "B", "label": "Bravo",   "x": 3,  "y": 10},
    {"name": "C", "label": "Charlie", "x": 6,  "y": 10},
    {"name": "D", "label": "Delta",   "x": 9,  "y": 10},
    # 上中段 (y=7~8)
    {"name": "E", "label": "Echo",    "x": 1,  "y": 8},
    {"name": "F", "label": "Foxtrot", "x": 4,  "y": 8},
    {"name": "G", "label": "Golf",    "x": 7,  "y": 7},
    {"name": "H", "label": "Hotel",   "x": 10, "y": 8},
    # 中段 (y=5)
    {"name": "I", "label": "India",   "x": 0,  "y": 5},
    {"name": "J", "label": "Juliet",  "x": 3,  "y": 5},
    {"name": "K", "label": "Kilo",    "x": 6,  "y": 5},
    {"name": "L", "label": "Lima",    "x": 9,  "y": 5},
    # 下中段 (y=2~3)
    {"name": "M", "label": "Mike",    "x": 1,  "y": 3},
    {"name": "N", "label": "November","x": 4,  "y": 2},
    {"name": "O", "label": "Oscar",   "x": 7,  "y": 3},
    {"name": "P", "label": "Papa",    "x": 10, "y": 2},
    # 下段 (y=0)
    {"name": "Q", "label": "Quebec",  "x": 0,  "y": 0},
    {"name": "R", "label": "Romeo",   "x": 3,  "y": 0},
    {"name": "S", "label": "Sierra",  "x": 6,  "y": 0},
    {"name": "T", "label": "Tango",   "x": 9,  "y": 0},
]

GRAPH_EDGES = [
    # 上段横
    {"from": "A", "to": "B", "distance": 3.0},
    {"from": "B", "to": "C", "distance": 3.0},
    {"from": "C", "to": "D", "distance": 3.0},
    # 上段→上中段（斜め）
    {"from": "A", "to": "E", "distance": 2.2},
    {"from": "B", "to": "F", "distance": 2.2},
    {"from": "C", "to": "G", "distance": 3.2},
    {"from": "D", "to": "H", "distance": 2.2},
    # 上中段横
    {"from": "E", "to": "F", "distance": 3.0},
    {"from": "F", "to": "G", "distance": 3.2},
    {"from": "G", "to": "H", "distance": 3.2},
    # 上中段→中段
    {"from": "E", "to": "I", "distance": 3.2},
    {"from": "E", "to": "J", "distance": 3.6},
    {"from": "F", "to": "J", "distance": 3.2},
    {"from": "F", "to": "K", "distance": 3.6},
    {"from": "G", "to": "K", "distance": 2.2},
    {"from": "H", "to": "L", "distance": 3.2},
    # 中段横
    {"from": "I", "to": "J", "distance": 3.0},
    {"from": "J", "to": "K", "distance": 3.0},
    {"from": "K", "to": "L", "distance": 3.0},
    # 中段→下中段
    {"from": "I", "to": "M", "distance": 2.2},
    {"from": "J", "to": "N", "distance": 3.2},
    {"from": "K", "to": "O", "distance": 2.2},
    {"from": "L", "to": "P", "distance": 3.2},
    # 下中段横
    {"from": "M", "to": "N", "distance": 3.2},
    {"from": "N", "to": "O", "distance": 3.2},
    {"from": "O", "to": "P", "distance": 3.2},
    # 下中段→下段
    {"from": "M", "to": "Q", "distance": 3.2},
    {"from": "M", "to": "R", "distance": 3.6},
    {"from": "N", "to": "R", "distance": 2.2},
    {"from": "N", "to": "S", "distance": 2.8},
    {"from": "O", "to": "S", "distance": 3.2},
    {"from": "P", "to": "T", "distance": 2.2},
    # 下段横
    {"from": "Q", "to": "R", "distance": 3.0},
    {"from": "R", "to": "S", "distance": 3.0},
    {"from": "S", "to": "T", "distance": 3.0},
    # クロスリンク（ショートカットと大回りを作る）
    {"from": "A", "to": "I", "distance": 5.0},
    {"from": "D", "to": "L", "distance": 5.0},
    {"from": "Q", "to": "I", "distance": 5.0},
    {"from": "T", "to": "L", "distance": 5.0},
    {"from": "B", "to": "J", "distance": 5.4},
    {"from": "G", "to": "L", "distance": 2.8},
]

db.graph_points.insert_many(GRAPH_POINTS)
db.graph_edges.insert_many(GRAPH_EDGES)
print(f"  graph_points: {len(GRAPH_POINTS)} 件")
print(f"  graph_edges: {len(GRAPH_EDGES)} 件")
