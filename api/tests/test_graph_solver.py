"""
グラフソルバーの正確性テスト
実行: cd api && python -m pytest tests/test_graph_solver.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.graph_solver import solve_graph, _dijkstra, _longest_path_bitdp, _build_adj

# テスト用のエッジデータ（本番と同じ）
EDGES = [
    {"from": "A", "to": "B", "distance": 3.6},
    {"from": "A", "to": "E", "distance": 2.2},
    {"from": "B", "to": "C", "distance": 3.0},
    {"from": "B", "to": "E", "distance": 4.0},
    {"from": "C", "to": "D", "distance": 3.2},
    {"from": "C", "to": "F", "distance": 4.0},
    {"from": "D", "to": "F", "distance": 4.2},
    {"from": "D", "to": "J", "distance": 6.0},
    {"from": "E", "to": "F", "distance": 3.0},
    {"from": "E", "to": "G", "distance": 2.2},
    {"from": "E", "to": "H", "distance": 4.1},
    {"from": "F", "to": "G", "distance": 2.8},
    {"from": "F", "to": "I", "distance": 4.0},
    {"from": "G", "to": "H", "distance": 2.8},
    {"from": "G", "to": "I", "distance": 2.8},
    {"from": "I", "to": "J", "distance": 3.2},
]


class TestDijkstraShortestPath:
    """Dijkstra最短経路の正確性テスト"""

    def test_a_to_j_shortest(self):
        """A→J の最短経路"""
        result = solve_graph("A", "J", EDGES)
        s = result["shortest"]
        assert s["path"][0] == "A"
        assert s["path"][-1] == "J"
        assert s["distance"] > 0
        # 手計算: A→E→G→I→J = 2.2+2.2+2.8+3.2 = 10.4
        assert s["distance"] == 10.4
        assert s["path"] == ["A", "E", "G", "I", "J"]

    def test_a_to_d_shortest(self):
        """A→D の最短経路"""
        result = solve_graph("A", "D", EDGES)
        s = result["shortest"]
        assert s["path"][0] == "A"
        assert s["path"][-1] == "D"
        # A→B→C→D = 3.6+3.0+3.2 = 9.8
        # A→E→F→D = 2.2+3.0+4.2 = 9.4 ← こちらが最短
        assert s["distance"] == 9.4

    def test_adjacent_nodes(self):
        """隣接ノード間の最短経路は直接エッジ"""
        result = solve_graph("A", "B", EDGES)
        assert result["shortest"]["path"] == ["A", "B"]
        assert result["shortest"]["distance"] == 3.6

    def test_reverse_direction(self):
        """逆方向も同じ距離"""
        r1 = solve_graph("A", "J", EDGES)
        r2 = solve_graph("J", "A", EDGES)
        assert r1["shortest"]["distance"] == r2["shortest"]["distance"]

    def test_shortest_is_simple_path(self):
        """最短経路はノードの重複がない"""
        result = solve_graph("A", "J", EDGES)
        path = result["shortest"]["path"]
        assert len(path) == len(set(path))


class TestDFSLongestPath:
    """DFS最長経路の正確性テスト"""

    def test_a_to_j_longest(self):
        """A→J の最長経路"""
        result = solve_graph("A", "J", EDGES)
        l = result["longest"]
        assert l["path"][0] == "A"
        assert l["path"][-1] == "J"
        assert l["distance"] > 0

    def test_longest_greater_than_shortest(self):
        """最長経路 >= 最短経路"""
        for start, end in [("A", "J"), ("A", "D"), ("B", "I"), ("H", "D")]:
            result = solve_graph(start, end, EDGES)
            assert result["longest"]["distance"] >= result["shortest"]["distance"], \
                f"{start}→{end}: longest={result['longest']['distance']} < shortest={result['shortest']['distance']}"

    def test_longest_is_simple_path(self):
        """最長経路はノードの重複がない（単純経路）"""
        result = solve_graph("A", "J", EDGES)
        path = result["longest"]["path"]
        assert len(path) == len(set(path))

    def test_longest_uses_valid_edges(self):
        """最長経路のすべての辺がグラフに存在する"""
        adj = _build_adj(EDGES)
        result = solve_graph("A", "J", EDGES)
        path = result["longest"]["path"]
        for i in range(len(path) - 1):
            neighbors = [v for v, _ in adj[path[i]]]
            assert path[i + 1] in neighbors, \
                f"Edge {path[i]}→{path[i+1]} does not exist"

    def test_longest_distance_matches_edges(self):
        """最長経路の合計距離がエッジ距離の合算と一致する"""
        edge_map = {}
        for e in EDGES:
            edge_map[(e["from"], e["to"])] = e["distance"]
            edge_map[(e["to"], e["from"])] = e["distance"]

        result = solve_graph("A", "J", EDGES)
        path = result["longest"]["path"]
        total = sum(edge_map[(path[i], path[i + 1])] for i in range(len(path) - 1))
        assert round(total, 1) == result["longest"]["distance"]


class TestEdgeCases:
    """エッジケーステスト"""

    def test_same_start_end_raises_or_empty(self):
        """同じ始点終点は空パス"""
        adj = _build_adj(EDGES)
        all_nodes = set()
        for e in EDGES:
            all_nodes.add(e["from"])
            all_nodes.add(e["to"])
        r = _longest_path_bitdp("A", "A", adj, all_nodes)
        assert r["distance"] == 0

    def test_disconnected_graph(self):
        """接続されていない2点は空パス"""
        edges = [{"from": "A", "to": "B", "distance": 1.0}]
        result = solve_graph("A", "C", edges)
        assert result["shortest"]["path"] == []
        assert result["longest"]["path"] == []

    def test_simple_triangle(self):
        """3ノード三角形での最短・最長"""
        edges = [
            {"from": "X", "to": "Y", "distance": 1.0},
            {"from": "Y", "to": "Z", "distance": 2.0},
            {"from": "X", "to": "Z", "distance": 10.0},
        ]
        result = solve_graph("X", "Z", edges)
        assert result["shortest"]["distance"] == 3.0  # X→Y→Z
        assert result["shortest"]["path"] == ["X", "Y", "Z"]
        assert result["longest"]["distance"] == 10.0  # X→Z 直接
        assert result["longest"]["path"] == ["X", "Z"]

    def test_all_pairs_have_paths(self):
        """10ノードグラフで全ペア間にパスが存在する"""
        nodes = set()
        for e in EDGES:
            nodes.add(e["from"])
            nodes.add(e["to"])
        nodes = sorted(nodes)

        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                result = solve_graph(a, b, EDGES)
                assert len(result["shortest"]["path"]) >= 2, f"No path from {a} to {b}"
                assert result["shortest"]["distance"] > 0


class TestPathDistanceVerification:
    """複数ペアで手計算と照合"""

    def test_h_to_d(self):
        """H→D の最短経路を手計算で検証"""
        result = solve_graph("H", "D", EDGES)
        s = result["shortest"]
        # H→G→E→F→D = 2.8+2.2+3.0+4.2 = 12.2
        # H→G→F→D = 2.8+2.8+4.2 = 9.8
        # H→G→F→C→D = 2.8+2.8+4.0+3.2 = 12.8
        # H→E→F→D = 4.1+3.0+4.2 = 11.3
        # H→G→I→J→D = 2.8+2.8+3.2+6.0 = 14.8
        # H→E→A→B→C→D = 4.1+2.2+3.6+3.0+3.2 = 16.1
        assert s["distance"] == 9.8
        assert s["path"] == ["H", "G", "F", "D"]

    def test_b_to_i(self):
        """B→I の最短経路"""
        result = solve_graph("B", "I", EDGES)
        s = result["shortest"]
        # B→E→G→I = 4.0+2.2+2.8 = 9.0
        # B→E→F→I = 4.0+3.0+4.0 = 11.0
        # B→C→F→I = 3.0+4.0+4.0 = 11.0
        assert s["distance"] == 9.0
        assert s["path"] == ["B", "E", "G", "I"]
