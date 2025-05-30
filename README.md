#  Code Review Analytics

This project looks at how developers review code on GitHub. It uses **data** and **AI** to help make code reviews better, faster, and easier to learn from.

---
### Day 0
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
### Day 1
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
### Day 2
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

---

