from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("COIN_GECKO_KEY")
IDS = ['bitcoin', 'ethereum']
VS_CURRENCY = 'usd'
BACKOFF_FACTOR = 2
MAX_RETRIES = 3
TIMEOUT = 10

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "crypto-tracker.db"

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_PATH = LOG_DIR / "crypto-tracker.log"

ALERT_THRESHOLD = 5
ALERT_COOLDOWN = 10