import sqlite3
from pathlib import Path
from datetime import datetime, timezone

FILE_PATH =  Path("database/crypto.db")

def get_connection():
    FILE_PATH.parent.mkdir(exist_ok=True, parents=True)
    return sqlite3.connect(str(FILE_PATH))

def init_db():

    connection = get_connection()
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
    connection.close()


def add_price(connection, prices: dict):

    cursor = connection.cursor()
    now = int(datetime.now(timezone.utc).timestamp())

    sql = """
    INSERT INTO prices (coin, price, timestamp)
    VALUES (?, ?, ?)
    """

    rows = []

    for coin, price in prices.items():
        rows.append([coin, price, now])

    cursor.executemany(sql, rows)


