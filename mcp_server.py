from mcp.server.fastmcp import FastMCP
import subprocess
import requests
from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import ollama

load_dotenv()

mcp = FastMCP("website-tools")

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"
REPO_DIR = BASE_DIR

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "")


def log(msg):
    """Log only to stderr (never stdout in MCP servers)."""
    print(msg, file=sys.stderr)


def run_git(cmd):
    """Run git command safely."""
    try:
        subprocess.run(
            cmd,
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        log(f"Git error: {e.stderr}")
        raise


def send_notification(message):
    """Send Telegram message to multiple recipients."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_IDS:
        log("Telegram configuration missing")
        return

    chat_ids = [c.strip() for c in TELEGRAM_CHAT_IDS.split(",") if c.strip()]

    for chat_id in chat_ids:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": message
                },
                timeout=5
            )
        except Exception as e:
            log(f"Telegram send failed for {chat_id}: {e}")


def deploy(path):
    """Commit and push changes."""
    try:
        run_git(["git", "add", str(path)])

        try:
            run_git(["git", "commit", "-m", "AI website update"])
        except:
            log("Nothing new to commit")

        run_git(["git", "push"])

        send_notification("🚀 Website updated and deployed successfully")

    except Exception as e:
        log(f"Deployment failed: {e}")
        raise


def generate_html(prompt):
    """Use local LLM to generate HTML."""
    try:
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a clean simple HTML homepage. Return only valid HTML."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        log(f"Ollama generation failed: {e}")
        raise


@mcp.tool()
def update_homepage_from_prompt(prompt: str):
    """
    Generate HTML from a natural-language prompt,
    update index.html, push to GitHub, and notify Telegram users.
    """

    try:
        html = generate_html(prompt)

        path = SITE_DIR / "index.html"

        if not SITE_DIR.exists():
            return "Site directory not found"

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        deploy(path)

        return "Homepage updated from prompt and deployed."

    except Exception as e:
        log(e)
        return f"Update failed: {str(e)}"


if __name__ == "__main__":
    log("Starting MCP server")
    mcp.run()