import argparse
import os
import sys
from pr_risk_checker import run_main_logic

def main():
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

    # GitHub Actions output
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"is_risky={str(result['is_risky']).lower()}\n")

    return result

if __name__ == "__main__":
    try:
        result = main()
    except ValueError as ve:
        print(f"::warning:: ValueError: {ve}")
        print("::notice:: is_risky=false")
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
                fh.write("is_risky=false\n")
        sys.exit(0)
    except Exception as e:
        print(f"::error:: Unexpected error: {e}")
        sys.exit(1)
