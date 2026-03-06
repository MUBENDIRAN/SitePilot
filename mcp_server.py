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


def get_project_structure():

    structure = []

    for root, dirs, files in os.walk(SITE_DIR):
        for f in files:
            structure.append(os.path.relpath(os.path.join(root, f), SITE_DIR))

    return "\n".join(structure)


def generate_files(prompt):

    structure = get_project_structure()

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": f"""
You maintain a static website.

Current project files:

{structure}

You may:
- modify existing files
- create new pages
- update CSS
- add JavaScript

Return updates in this format:

FILE: filename
code

Example:

FILE: index.html
<html>...</html>

FILE: styles.css
body {{...}}
"""
            },
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


def parse_files(ai_output):

    files = {}

    current = None
    buffer = []

    for line in ai_output.splitlines():

        if line.startswith("FILE:"):
            if current:
                files[current] = "\n".join(buffer)

            current = line.replace("FILE:", "").strip()
            buffer = []

        else:
            buffer.append(line)

    if current:
        files[current] = "\n".join(buffer)

    return files


def write_files(files):

    for name, content in files.items():

        path = SITE_DIR / name

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def main():

    if len(sys.argv) < 2:
        print("Prompt required")
        return

    prompt = sys.argv[1]

    ai_output = generate_files(prompt)

    files = parse_files(ai_output)

    write_files(files)

    deploy()

    notify("🚀 SitePilot deployed website update")


if __name__ == "__main__":
    main()