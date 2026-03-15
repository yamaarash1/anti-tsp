"""グラフ上の最短経路（Dijkstra）と最長経路（DFS全探索）"""
import heapq
from collections import defaultdict


def _build_adj(edges):
    """隣接リスト構築（双方向）"""
    adj = defaultdict(list)
    for e in edges:
        adj[e["from"]].append((e["to"], e["distance"]))
        adj[e["to"]].append((e["from"], e["distance"]))
    return adj


def _dijkstra(start, end, adj):
    """Dijkstraで最短経路"""
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        if u == end:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if end not in dist:
        return {"path": [], "distance": 0}

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev.get(node)
    path.reverse()
    return {"path": path, "distance": round(dist[end], 1)}


def _longest_path_dfs(start, end, adj):
    """DFS全探索で最長単純経路（10ノード程度なので高速）"""
    best = {"path": [], "dist": -1}

    def dfs(node, visited, path, total):
        if node == end:
            if total > best["dist"]:
                best["dist"] = total
                best["path"] = path[:]
            return
        for v, w in adj[node]:
            if v not in visited:
                visited.add(v)
                path.append(v)
                dfs(v, visited, path, total + w)
                path.pop()
                visited.remove(v)

    dfs(start, {start}, [start], 0)

    if best["dist"] < 0:
        return {"path": [], "distance": 0}
    return {"path": best["path"], "distance": round(best["dist"], 1)}


def solve_graph(start, end, edges):
    """最短・最長経路を返す"""
    adj = _build_adj(edges)
    return {
        "shortest": _dijkstra(start, end, adj),
        "longest": _longest_path_dfs(start, end, adj),
    }
