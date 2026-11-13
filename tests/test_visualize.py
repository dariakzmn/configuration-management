"""Tests for Mermaid graph generation."""

import unittest

from src.visualize import to_mermaid


class VisualizeTests(unittest.TestCase):
    """Verify Mermaid output."""

    def test_mermaid_contains_nodes_and_edge(self):
        graph = {"A": ["B"], "B": []}
        text = to_mermaid("A", graph)
        self.assertIn("graph TD", text)
        self.assertIn('N0["A"]', text)
        self.assertIn("N0 --> N1", text)


if __name__ == "__main__":
    unittest.main()
