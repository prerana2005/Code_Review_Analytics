"""Unit test for checking overlap cases in risky PR detection."""

import unittest
import pandas as pd
from analyze_risky_files import is_pr_risky

class TestOverlapCases(unittest.TestCase):
    """Tests that overlapping PR changes with complex functions are flagged as risky."""
    def test_detects_overlap_as_risky(self):
        """Should flag PR as risky if changes overlap with complex function blocks."""
        lizard_df = pd.DataFrame([
            {
                "filepath": "example.py",
                "function_name": "risky_function",
                "start_line": 20,
                "end_line": 30,
                "complexity": 15
            },
        ])

        pr_df = pd.DataFrame([
            {"filepath": "example.py", "start_line": 25, "end_line": 27},  # Inside risky
            {"filepath": "example.py", "start_line": 18, "end_line": 22},  # Ends inside
            {"filepath": "example.py", "start_line": 5, "end_line": 50},   # Fully surrounds
        ])

        self.assertTrue(is_pr_risky(pr_df, lizard_df))

if __name__ == "__main__":
    unittest.main()
