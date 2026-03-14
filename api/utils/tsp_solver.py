from itertools import permutations
from .haversine import haversine


def _route_distance(locations: list[dict], order: tuple[int, ...]) -> float:
    """巡回ルートの総距離を計算 (始点に戻る)"""
    total = 0.0
    for i in range(len(order)):
        a = locations[order[i]]
        b = locations[order[(i + 1) % len(order)]]
        total += haversine(a["lat"], a["lng"], b["lat"], b["lng"])
    return total


def solve(locations: list[dict]) -> dict:
    """
    最初の都市を固定し、残りの全順列を探索。
    最長 (Anti-TSP) と最短 (TSP) の両方を返す。
    locations: [{"name": str, "lat": float, "lng": float}, ...]
    """
    n = len(locations)
    if n < 3:
        raise ValueError("3件以上の都市が必要です")

    indices = list(range(1, n))
    best_long = None
    best_short = None
    max_dist = -1.0
    min_dist = float("inf")

    for perm in permutations(indices):
        order = (0,) + perm
        dist = _route_distance(locations, order)
        if dist > max_dist:
            max_dist = dist
            best_long = order
        if dist < min_dist:
            min_dist = dist
            best_short = order

    return {
        "longest": {
            "order": list(best_long),
            "distance_km": round(max_dist, 2),
        },
        "shortest": {
            "order": list(best_short),
            "distance_km": round(min_dist, 2),
        },
    }
