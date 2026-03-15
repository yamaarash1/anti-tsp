"""
グラフ上の最短経路（Dijkstra）と最長経路（ビットDP）

最長経路の計算量:
  DFS全探索: O(V!)
  ビットDP:  O(2^V * V^2) ← こちらを採用
  10ノードの場合: 2^10 * 100 = 102,400 演算
"""
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
    """Dijkstraで最短経路 O((V+E) log V)"""
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


def _longest_path_bitdp(start, end, adj, all_nodes):
    """
    ビットDPで最長単純経路 O(2^V * V^2)

    dp[mask][v] = 訪問済み集合が mask で、現在 v にいるときの最長距離
    parent[mask][v] = 経路復元用の (prev_mask, prev_node)

    mask: 各ノードの訪問状態をビットで表現
          例: ノード0,2を訪問済み → mask = 0b00101 = 5
    """
    nodes = sorted(all_nodes)
    n = len(nodes)
    idx = {name: i for i, name in enumerate(nodes)}

    if start not in idx or end not in idx:
        return {"path": [], "distance": 0}

    si = idx[start]
    ei = idx[end]

    # 隣接行列（インデックスベース）
    weight = [[0.0] * n for _ in range(n)]
    has_edge = [[False] * n for _ in range(n)]
    for node in nodes:
        for neighbor, dist in adj[node]:
            if neighbor in idx:
                i, j = idx[node], idx[neighbor]
                weight[i][j] = dist
                has_edge[i][j] = True

    INF = -1.0  # 未到達
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[None] * n for _ in range(1 << n)]

    # 初期状態: startのみ訪問済み、startにいる、距離0
    dp[1 << si][si] = 0.0

    best_dist = INF
    best_mask = 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue

            # u が end なら最長候補を更新
            if u == ei and dp[mask][u] > best_dist:
                best_dist = dp[mask][u]
                best_mask = mask

            # u から隣接ノード v への遷移
            for v in range(n):
                if mask & (1 << v):  # v は既に訪問済み
                    continue
                if not has_edge[u][v]:  # u-v 間にエッジがない
                    continue

                new_mask = mask | (1 << v)
                new_dist = dp[mask][u] + weight[u][v]

                if new_dist > dp[new_mask][v]:
                    dp[new_mask][v] = new_dist
                    parent[new_mask][v] = (mask, u)

    if best_dist == INF:
        return {"path": [], "distance": 0}

    # 経路復元
    path_indices = []
    mask = best_mask
    node = ei
    while node is not None:
        path_indices.append(node)
        p = parent[mask][node]
        if p is None:
            break
        mask, node = p
    path_indices.reverse()

    path = [nodes[i] for i in path_indices]
    return {"path": path, "distance": round(best_dist, 1)}


def solve_graph(start, end, edges):
    """最短経路（Dijkstra）と最長経路（ビットDP）を返す"""
    adj = _build_adj(edges)
    all_nodes = set()
    for e in edges:
        all_nodes.add(e["from"])
        all_nodes.add(e["to"])

    return {
        "shortest": _dijkstra(start, end, adj),
        "longest": _longest_path_bitdp(start, end, adj, all_nodes),
    }
