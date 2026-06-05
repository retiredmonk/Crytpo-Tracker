import requests
import logging
import random
import time
from env import get_settings


config = get_settings()

def send_alert(message: str):

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message
    }

    max_attempts = config.MAX_ATTEMPTS
    backoff_factor = config.BACKOFF_FACTOR

    for attempt in range(1, max_attempts+1):

        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()

            logging.info("Telegram notification sent successfully")
            return

        except requests.exceptions.RequestException as e:

            wait = random.uniform(0, backoff_factor * 2 ** attempt)
            logging.warning(
                f"Telegram notification failed, attempt: {attempt}/{max_attempts}"
                f"Retrying in {wait}s..."
            )

            time.sleep(wait)
    logging.error("Failed to send Telegram message after maximum retries")
