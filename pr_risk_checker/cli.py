"""
CLI entry point for running the PR risk checker with GitHub PR metadata.
"""

import argparse
from pr_risk_checker import run_main_logic

def main():
    """
    Entry point for parsing GitHub Action inputs and running PR risk analysis.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_owner', required=True)
    parser.add_argument('--repo_name', required=True)
    parser.add_argument('--pr_number', type=int, required=True)
    args = parser.parse_args()

    run_main_logic(args.repo_owner, args.repo_name, args.pr_number)

if __name__ == "__main__":
    main()
