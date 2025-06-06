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
    • Added a proper unit test using mock CSVs.
    • Introduced function `is_pr_risky()` to check if changed lines fall inside complex functions.
    • Test confirms PR is NOT flagged risky if only simple functions are changed.

- Refactored `analyze_risky_files.py`:
    • Improved merge logic between PR files and Lizard complexity data.
    • Added clear complexity filtering to identify risky functions.
    • Modularized with function `get_risky_functions()` for easier testing and reuse.
