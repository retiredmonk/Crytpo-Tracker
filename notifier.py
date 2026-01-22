import requests
from config import BOT_TOKEN, CHAT_ID


def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload, timeout=10)
    response.raise_for_status()
