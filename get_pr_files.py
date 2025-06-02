from dotenv import load_dotenv
load_dotenv()  # loads the .env file variables into environment

import os
from dotenv import load_dotenv
import requests

load_dotenv()  # Load env vars from .env

GITHUB_REPO = "prerana2005/Code_Review_Analytics"
PR_NUMBER = 1
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls/{PR_NUMBER}/files"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    files = response.json()
    changed_files = [file['filename'] for file in files]
    print("Changed files in PR:")
    for f in changed_files:
        print(f)
else:
    print("Error:", response.status_code)
    print("Message:", response.text)
