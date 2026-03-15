import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

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
    get_collection("users").create_index(
        [("username", ASCENDING)], unique=True, name="idx_users_username_unique",
    )
    get_collection("users").create_index(
        [("email", ASCENDING)], unique=True, name="idx_users_email_unique",
    )
    get_collection("calculation_history").create_index(
        [("user_id", ASCENDING), ("calculated_at", DESCENDING)],
        name="idx_history_user_calculated",
    )
    get_collection("city_sets").create_index(
        [("user_id", ASCENDING)], name="idx_city_sets_user_id",
    )
    print("[DB] Indexes ensured.")


def _sanitize_user(doc: dict) -> dict:
    """password_hash を除外してユーザー情報を返す"""
    doc["_id"] = str(doc["_id"])
    doc.pop("password_hash", None)
    return doc


# === Auth / Users ===

def create_user(username: str, email: str, password: str, display_name: str | None = None) -> dict:
    doc = {
        "username": username,
        "email": email,
        "password_hash": generate_password_hash(password),
        "display_name": display_name or username,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        result = get_collection("users").insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        doc.pop("password_hash")
        return doc
    except Exception as e:
        err = str(e)
        if "E11000" in err and "email" in err:
            raise ValueError("このメールアドレスは既に使用されています")
        if "E11000" in err and "username" in err:
            raise ValueError("このユーザー名は既に使用されています")
        if "E11000" in err:
            raise ValueError("ユーザー名またはメールアドレスが重複しています")
        raise


def authenticate_user(email: str, password: str) -> dict | None:
    doc = get_collection("users").find_one({"email": email})
    if not doc:
        return None
    if not check_password_hash(doc["password_hash"], password):
        return None
    return _sanitize_user(doc)


def find_user(username: str) -> dict | None:
    doc = get_collection("users").find_one({"username": username})
    if doc:
        return _sanitize_user(doc)
    return None


def list_users() -> list[dict]:
    docs = list(get_collection("users").find().sort("created_at", DESCENDING))
    return [_sanitize_user(d) for d in docs]


def update_user(username: str, updates: dict) -> dict | None:
    """ユーザー情報を更新。password指定時はハッシュ化。"""
    set_fields = {"updated_at": datetime.now(timezone.utc).isoformat()}
    if "display_name" in updates:
        set_fields["display_name"] = updates["display_name"]
    if "password" in updates:
        set_fields["password_hash"] = generate_password_hash(updates["password"])

    if len(set_fields) <= 1:
        return find_user(username)

    get_collection("users").update_one(
        {"username": username}, {"$set": set_fields}
    )
    return find_user(username)


def verify_password(username: str, password: str) -> bool:
    doc = get_collection("users").find_one({"username": username})
    if not doc:
        return False
    return check_password_hash(doc["password_hash"], password)


def get_user_profile_with_stats(username: str) -> dict | None:
    """$lookup で履歴数・都市セット数を eager loading"""
    pipeline = [
        {"$match": {"username": username}},
        {"$lookup": {
            "from": "calculation_history",
            "localField": "username", "foreignField": "user_id",
            "as": "_histories",
        }},
        {"$lookup": {
            "from": "city_sets",
            "localField": "username", "foreignField": "user_id",
            "as": "_city_sets",
        }},
        {"$addFields": {
            "history_count": {"$size": "$_histories"},
            "city_sets_count": {"$size": "$_city_sets"},
        }},
        {"$project": {"_histories": 0, "_city_sets": 0, "password_hash": 0}},
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
            "localField": "user_id", "foreignField": "username",
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
            r["user"].pop("password_hash", None)
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
