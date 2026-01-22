# Crypto Price Alert Bot 

A Python automation bot that monitors cryptocurrency prices using CoinGecko API,
stores price history in SQLite, and sends alerts to Telegram when conditions are met.

## Features
- API integration with retry + backoff
- SQLite price history storage
- Alert cooldown system
- Telegram notifications
- Long-running automation loop

## Tech Stack
- Python
- requests, sqlite
- Coin Gecko API
- Telegram Bot API

## Setup

1. Clone repo
2. Create virtualenv
3. Install requirements
4. Create `.env` file:

COIN_GECKO_KEY=your_key  
TELEGRAM_BOT_TOKEN=your_token  
TELEGRAM_CHAT_ID=your_chat_id

5. Run:

python main.py
