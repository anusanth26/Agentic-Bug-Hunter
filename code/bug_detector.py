import re

class BugDetector:
    def __init__(self, code):
        self.code = code
        self.risk_scores = {}

    def extract_patterns(self):
        # Regular expressions for ALL_CAPS macros and snake_case identifiers
        macro_pattern = r'\b[A-Z_]+\b'
        identifier_pattern = r'\b[a-z_]+\b'

        # Splitting the code into lines for analysis
        lines = self.code.split('\n')
        for line in lines:
            macro_matches = re.findall(macro_pattern, line)
            identifier_matches = re.findall(identifier_pattern, line)
            total_patterns = len(macro_matches) + len(identifier_matches)

            # Scoring logic based on pattern violation count
            self.risk_scores[line] = total_patterns

    def get_highest_risk_line(self):
        # Extract patterns first to populate risk scores
        self.extract_patterns()
        # Return the line with the highest risk score
        if self.risk_scores:
            return max(self.risk_scores, key=self.risk_scores.get)
        return None

# Example usage:
# detector = BugDetector(code_string)
# highest_risk = detector.get_highest_risk_line()