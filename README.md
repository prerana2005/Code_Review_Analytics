#  Code Review Analytics

This project looks at how developers review code on GitHub. It uses **data** and **AI** to help make code reviews better, faster, and easier to learn from.

---
### Day 1
##  What is Code Analytics?

**Code analytics** means collecting and studying information from coding activities — like commits, pull requests, and reviews on GitHub. It helps us understand:

- How good the code is  
- How well and fast developers work  
- How code reviews happen  
- How teams collaborate  
- Where bugs or technical debt may exist  

---

##  Types of Code Analytics

###  Static Code Analytics  
Analyzes code **without running it**. Helps catch bugs, bad styles, or security risks early.  
**Examples:**  
- Code complexity  
- Duplicate code  
- Linting errors  
**Tools:** SonarQube, ESLint, Pylint, Checkstyle

---

###  Dynamic Code Analytics  
Analyzes code **while it runs**. Focuses on runtime performance and test behavior.  
**Examples:**  
- Test coverage  
- Memory usage  
- Crashes or runtime errors  
**Tools:** Codecov, Valgrind, Dynatrace

---

###  Code Review & Process Analytics *(Focus of This Project)*  
Analyzes how developers review code on GitHub to improve **review speed, quality**, and **team collaboration**.  
**Examples:**  
- Time to first review  
- PR merge time  
- Reviewer participation  
- Comment quality and density  
**Tools:** keyanalytics, GitHub API

---

##  Expanded View: Other Kinds of Code Analytics

As I explore more, I found professionals look at code from different angles:

###  Code Quality Analytics  
Measures how clean and well-written code is.  
E.g., deep nesting, code smells, style issues

###  Code Review Analytics  
Tracks how code is reviewed and discussed.  
E.g., review delays, number of reviewers, comments per PR

###  Code Contribution Analytics  
Shows how developers are contributing to the project.  
E.g., active contributors, most changed files

###  Test & Coverage Analytics  
Checks how well code is tested.  
E.g., % code covered by tests, flaky tests, failures

###  Security Analytics  
Finds risky code or outdated libraries.  
E.g., hardcoded credentials, vulnerable dependencies

---

##  Why Use Code Analytics?

- Detect bugs or issues early  
- Improve code review quality and speed  
- Highlight who’s actively reviewing  
- Find files that often break or change  
- Support team collaboration  
- Make the software development process smoother  
- Give managers clear insights and reports  

---

##  About This Project

In this project, we focus on **analyzing code reviews from GitHub repositories**.  
We aim to:

- Use existing tools to track key metrics (KPIs)  
- Write custom scripts to track KPIs not already covered  
- Try using **Generative AI** (like ChatGPT or other LLMs) to review PRs and suggest improvements
  
This project will help teams **review code more effectively**, reduce errors, and build better software, faster
---

## Project Architecture

Here’s a visual overview of how this project collects, analyzes, and presents code review data:

