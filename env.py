from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    COIN_GECKO_KEY: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    BACKOFF_FACTOR:int = 120
    MAX_ATTEMPTS:int = 3
    IDS:list = ['bitcoin', 'ethereum']
    VS_CURRENCY:str = 'usd'
    ALERT_THRESHOLD:int = 5
    ALERT_COOLDOWN:int = 10

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()