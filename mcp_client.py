import sys
import subprocess

prompt = sys.argv[1]

subprocess.run(
    ["python", "mcp_server.py", prompt],
    check=True
)