![Image](https://github.com/user-attachments/assets/4af313a1-f530-462f-aa2d-c8e1c97a7cea)

Reference - [KeyAnalytics GitHub](https://github.com/apoorvasj/keyanalytics)

---  
### Day 2
## Cyclomatic Complexity

Cyclomatic Complexity is a code metric that helps identify:

- Code that’s hard to understand or maintain.
- Paths that need to be tested (helps improve test coverage).
- Complexity in logic that could lead to bugs or tech debt.

We will use this metric to assess the quality of code in different repositories.
![Image](https://github.com/user-attachments/assets/7ec614eb-7b40-4dee-b909-fa4a828366f5)

## Tool: Lizard

Lizard is a tool that automates the calculation of cyclomatic complexity.

It shows:
- Number of lines in a function
- Cyclomatic complexity value
- Number of parameters
- Location of the function in the file

--- 

## Cyclomatic Complexity Analysis using Lizard

- Installed and used a static analysis tool: Lizard
- Cloned the open-source **Flask** GitHub repository.
- Analyzed the codebase using Lizard to calculate complexity.
- Saved:
  - `all_lizard_output.txt`: Full complexity report of the Flask repo.
  - `high_complexity_functions.txt`: Filtered report with only functions having **CCN > 10**.

## Understanding Cyclomatic Complexity Ranges

Cyclomatic Complexity Number (CCN) indicates how complex a function or method is. Here’s a simple guide to interpret CCN values:
- 1-10: Simple procedure, little risk  
- 11-20: More complex, moderate risk  
- 21-50: Complex, high risk  
- Greater than 50: Untestable, very high risk 

--- 
### Day 3
## CSV Files Generated

### 1. `output.csv`

This file contains the full analysis of code functions with the following columns:

- `nloc` : Number of lines of code in the function  
- `CCN` : Cyclomatic Complexity Number  
- `token_count` : Number of tokens in the function  
- `parameter_count` : Number of parameters of the function  
- `length` : Length of the function in lines  
- `location` : Location of the function in the file  
- `filename` : Name of the file containing the function  
- `filepath` : Path to the file  
- `function_name` : Name of the function  
- `signature` : Full function signature  
- `start_line` : Line number where the function starts  
- `end_line` : Line number where the function ends (calculated as `start_line + length - 1`)

---

### 2. `output_ccn_gt_10.csv`

This file is a filtered subset of the above file and contains only functions with cyclomatic complexity (`CCN`) greater than 10. It has the same columns as `output_with_end_line.csv`.

The end_line calculation is performed by the Jupyter notebook calculate_end_line.ipynb
---

### Day 4 

- Creating and switching Git branches  
- Editing files and tracking changes  
- Staging updates and committing them to Git  
- Creating pull requests on GitHub  
- Merging pull requests
---

### Day 5

## Pull Request File Analysis
- Created a dummy Python file (`dummy_test.py`) in a new branch and raised a pull request to `main`.
- Generated a GitHub Personal Access Token with read-only permissions for repo contents and pull requests.
- Wrote a Python script `get_pr_files.py` to fetch and print the list of files changed in the pull request using the GitHub API.
- Updated this script to securely read the GitHub token from an environment variable instead of hardcoding it.

### To run `get_pr_files.py`

### Set your GitHub token as an environment variable

For Git Bash (Windows) or Linux/macOS terminal:

```bash
export GITHUB_TOKEN=your_token_here
```

### What the script does:

- Connects to GitHub API using the token.  
- Fetches the list of files changed in the specified pull request.  
- Prints the changed filenames.
---
### Day 6

#### 1. risky_test_files/
- Contains Python files that exhibit high complexity.
- These files simulate code that might be flagged as risky during pull request reviews.

#### 2. lizard_output_with_end_line.csv
- CSV file containing static code analysis results generated using Lizard.
- Includes metrics such as:
  - `nloc` (number of lines of code)
  - `CCN` (cyclomatic complexity)
  - `token_count`, `parameter_count`, and `length`
  - `start_line` and computed `end_line` (as `start_line + length - 1`)
    (end_line calculation is performed by calculate_end_line.ipynb)
- Used to identify complex or risky functions.

#### 3. get_pr_files.py
- Python script that uses the GitHub API to fetch details about files changed in a pull request.
- Extracts and saves:
  - File names
  - Additions
  - Deletions
  - Status (e.g., modified, added)
- Output is stored in `pr_files.csv`.

#### 4. pr_files.csv
- Contains metadata about each file that was part of a pull request.
- Generated by `get_pr_files.py`.

#### 5. analyze_risky_files.py
- Main analysis script.
- Loads both `pr_files.csv` and `lizard_output_with_end_line.csv`.
- Merges the two datasets based on file name or path.
- Filters functions where `CCN > 10`, indicating high complexity.
- Produces a new CSV: `risky_files_in_pr.csv`.

#### 6. risky_files_in_pr.csv
- Final result showing only those functions from the PR that are considered risky.
- Helps reviewers focus on potentially problematic code segments during review.

---
### Day 7

#### Test Case for False Positive Risk Detection in PR Analysis

**Objective:**  
To simulate and catch a bug in the risk classification logic where a file containing  
both complex and simple functions is always flagged as 'risky' even if the pull request  
only modifies a simple function.

**What was done:**  
- Created a failing unit test in `tests/test_false_positive.py` using `unittest`  
- Simulated input CSVs:  
    • `tests/mock_lizard_output.csv`: Contains metadata for multiple functions in a file (some complex, some simple)  
    • `tests/mock_pr_files.csv`: Simulates a pull request modifying only the simple function  
- Wrote a test to check if such a PR is wrongly marked as risky  
- Let the test fail intentionally, as the bug still exists

**Key Outcome:**  
This test fails as expected, showing that the current implementation doesn't check  
*which specific function* is edited. It wrongly flags a PR as risky just because  
a complex function exists in the file.

---

### Day 8 - Updates to False Positive Detection and Risk Analysis

**Objective:**  
Improve the risk detection logic to avoid false positives when PRs modify only simple functions,
even if complex functions exist in the same file.

**What was done:** 
- Updated `tests/test_false_positive.py`:
    - Added a proper unit test using mock CSVs.
    - Introduced function `is_pr_risky()` to check if changed lines fall inside complex functions.
    - Test confirms PR is NOT flagged risky if only simple functions are changed.

- Refactored `analyze_risky_files.py`:
    - Simplified logic to **file-level granularity** (since real PRs don't include line numbers).
    - Improved merge logic between PR files and Lizard complexity data.
    - Added clear complexity filtering to identify risky functions.
    - Modularized with function `get_risky_functions()` for easier testing and reuse.

---
### Day 9
### Updates 

- Moved the `is_pr_risky()` function to `analyze_risky_files.py` for better modularity and reuse.

- Updated the unit test (`tests/test_false_positive.py`) to import and use the real `is_pr_risky()` function instead of redefining it.

---
### Day 10

## Added test_get_risky_functions.py

### Purpose
- Added a new test file to check how the `get_risky_functions()` function works in `analyze_risky_files.py`.
- Makes sure the function finds risky functions based on their complexity and changes in the pull request.

---
### Day 11

Ensured the test correctly validates that modifying only a simple function does **not** mark the PR as risky.  

- **Prepared mock data**:
  - File contains **both a simple and a complex function**.
  - PR modifies **only the simple function**.  
- **Confirmed expected behavior**:  
  - The test runs with mock data.  
  - `is_pr_risky(...)` returns **`False`**, confirming that modifying only a simple function does **not** make the PR risky.  

---
### Day 12 

### Goal- Line-Level Risk Detection (Avoiding False Positives)

Improve the accuracy of risky PR detection by checking if the changed lines actually touch complex functions (`CCN > 10`) instead of just matching filenames.

- **Modified `analyze_risky_files.py`**:
  - Enhanced logic to ensure a PR is only marked "risky" if the **specific changed lines** fall inside functions with high cyclomatic complexity.
  - Avoids false positives caused by only matching filenames.

-  **Added `get_pr_changed_lines.py`**:
  - Parses PR diffs to extract all line-level changes.
  - Outputs `pr_lines.csv` with columns:
    - `filepath`
    - `start_line` (line number of each change in the PR)
- Used `lizard_output_with_end_line.csv` which includes:
  - Function name, file, `start_line`, and calculated `end_line` for accurate range checking.
- Validated the logic with test PRs that modify only safe functions — correctly detected as "Safe PR".
  
---
### Day 13

###  Enhanced `is_pr_risky()` logic:

- Previously only checked if `start_line` of PR change fell inside a risky function.
- Now supports three complete overlap cases:
  -  Change starts **inside** risky function
  -  Change starts **before** but ends **inside** risky function
  -  Change **completely surrounds** risky function

###  Modified input format in `pr_lines.csv`:

- Now includes both `start_line` and `end_line` for each changed chunk to enable better range detection.

###  Updated `analyze_risky_files.py`:

- Now compares PR line ranges with function ranges for complete overlap detection using:
  ```python
  if not (change_end < func_start or change_start > func_end):
      return True

### Testing

Created `tests/test_overlap_cases.py`:

- Uses `pandas.DataFrame` to simulate:
  - Risky function spans from lizard output
  - Pull request change ranges with different overlap conditions
- Covers and verifies all critical overlap scenarios

---
### Day 14

**1. Replaced Outdated Mock Test Files**

- Removed:
  - `tests/mock_pr_files.csv`
  - `tests/mock_lizard_output.csv`

- Added:
  - `tests/mock_pr_lines.csv`  
    → Format: `filepath, start_line, end_line`
  - `tests/mock_lizard_output_with_end_line.csv`  
    → Format: `function_name, start_line, end_line, CCN, filepath`

**2. Updated Test Scripts to Match New File Format**

- `test_get_risky_functions.py`
  - Ensures risky functions (CCN > 10) are filtered from PR-touched files
  - Uses new mock data format

- `test_false_positive.py`
  - Verifies that overlap detection behaves correctly using start/end line logic
  - Uses the updated `mock_pr_lines.csv` and `mock_lizard_output_with_end_line.csv`

---
### Day 15
**3. Removed Unused Scripts and Old Test Data**

- Deleted:
  - `get_pr_files.py` (no longer needed)
  - Its generated output file

**4. Updated Input Format**

- Replaced `lizard_output_with_end_line.csv` with a new version that includes:
  - `function_name, start_line, end_line, CCN, filepath`

**5. Modified Main Script to Match Updated Format**

- Updated `analyze_risky_files.py` to:
  - Read and process the new `lizard_output_with_end_line.csv` structure correctly

---
### Day 16

###  Code Quality & Pylint Improvements

To ensure professional and maintainable code, the entire codebase was refactored and improved using **pylint**, achieving a **10/10 score** across all Python files.

###  Improvements Made

-  **Added** module, class, and function docstrings
-  **Standardized** import ordering
-  **Resolved** all pylint warnings (e.g., variable naming, use of `sys.exit`)
-  **Wrapped** long lines to follow PEP8 (≤100 characters)
-  **Removed** trailing whitespace and ensured consistent formatting
-  **Removed** unused imports and variables
-  **Fixed** relative imports in test modules
-  **Cleaned and documented** all test files
-  **Specified** UTF-8 encoding in file read/write operations

These changes improve code readability, maintainability, and readiness for collaboration or scaling.

---
### Day 17

###  `get_pr_changed_lines.py`

To ensure the code is **cleaner**, **modular**, and **Pylint-compliant**, the logic was split into two focused helper functions:
-  One for **parsing patch lines** from the GitHub PR.
-  One for **writing grouped changed line blocks** to a CSV.

###  `analyze_risky_files.py`  – Using pandas vectorized logic

- The logic is fully vectorized using pandas; no `iterrows()` or row-wise loops are used.
- PR and function data are joined using `merge()` on the `filepath` column.
- Overlap between PR lines and function lines is detected using direct column comparisons.
- This ensures efficient and scalable processing for large PR datasets.

---
### Day 18

## Refactored `get_pr_changed_lines.py`

- Replaced row-wise iteration with **column-wise vectorized operations** using pandas.
- Improved performance and code clarity when grouping contiguous changed lines in a PR.

### Column Operations Used

| Operation      | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| `.diff()`       | Detects breaks in line continuity by computing differences between rows. |
| `.shift()`      | Compares each file row with the previous one to detect file changes.     |
| `.cumsum()`     | Generates unique group IDs by cumulatively summing boolean change markers. |
| `.groupby()`    | Groups rows by `filepath` and `group_id` to collect blocks of changes.   |
| `.agg()`        | Aggregates grouped blocks to compute `start_line` and `end_line`.         |

## Edge Case Handling

- Skipped files with missing or empty `patch` data from the GitHub API.
- CSV output (`pr_lines.csv`) is only written if valid changed lines exist.

---
### Day 19

## GitHub Actions Integration

Integrating **GitHub Actions** into the project to automate **pull request (PR) risk analysis**
The goal is to allow the system to automatically evaluate a PR and output whether it is **risky** or **safe**, based on the complexity and overlap of the changed lines.

All GitHub Actions workflow setup was done in a separate working branch:  
**Branch**: `pr-risk-check-test`

###  Implemented GitHub Action Workflow
-  Created `.github/workflows/pr_risk_check.yml`
-  This workflow:
  - Runs when a PR is opened or updated
  - Uses `run_analysis.py` to check the PR for risk
  - Prints whether the PR is risky or not

###  GitHub Actions Output Screenshot

Below is an example output from the GitHub Actions workflow that runs on every pull request:

![Image](https://github.com/user-attachments/assets/82d369b8-f9e5-4728-b21e-9ca8f3c714fc)

### 📝 Screenshot Explanation
- **Line 1**: The GitHub Action runs the command `python run_analysis.py --pr 2`
- **Lines 14-23**: It lists the changed files in PR #2
- **Line 25**: It indicates the output CSV was saved (`pr_lines.csv`)
- **Line 26**: The result: `Risky PR: It modifies complex code.`

This confirms the automation is correctly analyzing pull requests and surfacing potential risks for reviewers.

---
### Day 20

### 1. Made Inputs Dynamic

The GitHub Action runs a Python script (`run_analysis.py`) using dynamic inputs:

- `--repo_owner`
- `--repo_name`
- `--pr_number`

These values are passed using GitHub's context variables:

```yaml
--repo_owner: ${{ github.repository_owner }}
--repo_name: ${{ github.event.repository.name }}
--pr_number: ${{ github.event.pull_request.number }}
```

### 2. Created a Separate Repo: `analytics_user`

A new repository named `analytics_user` created to simulate real-world usage.

It includes:

- `dummy.py`: A simple Python file to test changes.
- `.github/workflows/risk_check.yml`: A GitHub Action that triggers on PR events.

### 3. GitHub Action Trigger

The risk analysis runs automatically when a pull request is opened or updated:

```yaml
on:
  pull_request:
    types: [opened, synchronize]
```

---
### Day 21

### 1. Refactored Code into a Package

- Created a new folder `pr_risk_checker/` inside the `Code_Review_Analytics` repo.
- Moved the logic from `run_analysis.py` into `pr_risk_checker/__init__.py`.
- Converted the script into a reusable function:

```python
def run_main_logic(repo_owner, repo_name, pr_number):
```

### 2. Built a CLI Interface

- Created `cli.py` inside the `pr_risk_checker/` package.
- Used `argparse` to wrap the logic and allow it to be executed from the terminal.
- Run command looks like:

```bash
python -m pr_risk_checker.cli --repo_owner <user> --repo_name <repo> --pr_number <pr>
```

### 3. Integrated with GitHub Actions

- Updated the `analytics_user` repository’s workflow file (`.github/workflows/risk_check.yml`).
- The workflow now automatically runs the CLI tool during pull requests, passing the PR metadata.

---
### GitHub Actions Workflow: Pull Request Risk Analysis

The workflow is triggered when a Pull Request is opened or updated in the `analytics-user` repository.

### Step-by-Step Execution Flow

#### 1. Set Up Job

- GitHub prepares the runner environment.
- Loads `GITHUB_TOKEN` and other secrets.
- Prepares workflow and downloads required actions.

#### 2. Checkout Repositories

The following repositories are checked out during execution:

- `analytics-user`: The target repository where the PR is raised.
- `Code_Review_Analytics`: Contains the reusable composite action that performs the risk analysis.

#### 3. Set Up Python Environment

- Python is installed using `actions/setup-python@v4`.
- This prepares the Python runtime required for analysis scripts.

#### 4. Install Required Dependencies

- All Python dependencies are installed from `Code_Review_Analytics/requirements.txt`:
  - `pandas`
  - `requests`

#### 5. Execute PR Risk Checker

The composite action runs the following command:

```bash
python -m pr_risk_checker.cli
```

### Inside `cli.py`

The `cli.py` module is the entry point for the PR Risk Checker logic. It performs the following key steps:


#### 1. Extract PR Context

- Retrieves metadata such as:
  - PR number
  - List of changed files
  - GitHub repository information

#### 2. Detect Changed Lines

- Parses the file diffs from the PR.
- Identifies and extracts blocks of changed lines.
- Saves the output to:
  - `pr_lines.csv`

#### 3. Run Complexity Analysis

- Uses the `lizard` library to compute:
  - Cyclomatic complexity
  - Function sizes
- Scans the entire codebase or changed files.
- Saves the output to:
  - `lizard_output_with_end_line.csv`

#### 4. Match Complexity with Changes

- Matches changed lines with complex code regions.
- Determines if any risky sections were modified.
- If so, flags the PR as risky.

#### 5. Log Result

- Logs the final result in GitHub Actions console:
  - If risky:
    ```
    Risky PR: It modifies complex code.
    ```
  - If safe:
    ```
    Safe PR: No risky changes detected.
    ```
---
### Optimization Summary

### `pr_risk_checker/__init__.py`
- Replaced subprocess-based invocation of `get_pr_changed_lines.py` with a direct function call to `extract_pr_changed_line_blocks`.
- Integrated Lizard and PR line data in-memory without intermediate CSVs.
- Ensured consistent use of DataFrames passed between logic layers.

### `pr_risk_checker/get_pr_changed_lines.py`
- No CSV files used — returns a DataFrame of `filepath`, `start_line`, and `end_line`.

### `pr_risk_checker/generate_lizard_csv.py`
- Renamed and repurposed to return a DataFrame instead of writing CSV output.
- Clean `analyze_codebase()` function now analyzes complexity using `lizard` and returns structured metrics in memory.

### `pr_risk_checker/analyze_risky_files.py`
- Updated to operate fully on in-memory pandas DataFrames.
- Implements efficient file-path normalization and overlap detection.
- Contains core risk analysis logic (`is_pr_risky` and `get_risky_functions`).

### `pr_risk_checker/cli.py`
-Directly invokes streamlined logic without subprocesses or file I/O.

### Removed/Avoided

-  Subprocess spawning (` get_pr_changed_lines.py`)  
-  Writing and reading temporary CSVs  
-  Redundant GitHub API calls (e.g., re-fetching changed files) 
