import unittest
import pandas as pd

# This function should be moved to your analyze_risky_files.py
def is_pr_risky(pr_df, lizard_df):
    for _, change in pr_df.iterrows():
        file_path = change["filepath"]
        changed_line = change["start_line"]

        # Get all functions in that file
        funcs_in_file = lizard_df[lizard_df["filepath"] == file_path]

        for _, func in funcs_in_file.iterrows():
            if func["CCN"] > 10:
                func_start = func["start_line"]
                func_end = func_start + func["length"] - 1

                # Only flag risky if the changed line is inside risky function
                if func_start <= changed_line <= func_end:
                    return True
    return False


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
