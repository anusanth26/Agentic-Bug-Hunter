def generate_explanation(bug_line, context, mcp_results):
    """
    Generate a concise explanation of the detected bug.
    
    Strategy:
    - Keep explanation SHORT (2–3 sentences max)
    - Always explain WHAT is wrong and WHY it violates a known rule
    - Use MCP rule text as authority
    - Avoid verbosity and filler
    """
    
    if not bug_line or not mcp_results:
        return "Unable to generate explanation."
    
    # Extract the core rule from the top MCP result
    rule_text = mcp_results[0].get("text", "").strip()
    
    # Truncate rule if too long (keep only first 2 sentences)
    sentences = rule_text.split('. ')
    if len(sentences) > 2:
        rule_summary = '. '.join(sentences[:2]) + '. '
    else:
        rule_summary = rule_text
    
    # Build concise explanation: what + why
    explanation = f"Line `{{bug_line}}` violates the rule: {{rule_summary}}"
    
    return explanation