import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timezone

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "anti_tsp"

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client


def get_db():
    return _get_client()[DB_NAME]


def get_collection(name="city_sets"):
    return get_db()[name]


def ensure_indexes():
    """全コレクションのインデックスを作成"""
    # users: username ユニークインデックス
    get_collection("users").create_index(
        [("username", ASCENDING)],
        unique=True,
        name="idx_users_username_unique",
    )
    # calculation_history: user_id + calculated_at 複合インデックス
    get_collection("calculation_history").create_index(
        [("user_id", ASCENDING), ("calculated_at", DESCENDING)],
        name="idx_history_user_calculated",
    )
    # city_sets: user_id インデックス
    get_collection("city_sets").create_index(
        [("user_id", ASCENDING)],
        name="idx_city_sets_user_id",
    )
    print("[DB] Indexes ensured.")


# === Users ===

def create_user(username: str, display_name: str | None = None) -> dict:
    col = get_collection("users")
    doc = {
        "username": username,
        "display_name": display_name or username,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        result = col.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except Exception as e:
        if "E11000" in str(e):
            raise ValueError(f"ユーザー名 '{username}' は既に使用されています")
        raise


def find_user(username: str) -> dict | None:
    doc = get_collection("users").find_one({"username": username})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def list_users() -> list[dict]:
    docs = list(get_collection("users").find().sort("created_at", DESCENDING))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


def get_user_profile_with_stats(username: str) -> dict | None:
    """$lookup で履歴数・都市セット数を eager loading"""
    pipeline = [
        {"$match": {"username": username}},
        {"$lookup": {
            "from": "calculation_history",
            "localField": "username",
            "foreignField": "user_id",
            "as": "_histories",
        }},
        {"$lookup": {
            "from": "city_sets",
            "localField": "username",
            "foreignField": "user_id",
            "as": "_city_sets",
        }},
        {"$addFields": {
            "history_count": {"$size": "$_histories"},
            "city_sets_count": {"$size": "$_city_sets"},
        }},
        {"$project": {"_histories": 0, "_city_sets": 0}},
    ]
    results = list(get_collection("users").aggregate(pipeline))
    if not results:
        return None
    user = results[0]
    user["_id"] = str(user["_id"])
    return user


# === Calculation History ===

def save_history(user_id: str, locations: list[dict], result: dict) -> dict:
    doc = {
        "user_id": user_id,
        "locations": locations,
        "result": result,
        "city_count": len(locations),
        "calculated_at": datetime.now(timezone.utc).isoformat(),
    }
    res = get_collection("calculation_history").insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc


def get_user_history_with_lookup(user_id: str, limit: int = 50) -> list[dict]:
    """$lookup でユーザー情報を結合して履歴取得 (N+1回避)"""
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "username",
            "as": "user",
        }},
        {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
        {"$sort": {"calculated_at": -1}},
        {"$limit": limit},
    ]
    results = list(get_collection("calculation_history").aggregate(pipeline))
    for r in results:
        r["_id"] = str(r["_id"])
        if "user" in r and r["user"]:
            r["user"]["_id"] = str(r["user"]["_id"])
    return results


# === City Sets ===

def load_city_sets(user_id: str | None = None) -> list[dict]:
    query = {"user_id": user_id} if user_id else {}
    docs = list(get_collection("city_sets").find(query).sort("created_at", DESCENDING))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


def save_city_set(data: dict) -> dict:
    result = get_collection("city_sets").insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def delete_city_set(set_id: str) -> bool:
    result = get_collection("city_sets").delete_one({"id": set_id})
    return result.deleted_count > 0


def find_city_set(set_id: str) -> dict | None:
    doc = get_collection("city_sets").find_one({"id": set_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc
