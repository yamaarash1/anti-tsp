"""
グラフソルバーの正確性テスト (10ノード版)
実行: cd api && python -m pytest tests/test_graph_solver.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.graph_solver import solve_graph, _dijkstra, _longest_path_bitdp, _build_adj

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
    def test_a_to_j_shortest(self):
        result = solve_graph("A", "J", EDGES)
        assert result["shortest"]["distance"] == 10.4
        assert result["shortest"]["path"] == ["A", "E", "G", "I", "J"]

    def test_a_to_d_shortest(self):
        result = solve_graph("A", "D", EDGES)
        assert result["shortest"]["distance"] == 9.4

    def test_adjacent_nodes(self):
        result = solve_graph("A", "B", EDGES)
        assert result["shortest"]["path"] == ["A", "B"]
        assert result["shortest"]["distance"] == 3.6

    def test_reverse_same_distance(self):
        r1 = solve_graph("A", "J", EDGES)
        r2 = solve_graph("J", "A", EDGES)
        assert r1["shortest"]["distance"] == r2["shortest"]["distance"]

    def test_shortest_is_simple_path(self):
        path = solve_graph("A", "J", EDGES)["shortest"]["path"]
        assert len(path) == len(set(path))


class TestBitDPLongestPath:
    def test_a_to_j_longest(self):
        result = solve_graph("A", "J", EDGES)
        assert result["longest"]["path"][0] == "A"
        assert result["longest"]["path"][-1] == "J"
        assert result["longest"]["distance"] > 0

    def test_longest_ge_shortest(self):
        for s, e in [("A", "J"), ("A", "D"), ("B", "I"), ("H", "D")]:
            r = solve_graph(s, e, EDGES)
            assert r["longest"]["distance"] >= r["shortest"]["distance"]

    def test_longest_is_simple_path(self):
        path = solve_graph("A", "J", EDGES)["longest"]["path"]
        assert len(path) == len(set(path))

    def test_longest_uses_valid_edges(self):
        adj = _build_adj(EDGES)
        path = solve_graph("A", "J", EDGES)["longest"]["path"]
        for i in range(len(path) - 1):
            assert path[i + 1] in [v for v, _ in adj[path[i]]]

    def test_longest_distance_matches_sum(self):
        em = {}
        for e in EDGES:
            em[(e["from"], e["to"])] = e["distance"]
            em[(e["to"], e["from"])] = e["distance"]
        r = solve_graph("A", "J", EDGES)
        path = r["longest"]["path"]
        total = sum(em[(path[i], path[i+1])] for i in range(len(path)-1))
        assert round(total, 1) == r["longest"]["distance"]


class TestEdgeCases:
    def test_disconnected_graph(self):
        edges = [{"from": "X", "to": "Y", "distance": 1.0}]
        r = solve_graph("X", "Z", edges)
        assert r["shortest"]["path"] == []
        assert r["longest"]["path"] == []

    def test_simple_triangle(self):
        edges = [
            {"from": "X", "to": "Y", "distance": 1.0},
            {"from": "Y", "to": "Z", "distance": 2.0},
            {"from": "X", "to": "Z", "distance": 10.0},
        ]
        r = solve_graph("X", "Z", edges)
        assert r["shortest"]["distance"] == 3.0
        assert r["longest"]["distance"] == 10.0

    def test_all_pairs_have_paths(self):
        nodes = set()
        for e in EDGES:
            nodes.add(e["from"])
            nodes.add(e["to"])
        assert len(nodes) == 10
        adj = _build_adj(EDGES)
        for a in sorted(nodes):
            for b in sorted(nodes):
                if a == b: continue
                assert len(_dijkstra(a, b, adj)["path"]) >= 2

    def test_h_to_d(self):
        r = solve_graph("H", "D", EDGES)
        assert r["shortest"]["distance"] == 9.8
        assert r["shortest"]["path"] == ["H", "G", "F", "D"]

    def test_b_to_i(self):
        r = solve_graph("B", "I", EDGES)
        assert r["shortest"]["distance"] == 9.0
        assert r["shortest"]["path"] == ["B", "E", "G", "I"]
