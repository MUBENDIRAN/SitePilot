from mcp.server.fastmcp import FastMCP
import subprocess
import requests
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

mcp = FastMCP("website-tools")

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


@mcp.tool()
def update_static_site(file: str, content: str):
    """Update a static website file and push changes to GitHub"""

    path = SITE_DIR / file

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    # Git operations
    subprocess.run(["git", "add", str(path)], check=False)
    subprocess.run(["git", "commit", "-m", "AI update"], check=False)
    subprocess.run(["git", "push"], check=False)

    return f"Website updated: {file}"


@mcp.tool()
def notify_friend(message: str):
    """Send notification to friend via Telegram"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        },
    )

    return "Message sent"


if __name__ == "__main__":
    mcp.run()