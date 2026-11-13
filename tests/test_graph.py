"""Tests for iterative BFS graph construction."""

import unittest
from pathlib import Path

from src.graph import build_graph
from src.sources import TestRepository


DATA = Path(__file__).parent / "data"


class GraphTests(unittest.TestCase):
    """Verify traversal, depth limits and cycles."""

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


if __name__ == "__main__":
    unittest.main()
