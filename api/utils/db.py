import os
from pymongo import MongoClient

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "anti_tsp"
COLLECTION_NAME = "city_sets"

_client = None


def _get_collection():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client[DB_NAME][COLLECTION_NAME]


def load_city_sets() -> list[dict]:
    collection = _get_collection()
    sets = []
    for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # ObjectId → str
        sets.append(doc)
    return sets


def save_city_set(data: dict) -> dict:
    collection = _get_collection()
    result = collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def delete_city_set(set_id: str) -> bool:
    collection = _get_collection()
    result = collection.delete_one({"id": set_id})
    return result.deleted_count > 0


def find_city_set(set_id: str) -> dict | None:
    collection = _get_collection()
    doc = collection.find_one({"id": set_id})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc
