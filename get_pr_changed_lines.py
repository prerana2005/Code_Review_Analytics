"""
   Fetches PR changed lines from GitHub and writes them to a CSV
   using pandas with column-wise operations.
"""

import os
import sys
import re
import requests
import pandas as pd

# ====== CONFIGURATION ======
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # export this in terminal
REPO_OWNER = "prerana2005"
REPO_NAME = "Code_Review_Analytics"
PR_NUMBER = 1
# ===========================

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def parse_patch_lines(patch, filename):
    """Extract changed lines from a diff patch string."""
    changed_lines = []
    current_line = None

    for line in patch.split("\n"):
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            if match:
                current_line = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++") and current_line is not None:
            current_line += 1
            changed_lines.append((filename, current_line))

    return changed_lines


def group_lines_to_blocks_vectorized(changed_lines):
    """Groups changed lines into start-end blocks using vectorized pandas logic."""
    df = pd.DataFrame(changed_lines, columns=["filepath", "line"])

    # Sort by file and line
    df = df.sort_values(by=["filepath", "line"])

    # Group breaks: when line difference is not 1 (non-contiguous lines)
    df["line_diff"] = df["line"].diff()
    df["file_change"] = df["filepath"] != df["filepath"].shift()
    df["group"] = (df["line_diff"] != 1) | df["file_change"]
    df["group_id"] = df["group"].cumsum()

    # Group by group_id and filepath, get min/max line
    blocks = (
        df.groupby(["filepath", "group_id"])
        .agg(start_line=("line", "min"), end_line=("line", "max"))
        .reset_index()
    )

    return blocks[["filepath", "start_line", "end_line"]]


def extract_pr_lines(repo_owner, repo_name, pr_number, request_headers):
    """Fetches PR files, extracts line changes, and saves them to CSV via pandas."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=request_headers, timeout=10)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        sys.exit()

    files = response.json()
    changed_lines = []
    print(f"Found {len(files)} changed files.\n")

    for file_info in files:
        filename = file_info["filename"]
        patch = file_info.get("patch")

        if not patch:
            print(f"No patch data for: {filename}")
            continue

        print(f"File: {filename}")
        changed_lines.extend(parse_patch_lines(patch, filename))

    # Group changed lines into blocks using vectorized operations
    if changed_lines:
        df_blocks = group_lines_to_blocks_vectorized(changed_lines)
        df_blocks.to_csv("pr_lines.csv", index=False, encoding="utf-8")
        print("\nSaved PR changed line blocks to 'pr_lines.csv'")
    else:
        print("No changed lines found.")


if __name__ == "__main__":
    extract_pr_lines(REPO_OWNER, REPO_NAME, PR_NUMBER, headers)
