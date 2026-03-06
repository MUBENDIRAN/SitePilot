import os
import sys
import subprocess
import requests
import ollama
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("TELEGRAM_NOTIFY_IDS", "").split(",")


# ---------------- GIT ----------------

def run_git(cmd):
    subprocess.run(
        cmd,
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )


def deploy():
    run_git(["git", "add", "."])
    run_git(["git", "commit", "-m", "AI website update"])
    run_git(["git", "push"])


# ---------------- TELEGRAM ----------------

def notify(message):

    if not TOKEN:
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for chat in CHAT_IDS:
        try:
            requests.post(
                url,
                json={"chat_id": chat, "text": message},
                timeout=5
            )
        except:
            pass


# ---------------- FILESYSTEM ----------------

def read_file(filename):

    path = SITE_DIR / filename

    if not path.exists():
        return "FILE NOT FOUND"

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(name, content):

    path = SITE_DIR / name

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def delete_file(name):

    path = SITE_DIR / name

    if path.exists():
        os.remove(path)


def list_files():

    files = []

    for root, dirs, filenames in os.walk(SITE_DIR):
        for f in filenames:
            files.append(
                os.path.relpath(os.path.join(root, f), SITE_DIR)
            )

    return files


# ---------------- AI AGENT ----------------

SYSTEM_PROMPT = """
You are an AI developer maintaining a website.

You can perform actions:

READ: filename
FILE: filename
<content>

DELETE: filename

Rules:
- Think step by step.
- If you need to see a file before editing it, use READ.
- When ready to modify or create files use FILE.
- When removing files use DELETE.
- Never use markdown.
- Never explain.
- Only output commands.

Example:

READ: index.html

FILE: index.html
<html>Hello</html>

DELETE: old.html
"""


def ask_ai(messages):

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=messages
    )

    return response["message"]["content"]


# ---------------- AGENT LOOP ----------------

def run_agent(prompt):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    for _ in range(10):  # max reasoning steps

        ai_output = ask_ai(messages)

        print("\nAI:", ai_output)

        messages.append({"role": "assistant", "content": ai_output})

        lines = ai_output.splitlines()

        # READ operation
        if lines[0].startswith("READ:"):

            filename = lines[0].replace("READ:", "").strip()

            content = read_file(filename)

            messages.append({
                "role": "user",
                "content": f"CONTENT OF {filename}:\n{content}"
            })

            continue

        # DELETE operation
        if lines[0].startswith("DELETE:"):

            filename = lines[0].replace("DELETE:", "").strip()

            delete_file(filename)

            continue

        # FILE write
        if lines[0].startswith("FILE:"):

            filename = lines[0].replace("FILE:", "").strip()

            content = "\n".join(lines[1:])

            write_file(filename, content)

            continue

        # stop if no commands
        break


# ---------------- MAIN ----------------

def main():

    if len(sys.argv) < 2:
        print("Prompt required")
        return

    prompt = sys.argv[1]

    print("\nUSER:", prompt)

    run_agent(prompt)

    deploy()

    notify("🚀 SitePilot deployed updated website")


if __name__ == "__main__":
    main()