import unittest
import pandas as pd
from analyze_risky_files import get_risky_functions

class TestRiskyFunctions(unittest.TestCase):
    def test_returns_only_risky_functions(self):
        pr_data = pd.DataFrame({
            "filepath": ["file1.py", "file2.py"],
        })

        lizard_data = pd.DataFrame({
            "filepath": ["file1.py", "file2.py", "file2.py"],
            "CCN": [5, 12, 9],
            "nloc": [20, 35, 18]
        })

        result = get_risky_functions(pr_data, lizard_data)

        # Expect only the function with CCN 12 (risky) from file2.py
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["filepath"], "file2.py")
        self.assertGreater(result.iloc[0]["complexity"], 10)

if __name__ == "__main__":
    unittest.main()
