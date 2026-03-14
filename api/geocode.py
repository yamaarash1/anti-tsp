import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


@app.route("/api/geocode", methods=["POST"])
def geocode():
    data = request.get_json()
    addresses = data.get("addresses", [])
    if not addresses:
        return jsonify({"error": "住所が指定されていません"}), 400

    results = []
    for i, addr in enumerate(addresses):
        if i > 0:
            time.sleep(1)  # Nominatim rate limit: 1req/sec

        resp = requests.get(
            NOMINATIM_URL,
            params={"q": addr, "format": "json", "limit": 1},
            headers={"User-Agent": "AntiTSP/1.0"},
            timeout=10,
        )
        hits = resp.json()
        if hits:
            results.append({
                "name": addr,
                "lat": float(hits[0]["lat"]),
                "lng": float(hits[0]["lon"]),
            })
        else:
            results.append({"name": addr, "lat": None, "lng": None, "error": "見つかりませんでした"})

    return jsonify({"locations": results})
