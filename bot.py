import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL")
#ALLOWED_USERNAME = os.environ.get("ALLOWED_USERNAME")  # Optional

print("Starting telegram-forwarder...")
print(WEBHOOK_URL)
if not TOKEN or not WEBHOOK_URL:
    raise ValueError("TELEGRAM_BOT_TOKEN and N8N_WEBHOOK_URL must be set")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    msg_time = message.date  # datetime in UTC
#    if datetime.utcnow() - msg_time > timedelta(seconds=30):
#        return  # ignore stale messages

    username = message.from_user.username if message.from_user else None
 #   if ALLOWED_USERNAME and username != ALLOWED_USERNAME:
 #       return

    payload = {
        "text": message.text,
        "username": username,
        "chat_id": message.chat.id
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Failed to send message to N8N: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    print("telegram-forwarder is running...")
    app.run_polling()