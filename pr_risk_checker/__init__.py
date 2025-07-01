import os
import sys
import subprocess
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyze_risky_files import is_pr_risky, get_risky_functions
from pr_risk_checker.generate_lizard_csv import analyze_codebase

def run_main_logic(repo_owner, repo_name, pr_number):
    """
    Executes the risk analysis pipeline for a given pull request.
    
    Args:
        repo_owner (str): GitHub repository owner
        repo_name (str): GitHub repository name
        pr_number (int): Pull request number
    """

    print(f" Analyzing PR #{pr_number} in {repo_owner}/{repo_name}")

    os.environ["GITHUB_TOKEN"] = os.getenv("GITHUB_TOKEN")
    os.environ["REPO_OWNER"] = repo_owner
    os.environ["REPO_NAME"] = repo_name
    os.environ["PR_NUMBER"] = str(pr_number)

    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "get_pr_changed_lines.py"))
    subprocess.run(["python", script_path], check=True)

    pr_lines = pd.read_csv("pr_lines.csv")
    if pr_lines.empty:
        print(" Safe PR: No changes found.")
        return

    if not os.path.exists("lizard_output_with_end_line.csv"):
        print("Generating lizard_output_with_end_line.csv...")
        analyze_codebase(["."], "lizard_output_with_end_line.csv")

    lizard = pd.read_csv("lizard_output_with_end_line.csv")
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
