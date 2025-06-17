import sys
import os
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyze_risky_files import is_pr_risky

# Mock risky function from lizard output
lizard_df = pd.DataFrame([
    {"filepath": "example.py","function_name": "risky_function", "start_line": 20, "end_line": 30, "complexity": 15},
])

# Simulated PR line changes with overlap cases
pr_df = pd.DataFrame([
    {"filepath": "example.py", "start_line": 25, "end_line": 27},  #  Inside risky
    {"filepath": "example.py", "start_line": 18, "end_line": 22},  #  Ends inside
    {"filepath": "example.py", "start_line": 5,  "end_line": 50},  #  Fully surrounds
])

# Test result
assert is_pr_risky(pr_df, lizard_df) == True
print(" All risky overlap cases detected.")
