import pandas as pd
from orchestrator import process_row

df = pd.read_csv("../samples.csv")

results = []

for _, row in df.iterrows():
    bug_line, explanation = process_row(row)

    results.append({
        "Code ID": row["ID"],
        "Detected Bug Line": bug_line,
        "Generated Explanation": explanation
    })

out_df = pd.DataFrame(results)
out_df.to_csv("../output.csv", index=False)

print("output.csv generated successfully")
