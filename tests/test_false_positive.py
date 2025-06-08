import unittest
import pandas as pd

from analyze_risky_files import is_pr_risky

class TestFalsePositiveDetection(unittest.TestCase):
    def test_change_in_simple_function_only(self):
        # Load the mock CSVs
        pr_changes = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/tests/mock_pr_files.csv")
        lizard_data = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/tests/mock_lizard_output.csv")

        # Run the updated logic
        is_risky = is_pr_risky(pr_changes, lizard_data)

        # We expect it to NOT be risky
        self.assertFalse(is_risky, "PR was incorrectly flagged as risky")

if __name__ == "__main__":
    unittest.main()
