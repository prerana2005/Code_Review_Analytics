"""Fetches PR changed lines from GitHub and writes them to a CSV."""

import os
import sys
import re
import csv
import requests

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


def parse_patch_lines(patch):
    """Extract changed lines from a diff patch string."""
    changed_lines = []
    current_line = None

    for line in patch.split("\n"):
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            if match:
                current_line = int(match.group(1)) - 1
        elif line.startswith("+") and not line.startswith("+++"):
            current_line += 1
            changed_lines.append(current_line)

    return changed_lines


def write_line_blocks_to_csv(changed_lines_data):
    """Write grouped line blocks to a CSV file."""
    with open("pr_lines.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filepath", "start_line", "end_line"])

        for item in changed_lines_data:
            filename = item["filename"]
            changed_lines = sorted(item["changed_lines"])

            if not changed_lines:
                continue

            start = prev = changed_lines[0]
            for line in changed_lines[1:]:
                if line != prev + 1:
                    writer.writerow([filename, start, prev])
                    start = line
                prev = line
            writer.writerow([filename, start, prev])


def extract_pr_lines(repo_owner, repo_name, pr_number, request_headers):
    """Extracts changed line blocks from a PR and writes to 'pr_lines.csv'."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=request_headers, timeout=10)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        sys.exit()

    files = response.json()
    changed_lines_data = []
    print(f"Found {len(files)} changed files.\n")

    for file_info in files:
        filename = file_info["filename"]
        patch = file_info.get("patch")

        if not patch:
            print(f"No patch data for: {filename}")
            continue

        print(f"\nFile: {filename}")
        changed_lines = parse_patch_lines(patch)
        changed_lines_data.append({
            "filename": filename,
            "changed_lines": changed_lines
        })

    write_line_blocks_to_csv(changed_lines_data)


if __name__ == "__main__":
    extract_pr_lines(REPO_OWNER, REPO_NAME, PR_NUMBER, headers)
