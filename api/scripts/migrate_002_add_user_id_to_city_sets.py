"""
Migration 002: 既存の city_sets に user_id フィールドを追加
- user_id が無いドキュメントにデフォルトユーザーを設定
- 指定がなければスキップ

使い方: cd api && python scripts/migrate_002_add_user_id_to_city_sets.py [default_username]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.db import get_db

db = get_db()
default_user = sys.argv[1] if len(sys.argv) > 1 else None

print("Migration 002: city_sets に user_id フィールド追加")

# user_id が無いドキュメントを検索
orphans = db.city_sets.count_documents({"user_id": {"$exists": False}})
print(f"  user_id なしの city_sets: {orphans} 件")

if orphans == 0:
    print("  マイグレーション不要です")
elif default_user:
    # デフォルトユーザーが存在するか確認
    user = db.users.find_one({"username": default_user})
    if not user:
        print(f"  [ERROR] ユーザー '{default_user}' が見つかりません")
        sys.exit(1)

    result = db.city_sets.update_many(
        {"user_id": {"$exists": False}},
        {"$set": {"user_id": default_user}},
    )
    print(f"  [OK] {result.modified_count} 件を user_id='{default_user}' に更新")
else:
    print("  デフォルトユーザーが指定されていません")
    print("  使い方: python scripts/migrate_002_add_user_id_to_city_sets.py <username>")
    print("  スキップします")

print("Migration 002: 完了")
