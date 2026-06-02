from apis.fetch_prices import fetch_prices
from database.db import init_db, add_price
from services.alert_service import check_alerts
from services import config_service as config
import logging
import time

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(config.LOG_PATH)
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def main():

    setup_logging()
    conn, cursor = init_db()

    prices = fetch_prices(config)
    if prices:
        add_price(cursor, conn, prices)
        check_alerts(conn, cursor, prices.keys())

    conn.close()


if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)
