"""Tests for CLI validation."""

import unittest

from src.config import build_parser, validate_args


class ConfigTests(unittest.TestCase):
    """Validate supported configuration parameters."""

    def test_negative_depth_is_rejected(self):
        parser = build_parser()
        namespace = parser.parse_args([
            "--package", "A",
            "--max-depth", "-1",
        ])
        with self.assertRaises(ValueError):
            validate_args(namespace)

    def test_non_png_output_is_rejected(self):
        parser = build_parser()
        namespace = parser.parse_args([
            "--package", "A",
            "--output", "graph.svg",
        ])
        with self.assertRaises(ValueError):
            validate_args(namespace)


if __name__ == "__main__":
    unittest.main()
