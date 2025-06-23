import os
import logging
import sys
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def load_config():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    webhook_url = os.environ.get("N8N_WEBHOOK_URL")
    allowed_user_ids = list(map(int, os.environ.get("TELEGRAM_USER_IDS", "").split(",")))
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set.")
    if not webhook_url:
        raise ValueError("N8N_WEBHOOK_URL is not set.")
    if not allowed_user_ids:
        raise ValueError("TELEGRAM_USER_IDS is not set or invalid.")
    return token, webhook_url, allowed_user_ids

TOKEN, WEBHOOK_URL, ALLOWED_USER_IDS = load_config()

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    if message.from_user and message.from_user.id not in ALLOWED_USER_IDS:
        logging.warning(f"Unauthorized user: {message.from_user.id}")
        return

    username = message.from_user.username if message.from_user else None

    payload = {
        "username": username,
        "chat_id": message.chat.id
    }

    if message.text:
        payload["text"] = message.text
    elif message.voice:
        payload["voice"] = message.voice.file_id

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except requests.exceptions.Timeout:
        logging.error("Request to N8N timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to N8N failed: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, forward_message))
    logging.info("telegram-forwarder is running...")
    app.run_polling(timeout=30, read_timeout=10)