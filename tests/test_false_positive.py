"""Unit test to check that simple, non-risky changes are not flagged as risky."""

import sys
import os
import unittest
import pandas as pd

from analyze_risky_files import is_pr_risky
# Add project root to Python path so we can import analyze_risky_files
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestFalsePositiveDetection(unittest.TestCase):
    """Test case for detecting false positives in PR risk analysis."""

    def test_change_in_simple_function_only(self):
        """Should not flag simple, low-complexity function changes as risky."""
        pr_changes = pd.read_csv("tests/mock_pr_lines.csv")
        lizard_data = pd.read_csv("tests/mock_lizard_output_with_end_line.csv")

        is_risky = is_pr_risky(pr_changes, lizard_data)

        self.assertFalse(is_risky, "PR was incorrectly flagged as risky")

if __name__ == "__main__":
    unittest.main()
