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

###  `get_pr_changed_lines.py`

To ensure the code is **cleaner**, **modular**, and **Pylint-compliant**, the logic was split into two focused helper functions:
-  One for **parsing patch lines** from the GitHub PR.
-  One for **writing grouped changed line blocks** to a CSV.

###  `analyze_risky_files.py`  – Using pandas vectorized logic

- The logic is fully vectorized using pandas; no `iterrows()` or row-wise loops are used.
- PR and function data are joined using `merge()` on the `filepath` column.
- Overlap between PR lines and function lines is detected using direct column comparisons.
- This ensures efficient and scalable processing for large PR datasets.
