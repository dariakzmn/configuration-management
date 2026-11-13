"""Tests for BFS graph operations."""

import unittest
from pathlib import Path

from src.graph import build_graph, load_order
from src.sources import TestRepository


DATA = Path(__file__).parent / "data"


class GraphTests(unittest.TestCase):
    """Verify traversal, depth limits, cycles and load order."""

    def test_bfs_builds_transitive_graph(self):
        source = TestRepository(str(DATA / "basic.json"))
        root, graph = build_graph(source, "A", 4)
        self.assertEqual(root, "A")
        self.assertEqual(set(graph), {"A", "B", "C", "D", "E"})

    def test_max_depth_stops_expansion(self):
        source = TestRepository(str(DATA / "deep.json"))
        _, graph = build_graph(source, "A", 2)
        self.assertEqual(set(graph), {"A", "B", "C"})
        self.assertEqual(graph["C"], [])

    def test_cycle_does_not_loop_forever(self):
        source = TestRepository(str(DATA / "cycle.json"))
        _, graph = build_graph(source, "A", 10)
        self.assertEqual(set(graph), {"A", "B", "C"})

    def test_load_order_places_dependencies_first(self):
        source = TestRepository(str(DATA / "basic.json"))
        _, graph = build_graph(source, "A", 4)
        order, cyclic = load_order(graph)
        self.assertFalse(cyclic)
        self.assertLess(order.index("D"), order.index("B"))
        self.assertLess(order.index("B"), order.index("A"))

    def test_load_order_reports_cycle(self):
        source = TestRepository(str(DATA / "cycle.json"))
        _, graph = build_graph(source, "A", 10)
        order, cyclic = load_order(graph)
        self.assertEqual(order, [])
        self.assertEqual(set(cyclic), {"A", "B", "C"})


if __name__ == "__main__":
    unittest.main()
