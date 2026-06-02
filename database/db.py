import sqlite3
from services.config_service import DB_PATH
from datetime import datetime, timezone

def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin TEXT,
            price REAL,
            timestamp INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alert_state(
            coin TEXT PRIMARY KEY,
            last_alert_time INTEGER,
            last_alert_price REAL
        )
    """)

    connection.commit()

    return connection, cursor


def add_price(cursor, connection, prices: dict):
    now = int(datetime.now(timezone.utc).timestamp())

    sql = """
    INSERT INTO prices (coin, price, timestamp)
    VALUES (?, ?, ?)
    """

    rows = []

    for coin, price in prices.items():
        rows.append([coin, price, now])

    cursor.executemany(sql, rows)
    connection.commit()


