import lizard
import pandas as pd

def analyze_codebase(code_dirs, output_csv):
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
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(" Lizard output written to {output_csv}")
