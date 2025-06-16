import pandas as pd

def get_risky_functions(pr_df, lizard_df):
    lizard_df = lizard_df.rename(columns={"CCN": "complexity"})
    risky_functions = []

    changed_lines_map = {}
    for _, row in pr_df.iterrows():
        filepath = row["filepath"]
        line = int(row["start_line"])
        changed_lines_map.setdefault(filepath, []).append(line)

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
                    "nloc": func["nloc"],
                    "function_name": func["function_name"],
                    "start_line": func_start,
                    "end_line": func_end
                })
                break

    return pd.DataFrame(risky_functions)

def is_pr_risky(pr_df, lizard_df):
    lizard_df = lizard_df.rename(columns={"CCN": "complexity"})  # ✅ ensure consistency

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
    pr_lines = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/pr_lines.csv")
    lizard = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/lizard_output_with_end_line.csv")

    pr_lines["start_line"] = pr_lines["start_line"].astype(int)
    pr_lines["end_line"] = pr_lines["end_line"].astype(int)
    lizard["CCN"] = lizard["CCN"].astype(int)
    lizard["start_line"] = lizard["start_line"].astype(int)
    lizard["end_line"] = lizard["end_line"].astype(int)

    if is_pr_risky(pr_lines, lizard):
        print("Risky PR: It modifies complex code.")
    else:
        print("Safe PR: No risky functions changed.")

    risky_functions = get_risky_functions(pr_lines, lizard)
    print("\n Risky functions touched in this PR:")
    print(risky_functions)

    risky_functions.to_csv("risky_files_in_pr.csv", index=False)
