import logging, requests, time
from typing import Optional, Dict
from services.error_service import APIRateLimitedError, APIResponseError, NetworkError
import random


def fetch_prices(config) -> Optional[Dict[str, float]]:

    base_url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {
        "x-cg-demo-api-key": config.API_KEY,
    }

    params = {
        "ids": ",".join(config.IDS),
        "vs_currencies": config.VS_CURRENCY,
    }

    backoff_factor = config.BACKOFF_FACTOR
    timeout = config.TIMEOUT
    max_retries = config.MAX_RETRIES
    saw_rate_limit = False
    saw_server_error = False
    saw_network_error = False


    for attempt in range(1, max_retries+1):
        wait = random.uniform(0, backoff_factor * 2 ** attempt)
        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=timeout)


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

            response.raise_for_status()
            data = response.json()

            price: Dict[str, float] = {}

            for coin in config.IDS:
                if coin not in data:
                    raise ValueError (f"No data found for {coin}")

                if config.VS_CURRENCY not in data[coin]:
                    raise ValueError (f"Currency {config.VS_CURRENCY} not found")

                raw_price = data[coin][config.VS_CURRENCY]

                if isinstance(raw_price, (int,float)):
                    price[coin] = float(raw_price)
                else:
                    raise ValueError (f"Price for {coin} must be a number")

            logging.info("Successfully fetched all coin prices")
            return price

        except requests.exceptions.RequestException as e:
            logging.warning(f"Network error: {e}. Retrying in {wait}s for (attempt {attempt})")
            time.sleep(wait)
            saw_network_error = True

        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise APIResponseError(f"Data validation error: {e}")

        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            raise APIResponseError(f"Unexpected error: {e}")


    if saw_rate_limit:
        logging.error("Rate limit reached, maximum retries reached")
        raise APIRateLimitedError("Rate limit reached, maximum retries reached")

    elif saw_network_error:
        logging.critical("Network error occurred")
        raise NetworkError("Network error occurred")

    elif saw_server_error:
        logging.error("Server error occurred, maximum retries reached")
        raise NetworkError("Failed to connect to server, maximum retries reached")

    else:
        logging.error("API failed after maximum retries")
        raise APIResponseError("Failed to retrieve data after maximum retries")
