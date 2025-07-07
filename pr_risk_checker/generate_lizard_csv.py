"""
Analyze code complexity using Lizard and return a structured DataFrame.
"""
import lizard
import pandas as pd

def analyze_codebase(code_dirs, output_format="df"):
    """
    Analyzes code complexity using Lizard and returns a DataFrame.

    Args:
        code_dirs (list[str]): List of paths to analyze (e.g., ['.'])
        output_format (str): 'df' returns a DataFrame

    Returns:
        pd.DataFrame: DataFrame with function-level complexity
    """
    data = []
    for result in lizard.analyze(code_dirs):
        for function in result.function_list:
            data.append({
                "filepath": result.filename,
                "function_name": function.name,
                "start_line": function.start_line,
                "end_line": function.end_line,
                "CCN": function.cyclomatic_complexity,
            })

    df = pd.DataFrame(data)

    if output_format == "df":
        return df
    raise ValueError(f"Unsupported output format: {output_format}")
