from mcp.server.fastmcp import FastMCP
import subprocess
import requests
from pathlib import Path

mcp = FastMCP("website-tools")


BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"

@mcp.tool()
def update_static_site(file: str, content: str):
    """Update a static website file"""

    path = SITE_DIR / file

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    subprocess.run(["git", "add", str(path)])
    subprocess.run(["git", "commit", "-m", "AI update"])
    subprocess.run(["git", "push"])

    return f"Website updated: {file}"


@mcp.tool()
def notify_friend(message: str):
    """Send notification to friend"""

    TOKEN="8797947540:AAEGYahY22bvXxKinMWudbHXuke_wp3qCPI"
    CHAT_ID="1902713619"

    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url,json={
        "chat_id":CHAT_ID,
        "text":message
    })

    return "Message sent"


if __name__ == "__main__":
    mcp.run()