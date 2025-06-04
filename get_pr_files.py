import requests
import csv
import os

# ====== CONFIGURATION ======  
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  #export this in terminal
REPO_OWNER = "prerana2005"
REPO_NAME = "Code_Review_Analytics"
PR_NUMBER = 1  
OUTPUT_CSV = "pr_files.csv"
# ===========================

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# URL to get the list of files changed in the specified pull request
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/files"

# Send GET request to GitHub API
response = requests.get(url, headers=headers)

# Parse JSON response to get file data
files = response.json()

# If API call fails, print the error
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
else:
    print(f"Fetched {len(files)} changed files.")
    with open(OUTPUT_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "status", "additions", "deletions", "changes"])
# Loop through each file in the PR and write its details
        for f in files:
            writer.writerow([
                f["filename"],   # Path of the file changed
                f["status"],     # Status: modified, added, or removed
                f["additions"],  # Number of lines added
                f["deletions"],  # Number of lines deleted
                f["changes"],    # Total changes (additions + deletions)
            ])
    print(f"Data written to {OUTPUT_CSV}")
