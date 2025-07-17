"""
Assign a reviewer to a pull request if the PR is considered very risky
based on code complexity and number of risky functions.
"""

import os
import requests
import random
import pandas as pd

# Risk thresholds
VERY_RISKY_COMPLEXITY = 15
VERY_RISKY_FUNCTION_COUNT = 2


def load_risky_functions(path="artifacts/risky_files_in_pr.csv"):
    """
    Load the CSV file containing risky functions.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing risky function information.
    """
    if not os.path.exists(path):
        print("No risk report found.")
        return pd.DataFrame()
    return pd.read_csv(path)


def is_very_risky(risky_df):
    """
    Determine if the PR is very risky based on complexity or function count.

    Args:
        risky_df (pd.DataFrame): DataFrame of risky functions.

    Returns:
        bool: True if the PR is very risky, False otherwise.
    """
    if len(risky_df) >= VERY_RISKY_FUNCTION_COUNT:
        return True
    if (risky_df["complexity"] > VERY_RISKY_COMPLEXITY).any():
        return True
    return False


def get_pr_author(repo_owner, repo_name, pr_number, token):
    """
    Fetch the author (username) of the pull request from GitHub.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Repository name.
        pr_number (str or int): Pull request number.
        token (str): GitHub API token.

    Returns:
        str: GitHub username of the PR author.

    Raises:
        RuntimeError: If the API request fails.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch PR: {response.status_code} - {response.text}")
    return response.json()["user"]["login"]


def pick_random_reviewer(reviewers, exclude):
    """
    Pick a random reviewer from a list, excluding the PR author.

    Args:
        reviewers (list): List of reviewer usernames.
        exclude (str): Username to exclude (the PR author).

    Returns:
        str or None: A selected reviewer or None if no eligible reviewers.
    """
    eligible = [r for r in reviewers if r.lower() != exclude.lower()]
    return random.choice(eligible) if eligible else None


def assign_reviewer(repo_owner, repo_name, pr_number, token, reviewer):
    """
    Assign a reviewer to the pull request via GitHub API.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Repository name.
        pr_number (str or int): Pull request number.
        token (str): GitHub API token.
        reviewer (str): GitHub username of the reviewer.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/requested_reviewers"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"reviewers": [reviewer]}
    response = requests.post(url, json=data, headers=headers, timeout=10)
    if response.status_code == 201:
        print(f"Assigned reviewer: {reviewer}")
    else:
        print(f"Failed to assign reviewer: {response.status_code}")
        print(response.json())


def main():
    """
    Main function to handle reviewer assignment logic for risky pull requests.
    """
    repo_owner = os.environ.get("REPO_OWNER")
    repo_name = os.environ.get("REPO_NAME")
    pr_number = os.environ.get("PR_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")
    reviewers_env = os.environ.get("REVIEWERS", "senior-reviewer")
    reviewers = [r.strip() for r in reviewers_env.split(",") if r.strip()]

    if not all([repo_owner, repo_name, pr_number, token]):
        print("Missing required environment variables (REPO_OWNER, REPO_NAME, PR_NUMBER, GITHUB_TOKEN).")
        exit(1)

    risky_df = load_risky_functions()
    if risky_df.empty or not is_very_risky(risky_df):
        print("PR not very risky — no reviewer assignment needed.")
        exit(0)

    print("PR is very risky — assigning reviewer.")

    try:
        pr_author = get_pr_author(repo_owner, repo_name, pr_number, token)
        print(f"PR Author: {pr_author}")
        print(f"Available Reviewers: {reviewers}")

        reviewer = pick_random_reviewer(reviewers, exclude=pr_author)

        if reviewer:
            print(f"Selected Reviewer: {reviewer}")
            assign_reviewer(repo_owner, repo_name, pr_number, token, reviewer)
        else:
            print("No eligible reviewer found after excluding PR author.")
    except Exception as exc:
        print(f"Error while assigning reviewer: {exc}")
        exit(1)


if __name__ == "__main__":
    main()
