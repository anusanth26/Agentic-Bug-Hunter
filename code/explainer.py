def generate_explanation(bug_line, context, mcp_results):
    explanation = f"The bug occurs at the line `{bug_line}`. "

    if context:
        explanation += f"This code relates to {context}. "

    if mcp_results:
        explanation += (
            "According to the known bug manual retrieved via MCP, "
            + mcp_results[0]["text"]
        )

    return explanation
