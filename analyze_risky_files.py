"""Analyze PR changes and identify risky functions
   based on complexity using vectorized operations
"""

import pandas as pd
import os

def normalize_path(path):
    return os.path.normpath(path).lstrip("./\\")

def get_risky_functions(pr_df, lizard_df):
    """
    Returns a DataFrame of risky functions (complexity > 10)
    that have overlapping line ranges with PR changes.
    """

    risky_funcs = lizard_df[lizard_df["complexity"] > 10].copy()

    pr_df = pr_df.rename(columns={
        "start_line": "start_line_pr",
        "end_line": "end_line_pr"
        })
    risky_funcs = risky_funcs.rename(columns={
        "start_line": "start_line_func",
        "end_line": "end_line_func"
        })

    # Normalize file paths
    pr_df["filepath"] = pr_df["filepath"].apply(normalize_path)
    risky_funcs["filepath"] = risky_funcs["filepath"].apply(normalize_path)
    
    # Merge PR changes and risky functions on filepath
    merged = pr_df.merge(risky_funcs, on="filepath", how="inner")

    # Check for line range overlap (if any PR lines fall in function lines)
    # Equivalent to: not (change ends before function starts OR starts after function ends)
    overlaps = ~(
        (merged["end_line_pr"] < merged["start_line_func"]) |
        (merged["start_line_pr"] > merged["end_line_func"])
    )

    risky_overlaps = merged[overlaps]

    return risky_overlaps[[
        "filepath", "function_name", "start_line_func",
        "end_line_func", "complexity"
    ]].rename(columns={
        "start_line_func": "start_line",
        "end_line_func": "end_line"
    })

def is_pr_risky(pr_df, lizard_df):
    """
    Returns True if any risky function (complexity > 10) is touched by PR changes.
    """
    risky_files = {normalize_path(f) for f in lizard_df[lizard_df["complexity"] > 10]["filepath"].unique()}
    changed_files = {normalize_path(f) for f in pr_df["filepath"].unique()}

    print("RISKY FILES:", risky_files)
    print("CHANGED FILES:", changed_files)
    
    return any(file in risky_files for file in changed_files)

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
    lizard["start_line"] = lizard["start_line"].astype(int)
    lizard["end_line"] = lizard["end_line"].astype(int)
    lizard["complexity"] = lizard["complexity"].astype(int)

    if is_pr_risky(pr_lines, lizard):
        print("Risky PR: It modifies complex code.")
    else:
        print("Safe PR: No risky functions changed.")

    risky_funcs_df = get_risky_functions(pr_lines, lizard)
    print("\nRisky functions touched in this PR:")
    print(risky_funcs_df)

    risky_funcs_df.to_csv("risky_files_in_pr.csv", index=False, encoding="utf-8")
