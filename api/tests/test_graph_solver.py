"""
グラフソルバーの正確性テスト (20ノード版)
実行: cd api && python -m pytest tests/test_graph_solver.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.graph_solver import solve_graph, _dijkstra, _longest_path_bitdp, _build_adj

# 20ノード版エッジデータ
EDGES = [
    # 上段横
    {"from": "A", "to": "B", "distance": 3.0},
    {"from": "B", "to": "C", "distance": 3.0},
    {"from": "C", "to": "D", "distance": 3.0},
    # 上段→上中段
    {"from": "A", "to": "E", "distance": 2.2},
    {"from": "B", "to": "F", "distance": 2.2},
    {"from": "C", "to": "G", "distance": 3.2},
    {"from": "D", "to": "H", "distance": 2.2},
    # 上中段横
    {"from": "E", "to": "F", "distance": 3.0},
    {"from": "F", "to": "G", "distance": 3.2},
    {"from": "G", "to": "H", "distance": 3.2},
    # 上中段→中段
    {"from": "E", "to": "I", "distance": 3.2},
    {"from": "E", "to": "J", "distance": 3.6},
    {"from": "F", "to": "J", "distance": 3.2},
    {"from": "F", "to": "K", "distance": 3.6},
    {"from": "G", "to": "K", "distance": 2.2},
    {"from": "H", "to": "L", "distance": 3.2},
    # 中段横
    {"from": "I", "to": "J", "distance": 3.0},
    {"from": "J", "to": "K", "distance": 3.0},
    {"from": "K", "to": "L", "distance": 3.0},
    # 中段→下中段
    {"from": "I", "to": "M", "distance": 2.2},
    {"from": "J", "to": "N", "distance": 3.2},
    {"from": "K", "to": "O", "distance": 2.2},
    {"from": "L", "to": "P", "distance": 3.2},
    # 下中段横
    {"from": "M", "to": "N", "distance": 3.2},
    {"from": "N", "to": "O", "distance": 3.2},
    {"from": "O", "to": "P", "distance": 3.2},
    # 下中段→下段
    {"from": "M", "to": "Q", "distance": 3.2},
    {"from": "M", "to": "R", "distance": 3.6},
    {"from": "N", "to": "R", "distance": 2.2},
    {"from": "N", "to": "S", "distance": 2.8},
    {"from": "O", "to": "S", "distance": 3.2},
    {"from": "P", "to": "T", "distance": 2.2},
    # 下段横
    {"from": "Q", "to": "R", "distance": 3.0},
    {"from": "R", "to": "S", "distance": 3.0},
    {"from": "S", "to": "T", "distance": 3.0},
    # クロスリンク
    {"from": "A", "to": "I", "distance": 5.0},
    {"from": "D", "to": "L", "distance": 5.0},
    {"from": "Q", "to": "I", "distance": 5.0},
    {"from": "T", "to": "L", "distance": 5.0},
    {"from": "B", "to": "J", "distance": 5.4},
    {"from": "G", "to": "L", "distance": 2.8},
]


class TestDijkstraShortestPath:
    """Dijkstra最短経路テスト"""

    def test_adjacent_nodes(self):
        """隣接ノード間は直接エッジ"""
        result = solve_graph("A", "B", EDGES)
        assert result["shortest"]["path"] == ["A", "B"]
        assert result["shortest"]["distance"] == 3.0

    def test_a_to_t_shortest(self):
        """A→T の最短経路が存在する"""
        result = solve_graph("A", "T", EDGES)
        s = result["shortest"]
        assert s["path"][0] == "A"
        assert s["path"][-1] == "T"
        assert s["distance"] > 0

    def test_reverse_same_distance(self):
        """双方向で同じ距離"""
        r1 = solve_graph("A", "T", EDGES)
        r2 = solve_graph("T", "A", EDGES)
        assert r1["shortest"]["distance"] == r2["shortest"]["distance"]

    def test_shortest_is_simple_path(self):
        """最短経路にノード重複なし"""
        result = solve_graph("A", "T", EDGES)
        path = result["shortest"]["path"]
        assert len(path) == len(set(path))

    def test_a_to_d_shortest(self):
        """A→D = A→B→C→D = 3+3+3 = 9.0"""
        result = solve_graph("A", "D", EDGES)
        assert result["shortest"]["distance"] == 9.0
        assert result["shortest"]["path"] == ["A", "B", "C", "D"]


class TestBitDPLongestPath:
    """ビットDP最長経路テスト"""

    def test_longest_exists(self):
        """A→T の最長経路が存在する"""
        result = solve_graph("A", "T", EDGES)
        l = result["longest"]
        assert l["path"][0] == "A"
        assert l["path"][-1] == "T"
        assert l["distance"] > 0

    def test_longest_ge_shortest(self):
        """最長 >= 最短（複数ペア）"""
        for start, end in [("A", "T"), ("A", "L"), ("Q", "D"), ("E", "P")]:
            result = solve_graph(start, end, EDGES)
            assert result["longest"]["distance"] >= result["shortest"]["distance"], \
                f"{start}→{end}"

    def test_longest_is_simple_path(self):
        """最長経路にノード重複なし"""
        result = solve_graph("A", "T", EDGES)
        path = result["longest"]["path"]
        assert len(path) == len(set(path))

    def test_longest_uses_valid_edges(self):
        """最長経路の全辺がグラフに存在"""
        adj = _build_adj(EDGES)
        result = solve_graph("A", "T", EDGES)
        path = result["longest"]["path"]
        for i in range(len(path) - 1):
            neighbors = [v for v, _ in adj[path[i]]]
            assert path[i + 1] in neighbors, f"Edge {path[i]}→{path[i+1]} not found"

    def test_longest_distance_matches_sum(self):
        """最長経路の合計距離がエッジ距離の合算と一致"""
        edge_map = {}
        for e in EDGES:
            edge_map[(e["from"], e["to"])] = e["distance"]
            edge_map[(e["to"], e["from"])] = e["distance"]

        result = solve_graph("A", "T", EDGES)
        path = result["longest"]["path"]
        total = sum(edge_map[(path[i], path[i + 1])] for i in range(len(path) - 1))
        assert round(total, 1) == result["longest"]["distance"]

    def test_longest_significantly_longer(self):
        """A→Tで最長は最短の2倍以上（大回りが効く）"""
        result = solve_graph("A", "T", EDGES)
        assert result["longest"]["distance"] > result["shortest"]["distance"] * 2


class TestEdgeCases:
    """エッジケーステスト"""

    def test_disconnected_graph(self):
        """接続されていない2点は空パス"""
        edges = [{"from": "X", "to": "Y", "distance": 1.0}]
        result = solve_graph("X", "Z", edges)
        assert result["shortest"]["path"] == []
        assert result["longest"]["path"] == []

    def test_simple_triangle(self):
        """三角形での最短・最長"""
        edges = [
            {"from": "X", "to": "Y", "distance": 1.0},
            {"from": "Y", "to": "Z", "distance": 2.0},
            {"from": "X", "to": "Z", "distance": 10.0},
        ]
        result = solve_graph("X", "Z", edges)
        assert result["shortest"]["distance"] == 3.0
        assert result["longest"]["distance"] == 10.0

    def test_all_20_nodes_reachable(self):
        """20ノード全ペア間にパスが存在"""
        nodes = set()
        for e in EDGES:
            nodes.add(e["from"])
            nodes.add(e["to"])
        assert len(nodes) == 20, f"Expected 20 nodes, got {len(nodes)}"

        nodes = sorted(nodes)
        # 全ペアは多すぎるのでDijkstraのみでサンプル検証
        adj = _build_adj(EDGES)
        for a in ["A", "E", "J", "O", "T"]:
            for b in nodes:
                if a == b:
                    continue
                r = _dijkstra(a, b, adj)
                assert len(r["path"]) >= 2, f"No path {a}→{b}"
