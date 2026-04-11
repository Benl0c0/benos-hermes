"""Configuration for Telegram Command Center"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from hermess home
load_dotenv('/home/benlo/.hermes/.env')

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('BOT_TOKEN')
AUTHORIZED_CHAT_ID = os.getenv('AUTHORIZED_CHAT_ID', '2029024880')
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
DB_PATH = Path.home() / '.hermes' / 'command-center' / 'data.db'

# Polling parameters
POLL_TIMEOUT = 50    # Long polling timeout in seconds
POLL_INTERVAL = 2    # Sleep between polls if error/no updates

# Validate
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env")
