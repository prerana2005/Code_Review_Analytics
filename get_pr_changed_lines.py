import requests
import os
import re
import csv

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

# URL to get the list of files changed in the PR
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/files"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

files = response.json()
changed_lines_data = []
print(f"Found {len(files)} changed files.\n")

for f in files:
    filename = f["filename"]
    patch = f.get("patch")

    if not patch:
        print(f"No patch data for: {filename}")
        continue

    print(f"\nFile: {filename}")
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

    changed_lines_data.append({
        "filename": filename,
        "changed_lines": changed_lines
    })

with open("pr_lines.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filepath", "start_line", "end_line"])  # updated

    for item in changed_lines_data:
        filename = item["filename"]
        changed_lines = sorted(item["changed_lines"])

        if not changed_lines:
            continue

        # Group consecutive lines into blocks
        start = prev = changed_lines[0]
        for line in changed_lines[1:]:
            if line != prev + 1:
                writer.writerow([filename, start, prev])
                start = line
            prev = line
        writer.writerow([filename, start, prev])  # write final block