"""Analyze PR changes and identify risky functions based on complexity."""

import pandas as pd

def get_risky_functions(pr_df, lizard_df):
    """
    Returns a DataFrame of risky functions that overlap with PR changes.

    A function is considered risky if its complexity is greater than 10,
    and if any PR change overlaps with its lines.
    """
    risky_functions = []

    changed_lines_map = {}
    for _, row in pr_df.iterrows():
        filepath = row["filepath"]
        start = int(row["start_line"])
        end = int(row["end_line"])
        changed_lines_map.setdefault(filepath, []).extend(range(start, end + 1))

    for _, func in lizard_df.iterrows():
        if int(func["complexity"]) <= 10:
            continue

        filepath = func["filepath"]
        func_start = int(func["start_line"])
        func_end = int(func["end_line"])

        if filepath not in changed_lines_map:
            continue

        for line in changed_lines_map[filepath]:
            if func_start <= line <= func_end:
                risky_functions.append({
                    "filepath": filepath,
                    "complexity": func["complexity"],
                    "function_name": func["function_name"],
                    "start_line": func_start,
                    "end_line": func_end
                })
                break

    return pd.DataFrame(risky_functions)

def is_pr_risky(pr_df, lizard_df):
    """
    Returns True if any risky function (complexity > 10) is touched by PR changes.

    It checks for any overlap between changed line blocks and risky function lines.
    """
    changed_blocks_map = {}
    for _, row in pr_df.iterrows():
        filepath = row["filepath"]
        start = int(row["start_line"])
        end = int(row["end_line"])
        changed_blocks_map.setdefault(filepath, []).append((start, end))

    for _, func in lizard_df.iterrows():
        if int(func["complexity"]) <= 10:
            continue

        filepath = func["filepath"]
        func_start = int(func["start_line"])
        func_end = int(func["end_line"])

        if filepath not in changed_blocks_map:
            continue

        for change_start, change_end in changed_blocks_map[filepath]:
            if (
                func_start <= change_start <= func_end or
                func_start <= change_end <= func_end or
                (change_start <= func_start and change_end >= func_end)
            ):
                return True

    return False

if __name__ == "__main__":
    pr_lines = pd.read_csv(
        "C:/Users/Prerana/Desktop/Code_Review_Analytics/pr_lines.csv"
        )
    lizard = pd.read_csv(
        "C:/Users/Prerana/Desktop/Code_Review_Analytics/lizard_output_with_end_line.csv"
        )
    lizard.columns = lizard.columns.str.strip()
    lizard = lizard.rename(columns={"CCN": "complexity"})

    pr_lines["start_line"] = pr_lines["start_line"].astype(int)
    pr_lines["end_line"] = pr_lines["end_line"].astype(int)
    lizard["complexity"] = lizard["complexity"].astype(int)
    lizard["start_line"] = lizard["start_line"].astype(int)
    lizard["end_line"] = lizard["end_line"].astype(int)

    if is_pr_risky(pr_lines, lizard):
        print("Risky PR: It modifies complex code.")
    else:
        print("Safe PR: No risky functions changed.")

    risky_funcs_df = get_risky_functions(pr_lines, lizard)
    print("\n Risky functions touched in this PR:")
    print(risky_funcs_df)

    risky_funcs_df.to_csv("risky_files_in_pr.csv", index=False)
