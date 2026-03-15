"""
Migration 003: calculation_history に city_count フィールドを追加
- city_count が無いドキュメントに locations の長さから自動計算

使い方: cd api && python scripts/migrate_003_add_city_count_to_history.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.db import get_db

db = get_db()

print("Migration 003: calculation_history に city_count 追加")

# city_count が無いドキュメントを検索
docs = list(db.calculation_history.find({"city_count": {"$exists": False}}))
print(f"  city_count なしの履歴: {len(docs)} 件")

if not docs:
    print("  マイグレーション不要です")
else:
    from pymongo import UpdateOne
    ops = []
    for doc in docs:
        city_count = len(doc.get("locations", []))
        ops.append(UpdateOne(
            {"_id": doc["_id"]},
            {"$set": {"city_count": city_count}},
        ))
    result = db.calculation_history.bulk_write(ops)
    print(f"  [OK] {result.modified_count} 件を更新")

print("Migration 003: 完了")
