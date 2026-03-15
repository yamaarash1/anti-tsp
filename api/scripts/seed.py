"""
シードデータ投入スクリプト
使い方: cd api && python scripts/seed.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.db import get_db, ensure_indexes
from utils.tsp_solver import solve

db = get_db()

# === 既存データをクリア ===
print("Clearing existing data...")
db.users.delete_many({})
db.city_sets.delete_many({})
db.calculation_history.delete_many({})

# === インデックス作成 ===
ensure_indexes()

# === ユーザー ===
USERS = [
    {"username": "taro", "display_name": "太郎", "created_at": "2026-01-10T09:00:00+00:00"},
    {"username": "hanako", "display_name": "花子", "created_at": "2026-02-15T10:00:00+00:00"},
    {"username": "jiro", "display_name": "次郎", "created_at": "2026-03-01T11:00:00+00:00"},
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
