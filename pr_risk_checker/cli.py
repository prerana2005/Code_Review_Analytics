"""
CLI entry point for running the PR risk checker with GitHub PR metadata.
"""
import argparse
import os
from pr_risk_checker import run_main_logic

def main():
    """
    Parses CLI arguments and runs the PR risk analysis.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_owner', required=True)
    parser.add_argument('--repo_name', required=True)
    parser.add_argument('--pr_number', type=int, required=True)
    parser.add_argument('--token', required=False)

    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN is not set")
    result = run_main_logic(args.repo_owner, args.repo_name, args.pr_number, token=token)

    print(f"::notice:: is_risky={result['is_risky']}")

    # If running inside GitHub Actions, send result to output
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"is_risky={str(result['is_risky']).lower()}\n")

if __name__ == "__main__":
    main()
