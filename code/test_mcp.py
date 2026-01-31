from mcp_client import MCPClient

mcp = MCPClient()

results = mcp.search_bug_manual(
    "RDI macro naming convention bug"
)

for i, r in enumerate(results):
    print(f"\nResult {i+1}")
    print("Text:", r["text"])
    print("Score:", r["score"])
