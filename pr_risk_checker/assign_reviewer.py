import os
import requests

def assign_reviewer(repo_owner, repo_name, pr_number, token, reviewer):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    # Get PR author
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    pr_response = requests.get(pr_url, headers=headers)
    pr_data = pr_response.json()
    pr_author = pr_data["user"]["login"]

    if pr_author.lower() == reviewer.lower():
        print(f"Skipping assignment: PR author is the same as reviewer ({reviewer})")
        return

    # Assign reviewer
    assign_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/requested_reviewers"
    data = {"reviewers": [reviewer]}
    assign_response = requests.post(assign_url, json=data, headers=headers)

    if assign_response.status_code == 201:
        print(f" Assigned reviewer: {reviewer}")
    else:
        print(f" Failed to assign reviewer: {assign_response.status_code}")
        print(assign_response.json())

if __name__ == "__main__":
    repo_owner = os.environ["REPO_OWNER"]
    repo_name = os.environ["REPO_NAME"]
    pr_number = os.environ["PR_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]
    reviewer = os.environ.get("REVIEWER", "senior-reviewer")

    assign_reviewer(repo_owner, repo_name, pr_number, token, reviewer)
