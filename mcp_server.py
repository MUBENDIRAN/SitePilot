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

    return "\n".join(files)


# ---------------- AI SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """
You are an AI developer maintaining a static website.

Available commands:

READ: filename

FILE: filename
<full file content>

DELETE: filename

Rules:
- Think step by step
- READ files before editing
- Use FILE to create or update files
- Use DELETE to remove files
- Only output commands
- Never explain
- Never use markdown
"""


# ---------------- OLLAMA CALL ----------------

def ask_ai(messages):

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=messages
    )

    return response["message"]["content"]


# ---------------- PARSER ----------------

def parse_commands(output):

    commands = []

    lines = output.splitlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if line.startswith("READ:"):
            commands.append(("READ", line.replace("READ:", "").strip()))
            i += 1
            continue

        if line.startswith("DELETE:"):
            commands.append(("DELETE", line.replace("DELETE:", "").strip()))
            i += 1
            continue

        if line.startswith("FILE:"):

            filename = line.replace("FILE:", "").strip()

            content_lines = []
            i += 1

            while i < len(lines) and not lines[i].startswith(("FILE:", "READ:", "DELETE:")):
                content_lines.append(lines[i])
                i += 1

            content = "\n".join(content_lines)

            commands.append(("FILE", filename, content))
            continue

        i += 1

    return commands


# ---------------- AGENT LOOP ----------------

def run_agent(prompt):

    structure = list_files()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Project files:\n{structure}\n\nTask:\n{prompt}"}
    ]

    for step in range(8):

        ai_output = ask_ai(messages)

        print("\nAI OUTPUT\n", ai_output)

        messages.append({"role": "assistant", "content": ai_output})

        commands = parse_commands(ai_output)

        if not commands:
            print("No commands returned")
            break

        did_write = False

        for cmd in commands:

            if cmd[0] == "READ":

                filename = cmd[1]

                content = read_file(filename)

                messages.append({
                    "role": "user",
                    "content": f"CONTENT OF {filename}:\n{content}"
                })

            elif cmd[0] == "DELETE":

                filename = cmd[1]

                delete_file(filename)

                print("Deleted", filename)

                did_write = True

            elif cmd[0] == "FILE":

                filename = cmd[1]
                content = cmd[2]

                write_file(filename, content)

                print("Updated", filename)

                did_write = True

        # stop reasoning if files changed
        if did_write:
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