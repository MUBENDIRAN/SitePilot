import os
import subprocess
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "SitePilot ready.\nUse /update <describe website change>"
    )

async def update_site(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /update <prompt>")
        return

    prompt = " ".join(context.args)

    await update.message.reply_text("Generating website update...")

    subprocess.run(
        ["python", "mcp_server.py", prompt],
        check=True
    )

    await update.message.reply_text("Website updated and deployed.")

if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("update", update_site))

    print("Telegram bot running")

    app.run_polling()