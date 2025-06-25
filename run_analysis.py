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
    Main function to parse PR details, run PR line extraction,
    perform risk analysis using complexity metrics, and output the result.
    """
    parser = argparse.ArgumentParser(description="Check if a PR is risky.")
    parser.add_argument("--repo_owner", type=str, required=True, help="Repository owner")
    parser.add_argument("--repo_name", type=str, required=True, help="Repository name")
    parser.add_argument("--pr_number", type=int, required=True, help="Pull Request number")
    args = parser.parse_args()

    os.environ["REPO_OWNER"] = args.repo_owner
    os.environ["REPO_NAME"] = args.repo_name
    os.environ["PR_NUMBER"] = str(args.pr_number)

    subprocess.run(["python", "Code_Review_Analytics/get_pr_changed_lines.py"], check=True)

    pr_lines = pd.read_csv("pr_lines.csv")
    if pr_lines.empty:
        print("This PR is safe. No changes found.")
        return

    lizard = pd.read_csv("Code_Review_Analytics/lizard_output_with_end_line.csv")
    lizard.columns = lizard.columns.str.strip()
    lizard = lizard.rename(columns={"CCN": "complexity"})

    pr_lines["start_line"] = pr_lines["start_line"].astype(int)
    pr_lines["end_line"] = pr_lines["end_line"].astype(int)
    lizard["start_line"] = lizard["start_line"].astype(int)
    lizard["end_line"] = lizard["end_line"].astype(int)
    lizard["complexity"] = lizard["complexity"].astype(int)

    if is_pr_risky(pr_lines, lizard):
        print(" Risky PR: It modifies complex code.")
    else:
        print(" Safe PR: No risky functions changed.")

    risky_funcs_df = get_risky_functions(pr_lines, lizard)
    risky_funcs_df.to_csv("risky_files_in_pr.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
