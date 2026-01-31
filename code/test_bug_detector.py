from mcp_client import MCPClient
from bug_detector import detect_bug_line

sample_code = """
#define RDI_begin() something
void func() {
    RDI_begin();
}
"""

mcp = MCPClient()
mcp_results = mcp.search_bug_manual("RDI macro naming bug")

line_no, line_text = detect_bug_line(sample_code, mcp_results)

print(line_no, line_text)
