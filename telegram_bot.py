import os
import asyncio
import subprocess
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


# ---------------- START COMMAND ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "🚀 SitePilot is ready\n\n"
        "Use:\n"
        "/pilot <describe website change>\n\n"
        "Example:\n"
        "/pilot create dark mode toggle button"
    )

    await update.message.reply_text(message)


# ---------------- PILOT COMMAND ----------------

async def pilot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/pilot <describe website change>"
        )
        return

    prompt = " ".join(context.args)

    await update.message.reply_text("🧠 SitePilot thinking...")

    try:

        process = await asyncio.create_subprocess_exec(
            "python",
            "mcp_server.py",
            prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            await update.message.reply_text(
                f"❌ Error:\n{stderr.decode()}"
            )
            return

        await update.message.reply_text(
            "🚀 Website updated and deployed successfully!"
        )

    except Exception as e:

        await update.message.reply_text(
            f"⚠️ Unexpected error:\n{str(e)}"
        )


# ---------------- STATUS COMMAND ----------------

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ SitePilot is running.\n"
        "AI website maintenance ready."
    )


# ---------------- MAIN ----------------

def main():

    if not TOKEN:
        print("TELEGRAM_TOKEN missing in .env")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pilot", pilot))
    app.add_handler(CommandHandler("status", status))

    print("🚀 Telegram bot running")

    app.run_polling()


if __name__ == "__main__":
    main()