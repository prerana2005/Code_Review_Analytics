import os
import pandas as pd
from pr_risk_checker.get_pr_changed_lines import extract_pr_changed_line_blocks
from pr_risk_checker.analyze_risky_files import is_pr_risky, get_risky_functions
from pr_risk_checker.generate_lizard_csv import analyze_codebase

def run_main_logic(repo_owner, repo_name, pr_number):
    """
    Executes the risk analysis pipeline for a given pull request.
    
    Args:
        repo_owner (str): GitHub repository owner
        repo_name (str): GitHub repository name
        pr_number (int): Pull request number

    Returns:
        dict: {
            "is_risky": bool,
            "risky_functions": pd.DataFrame
        }
    """
    print(f"Analyzing PR #{pr_number} in {repo_owner}/{repo_name}")

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise EnvironmentError("GITHUB_TOKEN is not set")

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get changed line blocks in PR
    pr_lines_df = extract_pr_changed_line_blocks(repo_owner, repo_name, pr_number, headers)
    if pr_lines_df.empty:
        print("Safe PR: No code lines changed.")
        return {
            "is_risky": False,
            "risky_functions": pd.DataFrame()
        }

    # Get Lizard metrics
    lizard_df = analyze_codebase(["."], output_format="df")
    lizard_df.columns = lizard_df.columns.str.strip()
    lizard_df = lizard_df.rename(columns={"CCN": "complexity"})

    for col in ["start_line", "end_line", "complexity"]:
        lizard_df[col] = lizard_df[col].astype(int)
    for col in ["start_line", "end_line"]:
        pr_lines_df[col] = pr_lines_df[col].astype(int)

    # Analyze risk
    is_risky = is_pr_risky(pr_lines_df, lizard_df)
    if is_risky:
        print("Risky PR: It modifies complex code.")
    else:
        print("Safe PR: No risky functions changed.")

    risky_funcs_df = get_risky_functions(pr_lines_df, lizard_df)
    if not risky_funcs_df.empty:
        print("\nRisky functions touched in this PR:")
        print(risky_funcs_df)
        os.makedirs("artifacts", exist_ok=True)
        risky_funcs_df.to_csv("artifacts/risky_files_in_pr.csv", index=False)
    else:
        print("\nNo risky functions found in PR.")

    return {
        "is_risky": is_risky,
        "risky_functions": risky_funcs_df
    }
