import time
from clients.notifier import send_alert
from env import get_settings

config = get_settings()

def get_latest_price (connection,coin):

    cursor = connection.cursor()
    cursor.execute('SELECT price,timestamp FROM prices WHERE coin = ? ORDER BY timestamp DESC LIMIT 1', (coin,))
    return cursor.fetchone()

def get_alert_state(connection,coin):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT last_alert_time, last_alert_price FROM alert_state WHERE coin = ?
    """, (coin,))
    return cursor.fetchone()

def update_alert_state(connection, coin, price, now):

    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO alert_state (coin, last_alert_time, last_alert_price) 
        VALUES (?, ?, ?)
        ON CONFLICT (coin)
        DO UPDATE SET
        last_alert_time = EXCLUDED.last_alert_time,
        last_alert_price = EXCLUDED.last_alert_price
    """, (coin, now, price))

    connection.commit()


def should_alert(price, last_alert_time, now):
    if price < config.ALERT_THRESHOLD:
        return False

    if last_alert_time is None:
        return True

    return (now - last_alert_time) >= config.ALERT_COOLDOWN


def check_alerts(connection, coins):

    cursor = connection.cursor()
    now = int(time.time())

    for coin in coins:
        latest = get_latest_price(cursor, coin)

        if not latest:
            continue

        price, _ = latest
        state = get_alert_state(cursor, coin)
        last_alert_time = state[0] if state else None

        if should_alert(price, last_alert_time, now):
            send_alert(f"🚨 ALERT: {coin.title()} price = {price}{config.VS_CURRENCY}")
            update_alert_state(connection, coin, price, now)