import os
import requests
import random
import pandas as pd

VERY_RISKY_COMPLEXITY = 15
VERY_RISKY_FUNCTION_COUNT = 2

def load_risky_functions(path="artifacts/risky_files_in_pr.csv"):
    if not os.path.exists(path):
        print(" No risk report found.")
        return pd.DataFrame()
    return pd.read_csv(path)

def is_very_risky(risky_df):
    if len(risky_df) >= VERY_RISKY_FUNCTION_COUNT:
        return True
    if (risky_df["complexity"] > VERY_RISKY_COMPLEXITY).any():
        return True
    return False

def get_pr_author(repo_owner, repo_name, pr_number, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch PR: {response.status_code} - {response.text}")
    return response.json()["user"]["login"]

def pick_random_reviewer(reviewers, exclude):
    eligible = [r for r in reviewers if r.lower() != exclude.lower()]
    return random.choice(eligible) if eligible else None

def assign_reviewer(repo_owner, repo_name, pr_number, token, reviewer):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/requested_reviewers"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"reviewers": [reviewer]}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f" Assigned reviewer: {reviewer}")
    else:
        print(f" Failed to assign reviewer: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    repo_owner = os.environ.get("REPO_OWNER")
    repo_name = os.environ.get("REPO_NAME")
    pr_number = os.environ.get("PR_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")
    reviewers_env = os.environ.get("REVIEWERS", "senior-reviewer")  # comma-separated
    reviewers = [r.strip() for r in reviewers_env.split(",") if r.strip()]

    if not all([repo_owner, repo_name, pr_number, token]):
        print(" Missing required environment variables.")
        exit(1)

    risky_df = load_risky_functions()
    if risky_df.empty or not is_very_risky(risky_df):
        print(" PR not very risky — no reviewer assignment needed.")
        exit(0)

    pr_author = get_pr_author(repo_owner, repo_name, pr_number, token)
    reviewer = pick_random_reviewer(reviewers, exclude=pr_author)

    if reviewer:
        assign_reviewer(repo_owner, repo_name, pr_number, token, reviewer)
    else:
        print(" No eligible reviewer found after excluding PR author.")
