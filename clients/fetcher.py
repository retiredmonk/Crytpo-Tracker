import logging
import requests
import random
import time
from typing import Optional, Dict
from services.data_processor import get_price
from utils.errors import  APIResponseError
from env import get_settings

config = get_settings()

def fetch_prices() -> Optional[Dict[str, float]]:

    base_url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {
        "x-cg-demo-api-key": config.COIN_GECKO_KEY,
    }

    params = {
        "ids": ",".join(config.IDS),
        "vs_currencies": config.VS_CURRENCY,
    }

    backoff_factor = config.BACKOFF_FACTOR
    max_attempts = config.MAX_ATTEMPTS

    saw_rate_limit = False
    saw_server_error = False
    saw_network_error = False

    for attempt in range(1, max_attempts+1):

        wait = random.uniform(0, backoff_factor * 2 ** attempt)

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 429:
                saw_rate_limit = True
                logging.warning(f"Rate limit {response.status_code}, Retrying in {wait} seconds...")
                time.sleep(wait)
                continue

            if 500 <= response.status_code < 600:
                saw_server_error = True
                logging.warning(f"Server error {response.status_code}. Retrying in {wait}s (attempt {attempt})")
                time.sleep(wait)
                continue

            data = response.json()

            if isinstance(data, dict) and data.get("message"):
                logging.error(f"API error: {data}")
                return None

            coins = config.IDS
            price = get_price(coins, data)

            logging.info("Successfully fetched all coin prices")
            return price

        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}. Retrying in {wait}s for (attempt {attempt})")
            time.sleep(wait)
            saw_network_error = True

        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise APIResponseError(f"Data validation error: {e}")

        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            raise APIResponseError(f"Unexpected error: {e}")


    if saw_rate_limit:
        logging.error("Rate limit reached after retries")

    elif saw_network_error:
        logging.critical("Network error persisted after retries")

    elif saw_server_error:
        logging.error("Server error persisted after retries")

    else:
        logging.critical("API failed after maximum retries")

    return None
