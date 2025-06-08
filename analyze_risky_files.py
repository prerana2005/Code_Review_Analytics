import pandas as pd

def get_risky_functions(pr_df, lizard_df):
    key = 'filepath' if 'filepath' in pr_df.columns and 'filepath' in lizard_df.columns else 'filename'
    lizard_df = lizard_df.rename(columns={"CCN": "complexity"})

    # Merge based on file path or filename
    merged = pd.merge(pr_df, lizard_df, on=key, how='inner')

    # Filter only complex functions
    risky_funcs = merged[merged['complexity'] > 10]

    # Return only relevant columns
    return risky_funcs[[key, 'complexity', 'nloc']]
def is_pr_risky(pr_df, lizard_df):
    for _, change in pr_df.iterrows():
        file_path = change["filepath"]
        changed_line = change["start_line"]

        funcs_in_file = lizard_df[lizard_df["filepath"] == file_path]

        for _, func in funcs_in_file.iterrows():
            if func["CCN"] > 10:
                func_start = func["start_line"]
                func_end = func_start + func["length"] - 1
                if func_start <= changed_line <= func_end:
                    return True
    return False

if __name__ == "__main__":
    pr_files = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/pr_files.csv")
    lizard = pd.read_csv("C:/Users/Prerana/Desktop/Code_Review_Analytics/lizard_output_with_end_line.csv")

    risky_functions = get_risky_functions(pr_files, lizard)

    print("\nRisky functions touched in this PR:")
    print(risky_functions)

    risky_functions.to_csv("risky_files_in_pr.csv", index=False)

