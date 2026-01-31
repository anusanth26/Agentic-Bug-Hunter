from mcp_client import MCPClient
from bug_detector import detect_bug_line
from explainer import generate_explanation

mcp = MCPClient()

def process_row(row):
    code = row["Code"]
    context = row.get("Context", "")

    # 1️⃣ Query MCP using context
    query = f"{context} common bug"
    mcp_results = mcp.search_bug_manual(query)

    # 2️⃣ Detect buggy line
    line_no, line_text = detect_bug_line(code, mcp_results)

    # 3️⃣ Generate explanation
    explanation = generate_explanation(line_text, context, mcp_results)

    return line_no, explanation
