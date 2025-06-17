import unittest
import pandas as pd
from analyze_risky_files import get_risky_functions

class TestRiskyFunctions(unittest.TestCase):
    def test_returns_only_risky_functions(self):
        pr_data = pd.DataFrame({
            "filepath": ["file2.py"],
            "start_line": [16],  # Line falls inside complex_func range
            "end_line": [16]
        })

        lizard_data = pd.DataFrame({
            "filepath": ["file2.py"],
            "function_name": ["complex_func"],
            "start_line": [15],
            "end_line": [25],
            "complexity": [12]
        })

        result = get_risky_functions(pr_data, lizard_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["filepath"], "file2.py")
        self.assertGreater(result.iloc[0]["complexity"], 10)

if __name__ == "__main__":
    unittest.main()
