"""
Migration 001: インデックス作成
- users.username ユニークインデックス
- calculation_history {user_id, calculated_at} 複合インデックス
- city_sets {user_id} インデックス

使い方: cd api && python scripts/migrate_001_add_indexes.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pymongo import ASCENDING, DESCENDING
from utils.db import get_db

db = get_db()

print("Migration 001: インデックス作成")

# users: username ユニーク
result = db.users.create_index(
    [("username", ASCENDING)],
    unique=True,
    name="idx_users_username_unique",
)
print(f"  [OK] users.{result}")

# calculation_history: user_id + calculated_at 複合
result = db.calculation_history.create_index(
    [("user_id", ASCENDING), ("calculated_at", DESCENDING)],
    name="idx_history_user_calculated",
)
print(f"  [OK] calculation_history.{result}")

# city_sets: user_id
result = db.city_sets.create_index(
    [("user_id", ASCENDING)],
    name="idx_city_sets_user_id",
)
print(f"  [OK] city_sets.{result}")

print("Migration 001: 完了")
