import pandas as pd

# Load the files
pr_files = pd.read_csv('C:/Users/Prerana/Desktop/Code_Review_Analytics/pr_files.csv')
lizard = pd.read_csv('C:/Users/Prerana/Desktop/Code_Review_Analytics/lizard_output_with_end_line.csv')

# Show available columns
print("PR files columns:", pr_files.columns)
print("Lizard columns:", lizard.columns)

# Decide on merge key
key = 'filepath' if 'filepath' in pr_files.columns and 'filepath' in lizard.columns else 'filename'

# Rename CCN to complexity for easier understanding
lizard.rename(columns={"CCN": "complexity"}, inplace=True)

# Merge PR and lizard data
merged = pd.merge(pr_files, lizard, on=key, how='inner')

# Filter for risky files
risky = merged[merged['complexity'] > 10]

# Print risky files
print("\nRisky files in your PR:")
print(risky[[key, 'complexity', 'nloc']])

# Save to CSV
risky.to_csv('risky_files_in_pr.csv', index=False)
