from clients.fetcher import fetch_prices
from database.db import init_db, add_price, get_connection
from services.alerts import check_alerts
from utils.logger import setup_logging
from env import get_settings
import time

config = get_settings()

def main():

    connection = get_connection()
    setup_logging()

    prices = fetch_prices()

    if prices:
        add_price(connection, prices)
        check_alerts(connection, prices.keys())

    connection.commit()
    connection.close()

if __name__ == "__main__":
    while True:
        main()
        time.sleep(120)
