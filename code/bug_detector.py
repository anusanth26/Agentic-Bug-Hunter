import re

def detect_bug_line(code: str, mcp_results: list):
    """
    Detect buggy line using MCP-derived bug descriptions.
    
    Improved strategy:
    - Extract meaningful patterns: ALL_CAPS macros, snake_case identifiers, function tokens
    - Ignore generic English words
    - Score each line by counting pattern matches
    - Return the highest-scoring line (most rule violations)

    Args:
        code (str): incorrect C/C++ code
        mcp_results (list): output from MCPClient.search_bug_manual

    Returns:
        (line_number, line_text)
    """

    lines = code.splitlines()
    
    if not lines or not mcp_results:
        return None, None

    # Step 1: Extract meaningful patterns from MCP text
    # Prioritize: ALL_CAPS macros, snake_case identifiers, function-like tokens
    patterns = set()
    common_words = {
        'the', 'and', 'or', 'for', 'with', 'this', 'that', 'from', 'to', 'a', 'an',
        'be', 'is', 'are', 'was', 'were', 'will', 'would', 'should', 'could', 'may',
        'can', 'do', 'does', 'did', 'have', 'has', 'had', 'in', 'on', 'at', 'by'
    }
    
    for res in mcp_results:
        text = res.get("text", "")
        words = text.split()
        
        for word in words:
            # Clean punctuation
            clean = re.sub(r'[^
^\w_]', '', word)
            
            # Skip short words and common English words
            if len(clean) <= 2 or clean.lower() in common_words:
                continue
            
            # Prefer ALL_CAPS identifiers (macros/constants)
            if re.match(r'^[A-Z_][A-Z0-9_]*$', clean) and '_' in clean:
                patterns.add(clean)
            
            # Prefer snake_case identifiers (variables/functions)
            elif re.match(r'^[a-z_][a-z0-9_]*$', clean) and '_' in clean:
                patterns.add(clean)
            
            # Include function-like patterns (from original word with parentheses)
            elif '()' in word:
                func_name = word.replace('()', '').replace('(', '').replace(')', '')
                if len(func_name) > 2:
                    patterns.add(func_name)

    if not patterns:
        return None, None

    # Step 2: Score each line based on pattern matches
    best_line = None
    best_score = 0
    best_idx = -1
    
    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        
        # Count how many patterns appear in this line
        score = 0
        for pattern in patterns:
            # Word boundary matching to avoid false positives
            if re.search(r'\b' + re.escape(pattern) + r'\b', line):
                score += 1
        
        # Keep track of highest-scoring line
        if score > best_score:
            best_score = score
            best_line = line.strip()
            best_idx = idx + 1
    
    if best_score > 0:
        return best_idx, best_line
    
    # Fallback (if nothing matched)
    return None, None