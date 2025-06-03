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

url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/files"

response = requests.get(url, headers=headers)
files = response.json()

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
else:
    print(f"Fetched {len(files)} changed files.")
    with open(OUTPUT_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "status", "additions", "deletions", "changes"])
        for f in files:
            writer.writerow([
                f["filename"],
                f["status"],
                f["additions"],
                f["deletions"],
                f["changes"],
            ])
    print(f"Data written to {OUTPUT_CSV}")
