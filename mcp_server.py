from mcp.server.fastmcp import FastMCP
import subprocess
import ollama
import requests
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("website-tools")

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"
REPO_DIR = BASE_DIR

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("TELEGRAM_NOTIFY_IDS", "").split(",")


def run_git(cmd):
    subprocess.run(
        cmd,
        cwd=REPO_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


def deploy(path):

    run_git(["git", "add", str(path)])

    try:
        run_git(["git", "commit", "-m", "AI website update"])
    except:
        pass

    run_git(["git", "push"])


def notify(message):

    if not TOKEN:
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for chat in CHAT_IDS:
        try:
            requests.post(
                url,
                json={
                    "chat_id": chat,
                    "text": message
                },
                timeout=5
            )
        except:
            pass


def generate_page(prompt):

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": """
You generate static webpages.

Follow the user's instructions exactly.

If they request:
- HTML only → produce pure HTML
- CSS styling → include <style>
- JavaScript → include <script>

Return ONLY valid webpage code.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


@mcp.tool()
def update_homepage(prompt: str):

    html = generate_page(prompt)

    path = SITE_DIR / "index.html"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    deploy(path)

    notify("🚀 Website updated successfully")

    return "Website updated"


if __name__ == "__main__":

    prompt = sys.argv[1] if len(sys.argv) > 1 else None

    if prompt:
        update_homepage(prompt)
    else:
        print("MCP server running", file=sys.stderr)
        mcp.run()