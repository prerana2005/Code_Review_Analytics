"""
Analyze PR changes and identify risky functions
based on complexity using vectorized operations.
"""

import pandas as pd
import os


def normalize_path(path):
    return os.path.normpath(path).lstrip("./\\")


def get_risky_functions(pr_df, lizard_df, risk_threshold=10):
    """
    Returns a DataFrame of risky functions (complexity > threshold)
    that have overlapping line ranges with PR changes.
    """
    risky_funcs = lizard_df[lizard_df["complexity"] > risk_threshold].copy()

    pr_df = pr_df.rename(columns={"start_line": "start_line_pr", "end_line": "end_line_pr"})
    risky_funcs = risky_funcs.rename(columns={"start_line": "start_line_func", "end_line": "end_line_func"})

    pr_df["filepath"] = pr_df["filepath"].apply(normalize_path)
    risky_funcs["filepath"] = risky_funcs["filepath"].apply(normalize_path)

    merged = pr_df.merge(risky_funcs, on="filepath", how="inner")

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


def is_pr_risky(pr_df, lizard_df, risk_threshold=10):
    """
    Returns True if any risky function (complexity > threshold) is touched by PR changes.
    """
    risky_files = {normalize_path(f) for f in lizard_df[lizard_df["complexity"] > risk_threshold]["filepath"].unique()}
    changed_files = {normalize_path(f) for f in pr_df["filepath"].unique()}

    return any(file in risky_files for file in changed_files)
