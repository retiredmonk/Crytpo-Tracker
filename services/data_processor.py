from typing import Dict
from env import get_settings

config = get_settings()
price: Dict[str, float] = {}

def get_price(coins, data):

    for coin in coins:

        if coin not in data:
            raise ValueError(f"No data found for {coin}")

        if config.VS_CURRENCY not in data[coin]:
            raise ValueError(f"Currency {config.VS_CURRENCY} not found")

        raw_price = data[coin][config.VS_CURRENCY]

        if isinstance(raw_price, (int, float)):
            price[coin] = float(raw_price)
        else:
            raise ValueError(f"Price for {coin} must be a number")


    return price