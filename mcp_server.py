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


# ---------------- PROJECT STRUCTURE ----------------

def get_project_structure():

    structure = []

    for root, dirs, files in os.walk(SITE_DIR):
        for f in files:
            structure.append(
                os.path.relpath(os.path.join(root, f), SITE_DIR)
            )

    return "\n".join(structure)


# ---------------- AI GENERATION ----------------

def generate_actions(prompt):

    structure = get_project_structure()

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "system",
                "content": f"""
You are an AI web developer maintaining a Dynamic website.

Current project files:

{structure}

You can perform operations:

CREATE / UPDATE file:

FILE: filename
code

DELETE file:

DELETE: filename

Rules:
- Only output FILE or DELETE instructions
- No explanations
- No markdown
- Follow exact format

Example:

DELETE: oldpage.html

FILE: index.html
<html>...</html>

FILE: styles.css
body {{ background:black; }}
"""
            },
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


# ---------------- PARSER ----------------

def parse_actions(ai_output) -> tuple[dict[Unknown, Unknown], list[Unknown]]:

    files = {}
    deletes = []

    current = None
    buffer = []

    for line in ai_output.splitlines():

        if line.startswith("DELETE:"):

            deletes.append(
                line.replace("DELETE:", "").strip()
            )

        elif line.startswith("FILE:"):

            if current:
                files[current] = "\n".join(buffer)

            current = line.replace("FILE:", "").strip()
            buffer = []

        else:
            buffer.append(line)

    if current:
        files[current] = "\n".join(buffer)

    return files, deletes


# ---------------- FILE OPERATIONS ----------------

def write_files(files):

    for name, content in files.items():

        path = SITE_DIR / name

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def delete_files(deletes):

    for name in deletes:

        path = SITE_DIR / name

        if path.exists():
            os.remove(path)


# ---------------- MAIN ----------------

def main():

    if len(sys.argv) < 2:
        print("Prompt required")
        return

    prompt: str = sys.argv[1]

    ai_output: str = generate_actions(prompt)

    files, deletes = parse_actions(ai_output)

    delete_files(deletes)

    write_files(files)

    deploy()

    notify("🚀 SitePilot deployed updated Website")


if __name__ == "__main__":
    main()