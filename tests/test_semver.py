"""Tests for Cargo-style version requirements."""

import unittest

from src.semver import satisfies


class SemverTests(unittest.TestCase):
    """Check common Cargo requirement forms."""

    def test_caret_requirement(self):
        self.assertTrue(satisfies("1.9.0", "^1.2.3"))
        self.assertFalse(satisfies("2.0.0", "^1.2.3"))

    def test_zero_major_caret_requirement(self):
        self.assertTrue(satisfies("0.4.9", "^0.4.2"))
        self.assertFalse(satisfies("0.5.0", "^0.4.2"))

    def test_tilde_requirement(self):
        self.assertTrue(satisfies("1.2.9", "~1.2.3"))
        self.assertFalse(satisfies("1.3.0", "~1.2.3"))

    def test_comparator_range(self):
        self.assertTrue(satisfies("1.5.0", ">=1.2, <2.0"))
        self.assertFalse(satisfies("2.1.0", ">=1.2, <2.0"))

    def test_wildcard_requirement(self):
        self.assertTrue(satisfies("1.2.9", "1.2.*"))
        self.assertFalse(satisfies("1.3.0", "1.2.*"))


if __name__ == "__main__":
    unittest.main()
