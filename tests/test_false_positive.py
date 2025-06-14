import unittest
import pandas as pd

from analyze_risky_files import is_pr_risky

class TestFalsePositiveDetection(unittest.TestCase):
    def test_change_in_simple_function_only(self):
        # Load updated mock files
        pr_changes = pd.read_csv("tests/mock_pr_lines.csv")
        lizard_data = pd.read_csv("tests/mock_lizard_output_with_end_line.csv")

        # Run the logic
        is_risky = is_pr_risky(pr_changes, lizard_data)

        # We expect it to NOT be risky
        self.assertFalse(is_risky, "PR was incorrectly flagged as risky")

if __name__ == "__main__":
    unittest.main()
