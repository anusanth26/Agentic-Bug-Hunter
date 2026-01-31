def detect_bug_line(code: str, mcp_results: list):
    """
    Detect buggy line using MCP-derived bug descriptions.

    Args:
        code (str): incorrect C/C++ code
        mcp_results (list): output from MCPClient.search_bug_manual

    Returns:
        (line_number, line_text)
    """

    lines = code.splitlines()

    # Step 1: extract meaningful keywords from MCP text
    keywords = set()
    for res in mcp_results:
        for word in res["text"].split():
            if len(word) > 3:   # avoid noise like 'the', 'and'
                keywords.add(word)

    # Step 2: scan code line-by-line for violations
    for idx, line in enumerate(lines):
        for key in keywords:
            if key in line:
                return idx + 1, line.strip()

    # Fallback (if nothing matched)
    return None, None
