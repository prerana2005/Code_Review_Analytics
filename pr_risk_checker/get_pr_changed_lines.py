"""
Fetches PR changed lines from GitHub and returns grouped line blocks.
"""

import sys
import re
import requests
import pandas as pd


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
    df = df.sort_values(by=["filepath", "line"])
    df["line_diff"] = df["line"].diff()
    df["file_change"] = df["filepath"] != df["filepath"].shift()
    df["group"] = (df["line_diff"] != 1) | df["file_change"]
    df["group_id"] = df["group"].cumsum()

    blocks = (
        df.groupby(["filepath", "group_id"])
        .agg(start_line=("line", "min"), end_line=("line", "max"))
        .reset_index()
    )

    return blocks


def extract_pr_changed_line_blocks(repo_owner, repo_name, pr_number, request_headers):
    """Returns grouped changed line blocks for a given PR."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=request_headers, timeout=10)

    if response.status_code != 200:
        raise ValueError(f"GitHub API returned {response.status_code}: {response.text}")

    files = response.json()
    changed_lines = []

    for file_info in files:
        filename = file_info["filename"]
        patch = file_info.get("patch")

        if not patch:
            continue

        changed_lines.extend(parse_patch_lines(patch, filename))

    if not changed_lines:
        return pd.DataFrame(columns=["filepath", "start_line", "end_line"])

    return group_lines_to_blocks_vectorized(changed_lines)
