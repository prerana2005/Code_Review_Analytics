import unittest
import pandas as pd

class TestFalsePositiveDetection(unittest.TestCase):

    def test_change_in_simple_function_only(self):
        # Load mock data
        lizard_data = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/tests/mock_lizard_output.csv")
        pr_changes = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/tests/mock_pr_files.csv")

        # Assume PR is risky if any changed file has a complex function
        # This is the current logic we're testing
        is_risky = False

        for _, change in pr_changes.iterrows():
            file_path = change["filepath"]
            changed_line = change["start_line"]

            # Get all functions in that file
            funcs_in_file = lizard_data[lizard_data["filepath"] == file_path]

            for _, func in funcs_in_file.iterrows():
                if func["CCN"] > 10:
                    # BUG: doesn't check if this function was actually modified
                    is_risky = True

        # Expectation: should not be risky (only a simple function was changed)
        self.assertFalse(is_risky, "PR was incorrectly flagged as risky")

if __name__ == "__main__":
    unittest.main()
