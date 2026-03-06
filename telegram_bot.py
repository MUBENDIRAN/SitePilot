import os
import subprocess
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot ready.\nUse /update <your request>"
    )

async def update_site(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage: /update <describe the page>"
        )
        return

    prompt = " ".join(context.args)

    await update.message.reply_text("Generating website...")

    subprocess.run(
        ["python", "mcp_client.py", prompt],
        check=True
    )

    await update.message.reply_text("Website updated successfully.")

if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("update", update_site))

    print("Telegram bot running")

    app.run_polling()