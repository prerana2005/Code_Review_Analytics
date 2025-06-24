"""
run_analysis.py

This script runs a risk analysis on a given GitHub pull request.
It checks which files and functions are changed and whether those
changes touch complex parts of the codebase.
"""

import argparse
import subprocess
import os
import pandas as pd
from analyze_risky_files import is_pr_risky, get_risky_functions

def main():
    """
    Main function to parse PR number, run PR line extraction,
    perform risk analysis using complexity metrics, and output the result.
    """
    parser = argparse.ArgumentParser(description="Check if a PR is risky.")
    parser.add_argument("--pr", type=int, required=True, help="Pull Request number")
    args = parser.parse_args()

    os.environ["REPO_OWNER"] = "prerana2005"
    os.environ["REPO_NAME"] = "Code_Review_Analytics"
    os.environ["PR_NUMBER"] = str(args.pr)

    subprocess.run(["python", "get_pr_changed_lines.py"], check=True)

    # Load PR changed lines CSV (output of the above script)
    pr_lines = pd.read_csv("pr_lines.csv")
    if pr_lines.empty:
        print(" This PR is safe. No changes found.")
        return

    # Load Lizard complexity data
    lizard = pd.read_csv("lizard_output_with_end_line.csv")
    lizard.columns = lizard.columns.str.strip()
    lizard = lizard.rename(columns={"CCN": "complexity"})

    # Type casting
    pr_lines["start_line"] = pr_lines["start_line"].astype(int)
    pr_lines["end_line"] = pr_lines["end_line"].astype(int)
    lizard["start_line"] = lizard["start_line"].astype(int)
    lizard["end_line"] = lizard["end_line"].astype(int)
    lizard["complexity"] = lizard["complexity"].astype(int)

    # Risk analysis
    if is_pr_risky(pr_lines, lizard):
        print(" Risky PR: It modifies complex code.")
    else:
        print(" Safe PR: No risky functions changed.")

    # Save risky functions to CSV
    risky_funcs_df = get_risky_functions(pr_lines, lizard)
    risky_funcs_df.to_csv("risky_files_in_pr.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
